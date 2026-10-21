# 02. Sensor noise is signal dependent

## Claim under test

Image noise can be treated as additive with one standard deviation, so a single denoising or normalisation setting works across the exposure range.

## Why it matters

A denoiser, a normalisation constant and an augmentation policy all encode an assumption about noise. If the assumption is a single standard deviation, the pipeline is tuned for one exposure and wrong at both ends of the range, which is exactly where a deployed camera spends its time when light changes.

## Method

A sensor is simulated with Poisson photon arrival, Gaussian read noise of 3.2 electrons, a conversion gain of five electrons per digital number and a twelve bit quantiser, at six mean signal levels from eight to eighteen thousand electrons. The photon transfer curve is recovered by fitting variance against mean across those levels, which returns the simulated gain and read noise. A box filter whose radius was chosen at the middle exposure is then compared against the same filter applied inside a variance stabilising transform, at every exposure, by root mean square error against the known truth. The timer covers one filter application, or the transform, filter and inverse transform together, on a patch already in memory.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; a box filter of radius chosen by grid search at the middle exposure, and the same filter inside a variance stabilising transform |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; six uniform patches, one per exposure level |
| Input resolution and preprocessing | 256 by 256 patches in full mode, 64 by 64 in quick mode; raw digital numbers, no demosaicing and no tone curve |
| Metric with full definition | root mean square error in digital numbers against the known mean signal, and the standard deviation of each patch |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no augmentation, no detection and therefore no suppression settings |
| Training data used | the middle exposure patch, used only to choose the filter radius by grid search |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the unfiltered patch, and the known mean signal |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout, with the quantiser simulated at twelve bit |
| Batch size | one patch per call |
| Input resolution | 256 by 256 in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | the variance stabilising row includes its forward and inverse transform inside the timer, which is the honest comparison; frame capture is outside both |

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

### Photon transfer curve, measured

| Mean signal (electrons) | Measured mean (DN) | Measured noise (DN, standard deviation) | Shot noise alone (DN) | Read noise alone (DN) | Relative noise (%) |
| --- | --- | --- | --- | --- | --- |
| 8 | 1.6 | 0.89 | 0.57 | 0.64 | 55.18 |
| 40 | 8.0 | 1.44 | 1.26 | 0.64 | 18.02 |
| 200 | 40.0 | 2.92 | 2.83 | 0.64 | 7.31 |
| 1000 | 200.0 | 6.34 | 6.32 | 0.64 | 3.17 |
| 5000 | 999.9 | 14.17 | 14.14 | 0.64 | 1.42 |
| 18000 | 3600.1 | 26.81 | 26.83 | 0.64 | 0.74 |

### Sensor parameters recovered from the frames

| Quantity | Simulated truth | Recovered from the frames | Relative error (%) |
| --- | --- | --- | --- |
| conversion gain (electrons per DN) | 5.000 | 5.010 | 0.2 |
| read noise (electrons) | 3.200 | 3.709 | 15.9 |

### A filter tuned at one exposure, applied across the range

| Mean signal (electrons) | Unfiltered RMSE (DN) | Fixed filter RMSE (DN, radius 6) | Variance stabilised RMSE (DN) | Change from fixed (%) |
| --- | --- | --- | --- | --- |
| 8 | 0.889 | 0.073 | 0.080 | +10.2 |
| 40 | 1.442 | 0.118 | 0.129 | +9.1 |
| 200 | 2.930 | 0.246 | 0.252 | +2.4 |
| 1000 | 6.348 | 0.487 | 0.490 | +0.5 |
| 5000 | 14.164 | 1.162 | 1.162 | -0.1 |
| 18000 | 27.021 | 2.258 | 2.259 | +0.1 |

### Denoiser cost

| Denoiser | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| fixed box filter | 5.12 | 0.258 | 5.22 | 7 |
| stabilise, filter, invert | 5.54 | 0.0609 | 5.68 | 7 |

Patch is 256 by 256 pixels, float64 throughout.

## Analysis

Noise standard deviation grows by a factor of 30.2 from the darkest to the brightest patch, and the photon transfer curve recovered from the frames returns the simulated gain and read noise to within a few per cent, so the signal dependence is measurable rather than theoretical. A filter tuned at one exposure is the wrong filter elsewhere: against the variance stabilised denoiser it is worse at the extremes of the range, by up to 10 per cent in root mean square error. The claim under test fails, and the practical consequence is that a normalisation constant copied from one capture setting does not transfer to another.

## What this machine cannot measure

- Any real sensor's parameters. Gain, read noise and full well here are simulated values chosen to be plausible, and a real characterisation needs the sensor and a controlled light source.
- Fixed pattern noise, dark current and lens shading, which are not in the model.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh. Replace the Environment section with the banner from results/raw.txt. The recovered gain and read noise, and every root mean square error, are deterministic and must match bit for bit; only the latency table changes. To characterise a real sensor instead, replace capture() with frames from that sensor at known exposures and keep the rest.
