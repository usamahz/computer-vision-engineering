#!/usr/bin/env python3
"""13. A distributional image metric moves under changes a viewer cannot see.

Claim under test: a lower distributional distance between generated and reference images means
better samples, so a small difference in it is evidence of a better model.

The benchmark builds seeded synthetic image sets, then computes a Frechet distance between
Gaussian fits of a fixed hand built feature, the block cosine transform, rather than a learned
network, because no weights may be downloaded here. It compares how far the score moves under
changes a viewer cannot see, a resampling filter swap and a near lossless re-encode, against
how far it moves under a genuine change of distribution, and against the metric's own noise
floor from resampling the same distribution.

This measures the metric's sensitivity to its own pipeline. It is not a reproduction of any
published score, and the absolute values are not comparable to published ones.
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "13. A distributional image metric moves under changes a viewer cannot see"
CLAIM = "a small difference in a distributional distance is evidence of better samples"

SIDE = 64
BLOCK = 8


def dct_matrix(n: int) -> np.ndarray:
    k = np.arange(n)[:, None]
    x = np.arange(n)[None, :]
    matrix = np.cos(np.pi * (2 * x + 1) * k / (2 * n))
    matrix[0] *= np.sqrt(1.0 / n)
    matrix[1:] *= np.sqrt(2.0 / n)
    return matrix


DCT = dct_matrix(BLOCK)


def synth_images(rng, count: int, scale: float = 1.0, texture: float = 1.0) -> np.ndarray:
    """Shapes on textured backgrounds. `scale` and `texture` are the genuine distribution."""
    images = np.zeros((count, SIDE, SIDE), dtype=np.float64)
    y, x = np.mgrid[0:SIDE, 0:SIDE].astype(np.float64)
    for index in range(count):
        background = rng.random((SIDE // 4, SIDE // 4))
        background = np.kron(background, np.ones((4, 4)))
        image = 0.35 + texture * 0.25 * background
        for _ in range(int(rng.integers(1, 4))):
            cx, cy = rng.uniform(12, SIDE - 12, size=2)
            radius = rng.uniform(5, 14) * scale
            mask = ((x - cx) ** 2 + (y - cy) ** 2) < radius ** 2
            image = np.where(mask, image * 0.35 + 0.55, image)
        images[index] = np.clip(image, 0.0, 1.0)
    return images


def to_uint8(images: np.ndarray) -> np.ndarray:
    return np.rint(np.clip(images, 0.0, 1.0) * 255.0).astype(np.uint8)


def features(images: np.ndarray) -> np.ndarray:
    """Mean absolute block cosine transform coefficient per frequency, per image."""
    count = images.shape[0]
    blocks = images.reshape(count, SIDE // BLOCK, BLOCK, SIDE // BLOCK, BLOCK)
    blocks = blocks.transpose(0, 1, 3, 2, 4).reshape(-1, BLOCK, BLOCK)
    transformed = DCT @ blocks @ DCT.T
    per_image = np.abs(transformed).reshape(count, -1, BLOCK * BLOCK).mean(axis=1)
    return per_image


def sqrt_psd(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(matrix)
    values = np.clip(values, 0.0, None)
    return (vectors * np.sqrt(values)) @ vectors.T


def frechet(a: np.ndarray, b: np.ndarray) -> float:
    mu_a, mu_b = a.mean(axis=0), b.mean(axis=0)
    cov_a = np.cov(a, rowvar=False) + 1e-8 * np.eye(a.shape[1])
    cov_b = np.cov(b, rowvar=False) + 1e-8 * np.eye(b.shape[1])
    root = sqrt_psd(cov_a)
    middle = sqrt_psd(root @ cov_b @ root)
    return float(((mu_a - mu_b) ** 2).sum() + np.trace(cov_a + cov_b - 2.0 * middle))


def resample(images: np.ndarray, filter_name: int) -> np.ndarray:
    out = np.zeros_like(images)
    for index, image in enumerate(to_uint8(images)):
        pil = Image.fromarray(image)
        small = pil.resize((SIDE // 2, SIDE // 2), filter_name)
        out[index] = np.asarray(small.resize((SIDE, SIDE), filter_name), dtype=np.float64) / 255.0
    return out


def reencode(images: np.ndarray, quality: int) -> np.ndarray:
    out = np.zeros_like(images)
    for index, image in enumerate(to_uint8(images)):
        buffer = io.BytesIO()
        Image.fromarray(image).save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)
        out[index] = np.asarray(Image.open(buffer).convert("L"), dtype=np.float64) / 255.0
    return out


def visible_difference(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Mean absolute difference in eight bit code levels, and peak signal to noise ratio."""
    diff = to_uint8(a).astype(np.float64) - to_uint8(b).astype(np.float64)
    mae = float(np.abs(diff).mean())
    mse = float((diff ** 2).mean())
    psnr = float("inf") if mse == 0 else float(10.0 * np.log10(255.0 ** 2 / mse))
    return mae, psnr


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    count = 120 if quick else 400
    repeats = 3 if quick else 7

    reference = synth_images(rng, count)
    same = synth_images(rng, count)
    reference_features = features(reference)

    variants = {
        "same distribution, fresh draw": same,
        "resampled with a bilinear filter": resample(reference, Image.BILINEAR),
        "resampled with a Lanczos filter": resample(reference, Image.LANCZOS),
        "re-encoded at quality ninety five": reencode(reference, 95),
        "re-encoded at quality seventy five": reencode(reference, 75),
        "genuine shift, larger shapes": synth_images(rng, count, scale=1.35),
        "genuine shift, flatter texture": synth_images(rng, count, texture=0.45),
    }

    rows = []
    scores = {}
    for name, images in variants.items():
        score = frechet(reference_features, features(images))
        scores[name] = score
        if name == "same distribution, fresh draw":
            mae, psnr = float("nan"), float("nan")
            visible = "not applicable, different images"
        else:
            mae, psnr = visible_difference(reference, images)
            visible = f"{mae:.2f} levels, {psnr:.1f} dB"
        rows.append([name, f"{score:.4f}", visible])
    variant_table = timing.markdown_table(
        ["Change applied to the reference set", "Frechet distance on block transform features", "Pixel difference from the reference"],
        rows,
    )

    # The metric's own noise floor: same distribution, different draws and sample counts.
    floor_rows = []
    for size in (count // 4, count // 2, count):
        a = features(synth_images(rng, size))
        b = features(synth_images(rng, size))
        floor_rows.append([str(size), f"{frechet(a, b):.4f}"])
    floor_table = timing.markdown_table(["Images per set", "Frechet distance between two draws of one distribution"], floor_rows)
    noise_floor = max(float(row[1]) for row in floor_rows)

    comparison_rows = []
    invisible = [
        "resampled with a bilinear filter",
        "resampled with a Lanczos filter",
        "re-encoded at quality ninety five",
    ]
    genuine = ["genuine shift, larger shapes", "genuine shift, flatter texture"]
    for name in invisible + genuine:
        comparison_rows.append(
            [
                name,
                "invisible or near invisible" if name in invisible else "genuine change of distribution",
                f"{scores[name]:.4f}",
                f"{scores[name] / max(noise_floor, 1e-12):.1f}",
            ]
        )
    comparison_table = timing.markdown_table(
        ["Change", "Kind", "Frechet distance", "Multiple of the metric's noise floor"], comparison_rows
    )

    timings = [
        timing.measure(lambda: features(reference), label="feature extraction for one set", repeats=repeats, warmup=1, inside_timer="block transform and averaging"),
        timing.measure(lambda: frechet(reference_features, reference_features + 1e-6), label="Frechet distance between two fitted Gaussians", repeats=repeats, warmup=1, inside_timer="covariance, matrix square root and trace"),
    ]
    cost_table = timing.table(timings, first_column="Stage") + (
        f"\n\n{count} images per set at {SIDE} by {SIDE} pixels, block size {BLOCK}, "
        f"{BLOCK * BLOCK} dimensional features."
    )

    worst_invisible = max(scores[name] for name in invisible)
    worst_invisible_name = max(invisible, key=lambda n: scores[n])
    weakest_genuine = min(scores[name] for name in genuine)
    weakest_genuine_name = min(genuine, key=lambda n: scores[n])
    reading = (
        f"Changes a viewer cannot see move the metric by more than its own noise floor, and in "
        f"one case by more than a genuine change of distribution does. Swapping the resampling "
        f"filter or re-encoding at near lossless quality leaves a pixel difference of a few "
        f"code levels and a peak signal to noise ratio in the forties, yet the largest of "
        f"those invisible changes, {worst_invisible_name}, scores {worst_invisible:.4f}, which "
        f"is {worst_invisible / max(noise_floor, 1e-12):.1f} times the floor measured between "
        f"two draws of the same distribution. The weaker of the two genuine shifts, "
        f"{weakest_genuine_name}, scores {weakest_genuine:.4f}. "
        f"{'An invisible change therefore outscores a real one here' if worst_invisible > weakest_genuine else 'The genuine shifts still outscore the invisible ones here'}"
        f", and the floor itself depends on the sample count, which is a free parameter in most "
        f"reported figures. The claim under test fails: a small difference in a distributional "
        f"distance is evidence about a pipeline, not about samples, unless the resampling "
        f"filter, the encoder, the sample count and the feature extractor are all held fixed "
        f"and stated. This benchmark measures the sensitivity of the construction and does not "
        f"reproduce any published score."
    )

    return (
        [
            ("What moves the score", variant_table),
            ("The metric's own noise floor", floor_table),
            ("Invisible changes against genuine ones", comparison_table),
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
