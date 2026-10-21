# 06. Padding and stride decide where a feature actually is

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Output size against feature alignment

| Kernel | Padding | Impulse coordinate | Final output size | Size matches the formula | Measured centre (output pixels) | Centre the padding aware mapping predicts | Residual (output pixels) | Offset from the naive mapping, referred to the input (input pixels) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | symmetric | even | 16 | yes | 8.000 | 8.000 | +0.000 | +0.00 |
| 3 | symmetric | odd | 16 | yes | 8.200 | 8.062 | +0.138 | +0.00 |
| 3 | trailing | even | 16 | yes | 7.200 | 7.062 | +0.138 | -15.00 |
| 3 | trailing | odd | 16 | yes | 7.250 | 7.125 | +0.125 | -15.00 |
| 3 | valid | even | 15 | yes | 7.200 | 7.062 | +0.138 | -15.00 |
| 3 | valid | odd | 15 | yes | 7.250 | 7.125 | +0.125 | -15.00 |
| 2 | symmetric | even | 16 | yes | 8.000 | 7.531 | +0.469 | -7.50 |
| 2 | symmetric | odd | 16 | yes | 8.000 | 7.594 | +0.406 | -7.50 |
| 2 | trailing | even | 16 | yes | 8.000 | 7.531 | +0.469 | -7.50 |
| 2 | trailing | odd | 16 | yes | 8.000 | 7.594 | +0.406 | -7.50 |
| 2 | valid | even | 16 | yes | 8.000 | 7.531 | +0.469 | -7.50 |
| 2 | valid | odd | 16 | yes | 8.000 | 7.594 | +0.406 | -7.50 |
| 5 | symmetric | even | 16 | yes | 8.000 | 8.000 | +0.000 | +0.00 |
| 5 | symmetric | odd | 16 | yes | 8.034 | 8.062 | -0.028 | +0.00 |
| 5 | trailing | even | 16 | yes | 6.122 | 6.125 | -0.003 | -30.00 |
| 5 | trailing | odd | 16 | yes | 6.188 | 6.188 | +0.000 | -30.00 |
| 5 | valid | even | 13 | yes | 6.122 | 6.125 | -0.003 | -30.00 |
| 5 | valid | odd | 13 | yes | 6.188 | 6.188 | +0.000 | -30.00 |

## Receptive field, measured by perturbation

| Kernel | Output positions changed by one input pixel | Square root of that count (output pixels across) | Analytic receptive field (input pixels) | Receptive field in output pixel units |
| --- | --- | --- | --- | --- |
| 3 | 1 | 1.0 | 31 | 1.9 |
| 5 | 9 | 3.0 | 61 | 3.8 |

## Convolution cost

| Configuration | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| stride one, symmetric padding | 1.3 | 1.56 | 3.25 | 7 |
| stride two, symmetric padding | 0.187 | 0.0189 | 0.226 | 7 |
| stride one, no padding | 1.75 | 0.0505 | 3.06 | 7 |

Input is 256 by 256, kernel three by three, float64 throughout.

## Reading

Output sizes matched the arithmetic in every configuration, and the feature still moved. For odd kernels the padding aware mapping predicts the measured response centre to within 0.138 output pixels, so that geometry is exactly calculable. It is not the mapping a reader assumes: dividing an input coordinate by the total stride is wrong by up to 30.00 input pixels after four strided stages, decided only by the padding convention and the kernel size, and only 4 of the 18 configurations leave it intact. The even kernel is worse than wrong, it is ambiguous: it has no centre tap, so the window centre convention and the position the response actually lands in disagree by 0.469 output pixels, which is the half pixel every resize and alignment argument in this field is about. Parity of the feature's own coordinate changes the result in 9 of the 9 configuration pairs, so the error is not even a constant within one network. The measured receptive field agrees with the analytic one, so this is alignment rather than extent. The claim under test fails: matching tensor shapes say nothing about whether two feature maps refer to the same place in the image.
