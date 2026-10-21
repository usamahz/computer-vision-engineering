# 08. A geometric augmentation that leaves the label alone breaks the label

## Claim under test

Augmentation is a property of the input pipeline, so a stronger policy is a free improvement.

## Why it matters

Augmentation code sits far from label code in most pipelines. When a geometric transform is added to the image path and the label path is forgotten, training still runs, losses still fall and the supervision is pointing at the wrong place. The failure is silent because every shape and every dtype is still correct.

## Method

A mask containing one elongated object is generated at 384 by 384 and its true box is the tight bounding box of the mask. Five augmentations are applied with nearest neighbour resampling: horizontal flip, rotation by ninety degrees, rotation by fifteen degrees, crop and resize, and a resize that changes the aspect ratio. For each one, three label handling strategies are scored against the truth recovered from the transformed mask: leaving the label alone, mapping the four box corners and taking the axis aligned hull, and transforming the mask and re-deriving the box. Overlap and the area ratio of the mapped box to the true box are reported. A second table converts the overlap loss into the share of a training run that would be supervised by a wrong box at a given augmentation probability. The timer covers the mask resampling and the corner transform separately.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; three label handling strategies applied to one known object |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; one object mask, five augmentations |
| Input resolution and preprocessing | 384 by 384 binary mask in full mode, 128 by 128 in quick mode; nearest neighbour resampling so that no interpolation softens the mask |
| Metric with full definition | intersection over union between the supervised box and the box re-derived from the transformed mask, and the ratio of their areas |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, each augmentation applied once deterministically, no detection and therefore no suppression settings |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the box re-derived from the transformed mask, which is the ground truth by construction |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | unsigned eight bit masks with float64 geometry |
| Batch size | one mask per call |
| Input resolution | 384 by 384 in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | the mask row times the resampling only, the corner row times the four point transform only; mask generation is outside both |

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

### Three label handling strategies against the truth

| Augmentation | Overlap when the label is left alone | Overlap when the box corners are mapped | Area of the mapped box over the true box | Overlap when the mask is transformed |
| --- | --- | --- | --- | --- |
| horizontal flip | 0.352 | 1.000 | 1.000 | 1.000 |
| rotate ninety degrees | 0.370 | 1.000 | 1.000 | 1.000 |
| rotate fifteen degrees | 0.788 | 0.753 | 1.328 | 1.000 |
| crop and resize | 0.639 | 0.990 | 0.999 | 1.000 |
| stretch, aspect changed | 0.328 | 0.991 | 1.000 | 1.000 |

### What a wrong label costs over a training run

| Probability the augmentation fires | Mean overlap of the supervised box with the object | Share of the training signal pointing at the wrong place (%) |
| --- | --- | --- |
| 0.10 | 0.933 | 6.7 |
| 0.25 | 0.832 | 16.8 |
| 0.50 | 0.664 | 33.6 |
| 0.90 | 0.395 | 60.5 |

### Cost of handling the label

| Label handling | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| transform the mask | 0.257 | 0.0248 | 0.289 | 7 |
| map the box corners | 0.00867 | 0.000724 | 0.00972 | 7 |

Mask is 384 by 384 pixels, nearest neighbour resampling, one object.

## Analysis

Leaving the label alone is not a small error. A horizontal flip, the cheapest augmentation in every pipeline, drops the overlap between the supervised box and the object to 0.352, which is below the threshold at which a detection would count as correct at evaluation time. Mapping the box corners fixes the axis aligned transforms exactly, and for a fifteen degree rotation it returns an overlap of 0.753 while inflating the box to 1.328 times the true area, because an axis aligned hull of a rotated rectangle is not the box of the rotated object. Only transforming the mask and re-deriving the box recovers the truth in every case. Re-deriving costs more than mapping four corners, and that cost is the whole reason pipelines get this wrong. The claim under test fails: a stronger policy is free only for the input.

## What this machine cannot measure

- Keypoint handedness and polygon masks, which fail in the same way and are not covered here.
- What any particular augmentation library does. The transforms here are applied explicitly so that the label handling is visible.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. Overlaps and area ratios are deterministic. The transfer to a real pipeline is a code review question: find the augmentation that is applied to the image and check whether the label path applies the same transform.
