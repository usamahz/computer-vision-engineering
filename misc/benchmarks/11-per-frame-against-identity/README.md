# 11. Per frame accuracy can rise while tracking quality falls

## Claim under test

A tracker with better per frame detection is a better tracker.

## Why it matters

A tracker exists to answer whether this object is the same object as before. Per frame precision and recall cannot see that question, so a tracker can improve on them while becoming useless for counting, re identification or any behaviour that spans frames.

## Method

Six ground truth trajectories are simulated over two hundred and forty frames, crossing each other, which is where identity is tested. A tracker is simulated with two knobs: a detection rate and a per frame identity failure rate, swept together so detection quality rises while identity quality falls. The same greedy overlap matching at one half is then scored two ways: per frame precision, recall and their harmonic mean, which ignore identity, and identity switches, multiple object tracking accuracy and an identity harmonic mean computed from a greedy one to one assignment between ground truth and track identities. The greedy assignment can only understate the identity score relative to the optimal assignment the standard metric uses, which is stated rather than smoothed over. The timer covers matching and both metric families.

## Evidence fields

Accuracy style result, all eight fields:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | no learned tracker; a simulated association with a detection rate and an identity failure rate as its two parameters |
| Dataset, split and version | synthetic data generated in process from seed 20261018 with numpy default_rng; no external dataset; one sequence of two hundred and forty frames with six objects in full mode |
| Input resolution and preprocessing | boxes of forty eight by forty eight pixels in a 600 by 400 frame; no images |
| Metric with full definition | per frame precision and recall at overlap one half with their harmonic mean; identity switches counted when a ground truth object's matched track identity changes; multiple object tracking accuracy as one minus the sum of misses, false positives and switches over ground truth count; an identity harmonic mean from a greedy one to one identity assignment |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | greedy per frame matching at overlap one half, no augmentation, no suppression because detections are simulated rather than decoded |
| Training data used | nothing is trained, so this row is a statement about the generator rather than a training set |
| Hardware | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Baseline compared against | the other end of the sweep, which stands in for a tracker that detects less and keeps identity |

Speed result, all seven fields:

| Field | Value |
| --- | --- |
| Hardware and count | one Intel Xeon Processor at 2.10 GHz, four virtual cores, hypervisor guest, 15.7 GiB memory, no GPU and no neural accelerator; one thread, with OMP_NUM_THREADS and OPENBLAS_NUM_THREADS set to one |
| Precision | float64 throughout |
| Batch size | one sequence per scoring call |
| Input resolution | not applicable to a scoring benchmark; the sequence is two hundred and forty frames with six objects |
| Framework and version, compile flags | numpy 2.5.3 on CPython 3.13.16, linked against scipy-openblas 0.3.34; Pillow 12.3.0 where images are encoded or resampled; no compilation step, so no compile flags; the matcher is a Python loop over frames and objects |
| Warmup and statistic reported | one warmup iteration discarded; median of seven in full mode with the interquartile range and the ninety fifth percentile |
| Preprocessing and postprocessing inside the timer | matching and both metric families are inside; trajectory and detection simulation are outside |

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

### Detection quality up, identity quality down

| Detection rate (%) | Identity failure rate per frame (%) | Per frame precision (%) | Per frame recall (%) | Per frame harmonic mean | Identity switches | Distinct identities emitted | Multiple object tracking accuracy | Identity harmonic mean, greedy assignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 80 | 0 | 100.0 | 81.0 | 0.895 | 12 | 6 | 0.802 | 0.890 |
| 86 | 2 | 100.0 | 86.0 | 0.925 | 31 | 35 | 0.838 | 0.355 |
| 92 | 6 | 100.0 | 92.0 | 0.958 | 82 | 84 | 0.863 | 0.241 |
| 96 | 12 | 100.0 | 96.7 | 0.983 | 177 | 183 | 0.844 | 0.126 |
| 99 | 20 | 100.0 | 98.6 | 0.993 | 288 | 290 | 0.786 | 0.079 |

### The two ends of the sweep read as two trackers

| Tracker | Per frame harmonic mean | Identity harmonic mean | Identity switches | Preferred by per frame | Preferred by identity |
| --- | --- | --- | --- | --- | --- |
| detects more, re-identifies poorly | 0.993 | 0.079 | 288 | yes | no |
| detects less, keeps identity | 0.895 | 0.890 | 12 | no | yes |

### Scoring cost

| Operation | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| score one sequence | 19.1 | 1.16 | 22.3 | 7 |

Sequence holds 240 frames and 6 objects, 1440 ground truth boxes, overlap threshold 0.5.

## Analysis

Across the sweep the per frame harmonic mean rises from 0.895 to 0.993 while the identity harmonic mean falls from 0.890 to 0.079, and the number of distinct identities emitted grows from 6 to 290 for 6 real objects. The two families of measure therefore disagree about which tracker is better. Multiple object tracking accuracy sits between them, because it charges for switches but is dominated by the detection terms, which is exactly why it can look healthy while a product that needs a stable identity is unusable. A per frame metric cannot stand in for tracking quality: it is blind to the only question a tracker exists to answer, which is whether this object is the same object as before.

## What this machine cannot measure

- The optimal identity assignment used by the published metric, which needs a bipartite matching this benchmark approximates greedily.
- Any real tracker's numbers, and anything about detector quality on real video, since detections here are simulated.
- Any GPU, Core ML, neural engine or other accelerator number. The machine has none, and no figure from other hardware is reproduced here.
- Any figure from a vendor runtime with a fused or hand written kernel. The only kernels available here are the ones numpy and Pillow ship.
- Frequency pinned timing. This is a shared virtual machine, so tails are fatter than on a laptop, which is why a dispersion measure travels with every median.

## Reproduce on another machine

Run ./run.sh and replace the Environment section with the banner from results/raw.txt. All metric values are deterministic. To score a real tracker, replace simulate_tracker() with its output in the same format and keep both metric families side by side, which is the whole point.
