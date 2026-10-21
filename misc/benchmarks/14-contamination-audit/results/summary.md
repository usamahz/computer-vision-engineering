# 14. Contamination is measurable without access to the model

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## How the corpora were built

| Quantity | Value |
| --- | --- |
| training documents before injection | 3000 |
| evaluation items | 300 |
| evaluation items injected verbatim | 87 |
| evaluation items injected as paraphrases | 57 |
| evaluation items left clean | 156 |
| distinct token sequences in the corpus index | 103752 |
| distinct shingles in the corpus index | 119444 |
| mean containment of a clean evaluation item | 0.001 |
| mean containment of a paraphrased injection | 0.379 |

## Two text detectors against two kinds of contamination

| Detector | Verbatim injections found (%) | Paraphrased injections found (%) | Precision (%) | False positives on the clean portion (%) |
| --- | --- | --- | --- | --- |
| exact match on 8 token sequences | 100.0 | 22.8 | 100.0 | 0.0 |
| shingle containment, 3 token shingles, threshold 0.35 | 100.0 | 59.6 | 100.0 | 0.0 |

## The image side, where a checksum fails

| How the copy was altered | Byte identical comparison finds it (%) | Average hash within six bits finds it (%) | Mean hash distance (bits) | False positives against unrelated images (%) |
| --- | --- | --- | --- | --- |
| verbatim | 100.0 | 100.0 | 0.00 | 0.0 |
| re-encoded | 0.0 | 100.0 | 1.05 | 0.0 |
| resized | 0.0 | 100.0 | 1.33 | 0.0 |
| shifted | 0.0 | 0.0 | 16.89 | 0.0 |

## Audit cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| build the token sequence index | 48.2 | 0 | 49.1 | 3 |
| audit every evaluation item | 0.851 | 0.0295 | 0.937 | 7 |

Corpus holds 3144 documents of 40 tokens over a vocabulary of 600, evaluation holds 300 items of 18 tokens.

## Reading

An audit that needs no access to the model, no weights and no training run finds 100.0 per cent of the verbatim injections by exact token sequence match, with 0.0 per cent false positives on the clean portion, and it costs a single pass over the corpus. The same detector finds only 22.8 per cent of the paraphrased injections, which is the point: a corpus owner who reports no exact overlap has reported almost nothing about contamination that arrives as a rewrite. Shingle containment, which asks what fraction of the evaluation item appears anywhere in the corpus rather than how similar two documents are, recovers 59.6 per cent of the paraphrases at 100.0 per cent precision and 0.0 per cent false positives. The image side behaves the same way: a re-encoded copy is byte identical in 0.0 per cent of cases, so a checksum finds nothing, while an average hash within six bits finds 100.0 per cent of them. The claim under test fails in both directions: overlap is not negligible merely because the corpus is large, and it is cheap enough to measure that an evaluation which does not report the audit has chosen not to run it.
