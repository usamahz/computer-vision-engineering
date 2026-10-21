# 14. Contamination is measurable without access to the model

## Claim under test

Evaluation on a public benchmark is sound because the training corpus is large and the overlap must be negligible.

## Why it matters

A benchmark whose items were on the open web before training measures memorisation as well as capability. The usual defence is that the corpus is too large for overlap to matter, which is an assertion about something cheap to measure, and the audit needs no access to the model or its weights.

## Method

A synthetic training corpus of three thousand documents of forty tokens over a vocabulary of six hundred is built, plus an evaluation set of three hundred items of eighteen tokens. A quarter of the evaluation items are injected into the corpus verbatim inside a host document, a quarter are injected as paraphrases with a fifth of their tokens dropped and one adjacent pair swapped, and the rest are left clean. Two detectors are run: exact match on eight token sequences, and shingle containment, the fraction of an item's three token shingles that appear anywhere in the corpus, at a threshold of thirty five hundredths. Containment rather than Jaccard similarity, because the question is whether a short item sits inside a long corpus. The image side repeats the exercise with an average hash against verbatim, re-encoded, resized and shifted copies. Recall by injection type, precision and the false positive rate on the clean portion are reported for each. The timer covers index construction and the audit separately.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no model of any kind, which is the point: the audit runs on the corpus and the evaluation set alone |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; three thousand corpus documents plus three hundred evaluation items in full mode, with injection type recorded per item as ground truth |
| Input resolution and preprocessing | token sequences for the text side; thirty two by thirty two grey images for the image side, hashed at eight by eight |
| Metric with full definition | recall per injection type, precision over flagged items, and the false positive rate on items known to be clean; mean Hamming distance in bits for the image hash |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | one audit pass, no augmentation, no detection and therefore no suppression settings; detection thresholds stated in the table rows |
| Training data used | the synthetic corpus, which is the object under audit rather than a training set for a model |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | byte identical comparison, which is what a checksum based audit would find |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | integer token identifiers and unsigned eight bit images |
| Batch size | the whole corpus for index construction, the whole evaluation set for the audit |
| Input resolution | not applicable to the text side; thirty two by thirty two for the image side |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; sets of token tuples and Pillow for the image hash |
| Warmup and statistic reported | one warmup iteration discarded; medians over three to seven repeats as printed, with the interquartile range and the ninety fifth percentile |
| Preprocessing and postprocessing inside the timer | index construction and lookup are timed separately and both are stated; corpus generation is outside both |

## Environment

Measured at run time by `misc/benchmarks/common/device.py` and reproduced here from
`results/raw.txt`. If this block and that file disagree, this file is wrong.

```
==============================================================================
machine (measured at run time, not typed into a README)
==============================================================================
  cpu                : Intel(R) Xeon(R) Processor @ 2.10GHz
  cores              : 4 logical, 4 physical
  memory             : 15.7 GiB
  virtual machine    : yes, guest of a hypervisor
  vector extensions  : sse4_2, avx, avx2, fma, avx512f, avx512_vnni, amx_int8
  accelerators       : none detected
  platform           : Linux-6.18.44-fc-v139-x86_64-with-glibc2.39
  python             : 3.13.16
  numpy              : 2.5.3 (blas: scipy-openblas 0.3.34.106.0)
  pillow             : 12.3.0
  thread limits      : OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1
  mode               : full
==============================================================================
```

Pinned through `requirements.txt`, which points at `../common/requirements.txt`: numpy 2.5.3 and
Pillow 12.3.0. The committed results came from `./run.sh` in this directory, which exports the thread
limits shown in the banner before Python starts.

## How to run

```sh
./run.sh            # full run, rewrites results/
QUICK=1 ./run.sh    # smoke test, under ten seconds, writes nothing
```

## Results

Reproduced from `results/summary.md`, which was written by the run that produced
`results/raw.txt` on the machine named above.

### How the corpora were built

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

### Two text detectors against two kinds of contamination

| Detector | Verbatim injections found (%) | Paraphrased injections found (%) | Precision (%) | False positives on the clean portion (%) |
| --- | --- | --- | --- | --- |
| exact match on 8 token sequences | 100.0 | 22.8 | 100.0 | 0.0 |
| shingle containment, 3 token shingles, threshold 0.35 | 100.0 | 59.6 | 100.0 | 0.0 |

### The image side, where a checksum fails

| How the copy was altered | Byte identical comparison finds it (%) | Average hash within six bits finds it (%) | Mean hash distance (bits) | False positives against unrelated images (%) |
| --- | --- | --- | --- | --- |
| verbatim | 100.0 | 100.0 | 0.00 | 0.0 |
| re-encoded | 0.0 | 100.0 | 1.05 | 0.0 |
| resized | 0.0 | 100.0 | 1.33 | 0.0 |
| shifted | 0.0 | 0.0 | 16.89 | 0.0 |

### Audit cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| build the token sequence index | 48.2 | 0 | 49.1 | 3 |
| audit every evaluation item | 0.851 | 0.0295 | 0.937 | 7 |

Corpus holds 3144 documents of 40 tokens over a vocabulary of 600, evaluation holds 300 items of 18 tokens.

## Analysis

An audit that needs no access to the model, no weights and no training run finds 100.0 per cent of the verbatim injections by exact token sequence match, with 0.0 per cent false positives on the clean portion, and it costs a single pass over the corpus. The same detector finds only 22.8 per cent of the paraphrased injections, which is the point: a corpus owner who reports no exact overlap has reported almost nothing about contamination that arrives as a rewrite. Shingle containment, which asks what fraction of the evaluation item appears anywhere in the corpus rather than how similar two documents are, recovers 59.6 per cent of the paraphrases at 100.0 per cent precision and 0.0 per cent false positives. The image side behaves the same way: a re-encoded copy is byte identical in 0.0 per cent of cases, so a checksum finds nothing, while an average hash within six bits finds 100.0 per cent of them. The claim under test fails in both directions: overlap is not negligible merely because the corpus is large, and it is cheap enough to measure that an evaluation which does not report the audit has chosen not to run it.

## What this machine cannot measure

- The contamination rate of any real corpus, which needs that corpus. This measures what the detectors can find at a known injection rate.
- Semantic contamination, where an item is reworded beyond shingle overlap, which neither detector here catches and which is the honest limit of the method.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. All rates are deterministic. To audit a real corpus, replace the generated corpus with a token stream from it, keep the containment detector, and expect the index to dominate the cost.
