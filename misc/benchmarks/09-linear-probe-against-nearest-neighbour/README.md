# 09. The probe is a choice of answer, not a measurement of the representation

## Claim under test

A linear probe accuracy ranks representations, so a higher probe number means a better representation.

## Why it matters

Self supervised pretraining is compared almost entirely through probes, and a probe is a model with its own assumptions. Two probes can rank the same pair of representations in opposite orders, and the protocol details that decide the answer, the distance, the regularisation and the feature preprocessing, are usually not reported.

## Method

Three seeded representations of the same labelled data are built in thirty two dimensions with eight classes. The first hides a small discriminative signal under high variance nuisance directions. The second places several tight clusters per class around a circle inside a two dimensional subspace, so the clusters of one class are interleaved with those of the others. The third arranges classes as concentric shells. Each is scored by a ridge linear probe solved in closed form on one hot targets, by one nearest neighbour under Euclidean distance, by one nearest neighbour under cosine distance, and by the first two again after standardising features using training statistics. The timer covers solving and scoring, with feature generation outside.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no pretrained checkpoint; a ridge linear probe with regularisation one hundredth and a one nearest neighbour probe, both specified in full in the method |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; 2000 items in full mode across eight classes, sixty per cent training and forty per cent test, one split |
| Input resolution and preprocessing | thirty two dimensional features; the standardised rows subtract the training mean and divide by the training standard deviation, and the unstandardised rows do nothing |
| Metric with full definition | top one accuracy on the held out split |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | one evaluation pass, no augmentation at probe time, no detection and therefore no suppression settings |
| Training data used | the training split of the same synthetic data, identical for both probes |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the other probe on the same representation, and the chance rate of one eighth |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | the whole split per probe call |
| Input resolution | thirty two dimensional features, 2000 items in full mode |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags |
| Warmup and statistic reported | warmup iterations are discarded and counted by the shared harness; the median of the timed repeats is the headline, reported beside the interquartile range and the ninety fifth percentile; seven repeats in full mode |
| Preprocessing and postprocessing inside the timer | feature extraction is outside the timer for both probes, which is how probe cost is usually quoted and is stated here because it hides the dominant cost of a real probe |

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

### Three representations, five probes

| Representation | Linear probe (%) | Nearest neighbour, euclidean (%) | Nearest neighbour, cosine (%) | Linear probe after standardising (%) | Nearest neighbour after standardising (%) |
| --- | --- | --- | --- | --- | --- |
| nuisance dominated | 86.1 | 11.9 | 12.9 | 86.1 | 73.6 |
| multi modal clusters | 12.5 | 99.9 | 99.9 | 12.5 | 97.1 |
| concentric shells | 16.0 | 13.8 | 12.5 | 16.0 | 13.5 |

### Which representation each probe prefers

| Probe | Ranking, best first | Top accuracy (%) | Spread across representations (percentage points) |
| --- | --- | --- | --- |
| linear | nuisance dominated then concentric shells then multi modal clusters | 86.1 | +73.6 |
| nearest neighbour, euclidean | multi modal clusters then concentric shells then nuisance dominated | 99.9 | +88.0 |
| nearest neighbour, cosine | multi modal clusters then nuisance dominated then concentric shells | 99.9 | +87.4 |
| nearest neighbour, standardised | multi modal clusters then nuisance dominated then concentric shells | 97.1 | +83.6 |

### Probe cost

| Probe | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| ridge linear probe | 0.273 | 0.0222 | 0.316 | 7 |
| nearest neighbour probe | 5.65 | 0.0887 | 5.93 | 7 |

2000 items, 32 dimensional features, 8 classes, 1200 training and 800 test items.

## Analysis

The two probes rank the same three representations differently. The linear probe puts nuisance dominated first, the nearest neighbour probe puts multi modal clusters first, and the ranking is therefore inverted between them. Neither number measures representation quality in general, because each probe is a statement about which structure counts. A linear map suppresses the high variance nuisance directions that a distance cannot, which is why the nuisance dominated representation scores 86.1 per cent under the linear probe and 11.9 per cent under the distance, close to the chance rate of 12.5 per cent. A distance reads several tight clusters per class that no single hyperplane isolates. The concentric shells are the case worth remembering: they defeat both probes, scoring 16.0 and 13.8 per cent, even though the class is recoverable from one scalar, the radius, because in this many dimensions every test point's nearest neighbour sits on the innermost shell. Protocol details that papers rarely state move the answer as much as the representation does: standardising features before probing lifts the nuisance case from 11.9 to 73.6 per cent. 2 of the three representations win under at least one probe. The claim under test fails: a probe number without its probe, its distance, its regularisation and its feature preprocessing ranks nothing.

## What this machine cannot measure

- Any statement about a real pretrained representation. These are synthetic structures chosen to isolate the mechanism, and the ranking of real checkpoints is an empirical question about those checkpoints.
- Fine tuning, which is the third probe in the literature and needs a trained network.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. All accuracies are deterministic. To apply it to real checkpoints, replace the three builders with cached features from those checkpoints and keep both probes and the standardisation rows.
