#!/usr/bin/env python3
"""01. Pixel values are not the measurement.

Claim under test: the array in memory is the scene, so the transfer function that produced it
is a detail that does not change what a pipeline computes.

The benchmark encodes one seeded linear-light scene through the piecewise curve used by the
standard colour space and through a plain power law, quantises both to eight bit, and then
asks three questions: how far apart the two arrays are in code levels, what happens when a
resize averages encoded values instead of linear ones, and how a threshold on an encoded
value differs from the same threshold applied to radiance.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "01. Pixel values are not the measurement"
CLAIM = (
    "the array in memory is the scene, so the transfer function that produced it does not "
    "change what a pipeline computes"
)

SRGB_BREAK_ENCODED = 0.04045
SRGB_BREAK_LINEAR = 0.0031308
MID_GREY = 0.18


def srgb_encode(linear: np.ndarray) -> np.ndarray:
    """Piecewise opto-electronic transfer function of the standard colour space."""
    linear = np.clip(linear, 0.0, 1.0)
    low = linear * 12.92
    high = 1.055 * np.power(np.maximum(linear, 1e-12), 1.0 / 2.4) - 0.055
    return np.where(linear <= SRGB_BREAK_LINEAR, low, high)


def srgb_decode(encoded: np.ndarray) -> np.ndarray:
    encoded = np.clip(encoded, 0.0, 1.0)
    low = encoded / 12.92
    high = np.power((encoded + 0.055) / 1.055, 2.4)
    return np.where(encoded <= SRGB_BREAK_ENCODED, low, high)


def power_encode(linear: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    return np.power(np.clip(linear, 0.0, 1.0), 1.0 / gamma)


def power_decode(encoded: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    return np.power(np.clip(encoded, 0.0, 1.0), gamma)


def radiance_scene(rng, size: int) -> np.ndarray:
    """A linear-light scene spanning about three decades, with texture and two highlights."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float64) / max(size - 1, 1)
    # Smooth illumination falloff, which is what a real scene does to radiance.
    field = 0.0015 + 0.75 * (x ** 2.2) * (0.35 + 0.65 * (1.0 - y))
    # Reflectance texture: piecewise constant patches, so edges exist at every brightness.
    patch = rng.uniform(0.18, 1.0, size=(8, 8))
    reflectance = np.kron(patch, np.ones((size // 8 + 1, size // 8 + 1)))[:size, :size]
    scene = field * reflectance
    # Two small specular highlights, which is where the encoded curve is flattest.
    for cx, cy, radius in ((0.72, 0.3, 0.035), (0.25, 0.8, 0.02)):
        mask = ((x - cx) ** 2 + (y - cy) ** 2) < radius ** 2
        scene = np.where(mask, np.minimum(scene + 0.9, 1.0), scene)
    return np.clip(scene, 0.0, 1.0)


def quantise(encoded: np.ndarray) -> np.ndarray:
    return np.rint(np.clip(encoded, 0.0, 1.0) * 255.0).astype(np.int16)


def halve(image: np.ndarray) -> np.ndarray:
    """Two by two box average, the cheapest resize a pipeline ever does."""
    h, w = image.shape[0] - image.shape[0] % 2, image.shape[1] - image.shape[1] % 2
    return image[:h, :w].reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    size = 256 if quick else 1024
    repeats = 3 if quick else 9
    scene = radiance_scene(rng, size)

    srgb_codes = quantise(srgb_encode(scene))
    power_codes = quantise(power_encode(scene))
    delta = np.abs(srgb_codes - power_codes)

    # How the two encodings disagree, by scene brightness decade.
    rows = []
    edges = [(0.0, 0.01), (0.01, 0.05), (0.05, 0.18), (0.18, 0.5), (0.5, 1.01)]
    for low, high in edges:
        mask = (scene >= low) & (scene < high)
        if not mask.any():
            continue
        rows.append(
            [
                f"{low:g} to {high:g}",
                int(mask.sum()),
                f"{delta[mask].mean():.2f}",
                int(delta[mask].max()),
                f"{100.0 * (delta[mask] > 1).mean():.1f}",
            ]
        )
    encoding_table = timing.markdown_table(
        ["Scene radiance band", "Pixels", "Mean code difference (levels)", "Max (levels)", "Over one level (%)"],
        rows,
    )

    # Averaging in the encoded domain against averaging in linear light.
    encoded = srgb_encode(scene)
    naive = srgb_decode(halve(encoded))
    correct = halve(scene)
    error = naive - correct
    rel = error / np.maximum(correct, 1e-6)
    bright = correct >= MID_GREY
    dark = correct < 0.05

    resize_table = timing.markdown_table(
        ["Region", "Pixels", "Mean signed error (linear light)", "RMSE (linear light)", "Mean relative error (%)"],
        [
            ["whole frame", int(correct.size), f"{error.mean():+.5f}", f"{np.sqrt((error ** 2).mean()):.5f}", f"{100 * rel.mean():+.2f}"],
            ["radiance below one twentieth", int(dark.sum()), f"{error[dark].mean():+.5f}", f"{np.sqrt((error[dark] ** 2).mean()):.5f}", f"{100 * rel[dark].mean():+.2f}"],
            ["radiance above mid grey", int(bright.sum()), f"{error[bright].mean():+.5f}", f"{np.sqrt((error[bright] ** 2).mean()):.5f}", f"{100 * rel[bright].mean():+.2f}"],
        ],
    )

    # A threshold that means one thing in radiance and another in code values.
    truth = scene >= MID_GREY
    on_encoded = encoded >= MID_GREY
    on_power = power_encode(scene) >= MID_GREY
    threshold_table = timing.markdown_table(
        ["Decision rule", "Pixels selected", "Disagreement with radiance rule (%)"],
        [
            ["radiance at or above mid grey", int(truth.sum()), "0.0"],
            ["standard encoded value at or above mid grey", int(on_encoded.sum()), f"{100 * (on_encoded != truth).mean():.1f}"],
            ["power law encoded value at or above mid grey", int(on_power.sum()), f"{100 * (on_power != truth).mean():.1f}"],
        ],
    )

    megapixels = scene.size / 1e6
    timings = [
        timing.measure(lambda: srgb_encode(scene), label="piecewise encode", repeats=repeats, inside_timer="encode only"),
        timing.measure(lambda: power_encode(scene), label="power law encode", repeats=repeats, inside_timer="encode only"),
        timing.measure(lambda: srgb_decode(encoded), label="piecewise decode", repeats=repeats, inside_timer="decode only"),
    ]
    cost_table = timing.table(timings, first_column="Conversion") + (
        f"\n\nFrame is {size} by {size} pixels, {megapixels:.3f} megapixels, float64 throughout."
    )

    worst = int(delta.max())
    disagree = 100 * (on_encoded != truth).mean()
    bias = 100 * rel.mean()
    reading = (
        f"The two encodings of one identical scene differ by up to {worst} code levels, so an "
        f"eight bit array is a statement about a transfer function and not about the scene. "
        f"Halving the frame by averaging encoded values instead of radiance biases the result "
        f"by {bias:+.2f} per cent in linear light, and the bias is systematic rather than "
        f"random, which is why a mismatched preprocessing step shifts a trained model's inputs "
        f"in one direction. A mid grey threshold applied to encoded values disagrees with the "
        f"same threshold on radiance for {disagree:.1f} per cent of pixels. The claim under "
        f"test fails on all three counts."
    )

    return (
        [
            ("Two encodings of one scene, by brightness band", encoding_table),
            ("Halving the frame in the encoded domain against linear light", resize_table),
            ("A threshold means different things in different domains", threshold_table),
            ("Conversion cost", cost_table),
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
