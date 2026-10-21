#!/usr/bin/env python3
"""03. A box blur is not a cheap Gaussian.

Claim under test: a box blur and a Gaussian of equal support are interchangeable, so the
cheaper one is free.

The benchmark measures three things on seeded synthetic images: the frequency response of
both filters, including the frequencies where the box filter inverts contrast; the edge
profile each one produces on an ideal step; and the cost of a separable Gaussian against the
same kernel applied as a full two dimensional convolution.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "03. A box blur is not a cheap Gaussian"
CLAIM = "a box blur and a Gaussian of equal support are interchangeable, so the cheaper one is free"

SIGMA = 2.0


def gaussian_kernel(sigma: float) -> np.ndarray:
    radius = int(np.ceil(3.0 * sigma))
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    kernel = np.exp(-(x ** 2) / (2.0 * sigma ** 2))
    return kernel / kernel.sum()


def box_kernel(width: int) -> np.ndarray:
    return np.full(width, 1.0 / width, dtype=np.float64)


def conv_rows(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    radius = len(kernel) // 2
    padded = np.pad(image, ((0, 0), (radius, radius)), mode="edge")
    out = np.zeros_like(image, dtype=np.float64)
    for offset, weight in enumerate(kernel):
        out += weight * padded[:, offset : offset + image.shape[1]]
    return out


def separable(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    return conv_rows(conv_rows(image, kernel).T, kernel).T


def full_2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """The same kernel applied as an outer product, which is what a naive implementation does."""
    kernel2d = np.outer(kernel, kernel)
    radius = len(kernel) // 2
    padded = np.pad(image, radius, mode="edge")
    out = np.zeros_like(image, dtype=np.float64)
    for dy in range(kernel2d.shape[0]):
        for dx in range(kernel2d.shape[1]):
            out += kernel2d[dy, dx] * padded[dy : dy + image.shape[0], dx : dx + image.shape[1]]
    return out


def sinusoid(width: int, cycles_per_pixel: float) -> np.ndarray:
    x = np.arange(width, dtype=np.float64)
    return 0.5 + 0.5 * np.cos(2.0 * np.pi * cycles_per_pixel * x)


def amplitude(signal: np.ndarray) -> float:
    centred = signal - signal.mean()
    return float(centred.max() - centred.min()) / 2.0


def signed_gain(original: np.ndarray, filtered: np.ndarray) -> float:
    """Gain with sign, so a contrast inversion shows up as a negative number."""
    a = original - original.mean()
    b = filtered - filtered.mean()
    denominator = float((a * a).sum())
    return float((a * b).sum() / denominator) if denominator else 0.0


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    size = 256 if quick else 1024
    repeats = 3 if quick else 7

    gauss = gaussian_kernel(SIGMA)
    width = len(gauss)
    box = box_kernel(width)
    # A box whose second moment matches the Gaussian, which is the fairest possible comparison.
    matched_width = max(3, int(round(np.sqrt(12.0 * SIGMA ** 2 + 1.0))))
    if matched_width % 2 == 0:
        matched_width += 1
    matched = box_kernel(matched_width)

    freqs = [0.02, 0.05, 0.0769, 0.1, 0.1538, 0.2, 0.25, 0.3, 0.4]
    rows = []
    for freq in freqs:
        row = sinusoid(size, freq)
        signal = np.tile(row, (8, 1))
        g = signed_gain(row, separable(signal, gauss)[4])
        b = signed_gain(row, separable(signal, box)[4])
        m = signed_gain(row, separable(signal, matched)[4])
        rows.append([f"{freq:.4f}", f"{1.0 / freq:.1f}", f"{g:+.4f}", f"{b:+.4f}", f"{m:+.4f}"])
    response_table = timing.markdown_table(
        [
            "Frequency (cycles per pixel)",
            "Period (pixels)",
            f"Gaussian gain (sigma {SIGMA:g})",
            f"Box gain (width {width})",
            f"Variance matched box gain (width {matched_width})",
        ],
        rows,
    )
    inversions = [row[0] for row in rows if float(row[3]) < 0]

    # Edge profile on an ideal step.
    step = np.zeros((16, size), dtype=np.float64)
    step[:, size // 2 :] = 1.0
    profiles = {
        "Gaussian": separable(step, gauss)[8],
        "box": separable(step, box)[8],
        "variance matched box": separable(step, matched)[8],
    }
    edge_rows = []
    for name, profile in profiles.items():
        centre = size // 2
        window = profile[centre - 16 : centre + 16]
        rise = int(np.sum((window > 0.1) & (window < 0.9)))
        overshoot = float(profile.max() - 1.0)
        second = np.diff(profile, n=2)
        edge_rows.append(
            [
                name,
                str(rise),
                f"{overshoot:+.2e}",
                f"{np.abs(second).max():.4f}",
                f"{np.sqrt(((profile - profiles['Gaussian']) ** 2).mean()):.4f}",
            ]
        )
    edge_table = timing.markdown_table(
        [
            "Filter",
            "Ten to ninety per cent rise (pixels)",
            "Overshoot (fraction of step)",
            "Largest second difference (per pixel)",
            "RMSE against the Gaussian profile",
        ],
        edge_rows,
    )

    image = rng.random((size, size))
    timings = [
        timing.measure(lambda: separable(image, gauss), label="separable Gaussian, two passes", repeats=repeats, inside_timer="convolution only"),
        timing.measure(lambda: full_2d(image, gauss), label="same kernel as a full two dimensional convolution", repeats=repeats, inside_timer="convolution only"),
        timing.measure(lambda: separable(image, box), label="separable box", repeats=repeats, inside_timer="convolution only"),
    ]
    cost_table = timing.table(timings, first_column="Implementation") + (
        f"\n\nImage is {size} by {size} pixels, kernel support {width} taps, float64 throughout."
    )
    speedup = timings[1].median_ms / timings[0].median_ms

    worst_gain_gap = max(abs(float(row[2]) - float(row[3])) for row in rows)
    reading = (
        f"The two filters are not the same operator. Across the frequency sweep their signed "
        f"gains differ by up to {worst_gain_gap:.2f}, and the box filter inverts contrast at "
        f"{len(inversions)} of the {len(rows)} tested frequencies, where the Gaussian stays "
        f"positive everywhere. Contrast inversion is not a small error: a feature that depends "
        f"on the sign of a gradient flips. On an ideal step the box filter produces a profile "
        f"whose second difference is larger, which is the visible blocking a reader will "
        f"recognise. Separability is where the cheap win actually is: the identical Gaussian "
        f"kernel applied as a full two dimensional convolution costs {speedup:.1f} times the "
        f"separable form. The claim under test fails, and the correct cheap filter is a "
        f"separable Gaussian rather than a box."
    )

    return (
        [
            ("Frequency response, measured on sinusoids", response_table),
            ("Edge profile on an ideal step", edge_table),
            ("Cost", cost_table),
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
