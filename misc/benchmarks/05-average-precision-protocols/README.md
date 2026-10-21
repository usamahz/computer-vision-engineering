# 05. One set of detections, three average precision protocols, three numbers

## Claim under test

Average precision is a property of a detector, so two papers quoting it are comparable.

## Why it matters

Detection progress is reported almost entirely in average precision, and the number depends on an interpolation rule, an overlap threshold or a set of them, a detections per image cap, a score floor and a choice between averaging over classes and pooling across them. None of those is the detector. A comparison that does not hold them fixed is measuring the protocol.

## Method

One seeded set of ground truth boxes and one seeded set of detections are generated over three hundred images and four classes, with localisation quality falling as score falls, duplicate detections on the same object, and low scoring background false positives. Matching is greedy by descending score with each ground truth box claimable once. The same fixed set is then scored under four protocols: eleven point interpolation at overlap one half, all point interpolation at overlap one half, hundred and one point interpolation at overlap one half, and hundred and one point interpolation averaged over ten overlap thresholds from one half to ninety five hundredths. Three further protocol choices are swept on the same data: a score floor, a detections per image cap, and per class averaging against pooling. The timer covers matching and integration.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned detector; one fixed seeded set of detections, which is what makes the comparison airtight, since the only thing changing between numbers is the protocol |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; three hundred images, four classes, one split |
| Input resolution and preprocessing | boxes in a 640 by 480 coordinate frame; no images and therefore no resize or normalisation |
| Metric with full definition | average precision under four rules, each stated in the results table: eleven recall points, every recall change, hundred and one recall points, and the mean of the last over ten overlap thresholds, all after making precision monotone to the right |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no test time augmentation, and no suppression applied, so that suppression cannot confound the protocol comparison; the suppression sweep is benchmark ten |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the same detections under the other three protocols, and a second detector formed by applying a deployable score floor |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | the whole detection set per scoring call |
| Input resolution | not applicable to a scoring benchmark; the box coordinate frame is 640 by 480 |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the matcher is a Python loop over detections, so these timings characterise this implementation |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | matching and integration are inside; data generation is outside |

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

### Four protocols, one set of detections

| Protocol, scored on the identical detections | Overlap threshold | Interpolation | Average precision (%) |
| --- | --- | --- | --- |
| eleven point interpolation of the early challenge | 0.50 | eleven recall points | 77.97 |
| all point interpolation that replaced it | 0.50 | every recall change | 80.07 |
| hundred and one point interpolation | 0.50 | hundred and one recall points | 79.88 |
| hundred and one point, averaged over ten thresholds | 0.50 to 0.95 | hundred and one recall points | 43.77 |

### Discarding low scoring detections before scoring

| Score floor applied before scoring | Detections kept | All point average precision (%) | Averaged over thresholds (%) |
| --- | --- | --- | --- |
| 0.00 | 1471 | 80.07 | 43.77 |
| 0.05 | 1390 | 80.01 | 43.71 |
| 0.10 | 1277 | 79.58 | 43.51 |
| 0.30 | 951 | 77.93 | 42.45 |
| 0.50 | 737 | 72.33 | 40.23 |

### Capping detections per image

| Detections per image kept | Detections scored | All point average precision (%) |
| --- | --- | --- |
| 1 | 299 | 32.25 |
| 5 | 1223 | 79.35 |
| 20 | 1471 | 80.07 |
| 100 | 1471 | 80.07 |

### Per class averaging against pooling

| Averaging | All point average precision (%) | Hundred and one point (%) |
| --- | --- | --- |
| mean over classes | 80.07 | 79.88 |
| pooled across classes | 79.99 | 79.83 |

### Cost of scoring

| Protocol | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| all point, single threshold | 25.6 | 1.29 | 28 | 7 |
| hundred and one point, ten thresholds | 265 | 9.62 | 284 | 7 |

Scored set holds 1471 detections against 865 ground truth boxes over 300 images and 4 classes.

## Analysis

One fixed set of detections scores 77.97, 80.07, 79.88 and 43.77 per cent under the four protocols, a total spread of 36.30 points with no change to the detector, the data or the matching. Most of that spread is the overlap threshold averaging rather than the interpolation, and it is worth separating the two: holding the overlap threshold at one half, the three interpolation rules alone still differ by 2.10 points, which is the margin a typical paper claims over its baseline. Three further protocol choices move the number as much. Discarding detections below half confidence costs 7.74 points of all point average precision, so a pipeline tuned for a sensible operating point scores worse than one that emits junk it would never act on. Capping detections per image moves it again, and so does swapping mean over classes for pooling across classes. On the pair of detectors, every protocol ranked the same one first, so the ordering was robust here, but the measured gap between them ranged from 2.80 to 6.85 points depending on protocol, which is the difference between a result worth shipping and a rounding error. The claim under test fails: an average precision figure is a property of a detector and a protocol together.

## What this machine cannot measure

- A reproduction of any official evaluation implementation. This is an independent implementation of the published rules on synthetic data, so it demonstrates the size of the protocol effect and is not a drop in replacement for an official scorer.
- Area range breakdowns and crowd annotations, which the official detection protocol includes and this does not.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. Every average precision figure is deterministic and must match bit for bit on any machine; only the cost table moves. To test a real detector, replace make_data() with its detections and the matching ground truth and keep the four protocols.
