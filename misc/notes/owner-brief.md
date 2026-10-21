# Owner brief

Read `conventions.md` and `voice.md` first. This file is the working contract: what an owner
must deliver, in what format, and what gets a draft sent back.

Sixteen owners, one section each, working in parallel. Owners do not touch `README.md`. The
editor merges the sixteen drafts into one voice and owns the product file.

## 1. Non-negotiable rules

Breaking any of these sends the draft back regardless of how good the content is.

1. **Primary sources only.** Original papers, authors' own repositories, official model cards
   and weight pages, framework and compiler documentation, dataset papers and official
   dataset pages, standards. No blogspam, no listicles, no aggregators, no paper mirrors, no
   AI generated posts, no course notes restating a paper, no leaderboards, no video.
   arXiv abstract pages count as primary; arXiv PDFs and reader front ends do not.
2. **Every URL resolves to the live canonical source.** No dead links. No third-party PDF
   mirror where an official copy exists. No aggregator landing page where the authors host it
   themselves. Verify before delivering, see section 5.
3. **One line per entry**, exactly `- [Title](URL) - Why it earns its place.`
4. **The reason is under one hundred and twenty characters**, one sentence or fragment,
   capital to full stop, no digits, no author names, no praise adjectives, no second person,
   no em dashes. The authority is `voice.md` section 1 and 2.
5. **Every number you examine goes in the `## Claims` block with a verdict.** Not a summary
   of the paper's results: the fields present, the fields missing, and one of four verdicts:
   stands, recorded unverified, watchlist, cut. The evidence marshal overrides any verdict and
   the owner does not get to argue the number back in.
6. **Reject in writing.** Anything you considered and left out goes in `## Rejected` with the
   specific rule it failed. A draft with an empty or thin `## Rejected` block is treated as
   unfinished work, because a section with nothing rejected means nothing was judged.
7. **No placeholders.** No `TODO`, no `TBD`, no "to be filled". If you cannot fill it,
   deliver fewer entries and say why in the draft.
8. **British spelling in prose**, titles keep their own. See `voice.md` section 3 for the
   `quantization` carve-out.

## 2. Size limits

- Two to four subsections per section. Each must be a real division of the subject.
- Three to six entries per subsection. Three is the floor, six is full.
- Section total therefore lands between six and twenty-four entries. Aim for twelve to
  eighteen. A section at twenty-four is almost certainly padding.
- At most one preamble sentence for the whole section, and only as a warning. See `voice.md`
  section 5. Most sections should have none.
- Section 1 is the exception: exactly ten numbered items, no subsections.

Where the same source is the obvious best entry for two sections, the earlier section keeps
it and the later owner picks something else. Flag the collision in `## Link notes`.

## 3. Coverage duty and suspicion

Each owner's suspicion is not decoration. It is the instrument that produces a sharp
`## Rejected` block. Apply it to the things you want to include, not only to the things you
already planned to cut.

The subsection names below are the required skeleton, so that sixteen sections merge into one
document. Rename a subsection only if the rename is a better division of the same ground, and
say so in the draft.

**1. Start here: the minimum mental model.** Ten items, strict reading order, each assuming
only the ones before it. No subsections. Covers: what an image is as a measurement, geometry
of projection, what a convolution computes, what a metric measures, what training does, what
deployment costs. *Suspicion: anything that assumes a background the reader does not have
yet.* An item that needs section 7 to make sense is disqualified no matter how good it is.

**2. Image formation: optics, sensors, the ISP, colour, noise.** Subsections: Optics and
projection; Sensors and noise; The image signal processor; Colour. Covers: lens and aperture
effects, exposure, photon and read noise models, demosaicing, tone mapping, colour spaces and
transfer functions, raw against processed. *Suspicion: work that treats an image as a clean
array of numbers that fell from the sky.*

**3. Classical foundations: filtering, features, multi-view geometry.** Subsections: Sampling
and filtering; Features and correspondence; Two-view and multi-view geometry; Estimation and
bundle adjustment. Covers: convolution and scale space, edge and corner detection, descriptors
and matching, epipolar geometry, homographies, calibration, robust estimation, least squares
refinement. *Suspicion: the claim that learning made geometry obsolete.*

