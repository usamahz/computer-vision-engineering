# 5. Evaluation: IoU, mAP, protocols, and the ways a metric misleads

Owner: metrics engineer who has reimplemented COCO evaluation from the paper, suspicious of any mAP quoted without its protocol.

## Section

## 5. Evaluation: IoU, mAP, protocols, and the ways a metric misleads

The protocols below are not versions of one metric, and a score produced under one of them cannot be compared with a score produced under another.

### What the detection metrics compute

- [The PASCAL Visual Object Classes Challenge 2007 Development Kit](https://host.robots.ox.ac.uk/pascal/VOC/voc2007/htmldoc/index.html) - Where the overlap threshold and the eleven point interpolated average precision were specified.
- [The PASCAL Visual Object Classes Challenge 2012 Development Kit](https://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html) - Why the same detections score differently once interpolation is replaced by the precision envelope area.
- [cocoeval.py](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py) - Where the detection protocol everyone quotes is defined, down to recall sampling and the per-image detection cap.
- [Generalized Intersection over Union](https://arxiv.org/abs/1902.09630) - Why overlap stops discriminating between two wrong boxes once they no longer intersect.

### Protocols and reporting

- [LVIS: A Dataset for Large Vocabulary Instance Segmentation](https://arxiv.org/abs/1908.03195) - What a false positive means when an image is annotated for only some of the categories it contains.
- [LVIS API](https://github.com/lvis-dataset/lvis-api) - Why an average precision computed here is not comparable with one computed under the detection benchmark.
- [Open Images evaluation protocols](https://storage.googleapis.com/openimages/web/evaluation.html) - What a protocol does with a label hierarchy and with boxes covering a group rather than one object.
- [Accounting for Variance in Machine Learning Benchmarks](https://arxiv.org/abs/2103.03098) - Whether a gap between two reported scores survives the randomness that produced both of them.

### Segmentation and dense metrics

- [Panoptic Segmentation](https://arxiv.org/abs/1801.00868) - Where a single score covering stuff and things was defined so that segmentation and recognition separate.
- [COCO 2018 Panoptic Segmentation Task API](https://github.com/cocodataset/panopticapi) - Where the void label and the crowd handling that move panoptic quality are settled rather than described.
- [Boundary IoU](https://arxiv.org/abs/2103.16562) - Why a mask score can rise while the boundary a viewer actually looks at gets worse.
- [Boundary IoU API](https://github.com/bowenc0221/boundary-iou-api) - What moves in the reported score when the same evaluation swaps mask overlap for boundary overlap.

### How a metric misleads

- [Diagnosing Error in Object Detectors](https://dhoiem.cs.illinois.edu/projects/detectionAnalysis/) - Where a single summary score was first broken into the failure types that produced it.
- [TIDE: A General Toolbox for Identifying Object Detection Errors](https://arxiv.org/abs/2008.08115) - Why two detectors with the same headline score fail in different ways and need different fixes.
- [Evaluating Large-Vocabulary Object Detectors](https://arxiv.org/abs/2102.01066) - How the score moves when the confidence calibration across categories changes and nothing else does.
- [A Metric Learning Reality Check](https://arxiv.org/abs/2003.08505) - What happens to a long run of reported gains once the evaluation protocol is held fixed.

## Rejected

- [Microsoft COCO: Common Objects in Context](https://arxiv.org/abs/1405.0312) - Rule failed: owner-brief section 2, a source that is the obvious entry for two sections belongs to the earlier one. Section 4 owns dataset construction and keeps it, so the detection protocol is cited here from the reference implementation, which is where the parameters are actually fixed and where a disagreement can be diffed.
- [The PASCAL Visual Object Classes (VOC) Challenge](https://www.cvlibs.net/projects/autonomous_vision_survey/literature/Everingham2010IJCV.pdf) - Rule failed: conventions.md section 6, aggregators and paper mirrors. A copy of the journal paper parked in an unrelated group's literature folder, where the challenge organisers publish the evaluation rules themselves in readable and diffable form.
- [The PASCAL Visual Object Classes Challenge 2012 Development Kit](https://datasets.cms.waikato.ac.nz/ufdl/data/pascalvoc2012/devkit_doc.pdf) - Rule failed: conventions.md section 6, aggregators and paper mirrors. A university dataset mirror's copy of the development kit document, superseded by the official pages admitted above, which also carry the revision note explaining the change of average precision definition.
- [Diagnosing Error in Object Detectors](https://videolectures.net/eccv2012_hoiem_detectors/) - Rule failed: conventions.md section 6, video lectures and talks. Not searchable, not quotable, not diffable, and the authors' own project page carries the same material plus the analysis code.
- [Diagnosing Error in Object Detectors](https://courses.cs.washington.edu/courses/cse590v/13au/eccv2012_detanalysis_derek.pdf) - Rule failed: owner-brief section 1 rule 2, no third-party PDF copy where an official copy exists. A teaching copy in a course directory, which rots on the course's schedule rather than the authors'.
- [PASCAL VOC](https://www.aiwiki.ai/wiki/pascal_voc) - Rule failed: conventions.md section 6, AI generated explainers. No provenance and no accountability for an error, and a check of its claims about the challenge against the organisers' own pages did not resolve.
- The detection leaderboards on paperswithcode - Rule failed: conventions.md section 6, leaderboards and benchmark trackers, and aggregators. A ranking is a snapshot of a protocol being gamed rather than the protocol, and the host is on the machine enforced mirror list, so no URL is recorded here.
- A mean average precision explainer on medium.com - Rule failed: conventions.md section 6, blogspam and content farms. It is the first thing a search for the interpolation question returns and it paraphrases the development kit admitted above, adding a layer of error over a page that is already short and openly readable. The host is on the machine enforced restatement list, so no URL is recorded here.
- The arXiv reader front end renderings of the panoptic and detection error papers on ar5iv and alphaxiv - Rule failed: conventions.md section 5, never cite an arXiv mirror or a reader front end where the arXiv page exists. Both hosts are on the machine enforced mirror list, so no URL is recorded here.
- The mean average precision page in a training framework's metrics documentation - Rule failed: conventions.md section 9, the size limit. It would have had to displace cocoeval.py, and a wrapper cannot settle a disagreement whose answer is defined by the implementation it wraps. Its own URL could not be confirmed from this container either, which is a second reason it is absent.
- The Cityscapes benchmark metrics page - Rule failed: owner-brief section 5, a URL that cannot be verified does not go in the draft. The host refused this container and the search budget was exhausted before its exact address and heading could be confirmed independently, so the instance weighted overlap point is dropped rather than guessed, and the segmentation subsection ships at four entries without it.
- The COCO detection evaluation page on the dataset website - Rule failed: owner-brief section 5, a URL that cannot be verified does not go in the draft. The host refused this container and the page is a client-side fragment of a single page application, so no fetch can distinguish a live evaluation tab from a home page that no longer carries one. See Link notes.

## Claims

### COCO average precision averages ten overlap thresholds and samples one hundred and one recall points, with detections capped at one hundred per image, from cocoeval.py

- Fields present: metric with its full definition; evaluation protocol, specifically the overlap thresholds, the recall sampling grid, the four area ranges and the three detection caps.
- Fields missing: model and exact checkpoint; dataset with split and version; input resolution and preprocessing; training data used; hardware; the baseline compared against. None of the six applies to a protocol definition.
- Verdict: stands
- Note: read from the parameter block and the accumulation step of the reference implementation rather than from a restatement of it. The implementation also sweeps the precision array backwards to make the envelope monotonic before sampling it, which is the step a reimplementation most often omits and the step that makes the result differ from a naive area under the curve.

### An average precision from the large vocabulary benchmark and one from the detection benchmark are not comparable, because the per-image detection cap differs, from lvis-api and cocoapi

- Fields present: metric with its full definition for both implementations; evaluation protocol for both, specifically the detection cap, the overlap thresholds, the recall sampling grid and the category frequency grouping.
- Fields missing: none that applies. Model and checkpoint, split and version, resolution and preprocessing, training data, hardware and baseline are not part of a comparison between two protocols.
- Verdict: stands
- Note: both implementations use the same ten overlap thresholds and the same one hundred and one recall points, so the caps are the visible difference, three hundred detections per image against one hundred. The large vocabulary implementation additionally drops, per image, every category that image does not annotate, which changes what a false positive is rather than how many are allowed. A score quoted as mAP without naming the implementation that produced it is therefore unrecoverable, which is the whole reason this section exists.

### Calibrating detector confidence across categories raises pooled average precision by 1.7 points on the large vocabulary benchmark, from Evaluating Large-Vocabulary Object Detectors

- Fields present: metric with its full definition, the paper's own pooled variant; dataset with split; the baseline compared against, the same detector uncalibrated.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings; training data used; hardware.
- Verdict: recorded unverified
- Note: the figure was read from the abstract as returned by search, not from the experimental section, because the host was unreachable from this container. The entry does not rest on it: it rests on the mechanism, that a metric which compares confidences across categories can be moved by rescaling those confidences and changing nothing else. The number is not repeated in the section.

### Generalised overlap used as a regression loss improves detectors on the classification benchmark and the detection benchmark, from Generalized Intersection over Union

- Fields present: dataset with split, two of them; metric with its full definition, reported under both the overlap based and the generalised measure; the baseline compared against, the same detectors with their original regression losses.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings; training data used; hardware.
- Verdict: recorded unverified
- Note: the entry rests on an analytic point that needs no measurement, that overlap is identically zero for every pair of disjoint boxes and therefore carries no gradient and no ordering between two equally wrong predictions. The improvement figures are not repeated in the section.

### A fifty-one fold reduction in compute cost for an estimator that randomises more than the seed, from Accounting for Variance in Machine Learning Benchmarks

- Fields present: hardware and how many of them, absent; precision, absent; batch size, absent; input resolution, absent; framework and version with compile flags, absent; warmup and the statistic reported, partly present as the number of training runs behind each estimate; whether preprocessing and postprocessing are inside the timer, absent.
- Fields missing: six of the seven speed claim fields by name, as listed above. The timer boundary is not declared at all, and what is being counted is training cost rather than inference latency, so preprocessing and postprocessing are outside anything that could be called the timer.
- Verdict: recorded unverified
- Note: this is a ratio between two estimator designs rather than a measurement of a machine, so the seven fields do not fit it and the honest reading is that the ratio is not reproducible from the paper alone. The entry stands on the procedure it recommends, randomising data sampling and initialisation as well as the seed before declaring a gap real.

### Panoptic quality factorises exactly into segmentation quality times recognition quality, with unique matching guaranteed above an overlap of one half, from panopticapi

- Fields present: metric with its full definition; evaluation protocol, specifically the void label, the crowd handling and the segment rejection rule.
- Fields missing: none that applies to a protocol definition.
- Verdict: stands
- Note: verified against the implementation, where the per-class score is the summed overlap of true positives divided by true positives plus half the false positives plus half the false negatives, and where a predicted segment is discarded when more than half of its area falls in void or crowd regions. Because the factorisation is exact, a panoptic quality quoted without its two factors has thrown away the part that says whether the failure was finding the segments or outlining them.

### Boundary overlap is more sensitive to boundary error on large objects without over-penalising small ones, from Boundary IoU

- Fields present: metric with its full definition; dataset with split, three of them; the baseline compared against, mask overlap and trimap overlap.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; evaluation protocol including the non-maximum suppression settings; training data used; hardware.
- Verdict: recorded unverified
- Note: the sensitivity claim is a property of the measure and is demonstrated with model outputs whose own protocol is not fully stated, so the demonstration is not reproducible as published while the measure's definition is. The entry rests on the definition.

### The repeated equivalence that the detection benchmark's average precision at an overlap of one half is the classification benchmark's metric

- Fields present: the metric name, and nothing else.
- Fields missing: metric with its full definition; evaluation protocol, specifically the interpolation rule and the per-image detection cap.
- Verdict: cut
- Note: the two differ in the interpolation rule, sampling at one hundred and one fixed recall points against exact area under the envelope at every unique recall value, and in the detection cap, one hundred per image against none. The fields contradict each other and the protocol as usually quoted is unrecoverable, so the equivalence does not enter the section in any form. It is recorded here because it is the most repeated false statement in this subject and the changelog counts examined numbers.

## Link notes

- https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py - github.com answered 403 to this container because repository access is gated per session, not because the page is missing, so the checker will read BLOCKED rather than DEAD here. Existence of the file at this exact path and ref was confirmed by fetching the same path from raw.githubusercontent.com, which returned 200 and the parameter block quoted in the claims above. The same applies to the three other repository links in the section.
- https://github.com/lvis-dataset/lvis-api - confirmed the same way. The repository README states in its own words that the code is a rewrite of the COCO PythonAPI with LVIS specific changes, which is why both are cited and neither stands in for the other.
- https://github.com/cocodataset/panopticapi - confirmed the same way. Title taken from the repository's own heading with the beta version suffix trimmed per voice.md section 4.
- https://github.com/bowenc0221/boundary-iou-api - confirmed the same way. Its README names a project page on github.io as well; the repository is cited because the repository is the artefact being cited, namely the evaluation code.
- The COCO website structure, and whether a deep link to the evaluation page is stable - the site is a single page whose sections are selected by client-side fragments, among them detection-eval, panoptic-eval, format-data and format-results. A fragment is never sent to the server, so any fetch of such an address verifies only the home page: the address can keep returning 200 long after the fragment stops matching any tab, and a link checker cannot tell the difference. The deep link is therefore stable in form and unverifiable in substance. Two official repositories, cocodataset/panopticapi and bowenc0221/boundary-iou-api, link those exact fragments from their READMEs, in both http and https form, which is good evidence that the form is canonical and no evidence at all that the target still exists. This container's egress policy also refused CONNECT to the host, and the web search budget was exhausted before an independent confirmation could be obtained. The section therefore cites the reference implementation instead, which carries the same parameters in a file that can be diffed, and the website address appears nowhere in the draft.
- https://host.robots.ox.ac.uk/pascal/VOC/voc2007/htmldoc/index.html and https://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html - the host refused CONNECT to this container, so both were confirmed by a search restricted to that domain, which returned each development kit page under its own heading along with the revision note describing the change from interpolated average precision to the area under the precision envelope. One caveat on the scheme. The search index carries the later kit over http and the earlier one over https, and both are cited here over https on the strength of the earlier confirmation, because an http address is fetched outside the proxy and fails as a resolver error, which reads like a dead domain rather than a blocked one. The editor should confirm the scheme from an unblocked network before release.
- https://dhoiem.cs.illinois.edu/projects/detectionAnalysis/ - the authors' own project page, chosen over a course directory copy of the same PDF and over a conference talk recording, both of which are in the rejected block. Not reachable from this container; confirmed by a search that returned this address under the paper's title.
- https://storage.googleapis.com/openimages/web/evaluation.html - reachable from this container, 200, page heading "Open Images evaluation protocols". The only URL in the section this container could fetch directly. The page states in its own words that the protocol is a variant of the earlier all-point average precision at an overlap threshold of one half, with separate handling for non-exhaustive image level labels, for the label hierarchy and for boxes that cover a group of objects, which is exactly the point the entry makes.
- https://arxiv.org/abs/1902.09630 - the authors also host a project page at giou.stanford.edu and the conference proceedings copy sits on the CVF open access site. Neither was reachable from this container. The arXiv abstract page is cited because it carries the version history, per conventions.md section 5; the editor may prefer the project page if it can be fetched.
- arXiv addresses throughout - search returned the PDF form first for several of these papers. The abstract form is cited in every case, per conventions.md section 5, and no PDF address appears in the section.
- https://arxiv.org/abs/1405.0312 - collision with section 4, which owns dataset construction and keeps it. Recorded in the rejected block rather than cited here.
- Collision with section 16 on calibration - section 16 owns probability calibration and reliability. This section's calibration material is confined to the cross-category confidence scaling that moves average precision, which is a property of the metric rather than of the model's probabilities, so the reliability literature is left to section 16 and is not duplicated here.
- Collision with section 11 on tracking metrics - identity aware metrics are section 11's, so nothing here covers them, and the entries above stay on frame level and pixel level measures.
- The Cityscapes benchmark page - not cited, for the reason in the rejected block. If the editor can reach the host, the instance weighted overlap point is worth a fifth entry in the segmentation subsection and would not need to displace anything.

## Benchmark proposal

The claim is that one fixed set of detections, scored under three published average precision
protocols, gives three different numbers, and that the spread is wide enough to change which of
two detectors wins. The three protocols are named exactly: the VOC2007 development kit's mean
of interpolated precision at eleven equally spaced recall levels, where interpolated precision
at a recall level is the maximum precision at any recall at least that high; the VOC2010 to
VOC2012 development kit's exact area under the monotonically decreasing precision envelope,
integrated over every unique recall value with no sampling; and cocoeval.py's mean of the same
monotonised envelope sampled at one hundred and one fixed recall points. The measurement
generates synthetic axis-aligned ground truth boxes and detections from a fixed seed with
numpy.random.default_rng, matches detections to ground truth greedily in descending confidence
order with at most one ground truth per detection and at most one detection per ground truth,
and then applies the three summarisation rules to one identical precision-recall curve. Held
fixed across all three: the ground truth, the detection boxes and their scores, the greedy
matcher, the single category, the single overlap threshold of one half, the absence of ignore,
crowd and difficult flags, and a per-image detection cap raised above the number of detections
so that the cap cannot be the cause of any difference. The only thing varied is how the curve
is summarised. A second row adds cocoeval.py's averaging over ten overlap thresholds, reported
separately so that the threshold averaging is never confounded with the interpolation effect.
The result settles the claim if, from the fixed seed, the three values at the single overlap
threshold differ in the third decimal place or earlier, and if a seeded search over detector
pairs finds at least one pair whose ranking inverts between the eleven point rule and the one
hundred and one point rule, because an inversion is the version of this claim that changes an
engineering decision. Every step is deterministic, so the accuracy numbers must be
bit-identical across runs on the same machine and any run-to-run movement is a bug rather than
noise. The claim is refuted if the three values agree to within one part in a thousand in every
generated regime and no inversion exists. Quick mode evaluates one seed and one detector pair
and finishes well inside ten seconds; the full run sweeps the number of detections per image
and the score distribution, because the eleven point rule is coarsest where recall is sampled
sparsely and the gap should widen there. numpy alone is sufficient, Pillow is not needed since
no image is decoded, and nothing is fetched at run time.
