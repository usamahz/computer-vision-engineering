# Voice

How the README is written. The linter enforces the mechanical rules in sections 2 and 3; the
rest is read for by the editor. Owners write to this file, the editor merges against it.

One sentence to hold on to: **the list is a colleague telling you what to read next, not a
publisher's catalogue.** A colleague says "that is where the protocol is actually defined".
A catalogue says "a comprehensive survey of modern approaches".

## 1. The reason line

The shape:

```
- [Title](URL) - Why it earns its place.
```

The reason answers one question: *why would a reader open this instead of the next thing?*
It is not a summary, not a verdict on quality, not a rating.

Three ways to get it right, in rough order of usefulness:

1. **Name the thing it is the source of.** "Where the evaluation protocol everyone quotes was
   defined."
2. **Name the mistake it prevents.** "Why a resize that looks identical moves accuracy."
3. **Name the question it settles.** "Whether attention beats convolution once data and
   compute are held equal."

Worked rewrites:

| Weak | Why it fails | Fixed |
| --- | --- | --- |
| A survey of object detection methods. | Describes contents. | Where the detector families were first laid out against each other. |
| The best introduction to colour science. | Praise, and contents. | Why two pipelines agree on pixels and disagree on colour. |
| Introduces a novel attention mechanism achieving 84.1% top-1. | Number without protocol, and novelty is not a reason. | Attention applied to patches with no convolution left in the stack. |
| You should read this before training ViTs. | Second person, and instruction rather than reason. | What a transformer needs from the data pipeline before it trains at all. |
| Kaiming He's residual networks paper. | Author name, and contents. | Why depth stopped being the thing that broke training. |

Length: under one hundred and twenty characters, counted from the first character after
`) - ` to the full stop inclusive. The budget is the point: it forces a single claim.

Grammar: one sentence or one fragment. A fragment is normal and often better. Starts with a
capital letter, ends with a full stop. No semicolons, no colons, no parentheses, no
exclamation marks, no question marks.

## 2. Banned in a reason line, enforced by the linter

- **Digits.** No numbers at all, in any form, including `3D`, `int8`, `COCO-2017`. Write
  "three dimensional", "eight bit integer", "the detection benchmark". A number in a reason
  line is a performance claim without a protocol, or it is noise.
- **Em dashes and en dashes.** The only dash is the hyphen, in hyphenated words and as the
  separator. This keeps the separator parseable and the line calm.
- **Second person.** No `you`, `your`, `yours`, `yourself`, `we`, `our`, `us`. The line
  describes the source, not the reader and not the maintainers.
- **Praise adjectives and the enthusiasm vocabulary.** Banned: best, better, great, excellent,
  amazing, awesome, essential, must-read, seminal, classic, iconic, legendary, brilliant,
  elegant, beautiful, groundbreaking, revolutionary, landmark, definitive, invaluable,
  indispensable, outstanding, remarkable, impressive, powerful, state-of-the-art, cutting-edge,
  comprehensive, exhaustive, gold standard, novel, famous, popular, influential.
  The list is mirrored in `misc/scripts/check_format.py`; change one and change the other.
  If an entry needs an adjective to justify itself, it does not earn a place.
- **Author names.** Not enforceable by script, so it is read for. A method name that happens
  to be a surname is not an author name in this sense when it is the established name of the
  method.

Also banned by the linter, because review found them doing the work of praise: everyone,
almost every, widely, actually, means nothing, most reports, became the default, ended up
inside.

Also banned, by convention rather than by script: hedging that pretends to be judgement
("arguably", "generally considered"), vague stakes ("important for practitioners"), and the
word "paper" used as the subject of the line ("paper that introduces ..."), which wastes the
budget on a fact the link already states.

### Tics the editor cuts

Review counted these across the merged draft, and each one flattens the list into a single
cadence. None is banned outright; each is cut on sight unless it is the only honest wording.

- **The `once` pivot.** "What X does once Y" became a reflex. Use when, or rewrite.
- **Rigour compliments.** "Derived rather than asserted", "shown instead of asserted",
  "settled rather than argued". They praise the source's method, which is not a motive.
- **Priority credits.** "First written down", "first introduced", "where X was first". A
  priority claim is history, and history earns a place only where conventions section 2 says.
- **Adoption verdicts.** "Most recipes copy", "the default everywhere". Popularity is not a
  reason to open anything.
- **Implicit performance claims.** "Matters more than", "removes most of the cost", "stops
  scoring well". Each is a number with no protocol. Name the mechanism instead, or the entry
  belongs on the watchlist.
- **Contents openers.** "The operator semantics that ...", "A card that ...". Say why the
  reader opens it, then what it contains if there is room.

## 3. Terms used

One spelling per concept, so that search inside the page works and so that two sections do
not look like two documents.

**Prose spelling.** British English in prose: colour, behaviour, favour, grey, labelled,
modelling, normalise, optimise, parameterise, centre, metre, analogue. Titles keep their own
spelling, always, including American spellings and vendor capitalisation.