**4. Datasets, labels and splits: where ground truth comes from and how it lies.**
Subsections: The datasets that set the terms; Annotation and label noise; Splits, leakage and
duplication; Documentation and audit. Covers: how the standard benchmarks were built and what
their label definitions actually are, annotator agreement, test set reuse, near duplicate
contamination, dataset documentation practice. *Suspicion: any result that ignores label noise
or split leakage.*

**5. Evaluation: IoU, mAP, protocols, and the ways a metric misleads.** Subsections: What the
detection metrics compute; Protocols and reporting; Segmentation and dense metrics; How a
metric misleads. Covers: IoU definitions, average precision interpolation, the official
evaluation implementations, panoptic and boundary metrics, significance and variance,
calibration of reported numbers. *Suspicion: any mAP quoted without its protocol.*

**6. Convolutional architectures.** Subsections: Foundations; Depth, residuals and width;
Efficient convolutional designs; Recipes against architectures. Covers: the architectures an
engineer still meets in production, what each one actually changed, and the recipe papers that
reassigned credit. *Suspicion: architecture claims that are training-recipe claims wearing a
hat.*

**7. Attention, vision transformers and hybrids.** Subsections: Attention; Vision
transformers; Data, scale and distillation; Hierarchies and hybrids. Covers: the attention
operator, patch embedding, what ViTs need from data, hierarchical designs, convolution and
attention compared, and the comparisons that were run at unequal budget. *Suspicion:
comparisons at unequal compute or unequal data.*

**8. Training: objectives, augmentation, schedules, regularisation.** Subsections: Objectives;
Augmentation; Schedules and optimisation; Regularisation and normalisation. Covers: the loss
functions that matter for vision, the augmentation policies that moved results, learning rate
schedules and batch size scaling, normalisation layers, and the baseline tuning literature.
*Suspicion: improvements that evaporate against a properly tuned baseline.*

**9. Self-supervised learning and vision foundation models.** Subsections: Contrastive
learning; Self-distillation and masked modelling; Vision foundation models and weights;
Evaluating representations. Covers: the pretext task families, the collapse problem, the open
weight families an engineer would actually load, and how representation quality is measured.
*Suspicion: linear-probe numbers presented as general capability.*

**10. Detection and segmentation.** Subsections: Detector families; Set prediction and
anchor-free designs; Segmentation; Postprocessing and what ships. Covers: the detector
lineages, label assignment, mask heads, promptable segmentation, non-maximum suppression and
its variants, and the production repositories. *Suspicion: latency that excludes non-maximum
suppression.*

**11. Video: temporal modelling and tracking.** Subsections: Temporal modelling; Video
datasets and their protocols; Tracking; Tracking metrics. Covers: temporal architectures,
optical flow, the action recognition benchmarks and their clip sampling protocols, tracking by
detection, association, and the identity-aware metrics. *Suspicion: per-frame metrics
presented as tracking quality.*

**12. 3D: depth, stereo, SfM, SLAM, radiance fields and splatting.** Subsections: Depth and
stereo; Structure from motion; Simultaneous localisation and mapping; Radiance fields and
splatting. Covers: stereo matching and monocular depth, incremental and global reconstruction,
the SLAM systems people still build on, neural fields and rasterised splatting, and the
reconstruction benchmarks. *Suspicion: results on scenes nobody else can reproduce.*

**13. Generative vision: diffusion, editing, control.** Subsections: Diffusion foundations;
Samplers and guidance; Latent and text conditioned systems; Control, editing and evaluation.
Covers: the forward and reverse process, score matching, samplers, classifier-free guidance,
latent diffusion, conditioning and control mechanisms, editing, and what the standard
generative metrics do and do not measure. *Suspicion: a distributional image metric standing
in for anything a user cares about.*

**14. Vision-language models.** Subsections: Contrastive image-text pretraining; Generative
vision-language models; Open weights and model cards; Benchmarks and contamination. Covers:
image-text pretraining, the adapter and projector designs, instruction tuning for vision,
open weight families with real cards, the standard benchmarks, and the contamination
literature. *Suspicion: benchmark contamination, and evaluations whose test set was on the
open web before training.*

