# 15. One speedup figure for a model is not a fact about a layer

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Accuracy of the integer product, by shape and scale granularity

| Layer shape | Dimensions, rows by inputs by outputs | Per tensor scale, signal to quantisation noise (dB) | Per channel scale, signal to quantisation noise (dB) | Per tensor worst absolute error | Per channel worst absolute error |
| --- | --- | --- | --- | --- | --- |
| pointwise convolution, small channels | 3136 by 64 by 64 | 30.2 | 40.9 | 0.1419 | 0.1419 |
| feature mixing, wide | 1024 by 256 by 256 | 25.6 | 36.7 | 0.4115 | 0.3694 |
| tall activation, narrow channels | 4096 by 32 by 128 | 26.8 | 37.6 | 0.1267 | 0.1389 |
| classifier head | 128 by 2048 by 1000 | 26.0 | 36.6 | 1.0865 | 1.1419 |

## Latency, with the timer boundary stated

| Layer shape | Float median (ms) | Integer core median (ms) | Integer with quantisation inside the timer, median (ms) | Speedup, integer core against float | Speedup, integer with quantisation against float | Integer core p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| pointwise convolution, small channels | 0.193 | 7.02 | 8.02 | 0.03 | 0.02 | 10.2 |
| feature mixing, wide | 0.917 | 71.3 | 71.9 | 0.01 | 0.01 | 76.5 |
| tall activation, narrow channels | 0.336 | 11.8 | 12.1 | 0.03 | 0.03 | 13.4 |
| classifier head | 4.22 | 238 | 302 | 0.02 | 0.01 | 493 |

## Weight storage

| Layer shape | Float weights (KiB, computed) | Integer weights plus per channel scales (KiB, computed) | Ratio |
| --- | --- | --- | --- |
| pointwise convolution, small channels | 16.0 | 4.2 | 3.76 |
| feature mixing, wide | 256.0 | 65.0 | 3.94 |
| tall activation, narrow channels | 16.0 | 4.5 | 3.56 |
| classifier head | 8000.0 | 2003.9 | 3.99 |

## Reading

The two halves of the claim come apart, and neither is a single number. On accuracy, moving from a per tensor scale to a per channel scale buys between 10.6 and 11.1 decibels of signal to quantisation noise depending on the shape, at no cost in arithmetic and almost none in storage, because a few outlier output channels otherwise set the scale for every channel. The spread across shapes is the point: the same change is worth different amounts in different layers of one network. On latency the result here is blunt. The integer core runs at 0.01 to 0.03 times the speed of the float product, so it is slower at every shape measured, and with the quantise and requantise steps inside the timer it runs at 0.01 to 0.03 times. The reason is the lesson rather than a caveat: the float product dispatches to a tuned library kernel, while the integer product falls back to a generic path that widens everything to a thirty two bit accumulator first, so cheaper arithmetic does not imply a faster layer unless a kernel exists for it on the target. That is also why a vendor's integer speedup does not transfer to another runtime, and why the timer boundary matters: the quantise and requantise steps are real work that a published figure often leaves outside. Weight storage is the one part that behaves as advertised, and it is computed rather than measured. The claim under test fails: a model level speedup figure, quoted without the shape, the scale granularity, the kernel and the timer boundary, describes no layer in the model.
