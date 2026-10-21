# 15. One speedup figure for a model is not a fact about a layer

## Claim under test

Integer quantisation makes a model smaller and faster, so a single speedup figure describes it.

## Why it matters

Quantisation is sold as one number for a whole model, and it is really a per layer trade between numerical error, scale granularity and whether a kernel exists for the integer path on the target. The sign of the latency change depends on all three, and the timer boundary decides whether the quantise and requantise steps are counted at all.

## Method

Four matrix shapes a vision network contains are generated with seeded activations and weights, with three per cent of output channels given nine times the magnitude of the rest, which is what real weights look like. Each is quantised symmetrically to eight bit with a per tensor scale and with a per channel scale, multiplied with a thirty two bit accumulator, and dequantised. Signal to quantisation noise ratio against the float result is reported for both granularities, with the worst absolute error beside it. Latency is timed three ways: the float product, the integer product alone, and the integer product with the quantise and requantise steps inside the timer. Weight storage is computed, not measured, and labelled as such.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned checkpoint; seeded matrices at four shapes, with the outlier channel fraction stated, standing in for layers rather than for a named model |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; one activation matrix and one weight matrix per shape |
| Input resolution and preprocessing | matrix shapes stated per row, from 3136 by 64 by 64 to 128 by 2048 by 1000; activations are non negative as they would be after a rectifier |
| Metric with full definition | signal to quantisation noise ratio in decibels, ten times the base ten logarithm of the ratio of the float output energy to the error energy, and the worst absolute elementwise error |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | one matrix product per configuration, no augmentation, no detection and therefore no suppression settings |
| Training data used | no training and no calibration set; scales are taken from the tensor itself, which is the best case for post training quantisation and is stated so the numbers are read as an upper bound |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the float32 product of the same matrices, elementwise |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float32 for the reference product, eight bit integers with a thirty two bit accumulator for the integer product |
| Batch size | the row count of each shape, stated per row, from one hundred and twenty eight to four thousand and ninety six |
| Input resolution | not an image benchmark; the layer shapes stand in for resolution and channel count and are stated per row |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the float product dispatches to the linear algebra library while the integer product takes a generic path, which is the finding rather than a caveat |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | reported both ways on purpose: one row times the integer product alone, and one times the quantise, product and cast back together, which is where a published figure usually draws its boundary |

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

### Accuracy of the integer product, by shape and scale granularity

| Layer shape | Dimensions, rows by inputs by outputs | Per tensor scale, signal to quantisation noise (dB) | Per channel scale, signal to quantisation noise (dB) | Per tensor worst absolute error | Per channel worst absolute error |
| --- | --- | --- | --- | --- | --- |
| pointwise convolution, small channels | 3136 by 64 by 64 | 30.2 | 40.9 | 0.1419 | 0.1419 |
| feature mixing, wide | 1024 by 256 by 256 | 25.6 | 36.7 | 0.4115 | 0.3694 |
| tall activation, narrow channels | 4096 by 32 by 128 | 26.8 | 37.6 | 0.1267 | 0.1389 |
| classifier head | 128 by 2048 by 1000 | 26.0 | 36.6 | 1.0865 | 1.1419 |

### Latency, with the timer boundary stated

| Layer shape | Float median (ms) | Integer core median (ms) | Integer with quantisation inside the timer, median (ms) | Speedup, integer core against float | Speedup, integer with quantisation against float | Integer core p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| pointwise convolution, small channels | 0.193 | 7.02 | 8.02 | 0.03 | 0.02 | 10.2 |
| feature mixing, wide | 0.917 | 71.3 | 71.9 | 0.01 | 0.01 | 76.5 |
| tall activation, narrow channels | 0.336 | 11.8 | 12.1 | 0.03 | 0.03 | 13.4 |
| classifier head | 4.22 | 238 | 302 | 0.02 | 0.01 | 493 |

### Weight storage

| Layer shape | Float weights (KiB, computed) | Integer weights plus per channel scales (KiB, computed) | Ratio |
| --- | --- | --- | --- |
| pointwise convolution, small channels | 16.0 | 4.2 | 3.76 |
| feature mixing, wide | 256.0 | 65.0 | 3.94 |
| tall activation, narrow channels | 16.0 | 4.5 | 3.56 |
| classifier head | 8000.0 | 2003.9 | 3.99 |

## Analysis

The two halves of the claim come apart, and neither is a single number. On accuracy, moving from a per tensor scale to a per channel scale buys between 10.6 and 11.1 decibels of signal to quantisation noise depending on the shape, at no cost in arithmetic and almost none in storage, because a few outlier output channels otherwise set the scale for every channel. The spread across shapes is the point: the same change is worth different amounts in different layers of one network. On latency the result here is blunt. The integer core runs at 0.01 to 0.03 times the speed of the float product, so it is slower at every shape measured, and with the quantise and requantise steps inside the timer it runs at 0.01 to 0.03 times. The reason is the lesson rather than a caveat: the float product dispatches to a tuned library kernel, while the integer product falls back to a generic path that widens everything to a thirty two bit accumulator first, so cheaper arithmetic does not imply a faster layer unless a kernel exists for it on the target. That is also why a vendor's integer speedup does not transfer to another runtime, and why the timer boundary matters: the quantise and requantise steps are real work that a published figure often leaves outside. Weight storage is the one part that behaves as advertised, and it is computed rather than measured. The claim under test fails: a model level speedup figure, quoted without the shape, the scale granularity, the kernel and the timer boundary, describes no layer in the model.

## What this machine cannot measure

- Any accelerator's integer throughput: no GPU, no neural engine, no vector unit integer kernel and no sparse matrix unit is available here, and no vendor figure is reproduced.
- Kernel selection inside a production runtime, which is the single largest factor in a real quantisation speedup.
- Accuracy on a real task, which needs a trained network and a dataset. Signal to quantisation noise ratio is a per layer proxy and is labelled as one.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. The noise ratios are deterministic. The latency table is the part that must be re-measured per target, and on a machine with an integer kernel the sign of the comparison may invert, which is exactly the claim being tested.
