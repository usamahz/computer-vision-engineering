#!/usr/bin/env python3
"""Generate misc/notes/changelog.md from the section drafts.

The changelog is the evidence that the bar was real: for every section it records what
shipped, what was rejected and which rule each rejection failed, how many performance claims
were examined and how they were judged, and the one claim the owner nominated for
measurement.

Standard library only. Deterministic: no timestamps, no ordering that depends on the
filesystem, so continuous integration can regenerate it and diff.

Usage:
  python3 misc/scripts/build_changelog.py            # write misc/notes/changelog.md
  python3 misc/scripts/build_changelog.py --check    # fail if the file on disk is stale
  python3 misc/scripts/build_changelog.py --stdout
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SECTIONS_DIR = REPO_ROOT / "misc" / "notes" / "sections"
OUTPUT = REPO_ROOT / "misc" / "notes" / "changelog.md"

WRAPPERS = ("Section", "Rejected", "Claims", "Link notes", "Benchmark proposal")
ENTRY = re.compile(r"^(?:- |\d+\. )\[(?P<title>[^\]]+)\]\((?P<url>[^)\s]+)\)")
VERDICT = re.compile(r"^\s*[-*]\s*Verdict\s*:\s*(?P<verdict>[^.\n]+)", re.IGNORECASE)
RULE = re.compile(r"rule failed\s*:?\s*(?P<rule>[^.]+)\.", re.IGNORECASE)
VERDICT_ORDER = ("stands", "recorded unverified", "watchlist", "cut")


@dataclass
class Draft:
    path: Path
    number: int
    title: str
    subsections: list[tuple[str, int]] = field(default_factory=list)
    entries: list[tuple[str, str]] = field(default_factory=list)
    rejected: list[tuple[str, str]] = field(default_factory=list)
    claims: list[tuple[str, str]] = field(default_factory=list)
    link_notes: int = 0
    proposal: str = ""


def split_blocks(lines: list[str]) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## ") and line[3:].strip() in WRAPPERS:
            current = line[3:].strip()
            blocks[current] = []
            continue
        if current:
            blocks[current].append(line)
    return blocks


def read_draft(path: Path) -> Draft | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    match = re.match(r"^(\d{2})-", path.name)
    if not match:
        return None
    number = int(match.group(1))
    blocks = split_blocks(lines)
    body = blocks.get("Section", [])

    title = ""
    for line in body:
        if line.startswith("## "):
            title = re.sub(r"^\d+\.\s*", "", line[3:].strip())
            break
    if not title:
        heading = next((l for l in lines if l.startswith("# ")), "")
        title = re.sub(r"^\d+\.\s*", "", heading[2:].strip())

    draft = Draft(path=path, number=number, title=title)

    current_sub: str | None = None
    counts: dict[str, int] = {}
    order: list[str] = []
    for line in body:
        if line.startswith("### "):
            current_sub = line[4:].strip()
            counts.setdefault(current_sub, 0)
            order.append(current_sub)
            continue
        found = ENTRY.match(line)
        if found:
            draft.entries.append((found.group("title"), found.group("url")))
            if current_sub:
                counts[current_sub] += 1
    draft.subsections = [(name, counts[name]) for name in order]

    for line in blocks.get("Rejected", []):
        found = ENTRY.match(line)
        if not found:
            continue
        rule = RULE.search(line)
        draft.rejected.append((found.group("title"), (rule.group("rule").strip() if rule else "rule not named")))

    claim_title = ""
    for line in blocks.get("Claims", []):
        if line.startswith("### "):
            claim_title = line[4:].strip()
            continue
        found = VERDICT.match(line)
        if found and claim_title:
            draft.claims.append((claim_title, found.group("verdict").strip().lower().rstrip(".")))
            claim_title = ""

    draft.link_notes = len([l for l in blocks.get("Link notes", []) if l.strip().startswith("- ")])

    proposal_lines = [l.strip() for l in blocks.get("Benchmark proposal", []) if l.strip()]
    if proposal_lines:
        text = " ".join(proposal_lines)
        first = text.split(". ")[0].strip()
        draft.proposal = first if first.endswith(".") else first + "."
    return draft


RAW = re.compile(r"^https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+)$")
MOVED = re.compile(r"^- `(?P<old>[^`]+)` became `(?P<new>[^`]+)`$")


def url_aliases() -> dict[str, str]:
    """Old URL to canonical URL, from the link verifier's record of canonical changes."""
    path = REPO_ROOT / "misc" / "notes" / "link-verification.md"
    aliases: dict[str, str] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            found = MOVED.match(line.strip())
            if found:
                aliases[found.group("old")] = found.group("new")
    return aliases


