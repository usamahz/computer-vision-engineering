# Conventions

Everything the checkers cannot enforce lives in this file. `misc/scripts/check_format.py` and
`misc/scripts/check_links.py` enforce the mechanical half of the house style; this file is the
other half, and it is the document a reviewer argues from.

Written before any section content. If a rule here and a rule in the README ever disagree,
this file is wrong and gets fixed, because the README is the product.

## 1. What this list is

A reading path for computer vision engineering, ordered from a photon hitting a sensor to a
model running in production. It is a path, not a library: an engineer should be able to read
it top to bottom over some weeks and come out able to reason about a vision system end to
end, including the parts that are not the model.

It is not a bibliography, not a leaderboard, and not a survey of surveys. Coverage is
deliberately incomplete. A subsection that could hold forty papers holds at most six, and the
six are chosen for what they unlock downstream, not for citation count.

## 2. Who it is for

An engineer who can already train a model and read a paper, and who now has to make
decisions: which preprocessing to ship, which metric to trust, which number in a paper is
load bearing and which is decoration. Not a beginner's first contact with machine learning,
and not a researcher's literature review.

Two consequences:

- Nothing is included because it is historically important if it no longer teaches anything a
  working engineer needs. History earns a place only where the modern practice is unreadable
  without it.
- Nothing is excluded for being old. Camera geometry and sampling theory did not expire.

## 3. Ordering logic

Three different orderings operate at three levels, and they are not interchangeable.

**Between sections: dependency order, down then out.** Section N may assume every section
before it and must assume nothing after it. Sections 1 to 5 are the trunk: the mental model,
how an image comes to exist, the classical operations, where ground truth comes from, and how
quality is measured. Only then do architectures appear, because an architecture is a claim
about data and measurement before it is a claim about layers. Sections 10 to 14 are task
families that branch off the trunk and do not depend on each other. Sections 15 and 16 come
last because both are read against a model that already exists.

The test for a correct position: if a reader at section N has to look forward to understand a
sentence, the ordering is broken. Not "would benefit from", has to.

**Inside a subsection: dependency order, never importance, never date.** The first entry is
the one that needs the least prior context; each later entry may assume the earlier ones. A
foundational paper from the nineties can therefore sit above a current one, and the current
one sits second because it reads as a reply to the first. Where two entries are genuinely
independent, the shorter read goes first.

Date order is banned because it smuggles in a false story of progress. Importance order is
banned because it is unfalsifiable and because it makes every list converge on the same five
famous papers.

**Inside Start here: strict reading order.** The ten items are numbered and the number is the
instruction. Item *k* assumes items 1 to *k-1* and nothing else. That is the only place in the
README where a numbered list is allowed, because it is the only place where order is the
content.

## 4. The entry line

One line, one entry:

```
- [Title](URL) - Why it earns its place.
```

The reason says why a reader would open it, not what it contains. "A survey of object
detection" describes a shelf. "Where the mAP protocol everyone quotes was actually defined"
describes a reason to click. Full wording rules, banned vocabulary, title trimming and the
watchlist line format are in `voice.md`, which is the authority for prose and which the
linter partially enforces.

Entries carry no dates, no author names and no numbers. Dates and authors are one click away
and they push the line past the length budget; numbers in a reason line are the single most
common way a list quietly becomes marketing, because a number with no protocol attached is
not evidence, it is decoration.

## 5. Admission: primary sources only

Admissible:

- The original paper, preferably the version the authors point at themselves.
- The authors' own repository, when the repository is the artefact being cited.
- Official model cards and weight pages published by whoever trained the model.
- Framework, runtime and compiler documentation published by whoever maintains it.
- Dataset papers and the official dataset page, which are usually two different URLs and
  often disagree; cite the one that answers the question the entry raises.
- Standards and specifications, and reference implementations published alongside them.

Two carve-outs, both narrow, both deliberate:

**arXiv counts as primary.** An arXiv abstract page is the authors' own deposit, not a
third-party copy, and for most of this field it is the version with a stable identifier that
the authors themselves cite. Prefer a journal, conference or project page where the authors
host the canonical copy and it is openly readable; use arXiv otherwise. Never cite an arXiv
mirror, a rehost, an aggregator's landing page or a reader front end when the arXiv or
publisher page exists. The abstract page is cited, not the PDF, because the abstract page
carries the version history.

**Books are admissible only where no paper plays their role.** Some things in this field
exist as a textbook treatment and nowhere else in citable form: projective geometry for
vision, the sampling and scale space material, the standard account of bundle adjustment.
Where the author hosts the canonical copy openly, the book is admissible and sits at the top
of its subsection as the thing that makes the papers readable. A book that merely restates
papers already in the list is not admissible, and no subsection may be majority books.

