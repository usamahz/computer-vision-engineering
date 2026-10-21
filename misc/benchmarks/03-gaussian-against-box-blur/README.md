# 03. A box blur is not a cheap Gaussian

## Claim under test

A box blur and a Gaussian of equal support are interchangeable, so the cheaper one is free.

## Why it matters

Preprocessing, pyramid construction and anti aliasing before a resize all involve a choice of low pass filter. A box filter has zeros in its frequency response and inverts contrast beyond them, so a feature that depends on the sign of a gradient can flip. The cheap win that does exist is separability, which is a different property from the kernel shape.

## Method

A Gaussian kernel at sigma two is built with support out to three sigma, giving thirteen taps, and compared against a box of the same support and against a box whose second moment matches the Gaussian. Signed gain is measured on sinusoids at nine spatial frequencies by projecting the filtered row onto the input row, so a contrast inversion appears as a negative gain. An ideal step edge gives the ten to ninety per cent rise distance, the overshoot and the largest second difference. Cost is timed three ways on a 1024 by 1024 random image: the separable Gaussian as two passes, the identical kernel applied as a full two dimensional convolution, and the separable box. The timer covers the convolution only.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; a Gaussian kernel at sigma two with thirteen taps, a box of thirteen taps, and a variance matched box |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; sinusoids at nine frequencies and one ideal step edge |
| Input resolution and preprocessing | 1024 by 1024 float64 in full mode, 256 by 256 in quick mode; no preprocessing |
| Metric with full definition | signed gain, the projection of the filtered signal onto the zero mean input divided by the input energy, so unity is transparent and a negative value is a contrast inversion; rise distance in pixels; largest absolute second difference |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no augmentation, no detection and therefore no suppression settings |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the Gaussian filtered profile, and the unfiltered sinusoid |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | one image per call |
| Input resolution | 1024 by 1024 in full mode, kernel support thirteen taps |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the convolution is a sum of shifted slices, not a library call |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | no; padding is inside the timed function because it is part of the convolution, while image generation is outside |

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

### Frequency response, measured on sinusoids

| Frequency (cycles per pixel) | Period (pixels) | Gaussian gain (sigma 2) | Box gain (width 13) | Variance matched box gain (width 7) |
| --- | --- | --- | --- | --- |
| 0.0200 | 50.0 | +0.9693 | +0.8932 | +0.9687 |
| 0.0500 | 20.0 | +0.8232 | +0.4411 | +0.8145 |
| 0.0769 | 13.0 | +0.6298 | +0.0044 | +0.5942 |
| 0.1000 | 10.0 | +0.4555 | -0.1989 | +0.3749 |
| 0.1538 | 6.5 | +0.1549 | -0.0001 | -0.0718 |
| 0.2000 | 5.0 | +0.0453 | +0.1250 | -0.2284 |
| 0.2500 | 4.0 | +0.0080 | -0.0757 | -0.1417 |
| 0.3000 | 3.3 | +0.0011 | -0.0285 | +0.0550 |
| 0.4000 | 2.5 | +0.0004 | -0.0465 | +0.0887 |

### Edge profile on an ideal step

| Filter | Ten to ninety per cent rise (pixels) | Overshoot (fraction of step) | Largest second difference (per pixel) | RMSE against the Gaussian profile |
| --- | --- | --- | --- | --- |
| Gaussian | 6 | +0.00e+00 | 0.0563 | 0.0000 |
| box | 10 | -3.33e-16 | 0.0769 | 0.0162 |
| variance matched box | 6 | -3.33e-16 | 0.1429 | 0.0039 |

### Cost

| Implementation | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| separable Gaussian, two passes | 43 | 2.72 | 45.7 | 7 |
| same kernel as a full two dimensional convolution | 253 | 15.4 | 261 | 7 |
| separable box | 64.7 | 11.1 | 79.5 | 7 |

Image is 1024 by 1024 pixels, kernel support 13 taps, float64 throughout.

## Analysis

The two filters are not the same operator. Across the frequency sweep their signed gains differ by up to 0.65, and the box filter inverts contrast at 5 of the 9 tested frequencies, where the Gaussian stays positive everywhere. Contrast inversion is not a small error: a feature that depends on the sign of a gradient flips. On an ideal step the box filter produces a profile whose second difference is larger, which is the visible blocking a reader will recognise. Separability is where the cheap win actually is: the identical Gaussian kernel applied as a full two dimensional convolution costs 5.9 times the separable form. The claim under test fails, and the correct cheap filter is a separable Gaussian rather than a box.

## What this machine cannot measure

- A comparison against a tuned library convolution. Both implementations here are written in numpy, so the ratio between them is meaningful and the absolute figures are not a statement about a production filter.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. Gains, rise distances and profile errors are deterministic. The separability ratio in the cost table will move with the machine's memory bandwidth, and that ratio is the only part worth re-reading on new hardware.
