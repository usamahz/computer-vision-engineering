"""One determinism setup, so two runs on one machine produce the same inputs.

Accuracy-style numbers in this repository must be bit-identical between runs on the same
machine. Only the timings move. Anything else is a bug in the benchmark, not noise.

Thread limits have to be set before numpy imports its BLAS, which means `run.sh` sets the
environment and this module reports what it found. A benchmark that silently inherits a
different thread count is not comparable with the committed results, so `require_threads`
says so loudly rather than quietly producing a different number.
"""

from __future__ import annotations

import os
import random
import sys

SEED = 20261018
THREAD_KEYS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")


def rng(seed: int = SEED):
    """The only random source a benchmark may use."""
    import numpy as np

    return np.random.default_rng(seed)


def seed_stdlib(seed: int = SEED) -> None:
    random.seed(seed)


def thread_limits() -> dict[str, str]:
    return {key: os.environ.get(key, "unset") for key in THREAD_KEYS}


def require_threads(expected: str = "1", *, strict: bool = False) -> None:
    """Warn, or fail, when the thread environment is not the one the results were taken under."""
    limits = thread_limits()
    wrong = {k: v for k, v in limits.items() if v != expected}
    if not wrong:
        return
    message = (
        "thread limits differ from the committed runs: "
        + ", ".join(f"{k}={v}" for k, v in wrong.items())
        + f" (expected {expected}). Run through ./run.sh, which sets them."
    )
    if strict:
        raise RuntimeError(message)
    print(f"warning: {message}", file=sys.stderr)


def describe(seed: int = SEED) -> str:
    return f"seed={seed}, thread limits " + ", ".join(f"{k}={v}" for k, v in thread_limits().items())
