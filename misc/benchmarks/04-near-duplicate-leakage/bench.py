#!/usr/bin/env python3
"""04. Near duplicate leakage inflates a score with no change to the model.

Claim under test: a random split is a fair split, so a held out score measures generalisation.

The benchmark builds a seeded dataset whose images come in groups, the way real data does:
several frames of one scene, several crops of one photograph, several captures of one product.
The same classifier is then scored under a random split, which lets frames of one scene sit on
both sides, and under a group split, which does not. Nothing about the model changes between
the two numbers.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "04. Near duplicate leakage inflates a score with no change to the model"
CLAIM = "a random split is a fair split, so a held out score measures generalisation"

CLASSES = 8
DIM = 48


def dataset(rng, scenes_per_class: int, frames_per_scene: int, jitter: float):
    """Features with group structure: class prototype, scene offset, then frame jitter."""
    prototypes = rng.normal(0.0, 0.55, size=(CLASSES, DIM))
    features, labels, groups = [], [], []
    group_id = 0
    for label in range(CLASSES):
        for _ in range(scenes_per_class):
            scene_offset = rng.normal(0.0, 1.6, size=DIM)
            centre = prototypes[label] + scene_offset
            for _ in range(frames_per_scene):
                features.append(centre + rng.normal(0.0, jitter, size=DIM))
                labels.append(label)
                groups.append(group_id)
            group_id += 1
    return np.array(features), np.array(labels), np.array(groups)


def nearest_neighbour(train_x, train_y, test_x) -> np.ndarray:
    """One nearest neighbour under Euclidean distance, computed without forming a loop."""
    train_sq = (train_x ** 2).sum(axis=1)[None, :]
    test_sq = (test_x ** 2).sum(axis=1)[:, None]
    distances = test_sq + train_sq - 2.0 * test_x @ train_x.T
    return train_y[np.argmin(distances, axis=1)]


def nearest_group(train_x, train_groups, test_x) -> np.ndarray:
    train_sq = (train_x ** 2).sum(axis=1)[None, :]
    test_sq = (test_x ** 2).sum(axis=1)[:, None]
    distances = test_sq + train_sq - 2.0 * test_x @ train_x.T
    return train_groups[np.argmin(distances, axis=1)]


def random_split(rng, n: int, fraction: float):
    order = rng.permutation(n)
    cut = int(n * fraction)
    return order[:cut], order[cut:]


def group_split(rng, groups: np.ndarray, fraction: float):
    unique = np.unique(groups)
    order = rng.permutation(unique)
    cut = int(len(unique) * fraction)
    train_groups = set(order[:cut].tolist())
    mask = np.array([g in train_groups for g in groups])
    return np.where(mask)[0], np.where(~mask)[0]


def evaluate(features, labels, groups, train_idx, test_idx):
    predicted = nearest_neighbour(features[train_idx], labels[train_idx], features[test_idx])
    accuracy = float((predicted == labels[test_idx]).mean())
    neighbour_group = nearest_group(features[train_idx], groups[train_idx], features[test_idx])
    same_group = float((neighbour_group == groups[test_idx]).mean())
    return accuracy, same_group


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    scenes_per_class = 12 if quick else 40
    frames_per_scene = 4
    repeats = 3 if quick else 7

    rows = []
    for jitter in (0.05, 0.15, 0.35, 0.8):
        features, labels, groups = dataset(rng, scenes_per_class, frames_per_scene, jitter)
        r_train, r_test = random_split(rng, len(labels), 0.6)
        g_train, g_test = group_split(rng, groups, 0.6)
        random_acc, random_leak = evaluate(features, labels, groups, r_train, r_test)
        group_acc, group_leak = evaluate(features, labels, groups, g_train, g_test)
        rows.append(
            [
                f"{jitter:.2f}",
                f"{100 * random_acc:.1f}",
                f"{100 * group_acc:.1f}",
                f"{100 * (random_acc - group_acc):+.1f}",
                f"{100 * random_leak:.1f}",
                f"{100 * group_leak:.1f}",
            ]
        )
    split_table = timing.markdown_table(
        [
            "Frame jitter (feature units)",
            "Random split accuracy (%)",
            "Group split accuracy (%)",
            "Inflation (percentage points)",
            "Test items whose nearest train neighbour shares their group, random split (%)",
            "Same, group split (%)",
        ],
        rows,
    )

    # A cheap audit any team can run before trusting a split.
    features, labels, groups = dataset(rng, scenes_per_class, frames_per_scene, 0.15)
    r_train, r_test = random_split(rng, len(labels), 0.6)
    train_x, test_x = features[r_train], features[r_test]
    train_sq = (train_x ** 2).sum(axis=1)[None, :]
    test_sq = (test_x ** 2).sum(axis=1)[:, None]
    distances = np.sqrt(np.maximum(test_sq + train_sq - 2.0 * test_x @ train_x.T, 0.0))
    nearest = distances.min(axis=1)
    neighbour_group = groups[r_train][np.argmin(distances, axis=1)]
    truly_duplicate = neighbour_group == groups[r_test]
    audit_rows = []
    for threshold in (0.5, 1.0, 1.5, 2.0):
        flagged = nearest < threshold
        if flagged.sum() == 0:
            audit_rows.append([f"{threshold:.1f}", "0", "0.0", "0.0"])
            continue
        precision = float(truly_duplicate[flagged].mean())
        recall = float(flagged[truly_duplicate].mean())
        audit_rows.append([f"{threshold:.1f}", str(int(flagged.sum())), f"{100 * precision:.1f}", f"{100 * recall:.1f}"])
    audit_table = timing.markdown_table(
        [
            "Distance threshold",
            "Test items flagged as leaked",
            "Flagged items that really share a group (%)",
            "Leaked items caught (%)",
        ],
        audit_rows,
    )

    timings = [
        timing.measure(
            lambda: nearest_neighbour(features[r_train], labels[r_train], features[r_test]),
            label="score the held out split",
            repeats=repeats,
            inside_timer="distance matrix and argmin",
        ),
        timing.measure(
            lambda: np.sqrt(np.maximum(test_sq + train_sq - 2.0 * test_x @ train_x.T, 0.0)).min(axis=1),
            label="leakage audit over the same pair",
            repeats=repeats,
            inside_timer="distance matrix and minimum",
        ),
    ]
    cost_table = timing.table(timings, first_column="Operation") + (
        f"\n\nDataset holds {len(labels)} items in {len(np.unique(groups))} groups across "
        f"{CLASSES} classes, {DIM} dimensional features."
    )

    worst = max(float(row[3]) for row in rows)
    tightest = rows[0]
    reading = (
        f"The same classifier, the same features and the same amount of training data give two "
        f"different held out numbers, and the gap is as large as {worst:.1f} percentage points. "
        f"At the tightest duplication tested, the random split reports "
        f"{tightest[1]} per cent where the group split reports {tightest[2]} per cent, because "
        f"{tightest[4]} per cent of test items find a training neighbour from their own group. "
        f"The inflation shrinks as the duplicates get less similar, which is the honest "
        f"caveat: leakage is a property of the data, not a constant. The audit costs the same "
        f"order of work as scoring the split itself, so there is no efficiency argument for "
        f"skipping it. The claim under test fails."
    )

    return (
        [
            ("Random split against group split, as duplication loosens", split_table),
            ("A leakage audit a reviewer can demand", audit_table),
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
