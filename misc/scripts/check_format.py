#!/usr/bin/env python3
"""Enforce the house rules on README.md, the section drafts and the benchmark READMEs.

Standard library only. Everything this script checks is mechanical; everything it cannot
check is written down in misc/notes/conventions.md section 11, which is the point of that section.

What it enforces:

  entry grammar          `- [Title](URL) - Why it earns its place.`
  reason length          under 120 characters
  reason vocabulary      no digits, no praise, no second person, no dashes beyond the hyphen
  headings               H2 for sections, H3 for subsections, nothing deeper, no tier headings
  subsection size        three to six entries, never empty, two to four subsections per section
  Start here             exactly ten numbered items, numbered 1 to 10, and the only numbered list
  preambles              at most one sentence between a section heading and its first entry
  watchlist              every line carries an observable promotion condition
  contents               every section listed, every listed section present, anchors resolve
  relative links         every repository-relative target exists on disk
  duplicate URLs         the same URL never appears twice inside one subsection
  placeholders           no TODO, TBD, FIXME, WIP, lorem, coming soon, empty table cells
  spelling               British spelling in prose, with the quantization carve-out
  benchmarks             one directory per section, every template section filled

Usage:
  python3 misc/scripts/check_format.py                     # README, CONTRIBUTING, benchmarks
  python3 misc/scripts/check_format.py --draft misc/notes/sections/05-evaluation.md
  python3 misc/scripts/check_format.py --readme-only
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

REASON_MAX = 120
WATCHLIST_MAX = 240
ENTRIES_MIN, ENTRIES_MAX = 3, 6
SUBSECTIONS_MIN, SUBSECTIONS_MAX = 2, 4
SECTION_COUNT = 16
START_HERE_ITEMS = 10

BULLET_ENTRY = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)\s]+)\) - (?P<reason>.+)$")
NUMBERED_ENTRY = re.compile(r"^(?P<num>\d+)\. \[(?P<title>[^\]]+)\]\((?P<url>[^)\s]+)\) - (?P<reason>.+)$")
WATCHLIST_ENTRY = re.compile(
    r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)\s]+)\) - (?P<reason>.+?)\. "
    r"Enters the core when (?P<condition>.+)\.$"
)
ANY_LINK = re.compile(r"\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]+)\)")
INLINE_CODE = re.compile(r"`[^`]*`")

# Mirrors misc/notes/voice.md section 2. Keep the two in step.
BANNED_PRAISE = (
    "best", "better", "great", "excellent", "amazing", "awesome", "essential", "must-read",
    "seminal", "classic", "iconic", "legendary", "brilliant", "elegant", "beautiful",
    "groundbreaking", "revolutionary", "landmark", "definitive", "invaluable",
    "indispensable", "outstanding", "remarkable", "impressive", "powerful",
    "state-of-the-art", "cutting-edge", "comprehensive", "exhaustive", "novel", "famous",
    "popular", "influential", "gold standard",
)
BANNED_PERSON = ("you", "your", "yours", "yourself", "we", "our", "ours", "us")
# Popularity offered as a motive, and intensifiers that carry praise without an adjective.
# Found by the editor's critic in review; see misc/notes/voice.md section 2.
BANNED_PHRASES = (
    "everyone", "almost every", "widely", "actually", "means nothing", "most reports",
    "became the default", "ended up inside",
)
VAGUE_CONDITIONS = (
    "matures", "mature", "stabilises", "stabilizes", "sees adoption", "proves itself",
    "gains traction", "becomes popular", "is ready", "settles down",
)
PLACEHOLDERS = ("todo", "tbd", "fixme", "xxx", "lorem ipsum", "coming soon", "to be filled", "wip")
TIER_WORDS = ("tier", "beginner", "intermediate", "advanced", "level one", "optional reading")

# American spellings that are not terms of art. The quantization carve-out and every other
# established technical term stays out of this list; see misc/notes/voice.md section 3.
AMERICANISMS = (
    "color", "colors", "coloring", "behavior", "behaviors", "favor", "favors", "labeled",
    "labeling", "modeling", "gray", "defense", "analyze", "analyzed", "catalog", "fulfill",
    "center", "centers", "meter", "meters", "practise",
)

# Tokens that may carry a capital letter inside a sentence case heading.
PROPER_TOKENS = {
    "IoU", "mAP", "SfM", "ViT", "ViTs", "PyTorch", "TensorFlow", "ImageNet", "Cityscapes",
    "Kinetics", "OpenVINO", "CoreML", "TensorRT", "NVIDIA", "Qualcomm", "Intel", "Arm",
    "Apple", "Gaussian", "Gaussians", "Fourier", "Laplacian", "Bayesian", "Bayer", "Hough",
    "COCO", "LVIS", "KITTI", "YOLO", "DETR", "CLIP", "DINO", "SAM", "MAE", "ONNX", "JPEG",
    "Contents", "Watchlist", "Start", "Rejected", "Claims", "Link", "Section", "Benchmark",
    "English", "MIT",
}


@dataclass
class Entry:
    lineno: int
    title: str
    url: str
    reason: str
    numbered: bool
    number: int | None
    section: str
    subsection: str | None


@dataclass
class Section:
    name: str
    lineno: int
    index: int | None
    subsections: list[tuple[str, int]] = field(default_factory=list)
    entries: list[Entry] = field(default_factory=list)
    preamble: list[str] = field(default_factory=list)


class Report:
    def __init__(self) -> None:
        self.problems: list[str] = []

    def add(self, where: str, message: str) -> None:
        self.problems.append(f"{where}: {message}")

    def ok(self) -> bool:
        return not self.problems

    def dump(self, label: str) -> None:
        if self.ok():
            print(f"PASS {label}")
            return
        print(f"FAIL {label}: {len(self.problems)} problem(s)")
        for problem in self.problems:
            print(f"  {problem}")


def strip_code(text: str) -> str:
    return INLINE_CODE.sub(" ", text)


def prose_of(line: str) -> str:
    """Drop inline code, link targets and link text, leaving prose a spelling rule may judge."""
    without_code = strip_code(line)
    return ANY_LINK.sub(" ", without_code)


def slug(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def check_reason(reason: str, where: str, report: Report, *, allow_two_sentences: bool = False) -> None:
    if len(reason) >= REASON_MAX:
        report.add(where, f"reason is {len(reason)} characters, limit is {REASON_MAX - 1}")
    if not reason[:1].isupper():
        report.add(where, "reason does not start with a capital letter")
    if not reason.endswith("."):
        report.add(where, "reason does not end with a full stop")
    if not allow_two_sentences and reason.count(".") != 1:
        report.add(where, "reason is not a single sentence or fragment")
    for char, name in (("\u2014", "em dash"), ("\u2013", "en dash")):
        if char in reason:
            report.add(where, f"reason contains an {name}")
    for char in ";:()!?":
        if char in reason:
            report.add(where, f"reason contains {char!r}")
    if re.search(r"\d", reason):
        report.add(where, "reason contains a digit")
    lowered = [w.lower() for w in words(reason)]
    joined = " ".join(lowered)
    for banned in BANNED_PRAISE:
        if " " in banned or "-" in banned:
            if banned in reason.lower():
                report.add(where, f"reason contains the praise term {banned!r}")
        elif banned in lowered:
            report.add(where, f"reason contains the praise term {banned!r}")
    for pronoun in BANNED_PERSON:
        if pronoun in lowered:
            report.add(where, f"reason contains the pronoun {pronoun!r}")
    for phrase in BANNED_PHRASES:
        if re.search(rf"\b{re.escape(phrase)}\b", reason.lower()):
            report.add(where, f"reason contains the phrase {phrase!r}")
    if " paper that " in f" {joined} " or joined.startswith("paper "):
        report.add(where, "reason describes the artefact rather than giving a reason to open it")


def check_heading_case(heading: str, where: str, report: Report) -> None:
    tokens = heading.split()
    for position, token in enumerate(tokens):
        bare = token.strip(".,:;()[]").replace("'s", "")
        if not bare or not bare[0].isalpha():
            continue
        if position == 0 or (position == 1 and tokens[0].rstrip(".").isdigit()):
            continue
        if bare.isupper() or bare in PROPER_TOKENS:
            continue
        if bare[0].isupper():
            report.add(where, f"heading is not sentence case: {bare!r}")


def parse(lines: list[str], *, source: str, entry_sections_only: bool = False) -> tuple[list[Section], dict]:
    sections: list[Section] = []
    meta: dict = {"headings": [], "fenced": set(), "h1": None}
    current: Section | None = None
    current_sub: str | None = None
    in_fence = False

    for lineno, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            meta["fenced"].add(lineno)
            continue
        if in_fence:
            meta["fenced"].add(lineno)
            continue

        if line.startswith("# "):
            meta["h1"] = (line[2:].strip(), lineno)
            meta["headings"].append(line[2:].strip())
            continue
        if line.startswith("## "):
            name = line[3:].strip()
            meta["headings"].append(name)
            index = None
            match = re.match(r"^(\d+)\.\s", name)
            if match:
                index = int(match.group(1))
            current = Section(name=name, lineno=lineno, index=index)
            sections.append(current)
            current_sub = None
            continue
        if line.startswith("### "):
            name = line[4:].strip()
            meta["headings"].append(name)
            if current is None:
                continue
            current.subsections.append((name, lineno))
            current_sub = name
            continue
        if re.match(r"^#{4,}\s", line):
            meta.setdefault("deep_headings", []).append((line, lineno))
            continue

        if current is None:
            continue

        bullet = BULLET_ENTRY.match(line)
        numbered = NUMBERED_ENTRY.match(line)
        if bullet or numbered:
            match = bullet or numbered
            current.entries.append(
                Entry(
                    lineno=lineno,
                    title=match.group("title"),
                    url=match.group("url"),
                    reason=match.group("reason"),
                    numbered=bool(numbered),
                    number=int(numbered.group("num")) if numbered else None,
                    section=current.name,
                    subsection=current_sub,
                )
            )
            continue
        if line.strip() and current_sub is None and not current.entries:
            current.preamble.append(line.strip())
        if line.strip().startswith(("- [ ]", "- [x]")):
            meta.setdefault("checkboxes", []).append(lineno)

    return sections, meta


def check_entries(sections: list[Section], report: Report, path: str) -> None:
    for section in sections:
        groups: dict[str | None, list[Entry]] = {}
        for entry in section.entries:
            groups.setdefault(entry.subsection, []).append(entry)
        for subsection, entries in groups.items():
            seen: dict[str, int] = {}
            for entry in entries:
                where = f"{path}:{entry.lineno}"
                check_reason(entry.reason, where, report)
                if entry.url in seen:
                    report.add(where, f"duplicate URL inside one subsection, first seen on line {seen[entry.url]}")
                else:
                    seen[entry.url] = entry.lineno
                if entry.title != entry.title.strip():
                    report.add(where, "title has surrounding whitespace")
                if len(entry.title) > 100:
                    report.add(where, f"title is {len(entry.title)} characters, trim it to the searchable part")


def check_readme(path: Path, report: Report) -> list[Section]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rel = str(path.relative_to(REPO_ROOT))
    sections, meta = parse(lines, source=rel)

    for line, lineno in meta.get("deep_headings", []):
        report.add(f"{rel}:{lineno}", "heading deeper than H3")
    for lineno in meta.get("checkboxes", []):
        report.add(f"{rel}:{lineno}", "checkbox list is not allowed")

    numbered = [s for s in sections if s.index is not None]
    if len(numbered) != SECTION_COUNT:
        report.add(rel, f"expected {SECTION_COUNT} numbered sections, found {len(numbered)}")
    for position, section in enumerate(numbered, start=1):
        if section.index != position:
            report.add(f"{rel}:{section.lineno}", f"section numbered {section.index}, expected {position}")

    names = [s.name for s in sections]
    for required in ("Contents", "Watchlist", "What earns a place"):
        if required not in names:
            report.add(rel, f"missing section {required!r}")

    for section in sections:
        check_heading_case(section.name, f"{rel}:{section.lineno}", report)
        for sub, lineno in section.subsections:
            check_heading_case(sub, f"{rel}:{lineno}", report)
            if any(word in sub.lower() for word in TIER_WORDS):
                report.add(f"{rel}:{lineno}", "tier heading is not allowed")

    meta_sections = {"Contents", "What earns a place", "Watchlist"}
    for section in sections:
        if section.name in meta_sections:
            continue
        if section.index is None:
            continue
        if section.index == 1:
            if section.subsections:
                report.add(f"{rel}:{section.lineno}", "Start here must not have subsections")
            items = section.entries
            if len(items) != START_HERE_ITEMS:
                report.add(f"{rel}:{section.lineno}", f"Start here holds {len(items)} items, expected {START_HERE_ITEMS}")
            for position, entry in enumerate(items, start=1):
                if not entry.numbered:
                    report.add(f"{rel}:{entry.lineno}", "Start here items must be a numbered list")
                elif entry.number != position:
                    report.add(f"{rel}:{entry.lineno}", f"item numbered {entry.number}, expected {position}")
            continue

        if not (SUBSECTIONS_MIN <= len(section.subsections) <= SUBSECTIONS_MAX):
            report.add(
                f"{rel}:{section.lineno}",
                f"section has {len(section.subsections)} subsections, allowed range is "
                f"{SUBSECTIONS_MIN} to {SUBSECTIONS_MAX}",
            )
        counts: dict[str, int] = {name: 0 for name, _ in section.subsections}
        for entry in section.entries:
            if entry.subsection is None:
                report.add(f"{rel}:{entry.lineno}", "entry sits directly under a section heading")
            else:
                counts[entry.subsection] = counts.get(entry.subsection, 0) + 1
            if entry.numbered:
                report.add(f"{rel}:{entry.lineno}", "numbered list outside Start here")
        for name, lineno in section.subsections:
            count = counts.get(name, 0)
            if count == 0:
                report.add(f"{rel}:{lineno}", f"subsection {name!r} is empty")
            elif not (ENTRIES_MIN <= count <= ENTRIES_MAX):
                report.add(
                    f"{rel}:{lineno}",
                    f"subsection {name!r} holds {count} entries, allowed range is {ENTRIES_MIN} to {ENTRIES_MAX}",
                )
        if section.preamble:
            text = " ".join(section.preamble)
            if len(section.preamble) > 1 or text.count(".") > 1:
                report.add(f"{rel}:{section.lineno}", "section preamble is longer than one sentence")

    check_entries([s for s in sections if s.index is not None and s.index != 1], report, rel)
    start_here = [s for s in sections if s.index == 1]
    check_entries(start_here, report, rel)

    watchlist = next((s for s in sections if s.name == "Watchlist"), None)
    if watchlist is not None:
        body = lines[watchlist.lineno : _section_end(lines, watchlist.lineno)]
        if not re.search(r"\b(19|20)\d\d\b", " ".join(body[:6])):
            report.add(f"{rel}:{watchlist.lineno}", "watchlist carries no review date")
        count = 0
        for offset, line in enumerate(body, start=watchlist.lineno + 1):
            if not line.startswith("- "):
                continue
            count += 1
            where = f"{rel}:{offset}"
            match = WATCHLIST_ENTRY.match(line)
            if not match:
                report.add(where, "watchlist line does not match `- [Title](URL) - Reason. Enters the core when condition.`")
                continue
            visible = len(line) - len(match.group("url"))
            if visible > WATCHLIST_MAX:
                report.add(where, f"watchlist line reads {visible} characters without its URL, limit is {WATCHLIST_MAX}")
            check_reason(match.group("reason") + ".", where, report)
            condition = match.group("condition")
            if re.search(r"\d", condition):
                report.add(where, "promotion condition contains a digit")
            for vague in VAGUE_CONDITIONS:
                if vague in condition.lower():
                    report.add(where, f"promotion condition is not observable: {vague!r}")
        if count < 3:
            report.add(f"{rel}:{watchlist.lineno}", f"watchlist holds {count} lines, expected at least three")

    first_seen: dict[str, int] = {}
    for section in sections:
        for entry in section.entries:
            base = entry.url.split("#")[0]
            if base in first_seen:
                report.add(f"{rel}:{entry.lineno}", f"source already listed on line {first_seen[base]}; each source appears once")
            else:
                first_seen[base] = entry.lineno

    _check_contents(lines, sections, rel, report)
    _check_links(lines, meta, rel, report)
    _check_text_rules(lines, meta, rel, report)
    return sections


def _section_end(lines: list[str], start_lineno: int) -> int:
    for index in range(start_lineno, len(lines)):
        if lines[index].startswith("## "):
            return index
    return len(lines)


def _check_contents(lines: list[str], sections: list[Section], rel: str, report: Report) -> None:
    contents = next((s for s in sections if s.name == "Contents"), None)
    if contents is None:
        return
    end = _section_end(lines, contents.lineno)
    listed: list[str] = []
    for lineno in range(contents.lineno, end):
        for match in ANY_LINK.finditer(lines[lineno]):
            target = match.group("target")
            if target.startswith("#"):
                listed.append(target[1:])
    expected = [slug(s.name) for s in sections if s.name != "Contents"]
    expected += [slug(name) for s in sections for name, _ in s.subsections]
    for anchor in expected:
        if anchor not in listed:
            report.add(f"{rel}:{contents.lineno}", f"Contents is missing an entry for #{anchor}")
    for anchor in listed:
        if anchor not in expected:
            report.add(f"{rel}:{contents.lineno}", f"Contents links #{anchor}, which is not a heading")


def _check_links(lines: list[str], meta: dict, rel: str, report: Report) -> None:
    anchors = {slug(h) for h in meta["headings"]}
    for lineno, line in enumerate(lines, start=1):
        if lineno in meta["fenced"]:
            continue
        for match in ANY_LINK.finditer(line):
            target = match.group("target")
            if target.startswith("#"):
                if target[1:] not in anchors:
                    report.add(f"{rel}:{lineno}", f"internal anchor {target} does not resolve")
            elif not target.startswith(("http://", "https://", "mailto:")):
                candidate = (REPO_ROOT / target.split("#")[0]).resolve()
                if not candidate.exists():
                    report.add(f"{rel}:{lineno}", f"relative link {target} does not exist on disk")


def _check_text_rules(lines: list[str], meta: dict, rel: str, report: Report) -> None:
    for lineno, line in enumerate(lines, start=1):
        if lineno in meta["fenced"]:
            continue
        if "\u2014" in line:
            report.add(f"{rel}:{lineno}", "em dash")
        lowered = line.lower()
        for placeholder in PLACEHOLDERS:
            if placeholder in lowered:
                report.add(f"{rel}:{lineno}", f"placeholder text {placeholder!r}")
        prose = prose_of(line)
        for american in AMERICANISMS:
            if re.search(rf"\b{american}\b", prose, flags=re.IGNORECASE):
                report.add(f"{rel}:{lineno}", f"American spelling {american!r} in prose")


def check_draft(path: Path, report: Report) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    rel = str(path.relative_to(REPO_ROOT)) if REPO_ROOT in path.resolve().parents else str(path)

    wrappers = ["Section", "Rejected", "Claims", "Link notes", "Benchmark proposal"]
    positions: dict[str, int] = {}
    for lineno, line in enumerate(lines, start=1):
        if line.startswith("## ") and line[3:].strip() in wrappers:
            positions[line[3:].strip()] = lineno
    for wrapper in wrappers:
        if wrapper not in positions:
            report.add(rel, f"draft is missing the `## {wrapper}` block")
    if "Section" not in positions:
        return

    ordered = sorted(positions.items(), key=lambda kv: kv[1])
    bounds: dict[str, tuple[int, int]] = {}
    for index, (name, start) in enumerate(ordered):
        end = ordered[index + 1][1] - 1 if index + 1 < len(ordered) else len(lines)
        bounds[name] = (start, end)

    body_start, body_end = bounds["Section"]
    body = lines[body_start:body_end]
    sections, meta = parse(body, source=rel)
    offset = body_start

    for _, lineno in meta.get("deep_headings", []):
        report.add(f"{rel}:{lineno + offset}", "heading deeper than H3")
    if not sections:
        report.add(rel, "the `## Section` block contains no section heading")
    for section in sections:
        where = f"{rel}:{section.lineno + offset}"
        check_heading_case(section.name, where, report)
        if section.index == 1:
            if len(section.entries) != START_HERE_ITEMS:
                report.add(where, f"Start here holds {len(section.entries)} items, expected {START_HERE_ITEMS}")
            for position, entry in enumerate(section.entries, start=1):
                if entry.number != position:
                    report.add(f"{rel}:{entry.lineno + offset}", f"item numbered {entry.number}, expected {position}")
        else:
            if not (SUBSECTIONS_MIN <= len(section.subsections) <= SUBSECTIONS_MAX):
                report.add(where, f"{len(section.subsections)} subsections, allowed range is {SUBSECTIONS_MIN} to {SUBSECTIONS_MAX}")
            counts: dict[str, int] = {name: 0 for name, _ in section.subsections}
            for entry in section.entries:
                if entry.subsection is None:
                    report.add(f"{rel}:{entry.lineno + offset}", "entry sits directly under the section heading")
                else:
                    counts[entry.subsection] += 1
                if entry.numbered:
                    report.add(f"{rel}:{entry.lineno + offset}", "numbered list outside Start here")
            for name, lineno in section.subsections:
                count = counts.get(name, 0)
                if not (ENTRIES_MIN <= count <= ENTRIES_MAX):
                    report.add(f"{rel}:{lineno + offset}", f"subsection {name!r} holds {count} entries, allowed range is {ENTRIES_MIN} to {ENTRIES_MAX}")
        if section.preamble:
            joined = " ".join(section.preamble)
            if len(section.preamble) > 1 or joined.count(".") > 1:
                report.add(where, "section preamble is longer than one sentence")
        for entry in section.entries:
            check_reason(entry.reason, f"{rel}:{entry.lineno + offset}", report)
        seen: dict[tuple[str | None, str], int] = {}
        for entry in section.entries:
            key = (entry.subsection, entry.url)
            if key in seen:
                report.add(f"{rel}:{entry.lineno + offset}", f"duplicate URL inside one subsection, first seen on line {seen[key] + offset}")
            seen[key] = entry.lineno

    rejected_start, rejected_end = bounds["Rejected"]
    rejected = [l for l in lines[rejected_start:rejected_end] if l.startswith("- ")]
    if len(rejected) < 4:
        report.add(f"{rel}:{rejected_start}", f"`## Rejected` holds {len(rejected)} entries, expected at least four")
    for index, line in enumerate(rejected):
        if "rule failed" not in line.lower() and "rule:" not in line.lower():
            report.add(f"{rel}:{rejected_start}", f"rejected entry {index + 1} does not name the rule it failed")

    claims_start, claims_end = bounds["Claims"]
    claim_block = lines[claims_start:claims_end]
    claim_headings = [l for l in claim_block if l.startswith("### ")]
    verdicts = [l for l in claim_block if re.match(r"^\s*[-*]\s*Verdict\s*:", l, flags=re.IGNORECASE)]
    if len(claim_headings) < 4:
        report.add(f"{rel}:{claims_start}", f"`## Claims` holds {len(claim_headings)} claims, expected at least four")
    if len(verdicts) < len(claim_headings):
        report.add(f"{rel}:{claims_start}", "every claim needs a Verdict line")
    for lineno, line in enumerate(claim_block, start=claims_start + 1):
        match = re.match(r"^\s*[-*]\s*Verdict\s*:\s*(?P<verdict>.+)$", line, flags=re.IGNORECASE)
        if match:
            verdict = match.group("verdict").strip().lower().rstrip(".")
            if verdict not in ("stands", "recorded unverified", "watchlist", "cut"):
                report.add(f"{rel}:{lineno}", f"verdict {verdict!r} is not one of stands, recorded unverified, watchlist, cut")

    notes_start, notes_end = bounds["Link notes"]
    if not [l for l in lines[notes_start:notes_end] if l.strip()]:
        report.add(f"{rel}:{notes_start}", "`## Link notes` is empty")
    proposal_start, proposal_end = bounds["Benchmark proposal"]
    if len([l for l in lines[proposal_start:proposal_end] if l.strip()]) < 2:
        report.add(f"{rel}:{proposal_start}", "`## Benchmark proposal` is empty or too thin")

    for lineno, line in enumerate(lines, start=1):
        lowered = line.lower()
        for placeholder in PLACEHOLDERS:
            if placeholder in lowered:
                report.add(f"{rel}:{lineno}", f"placeholder text {placeholder!r}")


BENCH_SECTIONS = (
    "Claim under test",
    "Why it matters",
    "Method",
    "Evidence fields",
    "Environment",
    "How to run",
    "Results",
    "Analysis",
    "What this machine cannot measure",
    "Reproduce on another machine",
)


def check_benchmarks(report: Report, expected_sections: int = SECTION_COUNT) -> None:
    root = REPO_ROOT / "misc" / "benchmarks"
    if not root.is_dir():
        report.add("benchmarks", "directory is missing")
        return
    dirs = sorted(p for p in root.iterdir() if p.is_dir() and p.name != "common")
    covered: set[int] = set()
    for directory in dirs:
        rel = f"misc/benchmarks/{directory.name}"
        match = re.match(r"^(\d{2})-", directory.name)
        if not match:
            report.add(rel, "directory name does not start with the section number")
        else:
            covered.add(int(match.group(1)))
        for required in ("bench.py", "run.sh", "README.md", "requirements.txt"):
            if not (directory / required).is_file():
                report.add(rel, f"missing {required}")
        for required in ("results/raw.txt", "results/summary.md"):
            path = directory / required
            if not path.is_file():
                report.add(rel, f"missing {required}")
            elif path.stat().st_size == 0:
                report.add(f"{rel}/{required}", "committed results file is empty")
        run = directory / "run.sh"
        if run.is_file() and not run.stat().st_mode & 0o111:
            report.add(f"{rel}/run.sh", "is not executable")
        readme = directory / "README.md"
        if readme.is_file():
            text = readme.read_text(encoding="utf-8")
            lines = text.splitlines()
            headings = [l[3:].strip() for l in lines if l.startswith("## ")]
            for required in BENCH_SECTIONS:
                if required not in headings:
                    report.add(f"{rel}/README.md", f"missing template section {required!r}")
            for lineno, line in enumerate(lines, start=1):
                lowered = line.lower()
                for placeholder in PLACEHOLDERS:
                    if placeholder in lowered:
                        report.add(f"{rel}/README.md:{lineno}", f"placeholder text {placeholder!r}")
                if re.match(r"^\|\s*\|", line) or re.search(r"\|\s+\|\s*$", line):
                    report.add(f"{rel}/README.md:{lineno}", "empty table cell in an evidence table")
                if "\u2014" in line:
                    report.add(f"{rel}/README.md:{lineno}", "em dash")
    missing = [n for n in range(1, expected_sections + 1) if n not in covered]
    if missing:
        report.add("benchmarks", f"no benchmark for section(s) {', '.join(str(m) for m in missing)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--draft", help="check one section draft under misc/notes/sections/")
    parser.add_argument("--readme-only", action="store_true")
    parser.add_argument("--skip-benchmarks", action="store_true")
    args = parser.parse_args(argv)

    if args.draft:
        path = Path(args.draft)
        if not path.is_absolute():
            path = REPO_ROOT / args.draft
        if not path.is_file():
            print(f"no such draft: {path}", file=sys.stderr)
            return 2
        report = Report()
        check_draft(path, report)
        report.dump(str(path.name))
        return 0 if report.ok() else 1

    failed = False
    readme = REPO_ROOT / "README.md"
    if readme.is_file():
        report = Report()
        check_readme(readme, report)
        report.dump("README.md")
        failed |= not report.ok()
    else:
        print("FAIL README.md: missing")
        failed = True

    if not args.readme_only:
        contributing = REPO_ROOT / "CONTRIBUTING.md"
        if contributing.is_file():
            report = Report()
            lines = contributing.read_text(encoding="utf-8").splitlines()
            _, meta = parse(lines, source="CONTRIBUTING.md")
            _check_text_rules(lines, meta, "CONTRIBUTING.md", report)
            _check_links(lines, meta, "CONTRIBUTING.md", report)
            report.dump("CONTRIBUTING.md")
            failed |= not report.ok()
        else:
            print("FAIL CONTRIBUTING.md: missing")
            failed = True

        if not args.skip_benchmarks:
            report = Report()
            check_benchmarks(report)
            report.dump("benchmarks")
            failed |= not report.ok()

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
