# 11. Per frame accuracy can rise while tracking quality falls

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Detection quality up, identity quality down

| Detection rate (%) | Identity failure rate per frame (%) | Per frame precision (%) | Per frame recall (%) | Per frame harmonic mean | Identity switches | Distinct identities emitted | Multiple object tracking accuracy | Identity harmonic mean, greedy assignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 80 | 0 | 100.0 | 81.0 | 0.895 | 12 | 6 | 0.802 | 0.890 |
| 86 | 2 | 100.0 | 86.0 | 0.925 | 31 | 35 | 0.838 | 0.355 |
| 92 | 6 | 100.0 | 92.0 | 0.958 | 82 | 84 | 0.863 | 0.241 |
| 96 | 12 | 100.0 | 96.7 | 0.983 | 177 | 183 | 0.844 | 0.126 |
| 99 | 20 | 100.0 | 98.6 | 0.993 | 288 | 290 | 0.786 | 0.079 |

## The two ends of the sweep read as two trackers

| Tracker | Per frame harmonic mean | Identity harmonic mean | Identity switches | Preferred by per frame | Preferred by identity |
| --- | --- | --- | --- | --- | --- |
| detects more, re-identifies poorly | 0.993 | 0.079 | 288 | yes | no |
| detects less, keeps identity | 0.895 | 0.890 | 12 | no | yes |

## Scoring cost

| Operation | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| score one sequence | 19.1 | 1.16 | 22.3 | 7 |

Sequence holds 240 frames and 6 objects, 1440 ground truth boxes, overlap threshold 0.5.

## Reading

Across the sweep the per frame harmonic mean rises from 0.895 to 0.993 while the identity harmonic mean falls from 0.890 to 0.079, and the number of distinct identities emitted grows from 6 to 290 for 6 real objects. The two families of measure therefore disagree about which tracker is better. Multiple object tracking accuracy sits between them, because it charges for switches but is dominated by the detection terms, which is exactly why it can look healthy while a product that needs a stable identity is unusable. A per frame metric cannot stand in for tracking quality: it is blind to the only question a tracker exists to answer, which is whether this object is the same object as before.
