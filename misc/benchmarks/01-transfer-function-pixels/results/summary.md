# 01. Pixel values are not the measurement

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Two encodings of one scene, by brightness band

| Scene radiance band | Pixels | Mean code difference (levels) | Max (levels) | Over one level (%) |
| --- | --- | --- | --- | --- |
| 0 to 0.01 | 241726 | 7.45 | 9 | 100.0 |
| 0.01 to 0.05 | 251748 | 3.77 | 6 | 100.0 |
| 0.05 to 0.18 | 391992 | 0.79 | 3 | 19.7 |
| 0.18 to 0.5 | 153112 | 1.18 | 2 | 22.1 |
| 0.5 to 1.01 | 9998 | 0.71 | 2 | 19.3 |

## Halving the frame in the encoded domain against linear light

| Region | Pixels | Mean signed error (linear light) | RMSE (linear light) | Mean relative error (%) |
| --- | --- | --- | --- | --- |
| whole frame | 262144 | -0.00012 | 0.00337 | -0.07 |
| radiance below one twentieth | 123327 | -0.00001 | 0.00019 | -0.06 |
| radiance above mid grey | 41008 | -0.00064 | 0.00848 | -0.18 |

## A threshold means different things in different domains

| Decision rule | Pixels selected | Disagreement with radiance rule (%) |
| --- | --- | --- |
| radiance at or above mid grey | 163110 | 0.0 |
| standard encoded value at or above mid grey | 688570 | 50.1 |
| power law encoded value at or above mid grey | 712542 | 52.4 |

## Conversion cost

| Conversion | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| piecewise encode | 10 | 0.436 | 10.2 | 9 |
| power law encode | 4.74 | 1.06 | 6.15 | 9 |
| piecewise decode | 9.01 | 0.435 | 9.45 | 9 |

Frame is 1024 by 1024 pixels, 1.049 megapixels, float64 throughout.

## Reading

The two encodings of one identical scene differ by up to 9 code levels, so an eight bit array is a statement about a transfer function and not about the scene. Halving the frame by averaging encoded values instead of radiance biases the result by -0.07 per cent in linear light, and the bias is systematic rather than random, which is why a mismatched preprocessing step shifts a trained model's inputs in one direction. A mid grey threshold applied to encoded values disagrees with the same threshold on radiance for 50.1 per cent of pixels. The claim under test fails on all three counts.
