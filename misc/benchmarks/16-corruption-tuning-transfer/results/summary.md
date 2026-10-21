# 16. A corruption suite score measures the suite as much as the model

Measured on: Intel(R) Xeon(R) Processor @ 2.10GHz, 4 logical cores, 15.7 GiB, Linux-6.18.44-fc-v139-x86_64-with-glibc2.39, Python 3.13.16, numpy 2.5.3.
Determinism: seed=20261018, thread limits OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1.

## Three pipelines, five conditions

| Pipeline | Chosen settings | clean accuracy (%) | additive noise accuracy (%) | contrast accuracy (%) | compression accuracy (%) | impulse dropout accuracy (%) | mean over the five (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tuned on clean data only | radius 2, threshold 0.0250 | 100.0 | 100.0 | 69.0 | 100.0 | 99.3 | 93.7 |
| tuned against additive noise alone | radius 0, threshold 0.0250 | 94.2 | 100.0 | 53.5 | 89.6 | 100.0 | 87.5 |
| tuned against a suite of noise and contrast | radius 2, threshold 0.0250 | 100.0 | 100.0 | 69.0 | 100.0 | 99.8 | 93.8 |

## How much of the tuning gain transfers

| Pipeline | Corruptions tuned against | Corruptions held out | Gain on tuned corruptions (percentage points) | Gain on held out corruptions (percentage points) | Share of the gain that transfers (%) |
| --- | --- | --- | --- | --- | --- |
| tuned against additive noise alone | additive noise | contrast, compression, impulse dropout | +0.0 | -8.4 | no gain to transfer |
| tuned against a suite of noise and contrast | additive noise, contrast | compression, impulse dropout | +0.0 | +0.2 | no gain to transfer |

## By severity, seen against held out

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

## Cost

| Stage | Median latency (ms) | IQR (ms) | p95 (ms) | Repeats |
| --- | --- | --- | --- | --- |
| score one pipeline on one batch | 22.9 | 0.941 | 23.5 | 7 |
| apply the compression corruption | 47.5 | 0 | 49 | 3 |

400 tuning and 400 test images at 48 by 48 pixels, 3 by 17 grid, severities [0.3, 0.6, 1.0].

## Reading

The pipeline tuned on clean data is the most robust of the three, with a mean of 93.7 per cent across the five conditions against 87.5 and 93.8 for the two tuned against corruptions, and a tuned pipeline wins on the mean. Tuning against additive noise changed nothing on the corruption it was tuned against, because the clean settings already handled it, and still cost -8.4 points on the corruptions held out from tuning. The suite is the sharper case. Tuning against the mean of two corruptions gained on impulse dropout and lost on nothing, so it got worse on one of the two corruptions it was being tuned against, and the suite average rewarded that trade because the average cannot see it. On the held out corruptions it is +0.2 points down. The mechanism is visible in the chosen settings rather than hidden in a weight matrix, which is the reason to run it this way: the setting that helps when a corruption raises high frequency energy is exactly wrong when a corruption removes it, and one threshold cannot do both. A score on a corruption suite is therefore a joint statement about the pipeline and the suite, and tuning against it moves the score without moving robustness. The claim under test fails. A robustness claim needs a corruption family held out from tuning, the per corruption numbers rather than the suite mean, and a statement of which corruptions were held out.
