# 04. Near duplicate leakage inflates a score with no change to the model

## Claim under test

A random split is a fair split, so a held out score measures generalisation.

## Why it matters

Real image data arrives in groups: frames of one scene, crops of one photograph, captures of one product. A random split over images puts members of a group on both sides, and the held out score then measures retrieval of a near duplicate rather than generalisation. The number looks good and does not survive contact with new scenes.

## Method

Features are generated with explicit group structure: a class prototype, a per scene offset larger than the class signal, and per frame jitter, with eight classes, forty scenes per class and four frames per scene in full mode. One nearest neighbour under Euclidean distance is scored twice on the same data, once under a random split over images and once under a split over scenes, at four jitter levels. A leakage audit is then run on the random split: the distance to the nearest training neighbour is thresholded, and precision and recall against the known group membership are reported. The timer covers the distance matrix and the argmin or minimum.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; one nearest neighbour under Euclidean distance, which has no parameters to fit and therefore cannot be the cause of the gap |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; 1280 items in 320 groups across eight classes in full mode, scored under a random split and a group split at the same sixty per cent training fraction |
| Input resolution and preprocessing | forty eight dimensional feature vectors, no normalisation, standing in for an embedding rather than for pixels |
| Metric with full definition | top one accuracy of the nearest neighbour classifier, and the fraction of test items whose nearest training neighbour belongs to their own group |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single evaluation pass, no augmentation, no detection and therefore no suppression settings |
| Training data used | the training side of whichever split is being scored, identical in size between the two splits |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the group split score, which is the honest number for the same model and the same data |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | the whole test split in one distance matrix |
| Input resolution | forty eight dimensional features, 1280 items in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | feature generation is outside the timer; the audit row times the same distance matrix the scoring row needs, which is the point of printing both |

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

### Random split against group split, as duplication loosens

| Frame jitter (feature units) | Random split accuracy (%) | Group split accuracy (%) | Inflation (percentage points) | Test items whose nearest train neighbour shares their group, random split (%) | Same, group split (%) |
| --- | --- | --- | --- | --- | --- |
| 0.05 | 97.3 | 51.6 | +45.7 | 92.2 | 0.0 |
| 0.15 | 99.2 | 42.8 | +56.4 | 96.9 | 0.0 |
| 0.35 | 96.9 | 36.1 | +60.7 | 96.1 | 0.0 |
| 0.80 | 94.7 | 31.2 | +63.5 | 93.0 | 0.0 |

### A leakage audit a reviewer can demand

| Distance threshold | Test items flagged as leaked | Flagged items that really share a group (%) | Leaked items caught (%) |
| --- | --- | --- | --- |
| 0.5 | 0 | 0.0 | 0.0 |
| 1.0 | 0 | 0.0 | 0.0 |
| 1.5 | 364 | 100.0 | 75.8 |
| 2.0 | 480 | 100.0 | 100.0 |

### Cost

| Operation | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| score the held out split | 4.68 | 0.42 | 5.81 | 7 |
| leakage audit over the same pair | 4 | 0.113 | 4.13 | 7 |

Dataset holds 1280 items in 320 groups across 8 classes, 48 dimensional features.

## Analysis

The same classifier, the same features and the same amount of training data give two different held out numbers, and the gap is as large as 63.5 percentage points. At the tightest duplication tested, the random split reports 97.3 per cent where the group split reports 51.6 per cent, because 92.2 per cent of test items find a training neighbour from their own group. The inflation shrinks as the duplicates get less similar, which is the honest caveat: leakage is a property of the data, not a constant. The audit costs the same order of work as scoring the split itself, so there is no efficiency argument for skipping it. The claim under test fails.

## What this machine cannot measure

- The leakage rate of any real dataset. The duplication here is synthetic and its strength is a knob, which is why the result is reported as a curve over that knob rather than as one number.
- Perceptual duplication, which needs pixels and an embedding rather than synthetic features.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. Accuracies are deterministic. To audit a real dataset, replace dataset() with your own features and group identifiers and keep the audit table, which is the part worth running before trusting a split.
