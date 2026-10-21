# 10. The suppression threshold is a product decision, and it is not free

## Claim under test

Non maximum suppression is a postprocessing detail, so a detector's quality and its latency can both be quoted without it.

## Why it matters

Suppression decides what a product acts on, and its threshold moves the precision and recall a user experiences more than it moves the published metric. It also costs real time that grows with the number of boxes, which is why the latency figure a paper quotes and the latency a camera sees are different numbers.

## Method

Detections are generated over two hundred images in two regimes, sparse and crowded, with several overlapping detections per object and low scoring background false positives. Greedy suppression is applied per image at seven overlap thresholds, plus a row with no suppression at all. For each, all point average precision at overlap one half is reported together with precision and recall at a fixed score of one half, which is the operating point a deployed system would use. Suppression cost is then timed separately against box count from one hundred to two thousand boxes. The timer covers the suppression only, with no decoding and no copy between devices.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned detector; one fixed seeded detection set per regime, so suppression is the only thing varying |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; two hundred images per regime, sparse and crowded, one split |
| Input resolution and preprocessing | boxes in a 640 by 480 coordinate frame; no images and therefore no resize |
| Metric with full definition | all point interpolated average precision at overlap one half, and precision, recall and their harmonic mean among detections scoring at least one half |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no test time augmentation, greedy suppression per image at the overlap threshold named in each row, class agnostic, no score floor before suppression |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the same detections with no suppression, and the threshold that maximises each of the two metrics |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | one image's boxes per suppression call |
| Input resolution | not applicable to the suppression step; box counts of one hundred to two thousand are swept instead |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; greedy suppression written as a Python loop over surviving boxes with vectorised overlap, so the absolute milliseconds characterise this implementation rather than a fused kernel |
| Warmup and statistic reported | one warmup iteration discarded; median of seven in full mode with the interquartile range and the ninety fifth percentile |
| Preprocessing and postprocessing inside the timer | the suppression is the whole of what is inside the timer; box generation, decoding and any device transfer are outside, which is the boundary a published figure usually draws and the reason this table exists |

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

### Suppression threshold sweep, sparse scenes

| Overlap threshold | Detections kept | All point average precision (%) | Precision at score 0.5 (%) | Recall at score 0.5 (%) | Harmonic mean at that score | Detections acted on |
| --- | --- | --- | --- | --- | --- | --- |
| 0.30 | 718 | 85.90 | 82.7 | 87.2 | 0.849 | 427 |
| 0.45 | 883 | 86.73 | 72.1 | 91.1 | 0.805 | 512 |
| 0.50 | 940 | 87.35 | 69.7 | 93.1 | 0.797 | 541 |
| 0.60 | 1060 | 85.34 | 62.6 | 93.8 | 0.751 | 607 |
| 0.70 | 1164 | 82.73 | 56.5 | 93.8 | 0.705 | 673 |
| 0.90 | 1223 | 81.67 | 53.7 | 93.8 | 0.683 | 707 |
| no suppression | 1225 | 81.66 | 53.7 | 93.8 | 0.683 | 708 |

### Suppression threshold sweep, crowded scenes

| Overlap threshold | Detections kept | All point average precision (%) | Precision at score 0.5 (%) | Recall at score 0.5 (%) | Harmonic mean at that score | Detections acted on |
| --- | --- | --- | --- | --- | --- | --- |
| 0.30 | 1572 | 54.77 | 82.5 | 54.4 | 0.656 | 1151 |
| 0.45 | 2446 | 72.99 | 74.8 | 73.6 | 0.742 | 1717 |
| 0.50 | 2815 | 77.89 | 71.3 | 79.5 | 0.752 | 1946 |
| 0.60 | 3559 | 84.15 | 64.7 | 89.2 | 0.750 | 2404 |
| 0.70 | 4174 | 84.39 | 58.6 | 92.7 | 0.718 | 2757 |
| 0.90 | 4577 | 83.31 | 54.5 | 93.5 | 0.689 | 2990 |
| no suppression | 4582 | 83.19 | 54.5 | 93.5 | 0.688 | 2995 |

### Cost of the suppression step alone

| Boxes entering suppression | Boxes surviving | Median latency (ms) | p95 (ms) | Microseconds per box |
| --- | --- | --- | --- | --- |
| 100 | 97 | 1.94 | 2.4 | 19.43 |
| 500 | 411 | 9.41 | 10.6 | 18.83 |
| 1000 | 737 | 20.2 | 20.8 | 20.24 |
| 2000 | 1243 | 44.5 | 47.4 | 22.27 |

## Analysis

The threshold moves both numbers, and it moves them differently. Average precision ranges over 5.69 points on sparse scenes and 29.62 points on crowded ones, while the harmonic mean of precision and recall at a fixed deployable score ranges over 0.166 and 0.096. They do not peak in the same place: on sparse scenes average precision is highest at overlap threshold 0.50 and the deployed operating point is highest at 0.30, and on crowded scenes at 0.70 and 0.50. Tuning against the published metric and tuning against the product are therefore different exercises, and a paper that reports only the former has not reported the decision a team has to make. The cost half of the claim fails too, with one caveat stated plainly: this is a greedy suppression written in numpy with a Python loop over surviving boxes, so the absolute milliseconds characterise this implementation and not a fused kernel. What transfers is the shape. Suppressing 2000 boxes takes 44.5 milliseconds here with a ninety fifth percentile of 47.4, the cost per box rises with the box count rather than staying flat, and the box count rises with the crowding of the scene. A latency figure should state whether this step is inside the timer. Most published figures do not.

## What this machine cannot measure

- A fused kernel's suppression cost, or a batched implementation on an accelerator. Neither is available here, and the absolute figures should not be read as the cost of suppression in a production runtime.
- Soft suppression and learned suppression variants, which change the quality curve and are not implemented.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. The quality tables are deterministic. The cost table is implementation bound, so on another machine or with another implementation re-measure it rather than carrying these numbers over.