## 6. Exclusions, and why

Rejected on sight, with the reason that matters rather than snobbery:

- **Blogspam and content farms.** A post that paraphrases a paper adds a layer of error and
  removes the ablation table, which is the only part of a paper that settles an argument.
- **Listicles and other lists.** Linking a list of lists moves the problem rather than
  solving it. If an entry in another list belongs here, admit the entry, not the list.
- **Aggregators and paper mirrors.** A page that wraps a paper hosted elsewhere adds nothing
  and rots independently of the paper. Machine enforced: `check_links.py` fails the build on
  known mirror and aggregator hosts.
- **AI generated explainers.** No provenance, no corrections, no accountability for an error.
- **Course notes that restate a paper.** Excellent teaching, wrong artefact: the notes drift
  from the paper, the notes are not what a disagreement gets resolved against. Course
  material is admissible only when it is itself the primary treatment of something (see the
  book carve-out), not when it is a readable version of a paper that is already in the list.
- **Leaderboards and benchmark trackers.** A leaderboard is a snapshot of a protocol being
  gamed. The protocol definition is admissible; its current ranking is not.
- **Marketing pages for closed models.** A page with no card, no weights, no protocol and no
  reproducible number is an advertisement. A proper model card from the same vendor is fine.
- **Video lectures and talks.** Not searchable, not quotable, not diffable. A talk that
  contains something no paper does is a watchlist candidate, not a core entry.
- **Code without a paper and papers without code,** where the entry's claim depends on the
  missing half. A method paper with no implementation anywhere is a watchlist item; a
  repository with no written account of what it does is a dependency, not a reading.

## 7. The evidence standard

The rule is simple and its application is not negotiable: a number may enter the list only
with the context that makes it checkable, and the list prefers to say nothing over saying
something unfalsifiable.

**An accuracy claim carries eight fields.** Model and exact checkpoint; dataset with split
and version; input resolution and preprocessing; metric with its full definition; evaluation
protocol including single-scale or test-time augmentation and the non-maximum suppression
settings; training data used; hardware; the baseline compared against.

**A speed claim carries seven fields.** Hardware and how many of them; precision; batch size;
input resolution; framework and version with compile flags; warmup and the statistic reported;
and whether preprocessing and postprocessing are inside the timer. Most published detection
latency numbers exclude both. Where a cited number excludes them, the notes say so.

**The ladder, applied by the evidence marshal, with no appeal:**

| Situation | Outcome |
| --- | --- |
| Every field present and consistent | The claim may be stated in notes; the entry stands on it |
| A field missing, entry does not rest on the number | Entry stands, claim recorded as unverified, number never repeated |
| A field missing, entry rests on the number | Watchlist, with the missing fields named in the line |
| Fields contradict each other, or the protocol is unstated and unrecoverable | Cut |
| Number is reproducible only by the authors on hardware or scenes nobody else has | Watchlist at best, cut if the entry has no other reason to exist |

Softening is forbidden. "Reported improvements are modest" is not a verdict; it is a way of
keeping an entry while pretending to have judged it. The verdicts are: stands, recorded
unverified, watchlist, cut.

Because reason lines carry no numbers, the evidence standard mostly governs what is
*admitted* rather than what is *printed*. The audit trail lives in `sections/NN-name.md`
under `## Claims`, and `misc/notes/changelog.md` counts it.

## 8. Core and watchlist

The core is the sixteen numbered sections. An item enters the core only when three things
exist at the same time:

1. A specification or an original paper.
2. A shipped implementation that someone outside the authors' group can run.
3. A public measurement that states every field the evidence standard requires.

Any one of the three missing means the watchlist. A mechanism can be real, interesting and
clearly the future and still sit on the watchlist, because the watchlist is not a quality
judgement, it is a statement about what can be checked today. That distinction is the whole
reason the watchlist exists: without it, every list drifts towards whatever is loudest.

Every watchlist line states the single condition that would promote it, in the form
`Enters the core when ...`, and the condition has to be an event somebody could observe, not
a mood. "Enters the core when it matures" is not a condition. "Enters the core when weights
and an evaluation script are published" is.

The watchlist carries a date, and the date is the last review, not the creation date. A
watchlist that has not been reviewed in a year is worse than no watchlist, and the date is how
a reader knows which one they are reading.

## 9. Size limits and displacement

- Sixteen sections. Not fifteen, not seventeen. New material displaces, it does not append.
- At most four subsections per section, each a real division of the subject rather than a
  bin for leftovers.
