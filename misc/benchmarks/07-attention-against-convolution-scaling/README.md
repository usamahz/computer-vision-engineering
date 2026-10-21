# 07. Attention and convolution do not scale alike

## Claim under test

A comparison of attention against convolution at one input resolution tells a reader which operator is cheaper.

## Why it matters

Architecture comparisons in vision are usually run at one resolution and one token count. The two operators have different growth exponents, so the comparison inverts somewhere, and where it inverts is inside the range of resolutions products actually use.

## Method

A single head of scaled dot product attention and a fixed support convolution of nine taps along the token axis are timed over the same token grids, at token counts from sixty four to two thousand and forty eight with a channel dimension of sixty four. The growth exponent of each is fitted by least squares on the logarithms of the measured medians. The score matrix and the layer activations are also reported in mebibytes at single precision, which are computed quantities rather than measured ones and are labelled as such. The timer covers the scores, the softmax and the value product for attention, with the projections excluded, and the convolution alone for the convolution.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model and no accuracy claim; this benchmark measures cost only, and the accuracy row is retained to say so explicitly |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; random token matrices, no labels and no split |
| Input resolution and preprocessing | token counts of sixty four to two thousand and forty eight, equivalent to patch grids from eight by eight to forty five by forty five, channel dimension sixty four |
| Metric with full definition | median wall clock latency in milliseconds, and the fitted exponent of latency against token count |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | one operator call per timed iteration, no augmentation, no detection and therefore no suppression settings |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the convolution, at every token count, and the arithmetic exponents of two and one |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 for the operator inputs, with memory figures quoted at single precision because that is what an inference engine would store |
| Batch size | one sequence per call, one head |
| Input resolution | token counts sixty four to two thousand and forty eight, channel dimension sixty four, convolution support nine |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the attention matrix product dispatches to the linear algebra library, the convolution is a sum of shifted slices |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | query, key and value projections are outside the timer for attention, which flatters attention and is stated here so the comparison can be read correctly; nothing else is excluded |

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

### Token count sweep

| Tokens | Equivalent patch grid | Attention median (ms) | Convolution median (ms) | Attention over convolution | Score matrix at single precision (MiB, computed) | Layer activations at single precision (MiB, computed) | Matrix over activations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 64 | 8 by 8 | 0.0443 | 0.0575 | 0.8 | 0.02 | 0.016 | 1 |
| 128 | 11 by 11 | 0.255 | 0.07 | 3.6 | 0.06 | 0.031 | 2 |
| 256 | 16 by 16 | 1.13 | 0.0993 | 11.4 | 0.25 | 0.062 | 4 |
| 512 | 23 by 23 | 4.64 | 0.177 | 26.3 | 1.00 | 0.125 | 8 |
| 1024 | 32 by 32 | 16.7 | 0.401 | 41.8 | 4.00 | 0.250 | 16 |
| 2048 | 45 by 45 | 69.6 | 1.29 | 54.0 | 16.00 | 0.500 | 32 |

### Fitted growth exponents

| Operator | Fitted growth exponent in token count | Expected from the arithmetic |
| --- | --- | --- |
| single head attention | 2.09 | two |
| depthwise convolution, support 9 | 0.88 | one |

### What each doubling of the token count costs

| Token count doubling | Attention cost multiplier | Convolution cost multiplier |
| --- | --- | --- |
| 64 to 128 | 5.76 | 1.22 |
| 128 to 256 | 4.45 | 1.42 |
| 256 to 512 | 4.09 | 1.78 |
| 512 to 1024 | 3.61 | 2.27 |
| 1024 to 2048 | 4.15 | 3.21 |

## Analysis

Measured over a token sweep, attention grows with an exponent of 2.09 in the token count and the fixed support convolution with an exponent of 0.88, which is what the arithmetic says and what a single resolution comparison hides. The cost ratio between the two moves across the sweep rather than staying put, and attention first becomes the more expensive of the two at 128 tokens on this machine, so a comparison taken below that point and a comparison taken above it support opposite conclusions. The score matrix is the second half of the story: it is a computed quantity rather than a measured one, and at the top of the sweep it needs 32 times the memory of the activations it is computed from. The claim under test fails, and the honest form of such a comparison states the token count, the support, the head count and the resolution together.

## What this machine cannot measure

- Anything about a fused or memory aware attention kernel, which changes the constant and the memory traffic without changing the exponent. No such kernel is available here.
- Multiple heads, batching and the cost of normalisation layers, none of which are included.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. The exponents should reproduce on any machine; the crossover token count will not, because it depends on the relative quality of the two kernels, which is exactly why a single resolution comparison does not transfer.
