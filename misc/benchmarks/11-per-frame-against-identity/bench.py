#!/usr/bin/env python3
"""11. Per frame accuracy can rise while tracking quality falls.

Claim under test: a tracker with better per frame detection is a better tracker.

The benchmark simulates ground truth trajectories that cross, then two trackers over the same
frames: one that detects more objects per frame but re-identifies them inconsistently at
crossings, and one that detects fewer and keeps identities. The same association is then
scored with per frame precision and recall, which ignore identity, and with identity aware
measures, which do not. One knob sweeps detection quality upward and identity quality
downward, so the divergence can be read as a trend rather than a single pair of numbers.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "11. Per frame accuracy can rise while tracking quality falls"
CLAIM = "a tracker with better per frame detection is a better tracker"

OBJECTS = 6
IOU_MATCH = 0.5


def trajectories(rng, frames: int):
    """Objects that cross each other, which is where identity is actually tested."""
    starts = rng.uniform(0, 600, size=OBJECTS)
    speeds = rng.uniform(-4.0, 4.0, size=OBJECTS)
    rows = []
    for frame in range(frames):
        for obj in range(OBJECTS):
            x = float((starts[obj] + speeds[obj] * frame) % 600)
            y = float(200 + 60 * np.sin(0.05 * frame + obj))
            rows.append([frame, obj, x, y, 48.0, 48.0])
    return np.array(rows, dtype=np.float64)


def simulate_tracker(rng, gt: np.ndarray, detect_rate: float, switch_rate: float, frames: int):
    """Detections carrying a track identity, with a configurable identity failure rate."""
    assigned = {obj: obj for obj in range(OBJECTS)}
    next_id = OBJECTS
    rows = []
    for frame in range(frames):
        present = gt[gt[:, 0] == frame]
        for row in present:
            obj = int(row[1])
            if rng.random() > detect_rate:
                continue
            if rng.random() < switch_rate:
                assigned[obj] = next_id
                next_id += 1
            jitter = rng.normal(0.0, 2.0, size=2)
            rows.append([frame, assigned[obj], row[2] + jitter[0], row[3] + jitter[1], row[4], row[5]])
    return np.array(rows, dtype=np.float64)


def iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = a[0] - a[2] / 2, a[1] - a[3] / 2, a[0] + a[2] / 2, a[1] + a[3] / 2
    bx1, by1, bx2, by2 = b[0] - b[2] / 2, b[1] - b[3] / 2, b[0] + b[2] / 2, b[1] + b[3] / 2
    inter = max(0.0, min(ax2, bx2) - max(ax1, bx1)) * max(0.0, min(ay2, by2) - max(ay1, by1))
    union = a[2] * a[3] + b[2] * b[3] - inter
    return inter / union if union > 0 else 0.0


def score(gt: np.ndarray, tracks: np.ndarray, frames: int) -> dict[str, float]:
    """Per frame counts, identity switches, and a greedy identity assignment.

    The identity assignment here is greedy rather than the optimal one the standard metric
    uses, which can only understate the identity score. It is named as an approximation in the
    README rather than passed off as the published measure.
    """
    true_positives = false_positives = false_negatives = switches = 0
    pairs: dict[tuple[int, int], int] = {}
    last_match: dict[int, int] = {}
    for frame in range(frames):
        g = gt[gt[:, 0] == frame]
        t = tracks[tracks[:, 0] == frame] if len(tracks) else np.zeros((0, 6))
        used = set()
        matched_this_frame: dict[int, int] = {}
        for row in g:
            obj = int(row[1])
            best, best_overlap = -1, 0.0
            for index, candidate in enumerate(t):
                if index in used:
                    continue
                overlap = iou(row[2:6], candidate[2:6])
                if overlap > best_overlap:
                    best, best_overlap = index, overlap
            if best >= 0 and best_overlap >= IOU_MATCH:
                used.add(best)
                true_positives += 1
                track_id = int(t[best][1])
                matched_this_frame[obj] = track_id
                pairs[(obj, track_id)] = pairs.get((obj, track_id), 0) + 1
                if obj in last_match and last_match[obj] != track_id:
                    switches += 1
            else:
                false_negatives += 1
        false_positives += len(t) - len(used)
        last_match.update(matched_this_frame)

    precision = true_positives / max(true_positives + false_positives, 1e-12)
    recall = true_positives / max(true_positives + false_negatives, 1e-12)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    total_gt = true_positives + false_negatives
    mota = 1.0 - (false_negatives + false_positives + switches) / max(total_gt, 1e-12)

    identity_true = 0
    claimed_gt: set[int] = set()
    claimed_track: set[int] = set()
    for (obj, track_id), count in sorted(pairs.items(), key=lambda kv: -kv[1]):
        if obj in claimed_gt or track_id in claimed_track:
            continue
        claimed_gt.add(obj)
        claimed_track.add(track_id)
        identity_true += count
    detections = true_positives + false_positives
    idf1 = 2 * identity_true / max(2 * identity_true + (total_gt - identity_true) + (detections - identity_true), 1e-12)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "switches": float(switches),
        "mota": mota,
        "idf1": idf1,
        "unique_ids": float(len(set(tracks[:, 1].astype(int).tolist())) if len(tracks) else 0),
    }


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    frames = 60 if quick else 240
    repeats = 3 if quick else 7
    gt = trajectories(rng, frames)

    rows = []
    sweep = [(0.80, 0.00), (0.86, 0.02), (0.92, 0.06), (0.96, 0.12), (0.99, 0.20)]
    scored = []
    for detect_rate, switch_rate in sweep:
        tracks = simulate_tracker(rng, gt, detect_rate, switch_rate, frames)
        result = score(gt, tracks, frames)
        scored.append(result)
        rows.append(
            [
                f"{100 * detect_rate:.0f}",
                f"{100 * switch_rate:.0f}",
                f"{100 * result['precision']:.1f}",
                f"{100 * result['recall']:.1f}",
                f"{result['f1']:.3f}",
                str(int(result["switches"])),
                str(int(result["unique_ids"])),
                f"{result['mota']:.3f}",
                f"{result['idf1']:.3f}",
            ]
        )
    sweep_table = timing.markdown_table(
        [
            "Detection rate (%)",
            "Identity failure rate per frame (%)",
            "Per frame precision (%)",
            "Per frame recall (%)",
            "Per frame harmonic mean",
            "Identity switches",
            "Distinct identities emitted",
            "Multiple object tracking accuracy",
            "Identity harmonic mean, greedy assignment",
        ],
        rows,
    )

    pair_table = timing.markdown_table(
        ["Tracker", "Per frame harmonic mean", "Identity harmonic mean", "Identity switches", "Preferred by per frame", "Preferred by identity"],
        [
            [
                "detects more, re-identifies poorly",
                f"{scored[-1]['f1']:.3f}",
                f"{scored[-1]['idf1']:.3f}",
                str(int(scored[-1]["switches"])),
                "yes" if scored[-1]["f1"] > scored[0]["f1"] else "no",
                "yes" if scored[-1]["idf1"] > scored[0]["idf1"] else "no",
            ],
            [
                "detects less, keeps identity",
                f"{scored[0]['f1']:.3f}",
                f"{scored[0]['idf1']:.3f}",
                str(int(scored[0]["switches"])),
                "yes" if scored[0]["f1"] > scored[-1]["f1"] else "no",
                "yes" if scored[0]["idf1"] > scored[-1]["idf1"] else "no",
            ],
        ],
    )

    tracks = simulate_tracker(rng, gt, 0.92, 0.06, frames)
    timings = [
        timing.measure(lambda: score(gt, tracks, frames), label="score one sequence", repeats=repeats, warmup=1, inside_timer="matching and both metric families"),
    ]
    cost_table = timing.table(timings, first_column="Operation") + (
        f"\n\nSequence holds {frames} frames and {OBJECTS} objects, "
        f"{len(gt)} ground truth boxes, overlap threshold {IOU_MATCH:g}."
    )

    f1_rising = scored[-1]["f1"] > scored[0]["f1"]
    idf1_falling = scored[-1]["idf1"] < scored[0]["idf1"]
    reading = (
        f"Across the sweep the per frame harmonic mean rises from {scored[0]['f1']:.3f} to "
        f"{scored[-1]['f1']:.3f} while the identity harmonic mean "
        f"{'falls' if idf1_falling else 'moves'} from {scored[0]['idf1']:.3f} to "
        f"{scored[-1]['idf1']:.3f}, and the number of distinct identities emitted grows from "
        f"{int(scored[0]['unique_ids'])} to {int(scored[-1]['unique_ids'])} for "
        f"{OBJECTS} real objects. The two families of measure therefore "
        f"{'disagree' if (f1_rising and idf1_falling) else 'agree'} about which tracker is "
        f"better. Multiple object tracking accuracy sits between them, because it charges for "
        f"switches but is dominated by the detection terms, which is exactly why it can look "
        f"healthy while a product that needs a stable identity is unusable. A per frame "
        f"metric cannot stand in for tracking quality: it is blind to the only question a "
        f"tracker exists to answer, which is whether this object is the same object as before."
    )

    return (
        [
            ("Detection quality up, identity quality down", sweep_table),
            ("The two ends of the sweep read as two trackers", pair_table),
            ("Scoring cost", cost_table),
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