- Three to six entries per subsection. Three is the floor: below three the subsection is not
  a division of the subject, it is an entry with a hat on. Six is full.
- A seventh entry has to displace one of the six, and the pull request has to name which one
  and why. This is the only mechanism that keeps the list finite, so it is enforced socially
  and the linter checks the count.
- Start here is exactly ten items and the ten are a reading order, so the usual subsection
  rules do not apply to it.
- Each source appears once in the whole list, compared without its fragment. When a source is
  the right entry for two places, the earlier place keeps it unless dependency order says
  otherwise, and the later section picks something else. The linter enforces this.

The displacement rule has a side effect worth stating plainly: a good entry can be rejected
for arriving late. That is the intended behaviour of a reading path.

## 10. Dating, retirement and rot

- Entries are not dated. The watchlist is.
- An entry is retired when its URL stops resolving to the thing it cited, when its claim is
  withdrawn, or when a later entry makes it redundant rather than merely superseded. Being
  superseded is not grounds for removal: a superseded paper is often the one that explains why
  the successor exists.
- Deprecated tooling stays only while the deprecation itself is the lesson, and the reason
  line says so without using a number or a date.
- Link rot is checked on every push and weekly. The checker separates dead from unreachable
  from blocked, because publishers and vendor documentation routinely refuse automated
  clients while serving a browser perfectly well, and a checker that calls that "dead" trains
  everyone to ignore it.

## 11. What the checkers cannot enforce

Named here so nobody mistakes a green build for a review:

- **Dependency order.** A linter can count entries; it cannot tell that entry three assumes
  something only entry five explains. Reviewers read a subsection top to bottom and say
  whether the order held.
- **Why not what.** The regex sees a reason of legal length. It cannot see that the reason
  describes contents instead of giving a motive to open the page.
- **Primary source judgement.** Mirror hosts are blocklisted, but the question of whether
  this page is the authors' own canonical copy is human work.
- **Author names in reasons.** No reliable test exists, so this one is read for.
- **Whether a claim's eight or seven fields are actually consistent.** The script counts
  nothing here. The evidence marshal reads the paper's experimental section.
- **Praise.** A blocklist of adjectives catches the obvious cases and nothing else.
  Enthusiasm leaks in through verbs.
- **Whether a book or standard still earns its carve-out.**
- **One voice.** Sixteen specialists write sixteen tones. The editor owns the merge, and the
  owners never touch the README.
- **Whether the list is still a path.** The only test is reading it start to finish, which is
  a person's job and the final gate before release.

## 12. How a veto is applied

The evidence marshal's veto is applied as ruled. The one editorial move that remains is the
honest one: where an entry's lasting value is a mechanism, a definition or a procedure that
the source really contains, and its reason line had been resting on a measured outcome, the
line is rewritten to name the mechanism and the number stays unverified. That move is not
available where the measured outcome is the reason anyone opens the source, and every such
rewrite goes back to the marshal, whose second ruling is final. Both rounds are recorded in
`misc/notes/evidence-marshal.md`.

## 13. Where things live

```
README.md          the product
CONTRIBUTING.md    the admission rules restated verbatim, plus review mechanics
LICENSE            MIT
.github/           issue and pull request templates, the quality and links workflows
misc/              everything that supports the product, in one directory
  notes/           conventions, briefs, section drafts, review records, generated changelog, status
  scripts/         link checker, format checker, changelog generator
  benchmarks/      one reproducible microbenchmark per section, plus the shared harness
```

The root carries three files and one supporting directory, `misc/`, so that the first
thing a reader sees is the product rather than its scaffolding. A `.gitignore` sits at the
root because build residue in a list repository is worse than a hidden file.

Section drafts in `misc/notes/sections/` are the audit trail: the section as delivered, plus what
was rejected, every number examined, every oddity about a URL, and the one claim from that
section worth measuring. They are inputs, not products, and nothing in them is written as if
a reader of the README will see it.

## 14. The benchmarks are part of the argument

A list can be forked by anyone. A list whose claims are measured on a named machine, with the
timer boundaries written down, cannot. `misc/benchmarks/` exists so that the parts of this subject
that are usually asserted get measured instead: preprocessing mismatch, interpolation choice,
letterbox against stretch, compression against accuracy, non-maximum suppression thresholds,
quantisation, batch size against tail latency, and the same checkpoint scored under three
published protocols.

Two rules, both absolute:

- A benchmark reports the machine it actually ran on, named exactly, and nobody else's
  hardware is quoted as if it were ours.
- A number that was not measured does not appear. Not as an estimate, not as a projection,
  not in parentheses.

`benchmark-brief.md` carries the layout, the measurement rules and the README template.