def canonical(url: str, aliases: dict[str, str]) -> str:
    """The form of a URL used to decide whether two citations are the same source."""
    url = url.split("#")[0]
    url = aliases.get(url, url)
    url = url.replace("http://host.robots.ox.ac.uk/", "https://host.robots.ox.ac.uk/")
    found = RAW.match(url)
    if found:
        owner, repo, ref, path = found.groups()
        url = f"https://github.com/{owner}/{repo}/blob/{ref}/{path}"
    return url


def readme_entries() -> tuple[dict[str, str], dict[str, str]]:
    """Core and watchlist entries in the README, keyed by URL without its fragment."""
    readme = REPO_ROOT / "README.md"
    core: dict[str, str] = {}
    watch: dict[str, str] = {}
    if not readme.is_file():
        return core, watch
    section = ""
    for line in readme.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        found = ENTRY.match(line)
        if not found or found.group("url").startswith("#"):
            continue
        target = watch if section == "Watchlist" else core
        target[canonical(found.group("url"), {})] = found.group("title")
    return core, watch


def readme_urls() -> set[str]:
    core, watch = readme_entries()
    return set(core) | set(watch)


def review_counts() -> dict[str, int]:
    """Counts from the review records, so the changelog covers the review as well as the drafts."""
    counts: dict[str, int] = {}
    red = REPO_ROOT / "misc" / "notes" / "red-team.md"
    if red.is_file():
        text = red.read_text(encoding="utf-8")
        counts["red team findings"] = len(re.findall(r"^- \*\*", text, flags=re.MULTILINE))
        answers = re.findall(r"^  - Answer: (\w+)", text, flags=re.MULTILINE)
        counts["answers written"] = len(answers)
        for word in ("Accepted", "Rejected", "Noted", "Filled", "Not", "Partly", "Superseded", "Resolved"):
            counts[f"answers beginning {word}"] = sum(1 for a in answers if a == word)
    marshal = REPO_ROOT / "misc" / "notes" / "evidence-marshal.md"
    if marshal.is_file():
        text = marshal.read_text(encoding="utf-8")
        counts["marshal rulings"] = len(re.findall(r"^  - Owner's verdict:", text, flags=re.MULTILINE))
        counts["marshal recheck rulings"] = len(re.findall(r"^  - Recheck:", text, flags=re.MULTILINE))
    return counts


