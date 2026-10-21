# 09. The probe is a choice of answer, not a measurement of the representation

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Three representations, five probes

| Representation | Linear probe (%) | Nearest neighbour, euclidean (%) | Nearest neighbour, cosine (%) | Linear probe after standardising (%) | Nearest neighbour after standardising (%) |
| --- | --- | --- | --- | --- | --- |
| nuisance dominated | 86.1 | 11.9 | 12.9 | 86.1 | 73.6 |
| multi modal clusters | 12.5 | 99.9 | 99.9 | 12.5 | 97.1 |
| concentric shells | 16.0 | 13.8 | 12.5 | 16.0 | 13.5 |

## Which representation each probe prefers

| Probe | Ranking, best first | Top accuracy (%) | Spread across representations (percentage points) |
| --- | --- | --- | --- |
| linear | nuisance dominated then concentric shells then multi modal clusters | 86.1 | +73.6 |
| nearest neighbour, euclidean | multi modal clusters then concentric shells then nuisance dominated | 99.9 | +88.0 |
| nearest neighbour, cosine | multi modal clusters then nuisance dominated then concentric shells | 99.9 | +87.4 |
| nearest neighbour, standardised | multi modal clusters then nuisance dominated then concentric shells | 97.1 | +83.6 |

## Probe cost

| Probe | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| ridge linear probe | 0.273 | 0.0222 | 0.316 | 7 |
| nearest neighbour probe | 5.65 | 0.0887 | 5.93 | 7 |

2000 items, 32 dimensional features, 8 classes, 1200 training and 800 test items.

## Reading

The two probes rank the same three representations differently. The linear probe puts nuisance dominated first, the nearest neighbour probe puts multi modal clusters first, and the ranking is therefore inverted between them. Neither number measures representation quality in general, because each probe is a statement about which structure counts. A linear map suppresses the high variance nuisance directions that a distance cannot, which is why the nuisance dominated representation scores 86.1 per cent under the linear probe and 11.9 per cent under the distance, close to the chance rate of 12.5 per cent. A distance reads several tight clusters per class that no single hyperplane isolates. The concentric shells are the case worth remembering: they defeat both probes, scoring 16.0 and 13.8 per cent, even though the class is recoverable from one scalar, the radius, because in this many dimensions every test point's nearest neighbour sits on the innermost shell. Protocol details that papers rarely state move the answer as much as the representation does: standardising features before probing lifts the nuisance case from 11.9 to 73.6 per cent. 2 of the three representations win under at least one probe. The claim under test fails: a probe number without its probe, its distance, its regularisation and its feature preprocessing ranks nothing.
