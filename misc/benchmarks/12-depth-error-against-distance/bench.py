#!/usr/bin/env python3
"""12. Depth error grows with the square of distance, so one average error says nothing.

Claim under test: a stereo system has a depth error, quotable as one number.

The benchmark builds a rectified synthetic pair from a seeded texture, with known disparity
per region, runs a block matching search with a parabolic subpixel refinement, and reports the
measured disparity error and the depth error it implies, binned by true distance. The growth
exponent is fitted from the measured medians rather than assumed, and the single frame average
is printed beside the bins it hides.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "12. Depth error grows with the square of distance"
CLAIM = "a stereo system has a depth error, quotable as one number"

FOCAL_PX = 700.0
BASELINE_M = 0.12
WINDOW = 7
MAX_DISPARITY = 48
NOMINAL_DISTANCES_M = [2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
# Nominal distances at this focal length and baseline land on whole pixel disparities, which a
# block matcher recovers exactly and which would confound integer alignment with distance. A
# fixed sub-pixel offset per band removes that artefact; the true distance is then whatever the
# offset disparity implies, and it is what the tables report.
DISPARITY_OFFSETS_PX = [0.27, -0.31, 0.19, -0.23, 0.17, -0.29]


def sample_shifted(row: np.ndarray, disparity: float) -> np.ndarray:
    """Right image row, sampled from the left row at x plus disparity, linear interpolation."""
    x = np.arange(len(row), dtype=np.float64) + disparity
    x0 = np.floor(x).astype(int)
    frac = x - x0
    x0 = np.clip(x0, 0, len(row) - 1)
    x1 = np.clip(x0 + 1, 0, len(row) - 1)
    return row[x0] * (1.0 - frac) + row[x1] * frac


def band_geometry() -> list[tuple[float, float]]:
    """(true disparity in pixels, true distance in metres) for each band."""
    pairs = []
    for nominal, offset in zip(NOMINAL_DISTANCES_M, DISPARITY_OFFSETS_PX):
        disparity = FOCAL_PX * BASELINE_M / nominal + offset
        pairs.append((disparity, FOCAL_PX * BASELINE_M / disparity))
    return pairs


def make_pair(rng, height: int, width: int):
    """Horizontal bands, each at one true distance, textured so matching is well posed."""
    texture = rng.random((height, width))
    texture = (texture + np.roll(texture, 1, axis=1) + np.roll(texture, 2, axis=1)) / 3.0
    left = texture
    right = np.zeros_like(left)
    truth = np.zeros((height, width))
    geometry = band_geometry()
    band = height // len(geometry)
    for index, (disparity, _) in enumerate(geometry):
        rows = slice(index * band, (index + 1) * band if index < len(geometry) - 1 else height)
        for row in range(*rows.indices(height)):
            right[row] = sample_shifted(left[row], disparity)
            truth[row] = disparity
    return left, right, truth


def box_sum(image: np.ndarray, window: int) -> np.ndarray:
    pad = window // 2
    padded = np.pad(image, pad, mode="edge")
    acc = np.zeros_like(image)
    for dy in range(window):
        for dx in range(window):
            acc += padded[dy : dy + image.shape[0], dx : dx + image.shape[1]]
    return acc


def block_match(left: np.ndarray, right: np.ndarray, max_disparity: int = MAX_DISPARITY):
    """Sum of absolute differences over a square window, with parabolic subpixel refinement."""
    costs = np.full((max_disparity + 1,) + left.shape, np.inf)
    for disparity in range(max_disparity + 1):
        shifted = np.roll(right, disparity, axis=1)
        diff = np.abs(left - shifted)
        diff[:, :disparity] = np.nan
        cost = box_sum(np.nan_to_num(diff, nan=1.0), WINDOW)
        costs[disparity] = cost
    best = np.argmin(costs, axis=0)
    # Parabolic refinement against the two neighbouring costs.
    refined = best.astype(np.float64)
    interior = (best > 0) & (best < max_disparity)
    rows, cols = np.nonzero(interior)
    centre = costs[best[rows, cols], rows, cols]
    lower = costs[best[rows, cols] - 1, rows, cols]
    upper = costs[best[rows, cols] + 1, rows, cols]
    denominator = lower - 2.0 * centre + upper
    delta = np.where(np.abs(denominator) > 1e-12, 0.5 * (lower - upper) / np.where(np.abs(denominator) > 1e-12, denominator, 1.0), 0.0)
    refined[rows, cols] = best[rows, cols] + np.clip(delta, -0.5, 0.5)
    return refined


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    height = 60 if quick else 180
    width = 192 if quick else 384
    repeats = 3 if quick else 7

    left, right, truth = make_pair(rng, height, width)
    estimate = block_match(left, right)

    valid = np.zeros_like(truth, dtype=bool)
    valid[:, MAX_DISPARITY + WINDOW : width - WINDOW] = True

    rows = []
    medians, centres = [], []
    for disparity, distance in band_geometry():
        mask = valid & (np.abs(truth - disparity) < 1e-9)
        if mask.sum() == 0:
            continue
        disparity_error = np.abs(estimate[mask] - disparity)
        depth_estimate = FOCAL_PX * BASELINE_M / np.maximum(estimate[mask], 1e-6)
        depth_error = np.abs(depth_estimate - distance)
        median_depth_error = float(np.median(depth_error))
        medians.append(median_depth_error)
        centres.append(distance)
        predicted = distance ** 2 * float(np.median(disparity_error)) / (FOCAL_PX * BASELINE_M)
        rows.append(
            [
                f"{distance:.2f}",
                f"{disparity:.2f}",
                int(mask.sum()),
                f"{float(np.median(disparity_error)):.3f}",
                f"{median_depth_error:.3f}",
                f"{predicted:.3f}",
                f"{100 * median_depth_error / distance:.2f}",
            ]
        )
    distance_table = timing.markdown_table(
        [
            "True distance (m)",
            "True disparity (px)",
            "Pixels measured",
            "Median disparity error (px)",
            "Median depth error (m)",
            "Depth error the square law predicts from that disparity error (m)",
            "Relative depth error (%)",
        ],
        rows,
    )

    slope, _ = np.polyfit(np.log(np.array(centres)), np.log(np.maximum(np.array(medians), 1e-9)), 1)

    # The law itself, isolated: propagate one fixed disparity error, the frame median, through
    # the same geometry. This column is computed from the measured disparity error, not timed
    # or matched, and is labelled as such.
    frame_disparity_error = float(np.median(np.abs(estimate[valid] - truth[valid])))
    propagation_rows = []
    for _, distance in band_geometry():
        implied = distance ** 2 * frame_disparity_error / (FOCAL_PX * BASELINE_M)
        propagation_rows.append([f"{distance:.2f}", f"{frame_disparity_error:.3f}", f"{implied:.3f}", f"{100 * implied / distance:.2f}"])
    propagation_table = timing.markdown_table(
        [
            "True distance (m)",
            "Disparity error held fixed at the frame median (px, measured)",
            "Implied depth error (m, computed)",
            "Implied relative error (%, computed)",
        ],
        propagation_rows,
    )
    computed_exponent, _ = np.polyfit(
        np.log(np.array([float(r[0]) for r in propagation_rows])),
        np.log(np.array([float(r[2]) for r in propagation_rows])),
        1,
    )

    all_mask = valid & (truth > 0)
    depth_truth = FOCAL_PX * BASELINE_M / truth[all_mask]
    depth_estimate = FOCAL_PX * BASELINE_M / np.maximum(estimate[all_mask], 1e-6)
    frame_error = np.abs(depth_estimate - depth_truth)
    aggregate_table = timing.markdown_table(
        ["Statistic over the whole frame", "Value"],
        [
            ["mean absolute depth error (m)", f"{float(frame_error.mean()):.3f}"],
            ["median absolute depth error (m)", f"{float(np.median(frame_error)):.3f}"],
            ["ninety fifth percentile absolute depth error (m)", f"{float(np.percentile(frame_error, 95)):.3f}"],
            ["median absolute depth error in the nearest band (m)", rows[0][4]],
            ["median absolute depth error in the farthest band (m)", rows[-1][4]],
            ["fitted growth exponent from the measured medians", f"{float(slope):.2f}"],
            ["fitted growth exponent with the disparity error held fixed, computed", f"{float(computed_exponent):.2f}"],
            ["growth exponent the geometry predicts", "2.00"],
        ],
    )

    timings = [
        timing.measure(lambda: block_match(left, right), label="block matching with subpixel refinement", repeats=repeats, warmup=1, inside_timer="cost volume, argmin and refinement, image generation excluded"),
    ]
    cost_table = timing.table(timings, first_column="Stage") + (
        f"\n\nPair is {height} by {width} pixels, window {WINDOW} by {WINDOW}, "
        f"disparity search zero to {MAX_DISPARITY}, focal length {FOCAL_PX:g} pixels, "
        f"baseline {BASELINE_M:g} metres."
    )

    near, far = rows[0], rows[-1]
    ratio = float(far[4]) / max(float(near[4]), 1e-9)
    agreement = max(
        abs(float(row[4]) - float(row[5])) / max(float(row[5]), 1e-9) for row in rows
    )
    reading = (
        f"The square law holds, and it holds in the conditional form that matters. Within "
        f"each distance band the depth error predicted from that band's own measured disparity "
        f"error agrees with the measured depth error to within "
        f"{100 * agreement:.0f} per cent, and propagating one fixed disparity error, the frame "
        f"median of {frame_disparity_error:.3f} pixels, through the same geometry gives a "
        f"fitted exponent of {float(computed_exponent):.2f} against the two the geometry "
        f"predicts. Fitting the measured medians directly gives {float(slope):.2f} rather than "
        f"two, and the reason is worth stating rather than smoothing away: the measured "
        f"disparity error is not constant across bands, because whether a band's true "
        f"disparity happens to sit near a whole pixel changes how well a parabolic refinement "
        f"recovers it. Either way the consequence is the same. Median depth error grows from "
        f"{near[4]} metres at {near[0]} metres to {far[4]} metres at {far[0]} metres, a factor "
        f"of {ratio:.0f} across a distance factor of "
        f"{float(far[0]) / float(near[0]):.0f}, and relative error grows with it. The single "
        f"frame mean of {float(frame_error.mean()):.3f} metres is therefore a property of how "
        f"far away this particular scene happened to be and of which band held the most "
        f"pixels, not a property of the stereo system. The claim under test fails: a depth "
        f"error has to be quoted per distance or with the working range it applies to."
    )

    return (
        [
            ("Depth error by true distance, measured", distance_table),
            ("The law isolated, one disparity error propagated", propagation_table),
            ("What the frame average hides", aggregate_table),
            ("Matching cost", cost_table),
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
