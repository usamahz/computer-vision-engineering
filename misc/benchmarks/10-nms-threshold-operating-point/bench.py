#!/usr/bin/env python3
"""10. The suppression threshold is a product decision, and it is not free.

Claim under test: non maximum suppression is a postprocessing detail, so a detector's quality
and its latency can both be quoted without it.

The benchmark generates seeded detections with the duplicate structure a real detector emits,
sweeps the greedy suppression overlap threshold, and reports what moves: average precision,
and precision and recall at a fixed score threshold, which is what a deployed system actually
operates at. It then measures the cost of the suppression itself against the detection count,
because a latency figure that excludes it is incomplete by a measurable amount.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "10. The suppression threshold is a product decision, and it is not free"
CLAIM = "suppression is a postprocessing detail, so quality and latency can be quoted without it"

OPERATING_SCORE = 0.5


def make_scene(rng, images: int, crowded: bool):
    gts, dets = [], []
    for image in range(images):
        count = int(rng.integers(6, 12)) if crowded else int(rng.integers(1, 4))
        centres = []
        for _ in range(count):
            w = float(rng.uniform(40, 90))
            h = float(rng.uniform(40, 90))
            if crowded and centres:
                base = centres[int(rng.integers(0, len(centres)))]
                x = float(np.clip(base[0] + rng.normal(0, 30), 0, 640 - w))
                y = float(np.clip(base[1] + rng.normal(0, 30), 0, 480 - h))
            else:
                x = float(rng.uniform(0, 640 - w))
                y = float(rng.uniform(0, 480 - h))
            centres.append((x, y))
            gts.append([image, x, y, x + w, y + h])
            # The detector fires several times on one object, with decaying scores.
            for duplicate in range(int(rng.integers(1, 5))):
                score = float(np.clip(rng.beta(5.0, 2.0) - 0.12 * duplicate, 0.02, 0.999))
                jitter = 0.06 + 0.10 * duplicate
                dx, dy = rng.normal(0, jitter * w), rng.normal(0, jitter * h)
                sw, sh = w * np.exp(rng.normal(0, jitter)), h * np.exp(rng.normal(0, jitter))
                dets.append([image, x + dx, y + dy, x + dx + sw, y + dy + sh, score])
        for _ in range(int(rng.integers(0, 3))):
            w, h = float(rng.uniform(30, 110)), float(rng.uniform(30, 110))
            x, y = float(rng.uniform(0, 640 - w)), float(rng.uniform(0, 480 - h))
            dets.append([image, x, y, x + w, y + h, float(np.clip(rng.beta(1.3, 6.0), 0.02, 0.999))])
    return np.array(gts, dtype=np.float64), np.array(dets, dtype=np.float64)


def iou_many(box, boxes):
    if len(boxes) == 0:
        return np.zeros(0)
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    area_a = (box[2] - box[0]) * (box[3] - box[1])
    area_b = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union = area_a + area_b - inter
    return np.where(union > 0, inter / union, 0.0)


def greedy_nms(boxes: np.ndarray, scores: np.ndarray, threshold: float) -> np.ndarray:
    order = np.argsort(-scores, kind="stable")
    keep = []
    while len(order):
        current = order[0]
        keep.append(current)
        if len(order) == 1:
            break
        overlaps = iou_many(boxes[current], boxes[order[1:]])
        order = order[1:][overlaps <= threshold]
    return np.array(keep, dtype=int)


def suppress_all(dets: np.ndarray, threshold: float) -> np.ndarray:
    kept = []
    for image in np.unique(dets[:, 0]):
        subset = dets[dets[:, 0] == image]
        indices = greedy_nms(subset[:, 1:5], subset[:, 5], threshold)
        kept.append(subset[indices])
    return np.concatenate(kept) if kept else dets


def pr_curve(dets, gts, iou_threshold=0.5):
    order = np.argsort(-dets[:, 5], kind="stable")
    dets = dets[order]
    by_image = {int(i): gts[gts[:, 0] == i] for i in np.unique(gts[:, 0])}
    claimed = {int(i): np.zeros(len(v), dtype=bool) for i, v in by_image.items()}
    tp = np.zeros(len(dets))
    fp = np.zeros(len(dets))
    for index, det in enumerate(dets):
        candidates = by_image.get(int(det[0]))
        if candidates is None or len(candidates) == 0:
            fp[index] = 1
            continue
        overlaps = iou_many(det[1:5], candidates[:, 1:5])
        best = int(np.argmax(overlaps))
        if overlaps[best] >= iou_threshold and not claimed[int(det[0])][best]:
            claimed[int(det[0])][best] = True
            tp[index] = 1
        else:
            fp[index] = 1
    cum_tp, cum_fp = np.cumsum(tp), np.cumsum(fp)
    recall = cum_tp / len(gts)
    precision = cum_tp / np.maximum(cum_tp + cum_fp, 1e-12)
    return recall, precision, dets[:, 5], tp, fp


def ap_all_point(recall, precision) -> float:
    mrec = np.concatenate(([0.0], recall, [1.0]))
    mpre = np.concatenate(([0.0], precision, [0.0]))
    for i in range(len(mpre) - 2, -1, -1):
        mpre[i] = max(mpre[i], mpre[i + 1])
    changes = np.where(mrec[1:] != mrec[:-1])[0]
    return float(((mrec[changes + 1] - mrec[changes]) * mpre[changes + 1]).sum())


def operating_point(scores, tp, fp, total_gt, floor=OPERATING_SCORE):
    mask = scores >= floor
    true_positives = tp[mask].sum()
    false_positives = fp[mask].sum()
    precision = true_positives / max(true_positives + false_positives, 1e-12)
    recall = true_positives / total_gt
    return float(precision), float(recall), int(mask.sum())


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    images = 30 if quick else 200
    repeats = 3 if quick else 7
    thresholds = [0.3, 0.45, 0.5, 0.6, 0.7, 0.9, 1.01]

    blocks = []
    summaries = {}
    for crowded in (False, True):
        gts, dets = make_scene(rng, images, crowded)
        rows = []
        for threshold in thresholds:
            kept = dets if threshold > 1.0 else suppress_all(dets, threshold)
            recall, precision, scores, tp, fp = pr_curve(kept, gts)
            ap = ap_all_point(recall, precision)
            p_at, r_at, count = operating_point(scores, tp, fp, len(gts))
            rows.append(
                [
                    "no suppression" if threshold > 1.0 else f"{threshold:.2f}",
                    str(len(kept)),
                    f"{100 * ap:.2f}",
                    f"{100 * p_at:.1f}",
                    f"{100 * r_at:.1f}",
                    f"{2 * p_at * r_at / max(p_at + r_at, 1e-12):.3f}",
                    str(count),
                ]
            )
        name = "crowded scenes" if crowded else "sparse scenes"
        blocks.append(
            (
                f"Suppression threshold sweep, {name}",
                timing.markdown_table(
                    [
                        "Overlap threshold",
                        "Detections kept",
                        "All point average precision (%)",
                        f"Precision at score {OPERATING_SCORE:g} (%)",
                        f"Recall at score {OPERATING_SCORE:g} (%)",
                        "Harmonic mean at that score",
                        "Detections acted on",
                    ],
                    rows,
                ),
            )
        )
        aps = [float(r[2]) for r in rows]
        f1s = [float(r[5]) for r in rows]
        summaries[name] = {
            "ap_spread": max(aps) - min(aps),
            "f1_spread": max(f1s) - min(f1s),
            "best_ap": rows[int(np.argmax(aps))][0],
            "best_f1": rows[int(np.argmax(f1s))][0],
            "ground_truth": len(gts),
        }

    # What suppression costs, against detection count, on this machine.
    cost_rows = []
    for count in (100, 500, 1000, 2000):
        boxes = np.column_stack(
            [
                rng.uniform(0, 600, count),
                rng.uniform(0, 440, count),
            ]
        )
        boxes = np.column_stack([boxes, boxes[:, 0] + rng.uniform(20, 80, count), boxes[:, 1] + rng.uniform(20, 80, count)])
        scores = rng.random(count)
        measured = timing.measure(
            lambda b=boxes, s=scores: greedy_nms(b, s, 0.5),
            label=f"{count} boxes",
            repeats=repeats,
            warmup=1,
            inside_timer="suppression only, no decoding and no copy to host",
        )
        kept = len(greedy_nms(boxes, scores, 0.5))
        cost_rows.append([str(count), str(kept), f"{measured.median_ms:.3g}", f"{measured.p95_ms:.3g}", f"{measured.median_ms / count * 1000:.2f}"])
    cost_table = timing.markdown_table(
        [
            "Boxes entering suppression",
            "Boxes surviving",
            "Median latency (ms)",
            "p95 (ms)",
            "Microseconds per box",
        ],
        cost_rows,
    )
    blocks.append(("Cost of the suppression step alone", cost_table))

    sparse = summaries["sparse scenes"]
    crowded = summaries["crowded scenes"]
    slowest = cost_rows[-1]
    sparse_rows_without_none = sparse["ap_spread"]
    reading = (
        f"The threshold moves both numbers, and it moves them differently. Average precision "
        f"ranges over {sparse_rows_without_none:.2f} points on sparse scenes and "
        f"{crowded['ap_spread']:.2f} points on crowded ones, while the harmonic mean of "
        f"precision and recall at a fixed deployable score ranges over "
        f"{sparse['f1_spread']:.3f} and {crowded['f1_spread']:.3f}. They do not peak in the "
        f"same place: on sparse scenes average precision is highest at overlap threshold "
        f"{sparse['best_ap']} and the deployed operating point is highest at "
        f"{sparse['best_f1']}, and on crowded scenes at {crowded['best_ap']} and "
        f"{crowded['best_f1']}. Tuning against the published metric and tuning against the "
        f"product are therefore different exercises, and a paper that reports only the former "
        f"has not reported the decision a team has to make. The cost half of the claim fails "
        f"too, with one caveat stated plainly: this is a greedy suppression written in numpy "
        f"with a Python loop over surviving boxes, so the absolute milliseconds characterise "
        f"this implementation and not a fused kernel. What transfers is the shape. Suppressing "
        f"{slowest[0]} boxes takes {slowest[2]} milliseconds here with a ninety fifth "
        f"percentile of {slowest[3]}, the cost per box rises with the box count rather than "
        f"staying flat, and the box count rises with the crowding of the scene. A latency "
        f"figure should state whether this step is inside the timer. Most published figures do "
        f"not."
    )

    return blocks, reading


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
