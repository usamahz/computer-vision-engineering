# Benchmark brief

`misc/benchmarks/` is the part of this repository that cannot be forked by copying a list. Every
section of the README gets at least one microbenchmark that measures one claim from that
section on a named machine, with the timer boundaries written down.

The standard is lower than a paper's and stricter than a blog post's: small, synthetic,
deterministic, reproducible from a clean checkout in minutes, and honest about what it did not
measure.

## 1. The machine

Everything in `results/` was produced on this machine and the READMEs name it exactly:

```
CPU       Intel(R) Xeon(R) Processor @ 2.10GHz, 4 vCPU, 1 thread per core, KVM guest
Memory    15.7 GiB
Kernel    Linux 6.18.44-fc-v139, x86_64
Python    3.13.16 (CPython)
numpy     2.5.3, linked against OpenBLAS 0.3.34 (DYNAMIC_ARCH)
Pillow    12.3.0
GPU       none
```

Rules about the machine, in order of importance:

1. **A benchmark reports the machine it ran on.** If a result was produced on an Apple M4 Pro
   it says Apple M4 Pro. If it was produced on this shared cloud virtual machine it says so,
   including that it is a virtual machine, because frequency is not pinned and the neighbours
   are invisible.
2. **Nobody else's hardware is quoted as if it were ours.** A published figure from a paper
   may appear in the Analysis section as a published figure, attributed, with its missing
   evidence fields named. It never appears in the results table.
3. **A number that was not measured does not appear.** Not as an estimate, not as a
   projection, not in parentheses, not with a tilde.
4. **What the machine cannot measure is stated, not approximated.** This machine has no GPU
   and no neural accelerator, so no benchmark here produces a GPU, CoreML or NPU number. Every
   README carries a `What this machine cannot measure` section saying which rows are absent
   and why.
5. **Variance is reported, not hidden.** A shared virtual machine has fatter tails than a
   laptop. Report the median, the interquartile range and the ninety-fifth percentile, and say
   how many repeats produced them.

`misc/benchmarks/common/device.py` emits the machine banner at run time, so the banner in
`results/raw.txt` is measured rather than typed. If the banner and the README disagree, the
README is wrong.

## 2. Directory layout

```
misc/benchmarks/
  common/
    __init__.py
    device.py          machine identification and the banner
    timing.py          warmup, repeats, median, interquartile range, p95
    determinism.py     seeding and thread pinning
    requirements.txt   the pinned environment, shared by every benchmark
    README.md          what the harness guarantees
  NN-slug/
    bench.py           the measurement, importable, no side effects on import
    run.sh             the entry point, honours QUICK=1
    requirements.txt   `-r ../common/requirements.txt` plus anything extra, pinned
    README.md          filled from the template in section 5, no placeholders
    results/
      raw.txt          stdout of the full run, including the machine banner
      summary.md       the results table and one paragraph reading it
```

`NN` matches the README section the benchmark belongs to, so that the mapping from claim to
measurement is mechanical. One directory may serve only one section.

Nothing in a benchmark directory may import from another benchmark directory. Shared code
goes in `common/`, which exists so that no two benchmarks disagree about how they measured:
one timing implementation, one device detection, one determinism setup.

## 3. Measurement rules

**Determinism.** All data is synthetic and generated from a fixed seed with
`numpy.random.default_rng`. No network access at run time, no downloads, no cached artefacts,
no reading of system entropy. Two runs on the same machine produce the same inputs and, up to
timing noise, the same accuracy numbers. Accuracy-style numbers must be bit-identical across
runs; a benchmark whose accuracy output moves between runs is broken.

**Threading.** `run.sh` sets `OMP_NUM_THREADS` and `OPENBLAS_NUM_THREADS` explicitly and the
README records the value. BLAS threading changes throughput by more than most of the effects
being measured, so leaving it implicit makes a benchmark meaningless.

**Warmup.** Discard warmup iterations before timing, and state how many. The first call into
a BLAS kernel or a Pillow resampler pays for allocation and code paths that steady state does
not.

**Repeats and statistics.** Time at least seven repeats in full mode. Report the median as
the headline, plus the interquartile range and the ninety-fifth percentile. Never report a
mean without a dispersion measure, never report a minimum as if it were typical, and never
report a single run.

**The timer boundary is declared.** Every timed section says in the README exactly what is
inside it. Where a claim in the field is routinely measured without preprocessing or
postprocessing, the benchmark measures both ways and shows the gap, because that gap is
usually the finding.

**Units and names.** Milliseconds for latency, images per second for throughput, and the
statistic is named in the column header. Accuracy columns name the metric and its definition.
No bare numbers.

**Budgets.** `QUICK=1 ./run.sh` finishes in under ten seconds so that continuous integration
can smoke test every benchmark on every push. A full run finishes in under five minutes.
`QUICK=1` writes nothing to `results/`: it prints to stdout and exits, so that a smoke test
never dirties committed evidence.

