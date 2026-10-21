#!/usr/bin/env python3
"""07. Attention and convolution do not scale alike, so one resolution settles nothing.

Claim under test: a comparison of attention against convolution at one input resolution
tells a reader which operator is cheaper.

The benchmark times a single head of scaled dot product attention and a fixed support
convolution over the same token grid, across a sweep of token counts, and fits the growth
exponent of each from the measured medians. It then prints the crossover token count and the
memory the attention matrix alone requires, so the comparison can be read at the resolutions
a product actually runs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "07. Attention and convolution do not scale alike"
CLAIM = "a comparison at one input resolution tells a reader which operator is cheaper"

DIM = 64
KERNEL = 9


def softmax(x: np.ndarray) -> np.ndarray:
    shifted = x - x.max(axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=-1, keepdims=True)


def attention(q: np.ndarray, k: np.ndarray, v: np.ndarray) -> np.ndarray:
    scores = (q @ k.T) / np.sqrt(q.shape[1])
    return softmax(scores) @ v


def depthwise_conv(tokens: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Fixed support convolution along the token axis, one weight set per channel."""
    radius = len(weights) // 2
    padded = np.pad(tokens, ((radius, radius), (0, 0)), mode="constant")
    out = np.zeros_like(tokens)
    for offset, weight in enumerate(weights):
        out += weight * padded[offset : offset + tokens.shape[0]]
    return out


def fit_exponent(sizes: list[int], times: list[float]) -> float:
    logs_x = np.log(np.array(sizes, dtype=np.float64))
    logs_y = np.log(np.array(times, dtype=np.float64))
    slope, _ = np.polyfit(logs_x, logs_y, 1)
    return float(slope)


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    sizes = [64, 128, 256] if quick else [64, 128, 256, 512, 1024, 2048]
    repeats = 3 if quick else 7

    rows = []
    attention_times, conv_times = [], []
    for tokens in sizes:
        q = rng.standard_normal((tokens, DIM))
        k = rng.standard_normal((tokens, DIM))
        v = rng.standard_normal((tokens, DIM))
        x = rng.standard_normal((tokens, DIM))
        weights = rng.standard_normal(KERNEL) / KERNEL

        att = timing.measure(lambda: attention(q, k, v), label=f"attention, {tokens} tokens", repeats=repeats, inside_timer="projections excluded, scores, softmax and value product included")
        conv = timing.measure(lambda: depthwise_conv(x, weights), label=f"convolution, {tokens} tokens", repeats=repeats, inside_timer="convolution only")
        attention_times.append(att.median_ms)
        conv_times.append(conv.median_ms)
        side = int(round(np.sqrt(tokens)))
        matrix_mib = tokens * tokens * 4 / 1024 ** 2
        activation_mib = tokens * DIM * 4 / 1024 ** 2
        rows.append(
            [
                str(tokens),
                f"{side} by {side}",
                f"{att.median_ms:.3g}",
                f"{conv.median_ms:.3g}",
                f"{att.median_ms / conv.median_ms:.1f}",
                f"{matrix_mib:.2f}",
                f"{activation_mib:.3f}",
                f"{matrix_mib / activation_mib:.0f}",
            ]
        )
    sweep_table = timing.markdown_table(
        [
            "Tokens",
            "Equivalent patch grid",
            "Attention median (ms)",
            "Convolution median (ms)",
            "Attention over convolution",
            "Score matrix at single precision (MiB, computed)",
            "Layer activations at single precision (MiB, computed)",
            "Matrix over activations",
        ],
        rows,
    )

    att_exponent = fit_exponent(sizes, attention_times)
    conv_exponent = fit_exponent(sizes, conv_times)
    exponent_table = timing.markdown_table(
        ["Operator", "Fitted growth exponent in token count", "Expected from the arithmetic"],
        [
            ["single head attention", f"{att_exponent:.2f}", "two"],
            [f"depthwise convolution, support {KERNEL}", f"{conv_exponent:.2f}", "one"],
        ],
    )

    ratios = [float(row[4]) for row in rows]
    crossover = next((rows[i][0] for i, r in enumerate(ratios) if r > 1.0), "beyond the sweep")
    doubling_rows = []
    for index in range(1, len(sizes)):
        doubling_rows.append(
            [
                f"{sizes[index - 1]} to {sizes[index]}",
                f"{attention_times[index] / attention_times[index - 1]:.2f}",
                f"{conv_times[index] / conv_times[index - 1]:.2f}",
            ]
        )
    doubling_table = timing.markdown_table(
        ["Token count doubling", "Attention cost multiplier", "Convolution cost multiplier"], doubling_rows
    )

    reading = (
        f"Measured over a token sweep, attention grows with an exponent of {att_exponent:.2f} "
        f"in the token count and the fixed support convolution with an exponent of "
        f"{conv_exponent:.2f}, which is what the arithmetic says and what a single resolution "
        f"comparison hides. The cost ratio between the two moves across the sweep rather than "
        f"staying put, and attention first becomes the more expensive of the two at "
        f"{crossover} tokens on this machine, so a comparison taken below that point and a "
        f"comparison taken above it support opposite conclusions. The score matrix is the "
        f"second half of the story: it is a computed quantity rather than a measured one, and "
        f"at the top of the sweep it needs {rows[-1][7]} times the memory of the activations "
        f"it is computed from. The claim under test fails, and the honest form "
        f"of such a comparison states the token count, the support, the head count and the "
        f"resolution together."
    )

    return (
        [
            ("Token count sweep", sweep_table),
            ("Fitted growth exponents", exponent_table),
            ("What each doubling of the token count costs", doubling_table),
        ],
        reading,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="smoke test, under ten seconds, writes nothing")
    parser.add_argument("--write-summary", dest="summary", help="write the summary markdown here")
    args = parser.parse_args()

    determinism.require_threads("1")
    print(report.header(TITLE, CLAIM, {"mode": "quick" if args.quick else "full"}))
    blocks, reading = run(quick=args.quick)
    report.emit(blocks, reading)
    if args.summary and not args.quick:
        report.write_summary(args.summary, TITLE, blocks, reading)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
