"""One timing implementation, so that no two benchmarks disagree about how they measured.

Rules this module enforces by construction:

- `time.perf_counter_ns` only, never `time.time`.
- Warmup iterations are discarded and their count is reported.
- The headline is the median. The interquartile range and the ninety-fifth percentile travel
  with it, because a shared virtual machine has fatter tails than a laptop and a median alone
  invites a misreading.
- The number of repeats is part of the result, printed next to the number.
- What is inside the timer is whatever the caller put inside the callable. Every benchmark
  README states it in prose; this module cannot know it, and does not pretend to.
"""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Callable, Sequence


@dataclass
class Timing:
    label: str
    samples_ms: list[float] = field(default_factory=list)
    warmup: int = 0
    inside_timer: str = "unstated"

    @property
    def repeats(self) -> int:
        return len(self.samples_ms)

    @property
    def median_ms(self) -> float:
        return statistics.median(self.samples_ms)

    @property
    def iqr_ms(self) -> float:
        if len(self.samples_ms) < 4:
            return 0.0
        quarters = statistics.quantiles(self.samples_ms, n=4, method="inclusive")
        return quarters[2] - quarters[0]

    @property
    def p95_ms(self) -> float:
        return percentile(self.samples_ms, 95)

    @property
    def min_ms(self) -> float:
        return min(self.samples_ms)

    def row(self) -> list[str]:
        return [
            self.label,
            f"{self.median_ms:.3g}",
            f"{self.iqr_ms:.3g}",
            f"{self.p95_ms:.3g}",
            str(self.repeats),
        ]


def percentile(values: Sequence[float], pct: float) -> float:
    """Nearest-rank percentile. No interpolation, so the number is always a measured sample."""
    if not values:
        raise ValueError("no samples")
    ordered = sorted(values)
    rank = max(1, min(len(ordered), int(round(pct / 100.0 * len(ordered) + 0.5))))
    return ordered[rank - 1]


def measure(
    fn: Callable[[], object],
    *,
    label: str,
    repeats: int = 7,
    warmup: int = 2,
    inside_timer: str = "unstated",
) -> Timing:
    """Time `fn` and return the distribution. The callable takes no arguments."""
    for _ in range(warmup):
        fn()
    samples: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        fn()
        samples.append((time.perf_counter_ns() - start) / 1e6)
    return Timing(label=label, samples_ms=samples, warmup=warmup, inside_timer=inside_timer)


def table(timings: list[Timing], *, first_column: str = "Variant") -> str:
    header = (
        f"| {first_column} | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |\n"
        "| --- | --- | --- | --- | --- |"
    )
    rows = [f"| {' | '.join(t.row())} |" for t in timings]
    return "\n".join([header, *rows])


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """A table for accuracy-style results, where the column headers carry the units."""
    head = f"| {' | '.join(str(h) for h in headers)} |"
    rule = f"| {' | '.join('---' for _ in headers)} |"
    body = [f"| {' | '.join(str(c) for c in row)} |" for row in rows]
    return "\n".join([head, rule, *body])


def throughput(items: int, timing: Timing) -> float:
    """Items per second computed from the median, never from the minimum."""
    return items / (timing.median_ms / 1000.0)
