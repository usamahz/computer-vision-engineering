# 01. Pixel values are not the measurement

## Claim under test

An image is a clean array of numbers, so the array is the scene and the transfer function that produced it is a detail.

## Why it matters

Every trained model is a function of the array it was fed, not of the scene. A pipeline that encodes with one curve at training time and another at inference time has changed its input distribution without changing a line of model code, and the resize inside that pipeline compounds it. This is the first thing to understand because everything later in the path assumes the array means what the reader thinks it means.

## Method

One linear light radiance field is generated at 1024 by 1024 in float64, spanning about three decades, with piecewise constant reflectance patches and two specular highlights. It is encoded twice, once through the piecewise curve of the standard colour space and once through a plain power law, and both are quantised to eight bit. Three questions follow: the code level difference between the two arrays by radiance band; the error introduced by halving the frame with a two by two average in the encoded domain rather than in linear light, measured in linear light; and the disagreement between a mid grey threshold applied to radiance and the same threshold applied to encoded values. The timer covers one encode or decode of the whole frame and nothing else. Quick mode uses 256 by 256 and three repeats.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; the deterministic transfer functions of the standard colour space and a power law with exponent two point two |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; one frame, no split |
| Input resolution and preprocessing | 1024 by 1024 float64 radiance in full mode, 256 by 256 in quick mode; no preprocessing beyond the encoding under test |
| Metric with full definition | absolute difference in eight bit code levels between the two encodings; root mean square and mean signed error in linear light for the resize; disagreement rate for the threshold |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no augmentation, no detection and therefore no suppression settings |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the radiance field itself, which is known exactly because it was generated |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | one frame per call |
| Input resolution | 1024 by 1024 in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; nine repeats in full mode |
| Preprocessing and postprocessing inside the timer | no; the timer covers one encode or decode of an array already in memory, and frame generation and quantisation are outside it |

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

### Two encodings of one scene, by brightness band

| Scene radiance band | Pixels | Mean code difference (levels) | Max (levels) | Over one level (%) |
| --- | --- | --- | --- | --- |
| 0 to 0.01 | 241726 | 7.45 | 9 | 100.0 |
| 0.01 to 0.05 | 251748 | 3.77 | 6 | 100.0 |
| 0.05 to 0.18 | 391992 | 0.79 | 3 | 19.7 |
| 0.18 to 0.5 | 153112 | 1.18 | 2 | 22.1 |
| 0.5 to 1.01 | 9998 | 0.71 | 2 | 19.3 |

### Halving the frame in the encoded domain against linear light

| Region | Pixels | Mean signed error (linear light) | RMSE (linear light) | Mean relative error (%) |
| --- | --- | --- | --- | --- |
| whole frame | 262144 | -0.00012 | 0.00337 | -0.07 |
| radiance below one twentieth | 123327 | -0.00001 | 0.00019 | -0.06 |
| radiance above mid grey | 41008 | -0.00064 | 0.00848 | -0.18 |

### A threshold means different things in different domains

| Decision rule | Pixels selected | Disagreement with radiance rule (%) |
| --- | --- | --- |
| radiance at or above mid grey | 163110 | 0.0 |
| standard encoded value at or above mid grey | 688570 | 50.1 |
| power law encoded value at or above mid grey | 712542 | 52.4 |

### Conversion cost

| Conversion | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| piecewise encode | 10 | 0.436 | 10.2 | 9 |
| power law encode | 4.74 | 1.06 | 6.15 | 9 |
| piecewise decode | 9.01 | 0.435 | 9.45 | 9 |

Frame is 1024 by 1024 pixels, 1.049 megapixels, float64 throughout.

## Analysis

The two encodings of one identical scene differ by up to 9 code levels, so an eight bit array is a statement about a transfer function and not about the scene. Halving the frame by averaging encoded values instead of radiance biases the result by -0.07 per cent in linear light, and the bias is systematic rather than random, which is why a mismatched preprocessing step shifts a trained model's inputs in one direction. A mid grey threshold applied to encoded values disagrees with the same threshold on radiance for 50.1 per cent of pixels. The claim under test fails on all three counts.

## What this machine cannot measure

- Any claim about a camera's own pipeline. The curves here are the standard ones, not a sensor vendor's tone curve, which is proprietary and usually not a closed form.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh on the target machine. The machine banner in results/raw.txt is measured, so the Environment section below has to be replaced with whatever the banner prints there. The code level differences and the resize errors are deterministic and must come out bit identical on any machine; only the latency table changes.
