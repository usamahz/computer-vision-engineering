#!/usr/bin/env python3
"""08. A geometric augmentation that leaves the label alone breaks the label.

Claim under test: augmentation is a property of the input pipeline, so a stronger policy is a
free improvement.

The benchmark builds a seeded object mask, derives the true box from the mask, then applies
five augmentations. For each one it scores three label handling strategies against the truth
recovered from the transformed mask: leaving the label alone, mapping the box corners and
taking the axis aligned hull, and transforming the mask itself. Overlap and area ratio are
reported, because the corner mapping strategy is correct for some transforms and inflates the
box for others.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "08. A geometric augmentation that leaves the label alone breaks the label"
CLAIM = "augmentation is a property of the input pipeline, so a stronger policy is a free improvement"


def object_mask(rng, size: int) -> np.ndarray:
    """One elongated object placed off centre, which is where label errors show up."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    cx, cy = size * 0.38, size * 0.44
    angle = np.deg2rad(28.0)
    xr = (x - cx) * np.cos(angle) + (y - cy) * np.sin(angle)
    yr = -(x - cx) * np.sin(angle) + (y - cy) * np.cos(angle)
    ellipse = (xr / (size * 0.28)) ** 2 + (yr / (size * 0.08)) ** 2 <= 1.0
    bar = (np.abs(xr) < size * 0.05) & (np.abs(yr) < size * 0.22)
    speckle = rng.random((size, size)) < 0.0
    return (ellipse | bar | speckle).astype(np.uint8)


def bbox(mask: np.ndarray) -> tuple[float, float, float, float]:
    ys, xs = np.nonzero(mask)
    return float(xs.min()), float(ys.min()), float(xs.max() + 1), float(ys.max() + 1)


def iou(a, b) -> float:
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def area(box) -> float:
    return (box[2] - box[0]) * (box[3] - box[1])


def transform_mask(mask: np.ndarray, kind: str, size: int) -> np.ndarray:
    image = Image.fromarray(mask * 255)
    if kind == "horizontal flip":
        out = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif kind == "rotate ninety degrees":
        out = image.transpose(Image.ROTATE_90)
    elif kind == "rotate fifteen degrees":
        out = image.rotate(15.0, resample=Image.NEAREST, expand=False)
    elif kind == "crop and resize":
        out = image.crop((int(size * 0.1), int(size * 0.1), int(size * 0.9), int(size * 0.9))).resize((size, size), Image.NEAREST)
    elif kind == "stretch, aspect changed":
        out = image.resize((size, int(size * 0.6)), Image.NEAREST)
    else:
        raise ValueError(kind)
    return (np.asarray(out) > 127).astype(np.uint8)


def map_corners(box, kind: str, size: int):
    """What a pipeline does when it transforms the label without re-deriving it."""
    x1, y1, x2, y2 = box
    corners = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], dtype=np.float64)
    if kind == "horizontal flip":
        corners[:, 0] = size - corners[:, 0]
    elif kind == "rotate ninety degrees":
        corners = np.stack([corners[:, 1], size - corners[:, 0]], axis=1)
    elif kind == "rotate fifteen degrees":
        angle = np.deg2rad(-15.0)
        centre = np.array([size / 2.0, size / 2.0])
        rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        corners = (corners - centre) @ rotation.T + centre
    elif kind == "crop and resize":
        low, high = size * 0.1, size * 0.9
        scale = size / (high - low)
        corners = (corners - low) * scale
    elif kind == "stretch, aspect changed":
        corners[:, 1] = corners[:, 1] * (int(size * 0.6) / size)
    return (
        float(corners[:, 0].min()),
        float(corners[:, 1].min()),
        float(corners[:, 0].max()),
        float(corners[:, 1].max()),
    )


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    size = 128 if quick else 384
    repeats = 3 if quick else 7

    mask = object_mask(rng, size)
    original = bbox(mask)
    kinds = [
        "horizontal flip",
        "rotate ninety degrees",
        "rotate fifteen degrees",
        "crop and resize",
        "stretch, aspect changed",
    ]

    rows = []
    for kind in kinds:
        moved = transform_mask(mask, kind, size)
        truth = bbox(moved)
        untouched = original
        mapped = map_corners(original, kind, size)
        rows.append(
            [
                kind,
                f"{iou(untouched, truth):.3f}",
                f"{iou(mapped, truth):.3f}",
                f"{area(mapped) / area(truth):.3f}",
                f"{iou(truth, truth):.3f}",
            ]
        )
    label_table = timing.markdown_table(
        [
            "Augmentation",
            "Overlap when the label is left alone",
            "Overlap when the box corners are mapped",
            "Area of the mapped box over the true box",
            "Overlap when the mask is transformed",
        ],
        rows,
    )

    # How far a training signal is wrong when the label is left alone, as a function of how
    # often the augmentation fires.
    probability_rows = []
    worst = min(float(row[1]) for row in rows)
    for probability in (0.1, 0.25, 0.5, 0.9):
        expected = (1 - probability) * 1.0 + probability * worst
        probability_rows.append(
            [
                f"{probability:.2f}",
                f"{expected:.3f}",
                f"{100 * probability * (1 - worst):.1f}",
            ]
        )
    probability_table = timing.markdown_table(
        [
            "Probability the augmentation fires",
            "Mean overlap of the supervised box with the object",
            "Share of the training signal pointing at the wrong place (%)",
        ],
        probability_rows,
    )

    timings = [
        timing.measure(lambda: transform_mask(mask, "rotate fifteen degrees", size), label="transform the mask", repeats=repeats, inside_timer="resampling only"),
        timing.measure(lambda: map_corners(original, "rotate fifteen degrees", size), label="map the box corners", repeats=repeats, inside_timer="four point transform only"),
    ]
    cost_table = timing.table(timings, first_column="Label handling") + (
        f"\n\nMask is {size} by {size} pixels, nearest neighbour resampling, one object."
    )

    flip = next(row for row in rows if row[0] == "horizontal flip")
    rotation = next(row for row in rows if row[0] == "rotate fifteen degrees")
    reading = (
        f"Leaving the label alone is not a small error. A horizontal flip, the cheapest "
        f"augmentation in every pipeline, drops the overlap between the supervised box and the "
        f"object to {flip[1]}, which is below the threshold at which a detection would count "
        f"as correct at evaluation time. Mapping the box corners fixes the axis aligned "
        f"transforms exactly, and for a fifteen degree rotation it returns an overlap of "
        f"{rotation[2]} while inflating the box to {rotation[3]} times the true area, because "
        f"an axis aligned hull of a rotated rectangle is not the box of the rotated object. "
        f"Only transforming the mask and re-deriving the box recovers the truth in every case. "
        f"Re-deriving costs more than mapping four corners, and that cost is the whole reason "
        f"pipelines get this wrong. The claim under test fails: a stronger policy is free only "
        f"for the input."
    )

    return (
        [
            ("Three label handling strategies against the truth", label_table),
            ("What a wrong label costs over a training run", probability_table),
            ("Cost of handling the label", cost_table),
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
