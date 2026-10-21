# 12. Depth error grows with the square of distance

## Claim under test

A stereo system has a depth error, quotable as one number.

## Why it matters

Depth from disparity is a reciprocal relationship, so a constant disparity error becomes a depth error that grows with the square of distance. A single average error, quoted over whatever scene the test set happened to contain, hides the range where the system actually fails, which is usually the range a product cares about.

## Method

A rectified pair is built from a seeded texture at 180 by 384, in six horizontal bands, each band at one true distance. Band disparities carry a fixed sub pixel offset so that no band lands on a whole pixel, because integer disparities would confound alignment luck with distance. The right image is sampled from the left with linear interpolation. Disparity is estimated by a sum of absolute differences search over a seven by seven window with a parabolic subpixel refinement, and converted to depth at a focal length of seven hundred pixels and a baseline of twelve centimetres. Median disparity error and median depth error are reported per band, beside the depth error the square law predicts from that band's own disparity error. A second table isolates the law by propagating one fixed disparity error, the frame median, through the same geometry, and is labelled as computed rather than measured. The timer covers the cost volume, the argmin and the refinement.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; block matching with a seven by seven window and parabolic subpixel refinement over a disparity range of zero to forty eight |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; one synthetic rectified pair with six distance bands, no split |
| Input resolution and preprocessing | 180 by 384 float64 in full mode, 60 by 192 in quick mode; no rectification needed because the pair is generated rectified, and no normalisation |
| Metric with full definition | median absolute disparity error in pixels, and median absolute depth error in metres, per distance band and over the whole frame, with the ninety fifth percentile also reported for the frame |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no augmentation, no detection and therefore no suppression settings; only pixels at least a window and a disparity range from the frame edge are scored |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the depth error the square law predicts from the measured disparity error, and the single frame average |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | one stereo pair per call |
| Input resolution | 180 by 384 in full mode, window seven by seven, disparity range zero to forty eight |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the cost volume is built with shifted slices and box sums |
| Warmup and statistic reported | one warmup iteration discarded; median of seven in full mode with the interquartile range and the ninety fifth percentile |
| Preprocessing and postprocessing inside the timer | the cost volume, the argmin and the subpixel refinement are inside; image generation is outside |

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

### Depth error by true distance, measured

| True distance (m) | True disparity (px) | Pixels measured | Median disparity error (px) | Median depth error (m) | Depth error the square law predicts from that disparity error (m) | Relative depth error (%) |
| --- | --- | --- | --- | --- | --- | --- |
| 1.99 | 42.27 | 9660 | 0.147 | 0.007 | 0.007 | 0.35 |
| 4.06 | 20.69 | 9660 | 0.150 | 0.029 | 0.029 | 0.72 |
| 7.86 | 10.69 | 9660 | 0.150 | 0.109 | 0.110 | 1.38 |
| 16.73 | 5.02 | 9660 | 0.018 | 0.060 | 0.060 | 0.36 |
| 30.05 | 2.79 | 9660 | 0.127 | 1.304 | 1.362 | 4.34 |
| 82.15 | 1.02 | 9660 | 0.018 | 1.482 | 1.460 | 1.80 |

### The law isolated, one disparity error propagated

| True distance (m) | Disparity error held fixed at the frame median (px, measured) | Implied depth error (m, computed) | Implied relative error (%, computed) |
| --- | --- | --- | --- |
| 1.99 | 0.124 | 0.006 | 0.29 |
| 4.06 | 0.124 | 0.024 | 0.60 |
| 7.86 | 0.124 | 0.091 | 1.16 |
| 16.73 | 0.124 | 0.414 | 2.47 |
| 30.05 | 0.124 | 1.335 | 4.44 |
| 82.15 | 0.124 | 9.977 | 12.14 |

### What the frame average hides

| Statistic over the whole frame | Value |
| --- | --- |
| mean absolute depth error (m) | 0.741 |
| median absolute depth error (m) | 0.093 |
| ninety fifth percentile absolute depth error (m) | 2.571 |
| median absolute depth error in the nearest band (m) | 0.007 |
| median absolute depth error in the farthest band (m) | 1.482 |
| fitted growth exponent from the measured medians | 1.46 |
| fitted growth exponent with the disparity error held fixed, computed | 2.00 |
| growth exponent the geometry predicts | 2.00 |

### Matching cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| block matching with subpixel refinement | 125 | 22.4 | 172 | 7 |

Pair is 180 by 384 pixels, window 7 by 7, disparity search zero to 48, focal length 700 pixels, baseline 0.12 metres.

## Analysis

The square law holds, and it holds in the conditional form that matters. Within each distance band the depth error predicted from that band's own measured disparity error agrees with the measured depth error to within 4 per cent, and propagating one fixed disparity error, the frame median of 0.124 pixels, through the same geometry gives a fitted exponent of 2.00 against the two the geometry predicts. Fitting the measured medians directly gives 1.46 rather than two, and the reason is worth stating rather than smoothing away: the measured disparity error is not constant across bands, because whether a band's true disparity happens to sit near a whole pixel changes how well a parabolic refinement recovers it. Either way the consequence is the same. Median depth error grows from 0.007 metres at 1.99 metres to 1.482 metres at 82.15 metres, a factor of 212 across a distance factor of 41, and relative error grows with it. The single frame mean of 0.741 metres is therefore a property of how far away this particular scene happened to be and of which band held the most pixels, not a property of the stereo system. The claim under test fails: a depth error has to be quoted per distance or with the working range it applies to.

## What this machine cannot measure

- Any real camera rig's error. Focal length, baseline and texture here are chosen values, and a real characterisation needs the rig and a measured target.
- Occlusion, repeated texture and untextured regions, which are the other three reasons stereo fails and which this synthetic pair avoids on purpose so the distance effect is isolated.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. The disparity and depth errors are deterministic. To apply this to a real rig, set FOCAL_PX and BASELINE_M to the rig's calibration and read the propagation table, which needs only the disparity error the rig achieves.
