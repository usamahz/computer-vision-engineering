# 06. Padding and stride decide where a feature actually is

## Claim under test

The output tensor has the size the arithmetic predicts, so the geometry is handled.

## Why it matters

Detection heads, segmentation masks and feature pyramids all map coordinates between resolutions. If the mapping assumes that an input coordinate divided by the total stride gives the output coordinate, it is wrong by an amount set by the padding convention and the kernel parity, and every tensor shape still matches.

## Method

A single pixel impulse is pushed through four convolution stages at stride two, with kernels of three, two and five taps, under symmetric padding, trailing padding and no padding, and with the impulse at an even and at an odd coordinate. The response centre of mass is compared against two predictions: the naive mapping, an input coordinate divided by the total stride, and a padding aware mapping derived from the window position. Output sizes are checked against the formula at every stage. The receptive field is measured by perturbation, by changing one input pixel and counting the output positions that move. The timer covers one convolution.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; uniform averaging kernels, so the response centre of mass is exactly the quantity under test |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; one impulse image per configuration and one random image for the perturbation test |
| Input resolution and preprocessing | 256 by 256 float64 in full mode, 128 by 128 in quick mode; no preprocessing |
| Metric with full definition | centre of mass of the response in output pixel units; residual against the padding aware prediction; offset from the naive mapping multiplied by the total stride to express it in input pixels |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no augmentation, no detection and therefore no suppression settings |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the arithmetic itself, in two forms: the output size formula and the padding aware coordinate mapping |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | one image per call |
| Input resolution | 256 by 256 in full mode, kernel three by three |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the convolution is a sum of strided slices, not a library call |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | padding is inside the timed function; image generation is outside |

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

### Output size against feature alignment

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

### Receptive field, measured by perturbation

| Kernel | Output positions changed by one input pixel | Square root of that count (output pixels across) | Analytic receptive field (input pixels) | Receptive field in output pixel units |
| --- | --- | --- | --- | --- |
| 3 | 1 | 1.0 | 31 | 1.9 |
| 5 | 9 | 3.0 | 61 | 3.8 |

### Convolution cost

| Configuration | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| stride one, symmetric padding | 1.3 | 1.56 | 3.25 | 7 |
| stride two, symmetric padding | 0.187 | 0.0189 | 0.226 | 7 |
| stride one, no padding | 1.75 | 0.0505 | 3.06 | 7 |

Input is 256 by 256, kernel three by three, float64 throughout.

## Analysis

Output sizes matched the arithmetic in every configuration, and the feature still moved. For odd kernels the padding aware mapping predicts the measured response centre to within 0.138 output pixels, so that geometry is exactly calculable. It is not the mapping a reader assumes: dividing an input coordinate by the total stride is wrong by up to 30.00 input pixels after four strided stages, decided only by the padding convention and the kernel size, and only 4 of the 18 configurations leave it intact. The even kernel is worse than wrong, it is ambiguous: it has no centre tap, so the window centre convention and the position the response actually lands in disagree by 0.469 output pixels, which is the half pixel every resize and alignment argument in this field is about. Parity of the feature's own coordinate changes the result in 9 of the 9 configuration pairs, so the error is not even a constant within one network. The measured receptive field agrees with the analytic one, so this is alignment rather than extent. The claim under test fails: matching tensor shapes say nothing about whether two feature maps refer to the same place in the image.

## What this machine cannot measure

- What any particular framework does by default. The three padding conventions here are implemented explicitly so the effect is visible; which one a given library applies is a question for that library's documentation.
- Transposed convolution and interpolation alignment, which have the same class of bug and are not covered.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. Every geometry number is deterministic. The useful variation on another machine is not the timing but swapping conv2d() for the target framework's convolution and checking that the measured centres still match the padding aware prediction.