**Scale honesty.** A microbenchmark on synthetic data measures a mechanism, not a product.
Where the mechanism's effect size would plausibly change on real data, the Analysis section
says so and says in which direction.

## 4. What each benchmark must produce

- `results/raw.txt`: the full run's stdout, unedited, including the machine banner and the
  seed. Committed from the machine named in the README.
- `results/summary.md`: the results table plus one paragraph that reads it. No new numbers
  that are not in `raw.txt`.
- A `README.md` with every section below filled in.

## 5. The README template

Copy this exactly. Every section is required. No section may be left empty, and no
placeholder text of any kind is permitted, including `TODO`, `TBD`, `n/a` as a dodge, or an
empty table row. If a section has nothing to say, the benchmark is not finished.

```markdown
# NN. Benchmark name

## Claim under test

One sentence stating the claim as the field states it, in the form a practitioner would
repeat it without thinking.

## Why it matters

Two or three sentences on what breaks downstream if the claim is believed and wrong.

## Method

What is generated, with the seed. What is varied, with the exact values. What is held fixed.
What is inside the timer and what is outside it. How many warmup iterations and repeats.
Which statistic is the headline.

## Evidence fields

For an accuracy result, all eight:

| Field | Value |
| --- | --- |
| Model and exact checkpoint | |
| Dataset, split and version | |
| Input resolution and preprocessing | |
| Metric with full definition | |
| Evaluation protocol, single-scale or test-time augmentation, NMS settings | |
| Training data used | |
| Hardware | |
| Baseline compared against | |

For a speed result, all seven:

| Field | Value |
| --- | --- |
| Hardware and count | |
| Precision | |
| Batch size | |
| Input resolution | |
| Framework and version, compile flags | |
| Warmup and statistic reported | |
| Preprocessing and postprocessing inside the timer | |

Where a field does not apply to a synthetic microbenchmark, say what stands in its place and
why. Do not delete the row.

## Environment

The machine banner, the thread settings, the pinned package versions and the exact command
that produced `results/raw.txt`.

## How to run

    ./run.sh
    QUICK=1 ./run.sh

## Results

The table from `results/summary.md`, with units and statistics in the column headers.

## Analysis

What the numbers say. What they do not say. Any published figure referenced here is
attributed and carries the list of evidence fields it is missing.

## What this machine cannot measure

The rows that are absent and why, named specifically.

## Reproduce on another machine

The procedure, and exactly which parts of this README change when the machine changes.
```

## 6. Style

- British spelling in prose. `quantization` keeps its American spelling when it names an API,
  a mode or a tool; the technique in prose is `quantisation`.
- No em dashes anywhere.
- No praise, no novelty claims, no "surprisingly". The number is the interesting part.
- Present tense for what the benchmark does, past tense for what the run found.
- Every table column header carries the unit and the statistic.
- Say "measured" for what the timer produced and "computed" for what was derived from it.
- A finding that contradicts the claim under test is stated plainly in the first sentence of
  the Analysis section. A finding that supports it is stated just as plainly, with the effect
  size.
- Do not round away the finding. Three significant figures for latency, and the raw values
  stay in `raw.txt`.

## 7. Candidate claims

One benchmark per README section. The claims worth measuring, assigned to the section whose
folklore they test:

| Section | Claim measured |
| --- | --- |
| 1 | Pixel values are not the measurement: the same scene under a different transfer function is a different array |
| 2 | Sensor noise is signal dependent, so a fixed denoising assumption is wrong at both ends of the exposure range |
| 3 | A separable Gaussian and a box blur of equal support are not interchangeable at an edge |
| 4 | Near duplicate leakage between splits inflates a score without any change to the model |
| 5 | The same detections scored under three published average precision protocols give three different numbers |
| 6 | Padding and stride choices change the receptive field and therefore the output geometry |
| 7 | Attention cost grows with the square of the token count while convolution grows linearly |
| 8 | Augmentation that changes the label geometry silently breaks the label |
| 9 | A linear probe and a nearest neighbour probe rank representations differently |
| 10 | Non-maximum suppression threshold moves the precision-recall curve and the chosen operating point |
| 11 | Per-frame accuracy can rise while identity consistency falls |
| 12 | Depth error scales with the square of distance under a fixed disparity error |
| 13 | A distributional image metric moves under changes a viewer cannot see |
| 14 | A substring overlap audit finds test items inside a training corpus |
| 15 | Integer quantisation changes both accuracy and latency, and the sign of each depends on the layer |
| 16 | A model tuned against one corruption suite does not transfer to a held out corruption |

A benchmark may be replaced by a better measurement of the same claim. It may not be replaced
by a measurement of a different claim without updating this table.
