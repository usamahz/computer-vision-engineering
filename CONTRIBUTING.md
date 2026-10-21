# Contributing

This list stays short by refusing things. Most proposals are declined, and a declined proposal
that names the rule it failed is a useful contribution in its own right, because it goes into
the record of what was considered.

Read [misc/notes/conventions.md](misc/notes/conventions.md) for the reasoning behind every rule below and
[misc/notes/voice.md](misc/notes/voice.md) for how a line is written.

## The rules

These are restated verbatim from the brief the list was built to, and they are not negotiable.

Primary sources only. Original papers, the authors' own repos, official model cards and
weights, framework and compiler documentation, dataset papers and their official pages,
standards. No blogspam, no listicles, no aggregators, no AI-generated posts, no course notes
restating a paper.

One line per entry, saying why it earns a place, not what it is. "A survey of object detection"
tells a reader nothing. "Where the mAP protocol everyone quotes was actually defined" tells them
why they would open it.

Every accuracy claim carries eight fields: model and exact checkpoint, dataset with split and
version, input resolution and preprocessing, metric with its full definition, evaluation
protocol including single-scale or TTA and NMS settings, training data used, hardware, and the
baseline compared against.

Every speed claim carries seven: hardware and count, precision, batch size, input resolution,
framework and version with compile flags, warmup and the statistic reported, and whether
preprocessing and postprocessing are inside the timer. Most published detection latency numbers
are not. Say so when they are not.

Missing any field means watchlist or cut. Not softened, not caveated. If the entry rests on that
number it moves to the watchlist with the missing fields named, or it goes.

Every URL resolves to the live canonical source. No dead links, no third-party PDF mirrors where
an official one exists, no paper-aggregator pages where the authors host it themselves.

## Qualify or reject

Work down the table. The first row that matches decides.

| Question | If the answer is no | If the answer is yes |
| --- | --- | --- |
| Is it a primary source as listed above? | Reject. Find the primary source it restates and propose that instead. | Continue. |
| Does the URL resolve to the canonical copy, not a mirror, an aggregator or an arXiv PDF path? | Reject until the canonical URL is supplied. | Continue. |
| Can the reason be written in under 120 characters, as a motive to open it rather than a description? | Reject. If nobody can say why to open it, nobody will. | Continue. |
| Does it fit the dependency order of one section, assuming nothing from a later section? | Reject, or propose it for the section where it does fit. | Continue. |
| Does the entry rest on a number? | Skip to the subsection check. | Every evidence field must be present. A missing field sends it to the watchlist with the field named, or out. |
| Do a specification or paper, a shipped implementation and a public measurement stating every field all exist? | Watchlist, with the event that would promote it. | Core. |
| Does the target subsection already hold six entries? | Add it. | Name the entry it displaces and argue the displacement in the pull request. |

## The entry format

One entry is exactly one line:

```
- [Title](URL) - Why it earns its place.
```

- The title is the source's own, trimmed to the part a reader would search for.
- The reason is under 120 characters, one sentence or fragment, capital letter to full stop.
- No digits, no author names, no praise adjectives, no second person, no em dashes, no colons,
  semicolons or parentheses in the reason.
- Order inside a subsection is dependency order: the entry needing least prior context first.
  Never importance, never date.

A watchlist line adds its promotion condition:

```
- [Title](URL) - Why it is being watched. Enters the core when <an event someone could observe>.
```

## The evidence fields

For an accuracy claim, all eight:

1. Model and exact checkpoint
2. Dataset with split and version
3. Input resolution and preprocessing
4. Metric with its full definition
5. Evaluation protocol, including single-scale or test-time augmentation and the NMS settings
6. Training data used
7. Hardware
8. The baseline compared against

For a speed claim, all seven:

1. Hardware and how many
2. Precision
3. Batch size
4. Input resolution
5. Framework and version, with compile flags
6. Warmup and the statistic reported
7. Whether preprocessing and postprocessing are inside the timer

The pull request template lists every field as a blank to fill. Fill the ones the entry rests on
and write "does not rest on a number" where it does not.

## How review goes

1. Open an issue with the matching template, or go straight to a pull request that fills in the
   template in full.
2. CI runs `misc/scripts/check_format.py`, `misc/scripts/check_links.py`, `misc/scripts/build_changelog.py --check`
   and every benchmark in quick mode. A red build is not reviewed.
3. Review applies the four roles the list was built with. The evidence marshal applies the
   evidence rules and has a veto that cannot be argued back. The link verifier confirms the URL
   is the canonical copy. The red team argues for cutting the entry, and the proposer answers in
   writing. The editor rewrites the line into the house voice and owns `README.md`.
4. A merged entry is recorded in its section draft under `misc/notes/sections/`, which is where the
   changelog is generated from. A rejected one is recorded there too, with the rule it failed.

## Running the checks locally

```sh
python3 misc/scripts/check_format.py
python3 misc/scripts/check_links.py
python3 misc/scripts/build_changelog.py --check
QUICK=1 misc/benchmarks/05-average-precision-protocols/run.sh
```

All three scripts are standard library only. The benchmarks need the pinned environment in
`misc/benchmarks/common/requirements.txt`.

## Benchmarks

A new benchmark follows [misc/notes/benchmark-brief.md](misc/notes/benchmark-brief.md). It reports the
machine it actually ran on, quick mode finishes in under ten seconds, and no number appears that
was not measured on the machine the README names.
