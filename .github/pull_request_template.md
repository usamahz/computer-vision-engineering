## What changes

<!-- One line per entry added, moved, reworded or removed. -->

## Admission questions

- Primary source, and which kind:
- Canonical URL, and how it was checked:
- Section and subsection:
- Why it sits where it does in dependency order:
- Entry it displaces, if the subsection already holds six, and why:
- Core or watchlist, and if watchlist, the event that would promote it:
- Considered and rejected while preparing this change, with the rule each failed:

## Accuracy evidence, if the entry rests on an accuracy number

- Model and exact checkpoint:
- Dataset with split and version:
- Input resolution and preprocessing:
- Metric with its full definition:
- Evaluation protocol, single-scale or test-time augmentation, NMS settings:
- Training data used:
- Hardware:
- Baseline compared against:

## Speed evidence, if the entry rests on a speed number

- Hardware and how many:
- Precision:
- Batch size:
- Input resolution:
- Framework and version, with compile flags:
- Warmup and the statistic reported:
- Preprocessing and postprocessing inside the timer:

## Checks

- [ ] `python3 misc/scripts/check_format.py` passes
- [ ] `python3 misc/scripts/check_links.py` reports no dead link and no mirror
- [ ] The section draft in `misc/notes/sections/` records the change, and `python3 misc/scripts/build_changelog.py` has been rerun
- [ ] Any benchmark touched still finishes `QUICK=1 ./run.sh` in under ten seconds