**15. Efficiency and deployment: quantisation, distillation, compilers, edge, NPU.**
Subsections: Quantisation; Distillation, pruning and sparsity; Compilers and runtimes; Edge,
accelerators and measurement. Covers: post-training and quantisation-aware training, integer
arithmetic in practice, distillation, structured sparsity, graph compilers and the runtimes
that actually ship, accelerator documentation, and how to time an inference properly.
*Suspicion: any speedup measured without preprocessing, at a different batch size, or on
hardware nobody deploys.*

**16. Robustness and failure modes: distribution shift, adversarial, bias, safety.**
Subsections: Distribution shift; Corruptions and synthetic perturbation; Adversarial
robustness; Bias, calibration and safety. Covers: shift taxonomies and the benchmarks that
measure it, corruption suites and their overfitting problem, adversarial examples and honest
evaluation of defences, bias audits, calibration under shift, and the safety-relevant failure
modes of deployed vision. *Suspicion: robustness claims evaluated only on the corruption
benchmark they were tuned against.*

## 4. Exact file format for a section draft

Write to `misc/notes/sections/NN-name.md`, with `NN` the two digit section number and `name` the
kebab-case section name. Exactly this structure, exactly these headings, in this order, with
no extra top level headings:

```markdown
# NN. Section name as it will appear

Owner: role, one line, including the suspicion.

## Section

<the section exactly as it should appear in the README, starting at the H2 heading,
 using H3 for subsections, obeying every rule in voice.md. no commentary.>

## Rejected

- [Title](URL) - Rule failed: <the specific rule>. <one sentence of why, plain prose.>

## Claims

### <claim, in one line, naming the source>

- Fields present: <list>
- Fields missing: <list, or none>
- Verdict: stands | recorded unverified | watchlist | cut
- Note: <one or two sentences. for a speed claim, state explicitly whether preprocessing and
  postprocessing are inside the timer.>

## Link notes

- <URL> - <redirect chain, paywall, host that refuses automated clients, mirror rejected in
  favour of an official copy, collision with another section, or anything else odd.>

## Benchmark proposal

The one claim from this section worth measuring, in one short paragraph: the claim, the
measurement that would settle it, and what result would count as settling it. It must be
runnable on a laptop class machine with no GPU, with a quick mode finishing in under ten
seconds, using only numpy and Pillow. No network access at run time.
```

Rules about the four blocks:

- `## Rejected`: at least four entries, more is better. Each names the rule from
  `conventions.md` section 5, 6 or 7 that it failed. "Not interesting enough" is not a rule.
  Entries rejected for the size limit say what they would have displaced.
- `## Claims`: at least four claims examined. Include the famous number from your area even
  when the entry does not rest on it, because the changelog counts examined numbers and the
  count is the evidence that the bar was real. State missing fields by name, using the field
  names from `conventions.md` section 7.
- `## Link notes`: may be short, but "nothing odd" is only acceptable if you actually checked
  every URL. Record redirects you followed, hosts that refused you, and mirrors you rejected.
- `## Benchmark proposal`: one claim, not a list. Pick the one where the field's folklore is
  most likely to be wrong.

The `## Section` block is the only part that reaches the README, and the editor will rewrite
its prose for one voice. Nothing in the other four blocks ships.

## 5. Verifying your links before delivery

Run the checker on your own draft:

```sh
python3 misc/scripts/check_links.py misc/notes/sections/NN-name.md
```

It separates `OK`, `REDIRECT`, `BLOCKED`, `UNREACHABLE`, `DEAD` and `MIRROR`. Fix every `DEAD`
and every `MIRROR` before delivering. Record `REDIRECT` and `BLOCKED` results in
`## Link notes`, with the final URL for a redirect: if the redirect is permanent, cite the
destination instead. A `BLOCKED` result means a host refused an automated client, which is
normal for publishers and vendor documentation; confirm the page exists by other means and
say in the note how you confirmed it.

A URL you cannot verify does not go in the draft. Not with a caveat, not in the hope that CI
will sort it out.

## 6. Delivery checklist

- [ ] Entry grammar and reason length pass `python3 misc/scripts/check_format.py --draft <file>`
- [ ] Two to four subsections, three to six entries each
- [ ] Dependency order inside every subsection, stated as an ordering decision in the draft
      if it is non-obvious
- [ ] Every URL verified, every oddity recorded
- [ ] Four blocks present and non-trivial
- [ ] No digits, no praise, no author names, no second person in any reason
- [ ] No placeholders anywhere in the file
