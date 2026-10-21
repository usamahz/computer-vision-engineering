#!/usr/bin/env python3
"""Check that every external URL in the list resolves to a live page.

Standard library only, so that continuous integration needs no dependencies and a
contributor can run it on a clean checkout.

The point of this script is the classification, not the pass or fail. Publishers and vendor
documentation refuse automated clients while serving a browser perfectly well, so a checker
that calls that "dead" trains everybody to ignore the badge. Six outcomes:

  OK           reached, final status in the two hundreds
  REDIRECT     reached after one or more redirects, recorded with the destination
  BLOCKED      host refused an automated client (401, 402, 403, 406, 429, 451)
  UNREACHABLE  resolver, transport or server failure that is probably not the page's fault
  DEAD         the page is gone (404, 410)
  MIRROR       a mirror or aggregator host, rejected by rule rather than by request

Only DEAD and MIRROR fail the build by default. UNREACHABLE is reported loudly and does not
fail, because a flaky resolver failing the build is worse than no checker at all. Pass
--fail-on-unreachable when you want the strict reading.

Usage:
  python3 misc/scripts/check_links.py                      # the default target set
  python3 misc/scripts/check_links.py --all                # also the section drafts
  python3 misc/scripts/check_links.py misc/notes/sections/05-evaluation.md
  python3 misc/scripts/check_links.py --report misc/notes/link-report.md --json report.json
  python3 misc/scripts/check_links.py --list               # print the URLs and exit
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_TARGETS = (
    "README.md",
    "CONTRIBUTING.md",
    "misc/notes/conventions.md",
    "misc/notes/voice.md",
    "misc/notes/owner-brief.md",
    "misc/notes/benchmark-brief.md",
    "misc/notes/status.md",
    ".github/ISSUE_TEMPLATE",
    ".github/pull_request_template.md",
    "misc/benchmarks",
)

DRAFT_TARGETS = ("misc/notes/sections",)

# Hosts that wrap or rehost material published elsewhere. Rejected by rule: an aggregator
# page adds nothing to the authors' own copy and rots on its own schedule.
MIRROR_HOSTS = {
    "academia.edu": "paper rehost",
    "alphaxiv.org": "arXiv front end",
    "ar5iv.org": "arXiv front end",
    "ar5iv.labs.arxiv.org": "arXiv front end",
    "arxiv-sanity-lite.com": "arXiv front end",
    "arxiv-vanity.com": "arXiv front end",
    "browse.arxiv.org": "use arxiv.org/abs",
    "citeseerx.ist.psu.edu": "paper rehost",
    "connectedpapers.com": "aggregator",
    "deepai.org": "paper rehost",
    "emergentmind.com": "aggregator",
    "paperswithcode.com": "aggregator and leaderboard",
    "pdfs.semanticscholar.org": "paper rehost",
    "researchgate.net": "paper rehost",
    "scholar.google.com": "search result, not a source",
    "sci-hub.se": "unauthorised rehost",
    "semanticscholar.org": "aggregator",
    "scribd.com": "paper rehost",
    "slideshare.net": "slide rehost",
    "summarizepaper.com": "generated summary",
    "typeset.io": "aggregator",
    "x-mol.com": "aggregator",
    "mlanthology.org": "aggregator",
    "opentrain.ai": "paper rehost",
    "bugsmash.io": "proxy rehost",
    "openread.academy": "aggregator",
    "chatpaper.com": "generated summary",
}

# Aggregator pages that live on an otherwise legitimate host, and the one path rule the house
# style needs: an arXiv abstract page carries the version history, the PDF path does not.
MIRROR_PATHS = (
    ("huggingface.co", "/papers", "paper aggregator page on a model host"),
    ("arxiv.org", "/pdf", "cite the abstract page, which carries the version history"),
    ("arxiv.org", "/html", "cite the abstract page, which carries the version history"),
    ("github.com", "/search", "search result, not a source"),
)

# Hosts whose business is restating primary sources. Not a mirror of one paper, but the same
# failure: a layer of error over something the list should cite directly.
RESTATEMENT_HOSTS = {
    "analyticsvidhya.com": "content farm",
    "dev.to": "blogspam",
    "geeksforgeeks.org": "content farm",
    "kdnuggets.com": "content farm",
    "machinelearningmastery.com": "content farm",
    "medium.com": "blogspam",
    "towardsdatascience.com": "blogspam",
    "quora.com": "forum restatement",
    "v7labs.com": "vendor content marketing",
    "viso.ai": "vendor content marketing",
    "roboflow.com": "vendor content marketing",
    "encord.com": "vendor content marketing",
    "labellerr.com": "vendor content marketing",
}

# The repository's own pages. A private repository answers 404 to an anonymous client for its
# badge and its Actions pages, which would make the checker fail on itself.
SELF_PREFIXES = ("https://github.com/usamahz/computer-vision-engineering",)

BLOCKED_CODES = {401, 402, 403, 406, 429, 451}
DEAD_CODES = {404, 410}
TIMEOUTS = (8, 16, 32)
USER_AGENT = (
    "Mozilla/5.0 (compatible; computer-vision-engineering link checker; "
    "+https://github.com/usamahz/computer-vision-engineering)"
)

MD_LINK = re.compile(r"\[[^\]]*\]\((?P<url>https?://[^)\s]+)\)")
MD_AUTOLINK = re.compile(r"<(?P<url>https?://[^>\s]+)>")
BARE_URL = re.compile(r"(?<![(<\w])(?P<url>https?://[^\s)<>\]\"']+)")

_orig_getaddrinfo = socket.getaddrinfo


def _ipv4_first(host, port, family=0, type=0, proto=0, flags=0):  # noqa: A002
    """Prefer A records over AAAA.

    Containers and runners routinely advertise IPv6 they cannot actually route, which shows
    up as a timeout and looks exactly like a dead link.
    """
    results = _orig_getaddrinfo(host, port, family, type, proto, flags)
    v4 = [r for r in results if r[0] == socket.AF_INET]
    if not v4:
        return results
    return v4 + [r for r in results if r[0] != socket.AF_INET]


class _ChainHandler(urllib.request.HTTPRedirectHandler):
    """Follow redirects while recording them."""

    def __init__(self) -> None:
        self.chain: list[tuple[int, str]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append((code, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class _HostGate:
    """One request at a time per host, with a small gap, so the checker is not abusive."""

    def __init__(self, min_interval: float = 0.25) -> None:
        self.min_interval = min_interval
        self._lock = threading.Lock()
        self._locks: dict[str, threading.Lock] = {}
        self._last: dict[str, float] = {}

    def lock_for(self, host: str) -> threading.Lock:
        with self._lock:
            return self._locks.setdefault(host, threading.Lock())

    def wait(self, host: str) -> None:
        with self._lock:
            last = self._last.get(host, 0.0)
            gap = time.monotonic() - last
        if gap < self.min_interval:
            time.sleep(self.min_interval - gap)
        with self._lock:
            self._last[host] = time.monotonic()


GATE = _HostGate()


def host_of(url: str) -> str:
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def mirror_reason(url: str) -> str | None:
    host = host_of(url)
    path = urllib.parse.urlsplit(url).path or "/"
    for bad_host, prefix, why in MIRROR_PATHS:
        if (host == bad_host or host.endswith("." + bad_host)) and path.startswith(prefix):
            return f"mirror: {why}"
    for table, label in ((MIRROR_HOSTS, "mirror"), (RESTATEMENT_HOSTS, "restatement")):
        for bad, why in table.items():
            if host == bad or host.endswith("." + bad):
                return f"{label}: {why}"
    return None


def iter_markdown(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        path = (REPO_ROOT / target) if not os.path.isabs(target) else Path(target)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md")))
        elif path.is_file():
            files.append(path)
    seen: set[Path] = set()
    unique: list[Path] = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)
    return unique


def collect(files: list[Path]) -> dict[str, list[str]]:
    """Map URL to the list of file:line places it appears."""
    found: dict[str, list[str]] = {}
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
            continue
        rel = path.relative_to(REPO_ROOT) if REPO_ROOT in path.resolve().parents else path
        in_fence = False
        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            urls = [m.group("url") for m in MD_LINK.finditer(line)]
            urls += [m.group("url") for m in MD_AUTOLINK.finditer(line)]
            if not urls:
                urls += [m.group("url") for m in BARE_URL.finditer(line)]
            for url in urls:
                url = url.rstrip(".,;:")
                found.setdefault(url, []).append(f"{rel}:{lineno}")
    return found


def _request(url: str, method: str, timeout: int) -> tuple[int, str, list[tuple[int, str]], str]:
    handler = _ChainHandler()
    opener = urllib.request.build_opener(handler)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
    }
    if method == "GET":
        headers["Range"] = "bytes=0-4095"
    req = urllib.request.Request(url, method=method, headers=headers)
    with opener.open(req, timeout=timeout) as resp:
        resp.read(4096)
        return resp.status, resp.geturl(), handler.chain, ""


def check(url: str) -> dict:
    """Return a record for one URL."""
    record: dict = {
        "url": url,
        "status": "UNREACHABLE",
        "code": None,
        "final_url": url,
        "redirects": [],
        "note": "",
    }
    if url.startswith(SELF_PREFIXES):
        record["status"] = "OK"
        record["note"] = "this repository, not checked"
        return record

    reason = mirror_reason(url)
    if reason:
        record["status"] = "MIRROR"
        record["note"] = reason
        return record

    target = urllib.parse.urlsplit(url)._replace(fragment="").geturl()
    host = host_of(url)
    gate = GATE.lock_for(host)

    attempts: list[tuple[str, int]] = []
    for timeout in TIMEOUTS:
        attempts.append(("HEAD", timeout))
        attempts.append(("GET", timeout))

    last_error = ""
    for index, (method, timeout) in enumerate(attempts):
        with gate:
            GATE.wait(host)
            try:
                code, final, chain, _ = _request(target, method, timeout)
            except urllib.error.HTTPError as exc:
                code, final, chain = exc.code, getattr(exc, "url", target), []
                record["code"] = code
                if code in DEAD_CODES:
                    # A server that rejects HEAD with 404 is common enough to be worth one
                    # confirming GET before calling a page dead.
                    if method == "HEAD":
                        last_error = f"HEAD {code}"
                        continue
                    record["status"] = "DEAD"
                    record["note"] = f"{code} on GET"
                    return record
                if code in BLOCKED_CODES:
                    record["status"] = "BLOCKED"
                    record["note"] = f"{code} refused automated client"
                    return record
                if code in (405, 400, 409, 501):
                    last_error = f"{method} {code}"
                    continue
                last_error = f"{method} {code}"
                record["note"] = last_error
                continue
            except (urllib.error.URLError, socket.timeout, ssl.SSLError, OSError) as exc:
                inner = getattr(exc, "reason", exc)
                last_error = f"{method} {type(inner).__name__}: {inner}"
                record["note"] = last_error
            else:
                record["code"] = code
                record["final_url"] = final
                record["redirects"] = [{"code": c, "to": u} for c, u in chain]
                if 200 <= code < 300:
                    if chain and _materially_different(url, final):
                        record["status"] = "REDIRECT"
                        record["note"] = f"{len(chain)} hop(s) to {final}"
                    else:
                        record["status"] = "OK"
                    return record
                last_error = f"{method} {code}"
        if index + 1 < len(attempts):
            time.sleep(min(2 ** (index // 2), 4))

    record["status"] = "UNREACHABLE"
    record["note"] = last_error or "no response"
    return record


def _materially_different(original: str, final: str) -> bool:
    a = urllib.parse.urlsplit(original)
    b = urllib.parse.urlsplit(final)
    norm = lambda s: (s.netloc.lower().removeprefix("www."), s.path.rstrip("/"))  # noqa: E731
    if norm(a) == norm(b):
        return False
    return True


def render_report(records: list[dict], places: dict[str, list[str]]) -> str:
    order = ["DEAD", "MIRROR", "UNREACHABLE", "BLOCKED", "REDIRECT", "OK"]
    by_status: dict[str, list[dict]] = {k: [] for k in order}
    for rec in records:
        by_status.setdefault(rec["status"], []).append(rec)

    lines = ["# Link report", ""]
    lines.append("| Outcome | Count |")
    lines.append("| --- | --- |")
    for status in order:
        lines.append(f"| {status} | {len(by_status[status])} |")
    lines.append("")
    for status in order:
        rows = by_status[status]
        if not rows or status == "OK":
            continue
        lines.append(f"## {status}")
        lines.append("")
        for rec in sorted(rows, key=lambda r: r["url"]):
            where = ", ".join(places.get(rec["url"], []))
            note = rec["note"] or ""
            lines.append(f"- {rec['url']}")
            lines.append(f"  - note: {note}")
            lines.append(f"  - seen at: {where}")
        lines.append("")
    lines.append(f"Checked {len(records)} unique URLs.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", help="markdown files or directories to check")
    parser.add_argument("--all", action="store_true", help="include the section drafts")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--report", help="write a markdown report to this path")
    parser.add_argument("--json", dest="json_path", help="write machine readable results here")
    parser.add_argument("--list", action="store_true", help="print the URLs and exit")
    parser.add_argument("--fail-on-unreachable", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    socket.getaddrinfo = _ipv4_first  # type: ignore[assignment]

    targets = list(args.paths) if args.paths else list(DEFAULT_TARGETS)
    if args.all and not args.paths:
        targets += list(DRAFT_TARGETS)
    files = iter_markdown(targets)
    if not files:
        print("no markdown files found", file=sys.stderr)
        return 2
    places = collect(files)
    urls = sorted(places)

    if args.list:
        for url in urls:
            print(url)
        return 0

    if not args.quiet:
        print(f"checking {len(urls)} unique URLs from {len(files)} files", file=sys.stderr)

    records: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for rec in pool.map(check, urls):
            records.append(rec)
            if not args.quiet:
                mark = {"OK": ".", "REDIRECT": "r", "BLOCKED": "b", "UNREACHABLE": "u", "DEAD": "X", "MIRROR": "M"}
                sys.stderr.write(mark.get(rec["status"], "?"))
                sys.stderr.flush()
    if not args.quiet:
        sys.stderr.write("\n")

    report = render_report(records, places)
    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = REPO_ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
    if args.json_path:
        out = Path(args.json_path)
        if not out.is_absolute():
            out = REPO_ROOT / out
        out.write_text(json.dumps({"records": records, "places": places}, indent=2), encoding="utf-8")

    print(report)

    failures = [r for r in records if r["status"] in ("DEAD", "MIRROR")]
    if args.fail_on_unreachable:
        failures += [r for r in records if r["status"] == "UNREACHABLE"]
    if failures:
        print(f"FAIL: {len(failures)} link(s) must be fixed", file=sys.stderr)
        return 1
    print("PASS: no dead links and no mirrors", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
