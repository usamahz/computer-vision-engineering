# 02. Sensor noise is signal dependent

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Photon transfer curve, measured

| Mean signal (electrons) | Measured mean (DN) | Measured noise (DN, standard deviation) | Shot noise alone (DN) | Read noise alone (DN) | Relative noise (%) |
| --- | --- | --- | --- | --- | --- |
| 8 | 1.6 | 0.89 | 0.57 | 0.64 | 55.18 |
| 40 | 8.0 | 1.44 | 1.26 | 0.64 | 18.02 |
| 200 | 40.0 | 2.92 | 2.83 | 0.64 | 7.31 |
| 1000 | 200.0 | 6.34 | 6.32 | 0.64 | 3.17 |
| 5000 | 999.9 | 14.17 | 14.14 | 0.64 | 1.42 |
| 18000 | 3600.1 | 26.81 | 26.83 | 0.64 | 0.74 |

## Sensor parameters recovered from the frames

| Quantity | Simulated truth | Recovered from the frames | Relative error (%) |
| --- | --- | --- | --- |
| conversion gain (electrons per DN) | 5.000 | 5.010 | 0.2 |
| read noise (electrons) | 3.200 | 3.709 | 15.9 |

## A filter tuned at one exposure, applied across the range

| Mean signal (electrons) | Unfiltered RMSE (DN) | Fixed filter RMSE (DN, radius 6) | Variance stabilised RMSE (DN) | Change from fixed (%) |
| --- | --- | --- | --- | --- |
| 8 | 0.889 | 0.073 | 0.080 | +10.2 |
| 40 | 1.442 | 0.118 | 0.129 | +9.1 |
| 200 | 2.930 | 0.246 | 0.252 | +2.4 |
| 1000 | 6.348 | 0.487 | 0.490 | +0.5 |
| 5000 | 14.164 | 1.162 | 1.162 | -0.1 |
| 18000 | 27.021 | 2.258 | 2.259 | +0.1 |

## Denoiser cost

| Denoiser | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| fixed box filter | 5.12 | 0.258 | 5.22 | 7 |
| stabilise, filter, invert | 5.54 | 0.0609 | 5.68 | 7 |

Patch is 256 by 256 pixels, float64 throughout.

## Reading

Noise standard deviation grows by a factor of 30.2 from the darkest to the brightest patch, and the photon transfer curve recovered from the frames returns the simulated gain and read noise to within a few per cent, so the signal dependence is measurable rather than theoretical. A filter tuned at one exposure is the wrong filter elsewhere: against the variance stabilised denoiser it is worse at the extremes of the range, by up to 10 per cent in root mean square error. The claim under test fails, and the practical consequence is that a normalisation constant copied from one capture setting does not transfer to another.