**The quantisation exception.** In prose the technique is `quantisation`. The term stays
`quantization` wherever it is part of a name rather than a word: an API path
(`torch.ao.quantization`), a named mode in a vendor's documentation, a paper or tool title,
or an established initialism's expansion where the vendor spells it that way. In practice:
"int8 quantisation moved accuracy" and "the post-training quantization pass in the runtime".
The same carve-out applies to any other established technical term whose American spelling is
the term of art, including `normalization layer` when naming a specific module type.

**Canonical forms.** mAP, AP, IoU, NMS, ISP, SfM, SLAM, ViT, CNN, MLP, FLOPs, NPU, SoC,
top-one accuracy (written out, because digits are banned in reasons), COCO, ImageNet,
PASCAL VOC, Cityscapes, Kinetics, KITTI, LVIS. Write "test-time augmentation", not "TTA", on
first use in prose and in reasons. Write "non-maximum suppression" in prose, "NMS" in tables
and benchmark READMEs.

**Preferred nouns.** "detector" rather than "detection model"; "checkpoint" rather than
"pretrained weights" when a specific file is meant; "runtime" for an inference engine;
"protocol" for the full evaluation recipe; "split" for a named subset of a dataset; "recipe"
for the training configuration. "Foundation model" is used only where the source uses it, and
never as a compliment.

**Verbs that carry their weight.** defines, specifies, measures, separates, isolates,
predicts, breaks, fails, holds, settles, exposes, standardises. Avoid "explores",
"investigates", "leverages", "showcases", "dives into".

## 4. Titles

The title is the source's own, trimmed to the part a reader would type into a search box.

- Drop a trailing subtitle after a colon when the first half is unambiguous:
  `Deep Residual Learning for Image Recognition` stays, `ImageNet Classification with Deep
  Convolutional Neural Networks` stays, but `SAM 2: Segment Anything in Images and Videos`
  may be trimmed to `SAM 2` only if no other entry could be meant, which here it could not.
- Keep the method name when the paper is known by it, even if the paper's title buries it.
  Prefer `YOLOv3` over the full sentence title where the community name is the searchable one,
  and keep the paper's own wording when the method has no separate name.
- Drop version suffixes that are not part of the name: no `(v2)`, no `arXiv:2103.00020`, no
  trailing `[cs.CV]`, no venue tags, no year in parentheses.
- Documentation titles are the page's own heading, trimmed of the product's marketing
  prefix: `Post-training quantization` rather than `Vendor Toolkit Documentation: Guide to
  Post-training quantization`.
- Repositories are titled with the thing, not the path: `Segment Anything` rather than
  `facebookresearch/segment-anything`, unless the repository name is the only name it has.
- Keep the source's capitalisation. Do not convert a title to sentence case.
- Soft ceiling of sixty characters. Over that, trim from the right, never paraphrase.

## 5. Section names, preambles and prose

**Section names** are sentence case: first word capitalised, everything else lower case
except acronyms, proper nouns and method names. Subsection names follow the same rule and are
noun phrases, never questions, never imperatives.

**Preambles.** A section gets at most one sentence of preamble, and only where a reader who
starts clicking without it will draw a wrong conclusion. Legitimate reasons for a preamble:

- The section's results are mostly not comparable to each other, and a reader will otherwise
  read the order as a ranking.
- The section contains a widely quoted number that is wrong in a specific way.
- The section's subject is routinely confused with a neighbouring one.

Not legitimate: introducing the topic, saying the topic is important, explaining the
structure, welcoming the reader. A preamble is a warning label. Sections with nothing to warn
about get no preamble, and most sections have nothing to warn about.

**Prose elsewhere** in the README, meaning the opening paragraphs and `What earns a place`, is
plain declarative sentences, present tense, no first person plural, no second person except
in `CONTRIBUTING.md` where instructions to a contributor are the point. Short paragraphs.
No bold for emphasis inside prose; bold is for the few table and list labels that need it.

## 6. Watchlist lines

A watchlist line is an entry line plus a promotion condition, and it is the one place where
two sentences are allowed:

```
- [Title](URL) - Why it is being watched. Enters the core when <observable event>.
```

Rules:

- The literal phrase `Enters the core when` appears exactly once, and the linter checks it.
- The condition is an event an outsider could observe and date: weights published, a protocol
  specified, a second group reproducing it, a runtime shipping the operator, a standard
  ratified. Not "matures", not "stabilises", not "sees adoption", not "proves itself".
- The reason half obeys every reason rule including the ban on digits and praise. The
  condition half may name a field that is missing from a claim, which is the one place the
  vocabulary of the evidence standard appears in the README.
- Under two hundred and forty characters as read, which is the line without its URL: a
  URL's length is the publisher's choice, not the author's.
- Watchlist entries are ordered by subject, matching the order of the core sections they
  would enter, so that a reader scanning for one subject finds its pending items together.

## 7. Things that look like style and are actually rules

- Numbered lists appear only in Start here.
- Each source appears once in the whole list, compared without its fragment. Start here is
  no exception: an entry there is not repeated in its home section.
- No tier headings, no `##### Advanced`, no stars, no badges inside sections, no emoji
  anywhere in the README, no checkboxes, no tables inside the sixteen sections.
- No placeholder text, ever, including in a draft that is about to be filled in. An empty
  subsection is deleted, not marked.
