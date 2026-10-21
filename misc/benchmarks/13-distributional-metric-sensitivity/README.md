# 13. A distributional image metric moves under changes a viewer cannot see

## Claim under test

A lower distributional distance between generated and reference images means better samples, so a small difference in it is evidence of a better model.

## Why it matters

Generative vision is compared through a distance between feature distributions, and that distance is a function of the whole pipeline: the resampling filter, the encoder, the sample count and the feature extractor. A difference smaller than the pipeline's own sensitivity is not evidence about samples.

## Method

Four hundred synthetic images of shapes on textured backgrounds are generated at sixty four by sixty four. Features are the mean absolute block cosine transform coefficient per frequency over eight by eight blocks, a fixed hand built feature, because no network weights may be downloaded here. A Frechet distance between Gaussian fits of those features is computed between the reference set and seven variants: a fresh draw of the same distribution, two resampling filter round trips, two re-encodes at quality ninety five and seventy five, and two genuine changes of distribution. Pixel difference in code levels and peak signal to noise ratio are reported alongside, as the proxy for what a viewer could see. The metric's own noise floor is measured by comparing two draws of the same distribution at three sample counts. This measures the sensitivity of the construction and does not reproduce any published score.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned feature extractor; an eight by eight block cosine transform, which is why the absolute values here are not comparable to any published figure |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; four hundred images per set in full mode, one hundred and twenty in quick mode |
| Input resolution and preprocessing | sixty four by sixty four grey images; the variants differ exactly in the preprocessing under test, which is the resampling filter or the encoder quality |
| Metric with full definition | Frechet distance between Gaussians fitted to the feature vectors, the squared mean difference plus the trace of the sum of covariances less twice the matrix square root of their product, with the square root taken through a symmetric eigendecomposition |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no augmentation, no detection and therefore no suppression settings; sample count stated per row because the metric depends on it |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the metric's own noise floor between two draws of one distribution, and two genuine changes of distribution |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 for features and the matrix square root, unsigned eight bit for the encode and resample steps |
| Batch size | the whole set per feature extraction call |
| Input resolution | sixty four by sixty four, four hundred images per set in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | one warmup iteration discarded; median of seven in full mode with the interquartile range and the ninety fifth percentile |
| Preprocessing and postprocessing inside the timer | feature extraction is timed separately from the distance, and image generation and the variant preprocessing are outside both |

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

### What moves the score

| Change applied to the reference set | Frechet distance on block transform features | Pixel difference from the reference |
| --- | --- | --- |
| same distribution, fresh draw | 0.0003 | not applicable, different images |
| resampled with a bilinear filter | 0.0319 | 7.17 levels, 28.5 dB |
| resampled with a Lanczos filter | 0.0141 | 5.54 levels, 30.7 dB |
| re-encoded at quality ninety five | 0.0001 | 0.93 levels, 45.7 dB |
| re-encoded at quality seventy five | 0.0031 | 3.05 levels, 35.5 dB |
| genuine shift, larger shapes | 0.0519 | 32.15 levels, 15.9 dB |
| genuine shift, flatter texture | 0.2738 | 30.99 levels, 16.1 dB |

### The metric's own noise floor

| Images per set | Frechet distance between two draws of one distribution |
| --- | --- |
| 100 | 0.0009 |
| 200 | 0.0002 |
| 400 | 0.0003 |

### Invisible changes against genuine ones

| Change | Kind | Frechet distance | Multiple of the metric's noise floor |
| --- | --- | --- | --- |
| resampled with a bilinear filter | invisible or near invisible | 0.0319 | 35.5 |
| resampled with a Lanczos filter | invisible or near invisible | 0.0141 | 15.6 |
| re-encoded at quality ninety five | invisible or near invisible | 0.0001 | 0.1 |
| genuine shift, larger shapes | genuine change of distribution | 0.0519 | 57.7 |
| genuine shift, flatter texture | genuine change of distribution | 0.2738 | 304.2 |

### Cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| feature extraction for one set | 9.42 | 0.511 | 10.6 | 7 |
| Frechet distance between two fitted Gaussians | 0.982 | 0.122 | 1.15 | 7 |

400 images per set at 64 by 64 pixels, block size 8, 64 dimensional features.

## Analysis

Changes a viewer cannot see move the metric by more than its own noise floor, and in one case by more than a genuine change of distribution does. Swapping the resampling filter or re-encoding at near lossless quality leaves a pixel difference of a few code levels and a peak signal to noise ratio in the forties, yet the largest of those invisible changes, resampled with a bilinear filter, scores 0.0319, which is 35.5 times the floor measured between two draws of the same distribution. The weaker of the two genuine shifts, genuine shift, larger shapes, scores 0.0519. The genuine shifts still outscore the invisible ones here, and the floor itself depends on the sample count, which is a free parameter in most reported figures. The claim under test fails: a small difference in a distributional distance is evidence about a pipeline, not about samples, unless the resampling filter, the encoder, the sample count and the feature extractor are all held fixed and stated. This benchmark measures the sensitivity of the construction and does not reproduce any published score.

## What this machine cannot measure

- Any published distributional score, which uses a learned feature network whose weights cannot be downloaded here. The mechanism transfers, the absolute values do not.
- Human preference, which is what the metric is standing in for and what no distributional distance measures.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. All distances are deterministic. To test a real pipeline, replace features() with the learned extractor and keep the variant list, especially the resampling filter and the encode quality rows.
