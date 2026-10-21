#!/usr/bin/env python3
"""15. One speedup figure for a model is not a fact about a layer.

Claim under test: integer quantisation makes a model smaller and faster, so a single speedup
figure describes it.

The benchmark quantises seeded matrices at four shapes a vision network actually contains,
multiplies them in eight bit integers with a thirty two bit accumulator, and reports the
signal to quantisation noise ratio against the float result under per tensor and per channel
scales. It then times three variants: the float product, the integer product alone, and the
integer product with the quantise and requantise steps inside the timer, which is where a
published speedup usually draws its boundary.

The machine has no GPU and no neural accelerator, so this measures the arithmetic and the
kernel available to it, not a vendor runtime's integer path.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "15. One speedup figure for a model is not a fact about a layer"
CLAIM = "integer quantisation makes a model smaller and faster, so one speedup figure describes it"

SHAPES = [
    ("pointwise convolution, small channels", 3136, 64, 64),
    ("feature mixing, wide", 1024, 256, 256),
    ("tall activation, narrow channels", 4096, 32, 128),
    ("classifier head", 128, 2048, 1000),
]


def make_layer(rng, m: int, k: int, n: int, outlier_fraction: float = 0.03):
    """Activations and weights, with a few outlier output channels, which is what real weights do."""
    activations = np.abs(rng.normal(0.0, 1.0, size=(m, k))).astype(np.float32)
    weights = rng.normal(0.0, 0.05, size=(k, n)).astype(np.float32)
    outliers = rng.choice(n, size=max(int(n * outlier_fraction), 1), replace=False)
    weights[:, outliers] *= 9.0
    return activations, weights


def quantise_per_tensor(matrix: np.ndarray):
    scale = float(np.abs(matrix).max()) / 127.0
    scale = scale if scale > 0 else 1.0
    return np.clip(np.rint(matrix / scale), -127, 127).astype(np.int8), scale


def quantise_per_channel(matrix: np.ndarray, axis: int = 0):
    scales = np.abs(matrix).max(axis=axis, keepdims=True) / 127.0
    scales = np.where(scales > 0, scales, 1.0)
    return np.clip(np.rint(matrix / scales), -127, 127).astype(np.int8), scales


def integer_product(a_q: np.ndarray, b_q: np.ndarray) -> np.ndarray:
    """Eight bit inputs, thirty two bit accumulator, which is what an integer kernel does."""
    return a_q.astype(np.int32) @ b_q.astype(np.int32)


def sqnr_db(reference: np.ndarray, approximation: np.ndarray) -> float:
    signal = float((reference.astype(np.float64) ** 2).sum())
    noise = float(((reference.astype(np.float64) - approximation.astype(np.float64)) ** 2).sum())
    if noise == 0:
        return float("inf")
    return 10.0 * np.log10(signal / noise)


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    repeats = 3 if quick else 7
    shapes = SHAPES[:2] if quick else SHAPES

    accuracy_rows = []
    latency_rows = []
    for name, m, k, n in shapes:
        if quick:
            m, k, n = max(m // 4, 32), max(k // 2, 16), max(n // 2, 16)
        activations, weights = make_layer(rng, m, k, n)
        reference = activations @ weights

        a_q, a_scale = quantise_per_tensor(activations)
        w_tensor_q, w_scale = quantise_per_tensor(weights)
        w_channel_q, w_scales = quantise_per_channel(weights, axis=0)

        per_tensor = integer_product(a_q, w_tensor_q).astype(np.float32) * (a_scale * w_scale)
        per_channel = integer_product(a_q, w_channel_q).astype(np.float32) * (a_scale * w_scales.astype(np.float32))

        accuracy_rows.append(
            [
                name,
                f"{m} by {k} by {n}",
                f"{sqnr_db(reference, per_tensor):.1f}",
                f"{sqnr_db(reference, per_channel):.1f}",
                f"{float(np.abs(reference - per_tensor).max()):.4f}",
                f"{float(np.abs(reference - per_channel).max()):.4f}",
            ]
        )

        float_timing = timing.measure(
            lambda a=activations, w=weights: a @ w,
            label=f"{name}, float",
            repeats=repeats,
            inside_timer="matrix product only",
        )
        integer_timing = timing.measure(
            lambda a=a_q, w=w_channel_q: integer_product(a, w),
            label=f"{name}, integer core",
            repeats=repeats,
            inside_timer="integer matrix product only, quantisation outside",
        )
        full_timing = timing.measure(
            lambda a=activations, w=weights: (
                integer_product(*(lambda q: (q[0], quantise_per_channel(w, axis=0)[0]))(quantise_per_tensor(a))).astype(np.float32)
            ),
            label=f"{name}, integer with quantisation inside",
            repeats=repeats,
            inside_timer="quantise, integer product and cast back, all inside",
        )
        latency_rows.append(
            [
                name,
                f"{float_timing.median_ms:.3g}",
                f"{integer_timing.median_ms:.3g}",
                f"{full_timing.median_ms:.3g}",
                f"{float_timing.median_ms / integer_timing.median_ms:.2f}",
                f"{float_timing.median_ms / full_timing.median_ms:.2f}",
                f"{integer_timing.p95_ms:.3g}",
            ]
        )

    accuracy_table = timing.markdown_table(
        [
            "Layer shape",
            "Dimensions, rows by inputs by outputs",
            "Per tensor scale, signal to quantisation noise (dB)",
            "Per channel scale, signal to quantisation noise (dB)",
            "Per tensor worst absolute error",
            "Per channel worst absolute error",
        ],
        accuracy_rows,
    )
    latency_table = timing.markdown_table(
        [
            "Layer shape",
            "Float median (ms)",
            "Integer core median (ms)",
            "Integer with quantisation inside the timer, median (ms)",
            "Speedup, integer core against float",
            "Speedup, integer with quantisation against float",
            "Integer core p95 (ms)",
        ],
        latency_rows,
    )

    size_rows = []
    for name, m, k, n in shapes:
        if quick:
            m, k, n = max(m // 4, 32), max(k // 2, 16), max(n // 2, 16)
        float_bytes = k * n * 4
        int_bytes = k * n * 1 + n * 4
        size_rows.append([name, f"{float_bytes / 1024:.1f}", f"{int_bytes / 1024:.1f}", f"{float_bytes / int_bytes:.2f}"])
    size_table = timing.markdown_table(
        ["Layer shape", "Float weights (KiB, computed)", "Integer weights plus per channel scales (KiB, computed)", "Ratio"],
        size_rows,
    )

    speedups = [float(row[4]) for row in latency_rows]
    full_speedups = [float(row[5]) for row in latency_rows]
    gains = [float(row[3]) - float(row[2]) for row in accuracy_rows]
    straddles = min(speedups) < 1.0 < max(speedups)
    all_slower = max(speedups) < 1.0
    reading = (
        f"The two halves of the claim come apart, and neither is a single number. On accuracy, "
        f"moving from a per tensor scale to a per channel scale buys between "
        f"{min(gains):.1f} and {max(gains):.1f} decibels of signal to quantisation noise "
        f"depending on the shape, at no cost in arithmetic and almost none in storage, because "
        f"a few outlier output channels otherwise set the scale for every channel. The spread "
        f"across shapes is the point: the same change is worth different amounts in different "
        f"layers of one network. On latency the result here is blunt. The integer core runs at "
        f"{min(speedups):.2f} to {max(speedups):.2f} times the speed of the float product, so "
        f"it is {'slower at every shape measured' if all_slower else 'faster at some shapes and slower at others'}"
        f", and with the quantise and requantise steps inside the timer it runs at "
        f"{min(full_speedups):.2f} to {max(full_speedups):.2f} times. "
        f"{'The ranges straddle parity, so the sign of the change depends on the shape. ' if straddles else ''}"
        f"The reason is the lesson rather than a caveat: the float product dispatches to a "
        f"tuned library kernel, while the integer product falls back to a generic path that "
        f"widens everything to a thirty two bit accumulator first, so cheaper arithmetic does "
        f"not imply a faster layer unless a kernel exists for it on the target. That is also "
        f"why a vendor's integer speedup does not transfer to another runtime, and why the "
        f"timer boundary matters: the quantise and requantise steps are real work that a "
        f"published figure often leaves outside. Weight storage is the one part that behaves "
        f"as advertised, and it is computed rather than measured. The claim under test fails: "
        f"a model level speedup figure, quoted without the shape, the scale granularity, the "
        f"kernel and the timer boundary, describes no layer in the model."
    )

    return (
        [
            ("Accuracy of the integer product, by shape and scale granularity", accuracy_table),
            ("Latency, with the timer boundary stated", latency_table),
            ("Weight storage", size_table),
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
