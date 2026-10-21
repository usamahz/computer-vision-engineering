# The shared harness

Four modules. Every benchmark imports from here and from nowhere else, so that the repository
has exactly one definition of what a measurement is.

| Module | Guarantees |
| --- | --- |
| `device.py` | The machine banner is measured at run time on Linux and macOS, so a result always names the hardware it came from. |
| `timing.py` | `perf_counter_ns` only, warmup discarded and counted, median as the headline with the interquartile range and the ninety-fifth percentile beside it, repeats reported. |
| `determinism.py` | One seed, one thread-limit report, and a loud warning when the environment differs from the one the committed results were taken under. |
| `report.py` | `results/raw.txt` and `results/summary.md` are written the same way everywhere, and the summary may hold no number that is not in the raw output. |

Two consequences worth stating, because they are the reason the harness exists:

- Accuracy-style numbers are bit-identical across runs on one machine. If one moves between
  runs, the benchmark is broken rather than noisy.
- Latency numbers move. That is why a median travels with a dispersion measure, and why no
  benchmark here reports a minimum as if it were typical.

## Running one

```sh
cd misc/benchmarks/05-average-precision-protocols
./run.sh            # full run, rewrites results/
QUICK=1 ./run.sh    # smoke test, under ten seconds, writes nothing
```

`run.sh` sets `OMP_NUM_THREADS` and `OPENBLAS_NUM_THREADS` to one before Python starts,
because the threading of the linear algebra library moves throughput by more than most of the
effects being measured. A benchmark run outside `run.sh` prints a warning saying so.

## Adding one

Read `misc/notes/benchmark-brief.md`. In short: one directory per README section, `bench.py` plus
`run.sh` plus a pinned `requirements.txt` plus a `README.md` filled from the template with no
placeholders, and `results/raw.txt` and `results/summary.md` committed from the machine the
README names. A quick mode that finishes in under ten seconds is mandatory, because
continuous integration smoke tests every benchmark on every push.
