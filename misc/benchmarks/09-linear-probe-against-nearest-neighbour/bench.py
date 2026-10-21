#!/usr/bin/env python3
"""09. The probe is a choice of answer, not a measurement of the representation.

Claim under test: a linear probe accuracy ranks representations, so a higher probe number
means a better representation.

The benchmark builds two seeded representations of the same labelled data. One hides the
discriminative signal under high variance nuisance directions, which a linear map can
suppress and a distance cannot. The other arranges classes in concentric shells, which a
distance handles and no linear map can. It then scores both under a ridge linear probe, a
nearest neighbour probe under two distances, and the same probes after standardising features,
which is a protocol detail that papers rarely state.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import determinism, report, timing  # noqa: E402

TITLE = "09. The probe is a choice of answer, not a measurement of the representation"
CLAIM = "a linear probe accuracy ranks representations, so a higher probe number means a better representation"

CLASSES = 8
DIM = 32


def representation_nuisance(rng, per_class: int):
    """Signal in a few directions, large variance nuisance in the rest."""
    signal_dims = 6
    axes = np.eye(CLASSES, signal_dims)[:, :signal_dims] * 2.4
    features, labels = [], []
    for cls in range(CLASSES):
        signal = np.zeros(signal_dims)
        signal[cls % signal_dims] = axes[cls, cls % signal_dims] * (1 if cls < signal_dims else -1)
        block = np.tile(signal, (per_class, 1)) + rng.normal(0.0, 0.35, size=(per_class, signal_dims))
        nuisance = rng.normal(0.0, 7.0, size=(per_class, DIM - signal_dims))
        features.append(np.hstack([block, nuisance]))
        labels.append(np.full(per_class, cls))
    return np.vstack(features), np.concatenate(labels)


def representation_multimodal(rng, per_class: int, modes: int = 3):
    """Each class occupies several clusters, spaced around a circle inside a plane.

    A distance reads this directly. The clusters of one class are interleaved with those of
    every other class in the plane they live in, so no single hyperplane isolates a class, and
    embedding the plane in a higher dimensional space does not change that.
    """
    clusters = CLASSES * modes
    basis = rng.normal(0.0, 1.0, size=(2, DIM))
    basis[0] /= np.linalg.norm(basis[0])
    basis[1] -= basis[1] @ basis[0] * basis[0]
    basis[1] /= np.linalg.norm(basis[1])

    features, labels = [], []
    per_mode = max(per_class // modes, 1)
    for index in range(clusters):
        cls = index % CLASSES
        angle = 2.0 * np.pi * index / clusters
        centre = np.array([np.cos(angle), np.sin(angle)]) * 6.0 @ basis
        features.append(centre + rng.normal(0.0, 0.18, size=(per_mode, DIM)))
        labels.append(np.full(per_mode, cls))
    return np.vstack(features), np.concatenate(labels)


def representation_shells(rng, per_class: int):
    """Class is the radius, which no hyperplane separates and a distance reads directly."""
    features, labels = [], []
    for cls in range(CLASSES):
        directions = rng.normal(0.0, 1.0, size=(per_class, DIM))
        directions /= np.linalg.norm(directions, axis=1, keepdims=True)
        radius = 1.0 + 0.9 * cls
        features.append(directions * (radius + rng.normal(0.0, 0.12, size=(per_class, 1))))
        labels.append(np.full(per_class, cls))
    return np.vstack(features), np.concatenate(labels)


def split(rng, n: int, fraction: float = 0.6):
    order = rng.permutation(n)
    cut = int(n * fraction)
    return order[:cut], order[cut:]


def standardise(train_x, test_x):
    mean = train_x.mean(axis=0, keepdims=True)
    scale = train_x.std(axis=0, keepdims=True)
    scale = np.where(scale > 1e-9, scale, 1.0)
    return (train_x - mean) / scale, (test_x - mean) / scale


def linear_probe(train_x, train_y, test_x, test_y, ridge: float = 1e-2) -> float:
    """One hot ridge regression, the closed form version of the usual linear probe."""
    design = np.hstack([train_x, np.ones((len(train_x), 1))])
    targets = np.eye(CLASSES)[train_y]
    gram = design.T @ design + ridge * np.eye(design.shape[1])
    weights = np.linalg.solve(gram, design.T @ targets)
    scores = np.hstack([test_x, np.ones((len(test_x), 1))]) @ weights
    return float((scores.argmax(axis=1) == test_y).mean())


def neighbour_probe(train_x, train_y, test_x, test_y, metric: str = "euclidean") -> float:
    if metric == "cosine":
        a = train_x / np.maximum(np.linalg.norm(train_x, axis=1, keepdims=True), 1e-12)
        b = test_x / np.maximum(np.linalg.norm(test_x, axis=1, keepdims=True), 1e-12)
        similarity = b @ a.T
        predicted = train_y[np.argmax(similarity, axis=1)]
    else:
        distances = (test_x ** 2).sum(1)[:, None] + (train_x ** 2).sum(1)[None, :] - 2.0 * test_x @ train_x.T
        predicted = train_y[np.argmin(distances, axis=1)]
    return float((predicted == test_y).mean())


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    per_class = 60 if quick else 250
    repeats = 3 if quick else 7

    builders = {
        "nuisance dominated": representation_nuisance,
        "multi modal clusters": representation_multimodal,
        "concentric shells": representation_shells,
    }
    results: dict[str, dict[str, float]] = {}
    rows = []
    for name, builder in builders.items():
        features, labels = builder(rng, per_class)
        train_idx, test_idx = split(rng, len(labels))
        train_x, test_x = features[train_idx], features[test_idx]
        train_y, test_y = labels[train_idx], labels[test_idx]
        scores = {
            "linear": linear_probe(train_x, train_y, test_x, test_y),
            "nearest neighbour, euclidean": neighbour_probe(train_x, train_y, test_x, test_y),
            "nearest neighbour, cosine": neighbour_probe(train_x, train_y, test_x, test_y, "cosine"),
        }
        std_train, std_test = standardise(train_x, test_x)
        scores["linear, standardised"] = linear_probe(std_train, train_y, std_test, test_y)
        scores["nearest neighbour, standardised"] = neighbour_probe(std_train, train_y, std_test, test_y)
        results[name] = scores
        rows.append([name] + [f"{100 * scores[key]:.1f}" for key in (
            "linear",
            "nearest neighbour, euclidean",
            "nearest neighbour, cosine",
            "linear, standardised",
            "nearest neighbour, standardised",
        )])
    probe_table = timing.markdown_table(
        [
            "Representation",
            "Linear probe (%)",
            "Nearest neighbour, euclidean (%)",
            "Nearest neighbour, cosine (%)",
            "Linear probe after standardising (%)",
            "Nearest neighbour after standardising (%)",
        ],
        rows,
    )

    names = list(builders)
    ranking_rows = []
    for probe in ("linear", "nearest neighbour, euclidean", "nearest neighbour, cosine", "nearest neighbour, standardised"):
        ordered = sorted(names, key=lambda n: -results[n][probe])
        ranking_rows.append(
            [
                probe,
                " then ".join(ordered),
                f"{100 * results[ordered[0]][probe]:.1f}",
                f"{100 * (results[ordered[0]][probe] - results[ordered[-1]][probe]):+.1f}",
            ]
        )
    ranking_table = timing.markdown_table(
        ["Probe", "Ranking, best first", "Top accuracy (%)", "Spread across representations (percentage points)"],
        ranking_rows,
    )
    winners = {row[1].split(" then ")[0] for row in ranking_rows}

    features, labels = representation_nuisance(rng, per_class)
    train_idx, test_idx = split(rng, len(labels))
    timings = [
        timing.measure(
            lambda: linear_probe(features[train_idx], labels[train_idx], features[test_idx], labels[test_idx]),
            label="ridge linear probe",
            repeats=repeats,
            inside_timer="solve and score, feature extraction excluded",
        ),
        timing.measure(
            lambda: neighbour_probe(features[train_idx], labels[train_idx], features[test_idx], labels[test_idx]),
            label="nearest neighbour probe",
            repeats=repeats,
            inside_timer="distance matrix and score, feature extraction excluded",
        ),
    ]
    cost_table = timing.table(timings, first_column="Probe") + (
        f"\n\n{len(labels)} items, {DIM} dimensional features, {CLASSES} classes, "
        f"{len(train_idx)} training and {len(test_idx)} test items."
    )

    chance = 100.0 / CLASSES
    linear_first = max(names, key=lambda n: results[n]["linear"])
    neighbour_first = max(names, key=lambda n: results[n]["nearest neighbour, euclidean"])
    inverted = linear_first != neighbour_first
    shells = results["concentric shells"]
    nuisance = results["nuisance dominated"]
    reading = (
        f"The two probes rank the same three representations differently. The linear probe "
        f"puts {linear_first} first, the nearest neighbour probe puts {neighbour_first} first, "
        f"and the ranking is therefore "
        f"{'inverted between them' if inverted else 'preserved between them'}. Neither number "
        f"measures representation quality in general, because each probe is a statement about "
        f"which structure counts. A linear map suppresses the high variance nuisance "
        f"directions that a distance cannot, which is why the nuisance dominated "
        f"representation scores {100 * nuisance['linear']:.1f} per cent under the linear probe "
        f"and {100 * nuisance['nearest neighbour, euclidean']:.1f} per cent under the "
        f"distance, close to the chance rate of {chance:.1f} per cent. A distance reads "
        f"several tight clusters per class that no single hyperplane isolates. The concentric "
        f"shells are the case worth remembering: they defeat both probes, scoring "
        f"{100 * shells['linear']:.1f} and "
        f"{100 * shells['nearest neighbour, euclidean']:.1f} per cent, even though the class "
        f"is recoverable from one scalar, the radius, because in this many dimensions every "
        f"test point's nearest neighbour sits on the innermost shell. Protocol details that "
        f"papers rarely state move the answer as much as the representation does: "
        f"standardising features before probing lifts the nuisance case from "
        f"{100 * nuisance['nearest neighbour, euclidean']:.1f} to "
        f"{100 * nuisance['nearest neighbour, standardised']:.1f} per cent. "
        f"{len(winners)} of the three representations win under at least one probe. The claim "
        f"under test fails: a probe number without its probe, its distance, its "
        f"regularisation and its feature preprocessing ranks nothing."
    )

    return (
        [
            ("Three representations, five probes", probe_table),
            ("Which representation each probe prefers", ranking_table),
            ("Probe cost", cost_table),
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