def render(drafts: list[Draft]) -> str:
    shipped = readme_urls()
    total_entries = sum(len(d.entries) for d in drafts)
    total_rejected = sum(len(d.rejected) for d in drafts)
    total_claims = sum(len(d.claims) for d in drafts)
    verdicts: dict[str, int] = {v: 0 for v in VERDICT_ORDER}
    for draft in drafts:
        for _, verdict in draft.claims:
            verdicts[verdict] = verdicts.get(verdict, 0) + 1
    aliases = url_aliases()
    in_readme = sum(1 for d in drafts for _, url in d.entries if canonical(url, aliases) in shipped)

    out: list[str] = []
    out.append("# Changelog")
    out.append("")
    out.append("Generated by `misc/scripts/build_changelog.py` from the section drafts in")
    out.append("`misc/notes/sections/`. Do not edit by hand: continuous integration regenerates it and")
    out.append("fails if the committed copy is stale.")
    out.append("")
    out.append("Why it exists: a curated list is only as good as what it refused. This file counts")
    out.append("the refusals and the numbers that were audited, so the claim that there was a bar")
    out.append("can be checked rather than believed.")
    out.append("")
    out.append("## Totals")
    out.append("")
    out.append("| Measure | Count |")
    out.append("| --- | --- |")
    out.append(f"| Sections delivered | {len(drafts)} |")
    out.append(f"| Entries delivered by owners | {total_entries} |")
    out.append(f"| Entries present in the README | {in_readme} |")
    out.append(f"| Entries considered and rejected | {total_rejected} |")
    out.append(f"| Performance claims examined | {total_claims} |")
    for verdict in VERDICT_ORDER:
        out.append(f"| Claims judged {verdict} | {verdicts.get(verdict, 0)} |")
    out.append(f"| Link oddities recorded | {sum(d.link_notes for d in drafts)} |")
    out.append("")
    ratio = (total_rejected / total_entries) if total_entries else 0.0
    out.append(f"Rejections per entry delivered: {ratio:.2f}.")
    out.append("")
    core, watch = readme_entries()
    aliases = url_aliases()
    drafted = {canonical(url, aliases) for d in drafts for _, url in d.entries}
    added = sorted((title, url) for url, title in core.items() if url not in drafted)
    removed = sorted(
        (d.number, title) for d in drafts for title, url in d.entries
        if canonical(url, aliases) not in core and canonical(url, aliases) not in watch
    )
    to_watch = sorted(
        (d.number, title) for d in drafts for title, url in d.entries if canonical(url, aliases) in watch
    )
    out.append("## Review")
    out.append("")
    out.append("After the merge, a red team, an evidence marshal, a link verifier and an editor's critic")
    out.append("reviewed the README. Their records are misc/notes/red-team.md, misc/notes/evidence-marshal.md and")
    out.append("misc/notes/link-verification.md. What the review changed:")
    out.append("")
    out.append("| Measure | Count |")
    out.append("| --- | --- |")
    for key, value in review_counts().items():
        out.append(f"| {key[0].upper() + key[1:]} | {value} |")
    out.append(f"| Drafted entries removed in review | {len(removed)} |")
    out.append(f"| Drafted entries moved to the watchlist | {len(to_watch)} |")
    out.append(f"| Entries added by the editor in review | {len(added)} |")
    out.append(f"| Core entries in the README | {len(core)} |")
    out.append(f"| Watchlist lines in the README | {len(watch)} |")
    out.append("")
    if added:
        out.append("Added in review, each filling a gap the red team named:")
        out.append("")
        out.extend(f"- {title}" for title, _ in added)
        out.append("")
    if to_watch:
        out.append("Moved from a draft to the watchlist:")
        out.append("")
        out.extend(f"- {number:02d}. {title}" for number, title in to_watch)
        out.append("")
    if removed:
        out.append("Removed in review:")
        out.append("")
        out.extend(f"- {number:02d}. {title}" for number, title in removed)
        out.append("")
    out.append("## By section, as delivered by the owners")
    out.append("")
    for draft in drafts:
        out.append(f"### {draft.number:02d}. {draft.title}")
        out.append("")
        subs = ", ".join(f"{name} ({count})" for name, count in draft.subsections) or "no subsections"
        out.append(f"- Entries delivered: {len(draft.entries)} across {len(draft.subsections)} subsections.")
        out.append(f"- Subsections: {subs}.")
        in_section_readme = sum(1 for _, url in draft.entries if canonical(url, aliases) in shipped)
        out.append(f"- Entries present in the README: {in_section_readme}.")
        out.append(f"- Rejected: {len(draft.rejected)}.")
        counted: dict[str, int] = {}
        for _, verdict in draft.claims:
            counted[verdict] = counted.get(verdict, 0) + 1
        breakdown = ", ".join(f"{k} {v}" for k, v in sorted(counted.items())) or "none recorded"
        out.append(f"- Claims examined: {len(draft.claims)} ({breakdown}).")
        out.append(f"- Link oddities recorded: {draft.link_notes}.")
        if draft.proposal:
            out.append(f"- Benchmark proposal: {draft.proposal}")
        out.append("")
        if draft.rejected:
            out.append("Rejected, with the rule each one failed:")
            out.append("")
            for title, rule in draft.rejected:
                out.append(f"- {title} - {rule}")
            out.append("")
        if draft.claims:
            out.append("Claims examined, with the verdict:")
            out.append("")
            for title, verdict in draft.claims:
                out.append(f"- {title} - {verdict}")
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if the committed file is stale")
    parser.add_argument("--stdout", action="store_true", help="print instead of writing")
    args = parser.parse_args(argv)

    if not SECTIONS_DIR.is_dir():
        print(f"no section drafts at {SECTIONS_DIR}", file=sys.stderr)
        return 2
    drafts: list[Draft] = []
    for path in sorted(SECTIONS_DIR.glob("*.md")):
        draft = read_draft(path)
        if draft is not None:
            drafts.append(draft)
    if not drafts:
        print("no section drafts found", file=sys.stderr)
        return 2
    drafts.sort(key=lambda d: d.number)
    text = render(drafts)

    if args.stdout:
        sys.stdout.write(text)
        return 0
    if args.check:
        if not OUTPUT.is_file():
            print("misc/notes/changelog.md is missing", file=sys.stderr)
            return 1
        if OUTPUT.read_text(encoding="utf-8") != text:
            print("misc/notes/changelog.md is stale: run python3 misc/scripts/build_changelog.py", file=sys.stderr)
            return 1
        print("misc/notes/changelog.md is current")
        return 0
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} from {len(drafts)} drafts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
