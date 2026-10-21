# 13. A distributional image metric moves under changes a viewer cannot see

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## What moves the score

| Change applied to the reference set | Frechet distance on block transform features | Pixel difference from the reference |
| --- | --- | --- |
| same distribution, fresh draw | 0.0003 | not applicable, different images |
| resampled with a bilinear filter | 0.0319 | 7.17 levels, 28.5 dB |
| resampled with a Lanczos filter | 0.0141 | 5.54 levels, 30.7 dB |
| re-encoded at quality ninety five | 0.0001 | 0.93 levels, 45.7 dB |
| re-encoded at quality seventy five | 0.0031 | 3.05 levels, 35.5 dB |
| genuine shift, larger shapes | 0.0519 | 32.15 levels, 15.9 dB |
| genuine shift, flatter texture | 0.2738 | 30.99 levels, 16.1 dB |

## The metric's own noise floor

| Images per set | Frechet distance between two draws of one distribution |
| --- | --- |
| 100 | 0.0009 |
| 200 | 0.0002 |
| 400 | 0.0003 |

## Invisible changes against genuine ones

| Change | Kind | Frechet distance | Multiple of the metric's noise floor |
| --- | --- | --- | --- |
| resampled with a bilinear filter | invisible or near invisible | 0.0319 | 35.5 |
| resampled with a Lanczos filter | invisible or near invisible | 0.0141 | 15.6 |
| re-encoded at quality ninety five | invisible or near invisible | 0.0001 | 0.1 |
| genuine shift, larger shapes | genuine change of distribution | 0.0519 | 57.7 |
| genuine shift, flatter texture | genuine change of distribution | 0.2738 | 304.2 |

## Cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| feature extraction for one set | 9.42 | 0.511 | 10.6 | 7 |
| Frechet distance between two fitted Gaussians | 0.982 | 0.122 | 1.15 | 7 |

400 images per set at 64 by 64 pixels, block size 8, 64 dimensional features.

## Reading

Changes a viewer cannot see move the metric by more than its own noise floor, and in one case by more than a genuine change of distribution does. Swapping the resampling filter or re-encoding at near lossless quality leaves a pixel difference of a few code levels and a peak signal to noise ratio in the forties, yet the largest of those invisible changes, resampled with a bilinear filter, scores 0.0319, which is 35.5 times the floor measured between two draws of the same distribution. The weaker of the two genuine shifts, genuine shift, larger shapes, scores 0.0519. The genuine shifts still outscore the invisible ones here, and the floor itself depends on the sample count, which is a free parameter in most reported figures. The claim under test fails: a small difference in a distributional distance is evidence about a pipeline, not about samples, unless the resampling filter, the encoder, the sample count and the feature extractor are all held fixed and stated. This benchmark measures the sensitivity of the construction and does not reproduce any published score.
