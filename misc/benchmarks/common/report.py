"""Writing the two committed evidence files, identically for every benchmark.

`results/raw.txt` is the unedited stdout of a full run, including the machine banner.
`results/summary.md` holds the tables and one paragraph that reads them, and may contain no
number that is not in `raw.txt`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import determinism, device


def header(title: str, claim: str, extra: dict[str, object] | None = None) -> str:
    return "\n".join(
        [
            f"# {title}",
            "",
            f"claim under test: {claim}",
            "",
            device.banner(extra),
            determinism.describe(),
            "",
        ]
    )


def write_summary(path: str | Path, title: str, blocks: list[tuple[str, str]], reading: str) -> None:
    """Write results/summary.md from the same strings that were printed to stdout."""
    out = [f"# {title}", "", f"Measured on: {device.short_machine()}.", f"Determinism: {determinism.describe()}.", ""]
    for heading, body in blocks:
        out.append(f"## {heading}")
        out.append("")
        out.append(body.rstrip())
        out.append("")
    out.append("## Reading")
    out.append("")
    out.append(reading.strip())
    out.append("")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(out), encoding="utf-8")
    print(f"\nwrote {path}", file=sys.stderr)


def emit(blocks: list[tuple[str, str]], reading: str) -> None:
    for heading, body in blocks:
        print(f"\n--- {heading} ---\n")
        print(body)
    print("\n--- reading ---\n")
    print(reading.strip())
