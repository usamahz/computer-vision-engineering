# 16. A corruption suite score measures the suite as much as the model

## Claim under test

A pipeline that scores well on a corruption benchmark is robust.

## Why it matters

Robustness is reported against fixed corruption suites, and a suite is a small arbitrary sample of the ways an image degrades. Tuning against it raises the score, and the thing being tuned is the fit between a pipeline and a particular corruption, which is not robustness. A suite average can also reward a change that made half the suite worse.

## Method

A two class task is built whose label depends on fine high frequency texture, at forty eight by forty eight, with four hundred tuning and four hundred test images. The pipeline is declared and has two knobs: a smoothing radius and a decision threshold on the ratio of detail energy to total energy. Three pipelines are produced by grid search: one tuned on clean data, which is the fair baseline because it is what a team ships before anybody mentions robustness, one tuned against additive noise, and one tuned against the mean accuracy over a suite of additive noise and contrast reduction. Each is scored on clean data and on four corruptions at three severities: additive noise, contrast reduction, compression and impulse dropout. Gains are reported against the clean tuned baseline, split into corruptions the pipeline was tuned against and corruptions held out from tuning. This measures the tuning transfer effect on a declared pipeline and does not reproduce any published robustness number.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned model; a declared two parameter pipeline, a smoothing radius and a threshold on a detail energy ratio, with the grid stated in the method |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; four hundred tuning and four hundred test images in full mode, disjoint draws, with corruption severities applied at evaluation time |
| Input resolution and preprocessing | forty eight by forty eight grey images; the smoothing radius is the preprocessing and is one of the two tuned knobs, which is why it is stated per pipeline in the results |
| Metric with full definition | top one accuracy over two classes, averaged over the three severities of each corruption, with clean accuracy reported separately |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | single scale, no test time augmentation, no detection and therefore no suppression settings; corruptions and severities named in the tables |
| Training data used | the tuning split, used only for the grid search; the corruptions used during tuning are named per pipeline and are the whole point of the comparison |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the pipeline tuned on clean data, scored on the identical test images and corruptions |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout, with compression applied through an eight bit encoder |
| Batch size | the whole test set per scoring call |
| Input resolution | forty eight by forty eight, four hundred images per batch in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | one warmup iteration discarded; medians over three to seven repeats as printed, with the interquartile range and the ninety fifth percentile |
| Preprocessing and postprocessing inside the timer | the scoring row has the corruption applied beforehand and the smoothing inside the timer; a second row times the compression corruption on its own, because applying a corruption suite is itself a measurable cost |

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

### Three pipelines, five conditions

| Pipeline | Chosen settings | clean accuracy (%) | additive noise accuracy (%) | contrast accuracy (%) | compression accuracy (%) | impulse dropout accuracy (%) | mean over the five (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tuned on clean data only | radius 2, threshold 0.0250 | 100.0 | 100.0 | 69.0 | 100.0 | 99.3 | 93.7 |
| tuned against additive noise alone | radius 0, threshold 0.0250 | 94.2 | 100.0 | 53.5 | 89.6 | 100.0 | 87.5 |
| tuned against a suite of noise and contrast | radius 2, threshold 0.0250 | 100.0 | 100.0 | 69.0 | 100.0 | 99.8 | 93.8 |

### How much of the tuning gain transfers

| Pipeline | Corruptions tuned against | Corruptions held out | Gain on tuned corruptions (percentage points) | Gain on held out corruptions (percentage points) | Share of the gain that transfers (%) |
| --- | --- | --- | --- | --- | --- |
| tuned against additive noise alone | additive noise | contrast, compression, impulse dropout | +0.0 | -8.4 | no gain to transfer |
| tuned against a suite of noise and contrast | additive noise, contrast | compression, impulse dropout | +0.0 | +0.2 | no gain to transfer |

### By severity, seen against held out

| Corruption | Severity | Tuned on clean data (%) | Tuned on noise (%) | Tuned on the suite (%) |
| --- | --- | --- | --- | --- |
| additive noise | 0.3 | 100.0 | 100.0 | 100.0 |
| additive noise | 0.6 | 100.0 | 100.0 | 100.0 |
| additive noise | 1 | 100.0 | 100.0 | 100.0 |
| impulse dropout | 0.3 | 100.0 | 100.0 | 100.0 |
| impulse dropout | 0.6 | 100.0 | 100.0 | 100.0 |
| impulse dropout | 1 | 98.8 | 100.0 | 98.8 |
| compression | 0.3 | 100.0 | 87.5 | 100.0 |
| compression | 0.6 | 100.0 | 86.8 | 100.0 |
| compression | 1 | 100.0 | 94.5 | 100.0 |

### Cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| score one pipeline on one batch | 22.9 | 0.941 | 23.5 | 7 |
| apply the compression corruption | 47.5 | 0 | 49 | 3 |

400 tuning and 400 test images at 48 by 48 pixels, 3 by 17 grid, severities [0.3, 0.6, 1.0].

## Analysis

The pipeline tuned on clean data is the most robust of the three, with a mean of 93.7 per cent across the five conditions against 87.5 and 93.8 for the two tuned against corruptions, and a tuned pipeline wins on the mean. Tuning against additive noise changed nothing on the corruption it was tuned against, because the clean settings already handled it, and still cost -8.4 points on the corruptions held out from tuning. The suite is the sharper case. Tuning against the mean of two corruptions gained on impulse dropout and lost on nothing, so it got worse on one of the two corruptions it was being tuned against, and the suite average rewarded that trade because the average cannot see it. On the held out corruptions it is +0.2 points down. The mechanism is visible in the chosen settings rather than hidden in a weight matrix, which is the reason to run it this way: the setting that helps when a corruption raises high frequency energy is exactly wrong when a corruption removes it, and one threshold cannot do both. A score on a corruption suite is therefore a joint statement about the pipeline and the suite, and tuning against it moves the score without moving robustness. The claim under test fails. A robustness claim needs a corruption family held out from tuning, the per corruption numbers rather than the suite mean, and a statement of which corruptions were held out.

## What this machine cannot measure

- Any published robustness number, which needs a trained network and the official corruption implementations. The mechanism transfers, the values do not.
- Adversarial robustness, which is a different threat model and is not touched here.
- Corruption severity calibration against the published suites, whose severities are defined by their own reference implementation.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. All accuracies are deterministic. To apply the method to a real model, keep the structure, replace the pipeline with the model and its preprocessing, and hold out a corruption family from tuning.
