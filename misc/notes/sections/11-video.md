# 11. Video: temporal modelling and tracking

Owner: video understanding and tracking specialist, suspicious of per-frame metrics presented as tracking quality.

Subsection names are the four the brief specifies, unrenamed. Two ordering decisions are not obvious and are stated here rather than in the shipped block. Under Temporal modelling, optical flow comes first because every later entry either consumes a motion field or argues about what motion field it needed, and brightness constancy is already in place from section 3. Under Video datasets and their protocols, Temporal Segment Networks sits with the datasets rather than with the architectures because its load bearing contribution for this section is the sampling rule, not the network, and the model zoo entry sits last because it only makes sense once a reader knows that a clip sampling rule exists. One title is kept over the soft sixty character ceiling, the multi-camera identity measures paper, because every trim point allowed by voice.md section 4 cuts the words that identify it.

## Section

## 11. Video: temporal modelling and tracking

Nothing in this section is comparable to anything else in it until the clip sampling protocol and the detector behind a tracking number are both stated.

### Temporal modelling

- [RAFT](https://arxiv.org/abs/2003.12039) - Where the motion field that a flow-fed temporal model consumes is actually estimated.
- [Quo Vadis, Action Recognition?](https://arxiv.org/abs/1705.07750) - Why a video backbone starts from image weights inflated along the time axis.
- [A Closer Look at Spatiotemporal Convolutions](https://arxiv.org/abs/1711.11248) - Whether a space-time filter has to be solid or can be split into space and then time.
- [TSM: Temporal Shift Module for Efficient Video Understanding](https://arxiv.org/abs/1811.08383) - Why temporal modelling does not have to cost an extra dimension of convolution.
- [SlowFast Networks for Video Recognition](https://arxiv.org/abs/1812.03982) - Why the rate at which frames are sampled is an architectural choice and not a property of the video.

### Video datasets and their protocols

- [UCF101](https://arxiv.org/abs/1212.0402) - Where the split protocol behind the older action recognition numbers is defined.
- [The Kinetics Human Action Video Dataset](https://arxiv.org/abs/1705.06950) - Why two groups training on the same named benchmark may not hold the same videos.
- [Something-Something](https://arxiv.org/abs/1706.04261) - Where a model that ignores the order of the frames stops scoring well.
- [Temporal Segment Networks](https://arxiv.org/abs/1608.00859) - Where sparse frame sampling and the habit of averaging snippet scores come from.
- [PySlowFast Model Zoo and Baselines](https://raw.githubusercontent.com/facebookresearch/SlowFast/main/MODEL_ZOO.md) - Where the crop and clip count at test time sits beside every accuracy it produced.

### Tracking

- [Simple Online and Realtime Tracking](https://arxiv.org/abs/1602.00763) - Where a tracker reduces to a motion model and one assignment problem solved per frame.
- [Deep SORT](https://arxiv.org/abs/1703.07402) - What an appearance embedding adds to association once box overlap alone stops being enough.
- [Tracking without bells and whistles](https://arxiv.org/abs/1903.05625) - How much of a tracking score belongs to the detector rather than to the tracker.
- [ByteTrack](https://arxiv.org/abs/2110.06864) - Why discarding low scoring boxes costs identity continuity rather than precision.

### Tracking metrics

- [MOT16](https://arxiv.org/abs/1603.00831) - Where the public detection protocol that makes two tracking numbers comparable is defined.
- [Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking](https://arxiv.org/abs/1609.01775) - Where identity is scored over a whole trajectory instead of one frame at a time.
- [HOTA](https://link.springer.com/article/10.1007/s11263-020-01375-2) - Where detection accuracy and association accuracy become two numbers that can disagree.
- [MOTChallenge Official Evaluation Kit](https://raw.githubusercontent.com/JonathonLuiten/TrackEval/master/docs/MOTChallenge-Official/Readme.md) - Where a disagreement about which metric was computed gets settled rather than argued.

## Rejected

- [Observation-Centric SORT](https://arxiv.org/abs/2203.14360) - Rule failed: conventions section 9, three to six entries per subsection. It would have displaced Deep SORT, and Deep SORT stays because every later association scheme is written as a reply to it.
- [FairMOT](https://arxiv.org/abs/2004.01888) - Rule failed: conventions section 7, the speed claim the entry would rest on. The published claim that the entire system reaches thirty frames per second names no hardware, no precision, no batch size and no timer boundary, so joint detection and embedding is asserted to be free rather than shown to be.
- [Is Space-Time Attention All You Need for Video Understanding?](https://arxiv.org/abs/2102.05095) - Rule failed: owner brief section 2, the earlier section keeps a shared source, plus the section 9 size limit. Attention belongs to section 7, and it would have displaced the temporal shift entry, which teaches the same lesson about cheap temporal mixing earlier in the dependency chain.
- [SAM 2](https://arxiv.org/abs/2408.00714) - Rule failed: owner brief section 2, collision with section 10, which owns promptable segmentation and therefore owns this source.
- [X3D](https://arxiv.org/abs/2004.04730) - Rule failed: conventions section 9, size limit. It would have displaced SlowFast Networks, and the efficiency axis it argues about is section 15 material rather than a claim about motion.
- [py-motmetrics](https://raw.githubusercontent.com/cheind/py-motmetrics/master/Readme.md) - Rule failed: conventions section 5, primary sources only. It is a third party reimplementation of metrics whose authors publish their own reference implementation, and the benchmark's own devkit now points at that implementation instead.
- [MOTChallenge results table](https://motchallenge.net/results/2D_MOT_2015/) - Rule failed: conventions section 6, leaderboards and benchmark trackers. The protocol definition is admissible and is cited above; a ranking of submissions under it is a snapshot of a protocol being gamed.
- [MMAction2](https://raw.githubusercontent.com/open-mmlab/mmaction2/main/README.md) - Rule failed: conventions section 5, primary sources only, as applied to the purpose it would serve here. Its model zoo does carry the testing protocol beside each number, but that protocol information is published by the model authors themselves, so the authors' own model zoo is cited instead. It was used only to verify titles and identifiers.

## Claims

### I3D reaches top-one accuracy of seventy-one point one for the RGB stream and seventy-four point two for two streams on the Kinetics test set, as published in the authors' own release

- Fields present: model and exact checkpoint, the released RGB-I3D, Flow-I3D and Two-Stream I3D checkpoints; dataset with split, the Kinetics test split; input resolution and preprocessing, frames sampled at twenty-five per second, short side resized to two hundred and fifty-six with bilinear interpolation, pixel values rescaled to minus one and one, centre crop of two hundred and twenty-four at test; metric with its full definition, top-one and top-five; evaluation protocol, a single centre crop over the whole video with no multi-clip averaging; training data used, Kinetics train with and without ImageNet initialisation reported as separate columns; baseline compared against, the same models without ImageNet initialisation.
- Fields missing: hardware; dataset with version, since the Kinetics copy is not pinned.
- Verdict: recorded unverified.
- Note: The protocol here is one centre crop over whole videos on the test split, while the numbers it is routinely compared against are validation split numbers averaged over thirty views. The two are different measurements of different sets, so the comparison that this number usually appears inside is not a comparison at all.

### SlowFast with a fifty layer backbone at frame length eight and sample rate eight reaches top-one accuracy of seventy-seven on Kinetics-400 under three crops by ten clips, as published in the authors' model zoo

- Fields present: model and exact checkpoint, the linked SlowFast eight by eight checkpoint file; dataset with split, Kinetics-400; metric with its full definition, top-one and top-five; evaluation protocol, three crops by ten clips with frame length and sample rate stated per row; training data used, Kinetics-400 train with no pretraining listed; baseline compared against, the C2D, I3D and Slow rows in the same table trained and evaluated identically.
- Fields missing: hardware; input resolution and preprocessing beyond frame length and sample rate; dataset with version.
- Verdict: recorded unverified.
- Note: The view count is stated, which is the only reason this number is usable at all. Quoted without the three crops by ten clips it becomes a different and unfalsifiable claim, which is how most published video accuracies travel.

### The same X3D checkpoint scores differently at ten views and at thirty views, as published side by side in the authors' model zoo

- Fields present: model and exact checkpoint, one checkpoint per row scored twice; dataset with split, Kinetics-400; metric with its full definition, top-one; evaluation protocol, both view counts named as separate columns; training data used, identical by construction; baseline compared against, the same checkpoint under the other protocol.
- Fields missing: hardware; input resolution and preprocessing beyond frame length and sample rate; dataset with version.
- Verdict: stands.
- Note: Every field that is absent is held fixed across the two columns, so the gap between the ten view and thirty view figures is attributable to the protocol and nothing else. The extra-small, medium and large rows all move in the same direction, each by roughly half a point to a point of top-one. This is the cleanest published demonstration that clip sampling is not a reporting detail, and it is why the model zoo earns an entry.

### Kinetics-400 top-one accuracies are comparable across papers

- Fields present: metric with its full definition; the split name.
- Fields missing: dataset with split and version, and here the version is unrecoverable rather than merely absent; input resolution and preprocessing; evaluation protocol; hardware.
- Verdict: cut.
- Note: Kinetics is distributed as video identifiers rather than videos, and links expire. One maintained framework records its own copy at two hundred and forty thousand four hundred and thirty-six training and nineteen thousand seven hundred and ninety-six validation videos and warns that copies differ; the dataset's own release notes record corrupted files replaced and held-out lists added after publication. Two Kinetics numbers are therefore not measured on the same test set, and no amount of protocol reporting repairs that.

### Tracktor's MOT17 result improved because the detector was retrained, with no conceptual change to the tracker

- Fields present: model and exact checkpoint, the provided MOT17 Faster R-CNN with feature pyramid detector initialised from COCO, plus the re-identification network; dataset with split, MOT17 train and test; metric with its full definition, MOTA, IDF1 and identity switches as computed by the official kit; evaluation protocol, private detections, since the detector was trained by the authors; training data used, the MOT17 detection train set; baseline compared against, the original conference version on its own branch.
- Fields missing: hardware; input resolution and preprocessing.
- Verdict: stands.
- Note: The authors state plainly that the newer figures surpass the published ones because of a newly trained object detector and that the method did not change, and they publish the detector's own average precision on the detection split separately. This is the single most useful admission in the tracking literature for anyone reading a tracking table, and it is why this entry sits before ByteTrack.

### ByteTrack reaches MOTA of ninety and IDF1 of eighty-three point three at twenty-nine point six frames per second, as published in the authors' model zoo

- Fields present: model and exact checkpoint, the extra-large MOT17 checkpoint; dataset with split, evaluated on MOT17 train as the table itself states; metric with its full definition, MOTA, IDF1 and identity switches; training data used, CrowdHuman with MOT17, Cityperson and ETHZ mixed in; baseline compared against, the smaller checkpoints in the same table.
- Fields missing: hardware and how many; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing, the detector forward pass and the association are inside the timer; evaluation protocol detail, including the similarity threshold and which evaluation kit produced the figures.
- Verdict: recorded unverified.
- Note: For the speed half, neither preprocessing nor the detector forward pass is declared as inside or outside the timer, and the published table gives no hardware at all. For the accuracy half, the training data line is most of the claim, because a privately trained detector fed four extra corpora is a detection result reported as a tracking result. The table is also a train split row, while the number people repeat from this work is a test server row, so the two get conflated routinely.

### FairMOT's entire system reaches thirty frames per second under the private detector protocol, with MOTA of seventy-three point seven on the MOT17 test set

- Fields present: model and exact checkpoint, the published backbone checkpoint named as the one that produced the figure; dataset with split, MOT17 test; metric with its full definition, MOTA; evaluation protocol, the private detector protocol on the benchmark's evaluation server; training data used, the named mixture of pedestrian corpora.
- Fields missing: hardware and how many; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer; baseline compared against.
- Verdict: watchlist.
- Note: The entry this number would support is the claim that joint detection and embedding costs nothing, so the entry rests on the number and the number is missing every speed field. Preprocessing and postprocessing are not stated as inside or outside the timer, and a single frame rate for an entire system without hardware is not a measurement.

### MOTA is dominated by detection errors and cannot stand in for association quality

- Fields present: metric with its full definition, including the decomposition into a detection term and an association term; evaluation protocol, since the measure is defined over the matching it specifies; baseline compared against, the existing detection-weighted and identity-weighted measures; the reference implementation, published by the same authors and named as the benchmark's official kit.
- Fields missing: model and exact checkpoint, hardware and training data used do not apply, because the claim is about a metric rather than about a model.
- Verdict: stands.
- Note: This is the claim the whole subsection exists to deliver, and it is checkable by running the published implementation rather than by trusting the paper. It is also the reason a per-frame detection quality metric cannot be reported as tracking quality, which is the claim the benchmark below measures directly.

## Link notes

- https://arxiv.org/abs/2003.12039 - Nothing outside raw.githubusercontent.com is reachable from this container. The proxy's own status endpoint records a gateway refusal to CONNECT for several of the hosts involved, so these are policy denials, not dead pages. The session's WebSearch budget was exhausted by other owners before this section started, so no identifier here was confirmed by search. Every arXiv identifier below was instead confirmed from a primary artefact fetched over raw.githubusercontent.com, where the authors' own file states the title and the identifier together. This identifier comes from the RAFT authors' repository, which links the same identifier as a PDF; the abstract page is cited per conventions section 5.
- https://arxiv.org/abs/1705.07750 - Title and identifier confirmed from the DeepMind I3D repository, which is also where the Kinetics identifier and the I3D accuracy table in the claims block come from.
- https://arxiv.org/abs/1711.11248 - Title and identifier confirmed from the MMAction2 collection metafile, which pairs them explicitly. The authors' own repository links a research.fb.com PDF instead, which is unreachable, and the conference open access page was not confirmable, so the arXiv abstract page is cited.
- https://arxiv.org/abs/1711.07971 - Collision, resolved in favour of the earlier section. Non-local Neural Networks was wanted under Temporal modelling for the moment the locality assumption is dropped, but section 7 has already taken it as an attention operator entry, so under owner brief section 2 the earlier section keeps it and this section picked the temporal shift paper instead. That owner's draft offers the video reading back; it is declined, because a second appearance of one URL is something the conventions prefer to avoid and the replacement teaches a different point rather than the same one twice. The identifier is confirmed from the authors' own non-local video repository and again from the PySlowFast README.
- https://arxiv.org/abs/1811.08383 - Title and identifier confirmed from the MMAction2 collection metafile, which pairs them explicitly. The authors' own repository was not reachable for confirmation under this egress policy, so this identifier rests on a maintained third party assertion rather than on the authors' own file.
- https://arxiv.org/abs/1812.03982 - Confirmed from the PySlowFast README, which is the authors' own repository.
- https://arxiv.org/abs/1212.0402 - Confirmed from the MMAction2 UCF101 preparation document, whose citation gives the title and the arXiv volume. The official host is asserted in two different forms by two primary repositories, as crcv.ucf.edu/data/UCF101.php in one and www.crcv.ucf.edu/research/data-sets/ucf101/ in the other, and neither could be reached, so the dataset report is cited rather than the dataset page.
- https://arxiv.org/abs/1705.06950 - Unstable official page, recorded as instructed. Two primary repositories assert two different DeepMind URLs for the Kinetics page, one of them malformed, and the deepmind.com domain has since moved to deepmind.google. No official Kinetics page is cited because none could be confirmed. The videos themselves are YouTube identifiers that expire, copies are redistributed by a third party foundation, and the dataset's release notes record corrupted files being replaced after publication, so a Kinetics number has no recoverable dataset version.
- https://arxiv.org/abs/1706.04261 - Unstable official page, recorded as instructed. Confirmed from the MMAction2 preparation document, which also states that the dataset's original official site is unavailable and that annotations have to be taken from a third party; the dataset later moved behind a vendor developer portal that requires registration. Only the dataset paper is cited, and the videos are not openly retrievable.
- https://arxiv.org/abs/1608.00859 - Confirmed twice, from the authors' own repository and from the MMAction2 collection metafile.
- https://raw.githubusercontent.com/facebookresearch/SlowFast/main/MODEL_ZOO.md - Raw host used deliberately. Both github.com and api.github.com answer 403 through this session's proxy, while raw file fetches return 200, so this is the only confirmable address for the file. It is the authors' own weight page and it carries the crops by clips column and the separate ten view and thirty view columns that the claims block quotes.
- https://arxiv.org/abs/1602.00763 - Confirmed from the SORT author's own repository, which also supplied the leaderboard URL used in the rejected block.
- https://arxiv.org/abs/1703.07402 - Confirmed from the Deep SORT author's own repository, including the full title in its citation block.
- https://arxiv.org/abs/1903.05625 - Confirmed from the authors' own repository, which is also the source of the detector admission and the MOT17 figures in the claims block.
- https://arxiv.org/abs/2110.06864 - Confirmed from the authors' own repository, which states the title and the identifier together and carries paperswithcode badges that were deliberately not copied into this draft, because the link checker fails the build on aggregator hosts by rule.
- https://arxiv.org/abs/1603.00831 - Confirmed from the reference list of py-motmetrics, which is rejected as an entry but is a maintained repository that states the title and the identifier together. This is the weakest confirmation in the section, because the assertion is not the authors' own.
- https://arxiv.org/abs/1609.01775 - Confirmed from the TrackEval documentation, which names it as the identity metrics paper, and the full title is confirmed from the py-motmetrics reference list.
- https://link.springer.com/article/10.1007/s11263-020-01375-2 - Publisher page preferred over the arXiv version per conventions section 5, because the authors' own reference implementation names this as the open access journal version and lists the arXiv deposit second. The host refuses this container entirely. If the journal page ever stops being openly readable, the fallback is the arXiv abstract page that the same README names.
- https://raw.githubusercontent.com/JonathonLuiten/TrackEval/master/docs/MOTChallenge-Official/Readme.md - Raw host used for the same reason as the model zoo file. This document states that this codebase is now the official evaluation kit for the benchmark, names the metric families it computes and names the splits, and it replaces an earlier devkit that now redirects readers to it.
- https://motchallenge.net/results/2D_MOT_2015/ - Appears only in the rejected block, as a leaderboard. The URL is confirmed from the SORT author's own repository. The host is unreachable from here, which the link checker will report as blocked or unreachable rather than dead.
- https://arxiv.org/abs/2009.07736 - Not cited as an entry, recorded here as the fallback for the HOTA journal page.
- Left out for lack of a confirmable URL: the original two-stream action recognition paper, which was wanted as the first entry under Temporal modelling. It has no authors' repository, its proceedings host and arXiv are both unreachable, and no primary artefact in reach states its identifier, so it was not guessed. Its ground is partly covered by the inflated two-stream entry that follows.
- Left out for lack of a confirmable URL: the CLEAR MOT metrics paper, which is where MOTA and MOTP are originally defined. The open access journal article could not be confirmed from any primary artefact in reach. MOTA and MOTP as the benchmark actually computes them are reached instead through the benchmark paper and the official evaluation kit, which is arguably the better citation for an engineer but is recorded here as a substitution rather than a preference.
- Left out for lack of a confirmable URL: HMDB51, whose only official host is a university laboratory page that could not be confirmed. It is half of the classic action recognition protocol and its absence is a real gap in the datasets subsection.
- Checker outcome for this draft, recorded as required: twenty-three unreachable, four reached, zero dead, zero mirror and zero redirect. Every unreachable result is the same gateway refusal to CONNECT, and the four that were reached are the raw repository files. The script's blocked category never fires here because the refusal happens at the tunnel rather than at the origin, so a reviewer re-running this from an unrestricted network should expect those twenty-three to come back as reached or redirected.
- Section collisions flagged: promptable video segmentation belongs to section 10, video attention architectures belong to section 7, and the efficiency framing of video backbones belongs to section 15.

## Benchmark proposal

Per-frame detection accuracy can rise while identity consistency falls, so a per-frame metric
cannot stand in for tracking quality. The measurement generates a deterministic synthetic
sequence from a fixed seed, with several boxes on linear trajectories that cross, then sweeps a
family of synthetic trackers indexed by one parameter that raises per-frame recall, by emitting
more correct boxes and fewer misses, while also raising the identity swap rate at those
crossings. Each output is scored twice from the same intersection over union matching at a fixed
threshold, with a greedy assignment in numpy: once with per-frame precision, recall and their
harmonic mean plus MOTA, whose identity switch term is a raw count divided by the number of
ground truth boxes; and once with IDF1 and with the detection and association terms of the
higher order metric computed separately. Pillow renders a contact sheet of a few frames with
boxes and identity colours, so the swap is visible rather than asserted. The claim is settled if
per-frame accuracy and MOTA both rise monotonically across the sweep while IDF1 and the
association term fall, and the detection term rises in the same run in which the association
term falls. It is refuted if IDF1 tracks per-frame accuracy within run to run noise, which for
bit-identical synthetic data means exactly. Quick mode uses a short sequence and few
trajectories, needs no network, and finishes in under ten seconds, with accuracy outputs
identical across runs.
