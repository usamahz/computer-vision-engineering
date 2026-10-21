#!/usr/bin/env python3
"""14. Contamination is measurable without access to the model.

Claim under test: evaluation on a public benchmark is sound because the training corpus is
large and the overlap must be negligible.

The benchmark builds a seeded synthetic training corpus and a seeded evaluation set, injects a
known fraction of the evaluation items into the corpus verbatim and a known fraction as
paraphrases, and then audits the corpus with two detectors that need nothing but the text: an
exact token sequence match, and a shingle overlap estimate. It repeats the exercise on the
image side with an average hash against re-encoded and resized copies. Recall, precision and
the false positive floor on the clean portion are reported for each.
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

TITLE = "14. Contamination is measurable without access to the model"
CLAIM = "a large training corpus makes overlap with a public benchmark negligible"

VOCAB = 600
DOC_TOKENS = 40
EVAL_TOKENS = 18
NGRAM = 8
SHINGLE = 3
CONTAINMENT_THRESHOLD = 0.35


def sentence(rng, length: int) -> tuple[int, ...]:
    return tuple(int(t) for t in rng.integers(0, VOCAB, size=length))


def paraphrase(rng, tokens: tuple[int, ...]) -> tuple[int, ...]:
    """Drop a fifth of the tokens and swap one adjacent pair, which is what a rewrite looks like."""
    keep = [t for t in tokens if rng.random() > 0.2]
    if len(keep) > 3:
        index = int(rng.integers(0, len(keep) - 1))
        keep[index], keep[index + 1] = keep[index + 1], keep[index]
    return tuple(keep)


def ngrams(tokens: tuple[int, ...], n: int) -> set[tuple[int, ...]]:
    return {tokens[i : i + n] for i in range(max(len(tokens) - n + 1, 0))}


def containment(item: tuple[int, ...], index: set[tuple[int, ...]]) -> float:
    """Fraction of the item's shingles that appear anywhere in the corpus.

    Containment rather than Jaccard similarity, because the question is whether the short
    evaluation item is inside the long corpus, and a symmetric similarity is diluted by
    everything else in the host document.
    """
    shingles = ngrams(item, SHINGLE)
    if not shingles:
        return 0.0
    return len(shingles & index) / len(shingles)


def average_hash(image: np.ndarray) -> np.ndarray:
    small = np.asarray(Image.fromarray(image).resize((8, 8), Image.BILINEAR), dtype=np.float64)
    return (small > small.mean()).ravel()


def image_variants(rng, image: np.ndarray, kind: str) -> np.ndarray:
    pil = Image.fromarray(image)
    if kind == "verbatim":
        return image
    if kind == "re-encoded":
        buffer = io.BytesIO()
        pil.save(buffer, format="JPEG", quality=70)
        buffer.seek(0)
        return np.asarray(Image.open(buffer).convert("L"), dtype=np.uint8)
    if kind == "resized":
        return np.asarray(pil.resize((48, 48), Image.BILINEAR).resize(pil.size, Image.BILINEAR), dtype=np.uint8)
    if kind == "shifted":
        return np.roll(image, 2, axis=1)
    raise ValueError(kind)


def run(quick: bool) -> tuple[list[tuple[str, str]], str]:
    rng = determinism.rng()
    corpus_size = 600 if quick else 3000
    eval_size = 120 if quick else 300
    repeats = 3 if quick else 7

    evaluation = [sentence(rng, EVAL_TOKENS) for _ in range(eval_size)]
    labels = []
    corpus = [sentence(rng, DOC_TOKENS) for _ in range(corpus_size)]

    for index, item in enumerate(evaluation):
        draw = rng.random()
        if draw < 0.25:
            kind = "verbatim"
            host = list(sentence(rng, DOC_TOKENS - EVAL_TOKENS))
            cut = int(rng.integers(0, len(host)))
            corpus.append(tuple(host[:cut] + list(item) + host[cut:]))
        elif draw < 0.5:
            kind = "paraphrased"
            rewritten = paraphrase(rng, item)
            host = list(sentence(rng, DOC_TOKENS - len(rewritten)))
            cut = int(rng.integers(0, len(host)))
            corpus.append(tuple(host[:cut] + list(rewritten) + host[cut:]))
        else:
            kind = "clean"
        labels.append(kind)

    corpus_ngrams: set[tuple[int, ...]] = set()
    for document in corpus:
        corpus_ngrams |= ngrams(document, NGRAM)
    corpus_shingles: set[tuple[int, ...]] = set()
    for document in corpus:
        corpus_shingles |= ngrams(document, SHINGLE)

    exact_flags, shingle_flags = [], []
    containments = []
    for item in evaluation:
        exact_flags.append(bool(ngrams(item, NGRAM) & corpus_ngrams))
        value = containment(item, corpus_shingles)
        containments.append(value)
        shingle_flags.append(value >= CONTAINMENT_THRESHOLD)

    def stats(flags: list[bool]) -> list[str]:
        flags_array = np.array(flags)
        kinds = np.array(labels)
        contaminated = kinds != "clean"
        true_positives = int((flags_array & contaminated).sum())
        false_positives = int((flags_array & ~contaminated).sum())
        recall_verbatim = float(flags_array[kinds == "verbatim"].mean()) if (kinds == "verbatim").any() else 0.0
        recall_para = float(flags_array[kinds == "paraphrased"].mean()) if (kinds == "paraphrased").any() else 0.0
        precision = true_positives / max(true_positives + false_positives, 1e-12)
        false_rate = float(flags_array[~contaminated].mean())
        return [
            f"{100 * recall_verbatim:.1f}",
            f"{100 * recall_para:.1f}",
            f"{100 * precision:.1f}",
            f"{100 * false_rate:.1f}",
        ]

    text_table = timing.markdown_table(
        [
            "Detector",
            f"Verbatim injections found (%)",
            "Paraphrased injections found (%)",
            "Precision (%)",
            "False positives on the clean portion (%)",
        ],
        [
            [f"exact match on {NGRAM} token sequences"] + stats(exact_flags),
            [f"shingle containment, {SHINGLE} token shingles, threshold {CONTAINMENT_THRESHOLD:g}"] + stats(shingle_flags),
        ],
    )

    counts = {kind: labels.count(kind) for kind in ("verbatim", "paraphrased", "clean")}
    setup_table = timing.markdown_table(
        ["Quantity", "Value"],
        [
            ["training documents before injection", str(corpus_size)],
            ["evaluation items", str(eval_size)],
            ["evaluation items injected verbatim", str(counts["verbatim"])],
            ["evaluation items injected as paraphrases", str(counts["paraphrased"])],
            ["evaluation items left clean", str(counts["clean"])],
            ["distinct token sequences in the corpus index", str(len(corpus_ngrams))],
            ["distinct shingles in the corpus index", str(len(corpus_shingles))],
            ["mean containment of a clean evaluation item", f"{float(np.mean([c for c, k in zip(containments, labels) if k == 'clean'])):.3f}"],
            ["mean containment of a paraphrased injection", f"{float(np.mean([c for c, k in zip(containments, labels) if k == 'paraphrased'])):.3f}"],
        ],
    )

    # The image side, where a re-encode or a resize defeats a checksum.
    image_count = 60 if quick else 150
    base = (rng.random((image_count, 32, 32)) * 255).astype(np.uint8)
    rows = []
    for kind in ("verbatim", "re-encoded", "resized", "shifted"):
        copies = np.stack([image_variants(rng, image, kind) for image in base])
        exact = float(np.mean([bool((copies[i] == base[i]).all()) for i in range(image_count)]))
        hashes_base = np.stack([average_hash(image) for image in base])
        hashes_copy = np.stack([average_hash(image) for image in copies])
        distances = (hashes_base != hashes_copy).sum(axis=1)
        found = float((distances <= 6).mean())
        cross = np.stack([average_hash(image) for image in base[::-1]])
        cross_distance = (hashes_base != cross).sum(axis=1)
        false_rate = float((cross_distance <= 6).mean())
        rows.append([kind, f"{100 * exact:.1f}", f"{100 * found:.1f}", f"{float(distances.mean()):.2f}", f"{100 * false_rate:.1f}"])
    image_table = timing.markdown_table(
        [
            "How the copy was altered",
            "Byte identical comparison finds it (%)",
            "Average hash within six bits finds it (%)",
            "Mean hash distance (bits)",
            "False positives against unrelated images (%)",
        ],
        rows,
    )

    timings = [
        timing.measure(lambda: {n for d in corpus for n in ngrams(d, NGRAM)}, label="build the token sequence index", repeats=max(repeats - 4, 3), warmup=1, inside_timer="index construction only"),
        timing.measure(lambda: [bool(ngrams(i, NGRAM) & corpus_ngrams) for i in evaluation], label="audit every evaluation item", repeats=repeats, warmup=1, inside_timer="lookup only, index built beforehand"),
    ]
    cost_table = timing.table(timings, first_column="Stage") + (
        f"\n\nCorpus holds {len(corpus)} documents of {DOC_TOKENS} tokens over a vocabulary of "
        f"{VOCAB}, evaluation holds {eval_size} items of {EVAL_TOKENS} tokens."
    )

    exact_stats = stats(exact_flags)
    shingle_stats = stats(shingle_flags)
    reencoded = next(row for row in rows if row[0] == "re-encoded")
    reading = (
        f"An audit that needs no access to the model, no weights and no training run finds "
        f"{exact_stats[0]} per cent of the verbatim injections by exact token sequence match, "
        f"with {exact_stats[3]} per cent false positives on the clean portion, and it costs a "
        f"single pass over the corpus. The same detector finds only {exact_stats[1]} per cent "
        f"of the paraphrased injections, which is the point: a corpus owner who reports no "
        f"exact overlap has reported almost nothing about contamination that arrives as a "
        f"rewrite. Shingle containment, which asks what fraction of the evaluation item "
        f"appears anywhere in the corpus rather than how similar two documents are, recovers "
        f"{shingle_stats[1]} per cent of the paraphrases at {shingle_stats[2]} per cent "
        f"precision and {shingle_stats[3]} per cent false positives. The image side behaves the "
        f"same way: a re-encoded copy is byte identical in {reencoded[1]} per cent of cases, "
        f"so a checksum finds nothing, while an average hash within six bits finds "
        f"{reencoded[2]} per cent of them. The claim under test fails in both directions: "
        f"overlap is not negligible merely because the corpus is large, and it is cheap enough "
        f"to measure that an evaluation which does not report the audit has chosen not to run "
        f"it."
    )

    return (
        [
            ("How the corpora were built", setup_table),
            ("Two text detectors against two kinds of contamination", text_table),
            ("The image side, where a checksum fails", image_table),
            ("Audit cost", cost_table),
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
