"""Shared harness for the microbenchmarks.

Three modules, one responsibility each:

- `device`   what machine this is, measured at run time
- `timing`   warmup, repeats, median, interquartile range, ninety-fifth percentile
- `determinism`  the seed and the thread limits

A benchmark imports from here and nowhere else. Nothing in `misc/benchmarks/NN-slug/` may import
from another benchmark directory, so that the three things above have exactly one definition
in the repository.
"""

from . import determinism, device, report, timing  # noqa: F401

__all__ = ["determinism", "device", "report", "timing"]
