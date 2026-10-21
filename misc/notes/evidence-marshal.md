# Evidence marshal

The evidence marshal applies misc/notes/conventions.md section 7 to every number examined in the
section drafts, and has a veto: an entry can be sent to the watchlist or cut, and the owner does
not get to argue the number back in. This file is the record of every ruling.

## Round one

Rulings: 171. Verdicts: stands 13, recorded unverified 78, watchlist 39, cut 41.
Entry actions: none 132, move to watchlist 30, cut entry 9.

How the editor applied the vetoes. Where the source's lasting value is the measured outcome,
the veto was applied as ruled. Where the value is a mechanism, definition or procedure the source
genuinely contains, the reason line was rewritten so the entry no longer rests on the number,
and the number stays unverified. Every such rewrite went back to the marshal for a second
ruling, recorded below under the recheck, and the marshal's second ruling is final.

### Section 1

- The sRGB transfer function is a single power law with an exponent of two point two (repeated around item one)
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The quoted single exponent contradicts the definition it is attributed to: the curve is piecewise, with a linear segment near black and an offset power segment. Fields contradict, so the claim is cut. Item one (the radiance map paper) does not cite this source. The only README entry that does is the section 2 Colour entry. Its reason says the opposite of the claim ...

- The camera response curve is recoverable from differently exposed photographs only up to one global scale factor (radiance map paper, item one)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, hardware, baseline compared against (demonstrating on film and on digital is not a baseline).
  - Reasoning: A claim stands only when every field is present. The owner lists four fields as absent or not applicable, and an identifiability argument does not exempt a claim from the ladder. Item one's reason ('recovered rather than assumed') and the section 2 reason ('not radiance until the response curve has been recovered') rest on recoverability, not on how many scale factors ...

- Classification improvement over the earlier convolutional model in the feature visualisation paper (item five)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing per reported row, hardware.
  - Reasoning: No checkpoint was released, and rows mix crop and ensemble variants. Item five's reason ('What a learned filter responds to, shown instead of asserted') rests on the visualisation method, which a reader can inspect. It does not rest on the error figure.

- Convolutional networks fit randomly labelled training data to zero training error (item seven)
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The claim's own dataset field names both the small image corpus and the ImageNet training split. In the paper's ImageNet table the random-label rows stop short of full training accuracy (best row about ninety-five per cent top-one, lower with regularisers). Only the CIFAR rows reach zero error. The number contradicts its own dataset field, so the claim is cut. Item seven's ...

- Human top-five error figure from the challenge paper (item six)
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: none.
  - Missing fields: model and exact checkpoint (an annotator cannot be re-run), input resolution and preprocessing, training data used (the annotator's practice set), hardware.
  - Reasoning: Only the group that ran the annotation can reproduce the figure, so the ladder caps it at watchlist. The owner lists the baseline as missing, but it is present: the paper scores a named network on the same sampled images. Item six's reason (task definition and scoring rule) does not rest on the figure. Nor does the section 4 reason for the same URL (how the label rule was ...

- Latency comparisons in the efficient design paper, including the mobile rows (item nine); also the implicit speed claim in its reason line 'counted operations do not predict latency'
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: precision, framework and version with compile flags (only cuDNN 7.0 is named; the ARM runtime is an in-house Neon implementation outsiders cannot run), warmup and the statistic reported (mean of a hundred runs, no warmup or dispersion stated), whether preprocessing and postprocessing are inside the timer.
  - Reasoning: Two of the owner's fields are wrong. The paper names the hardware (one GTX 1080Ti, and a Snapdragon 810 on a single thread) and states batch sizes (eight on GPU, one on ARM), input resolution and the mean over a hundred runs. Precision, framework flags, warmup and the timer boundary are still missing. The owner's 'forward pass alone' is an inference, not a stated field. The ...

- Re-scored validation accuracy against the reassessed labels (item eight)
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint for each re-scored classifier, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation, training data used, hardware.
  - Reasoning: The source is cited twice. Section 1 item eight ('What the single label per image assumption hides when a picture holds several objects') rests on multi-label images existing. The released label file shows this directly: of 50000 lists, 7443 carry several labels. So item eight does not rest on the accuracy figure. The section 4 entry ('Why relabelling a validation set ...

- Accuracy drop on the rebuilt test set, from the paper rejected for the size limit
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: dataset with split and version (which of the new test set variants the drop is quoted for; the magnitude depends on the variant), model and exact checkpoint (the section 1 and section 4 drafts disagree on whether it is pinned; not established), input resolution and preprocessing per model, evaluation protocol including single-scale or test-time augmentation, hardware.
  - Reasoning: The paper is rejected only from Start here. The README carries it in section 4, and the section 4 reason ('What a fresh test set built to the original recipe does to published accuracy') has the measured accuracy effect as its whole subject. It rests on this number. With fields missing, the claim goes to the watchlist and the section 4 entry moves. Same number as the ...

### Section 2

- Peak signal to noise ratio gain over bilinear demosaicing, quoted on the research listing
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, training data used, hardware, model and exact checkpoint.
  - Reasoning: The reason ('Where the linear demosaicing baseline that later methods are measured against is specified') is about provenance and adoption, not the gain. Fields are missing and the entry does not rest on the number.

- Raw-frame noise is Poissonian-Gaussian with variance affine in the signal and two parameters sufficient to describe it
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, dataset with split and version (sensor, gain, exposure and temperature behind the example raw data not fully specified), metric with its full definition (no goodness-of-fit criterion for 'sufficient'), baseline compared against.
  - Reasoning: The owner concedes that the hardware and the acquisition conditions are missing, and the ladder grants stands only when every field is present. 'Two parameters sufficient' is an empirical adequacy claim, not a derivation. It also holds only below clipping, where the source itself models the observed variance as non-affine. The reason ('noise in a raw frame depends on the ...

- A denoiser trained on noise synthesised by inverting the pipeline outperforms one trained on noise added after processing; also the implicit claim in the reason line 'have to be inverted before processed images can ...
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: hardware, evaluation protocol including single-scale or test-time augmentation, and the ablation condition behind each removed stage.
  - Reasoning: The owner lists the checkpoint as missing, but the authors' repository (fetched over raw.githubusercontent.com) names a released checkpoint file. The benchmark, training corpus and metric are present. Hardware and the comparison protocol are not established from anything reachable, and the burden of proof sits with the entry. The README reason makes sense only if training ...

- The burst pipeline produces a finished twelve megapixel image in about four seconds on device
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: none.
  - Missing fields: hardware and how many of them (handset not named), precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The listing confirms the figure. The timed artefact is the vendor's closed on-device implementation, so only the authors can rerun this timing, which caps the claim at watchlist. This matches the owner's own treatment of the ShuffleNet ARM rows. The entry's reason ('What a shipped pipeline does instead of one exposure and one denoiser') does not rest on the time.

- The pipeline operates down to about three tenths of a lux
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: none.
  - Missing fields: metric with its full definition (what 'operates' means), evaluation protocol (where and how illuminance was measured, metering), dataset with split and version (no public capture set), hardware and count.
  - Reasoning: The figure and the unaided-vision baseline come from the very-low-light paper, which section 2 rejects and the README carries on the watchlist. The burst photography entry beside it does not carry them. A closed pipeline on one vendor's handsets with no capture set can be reproduced only by the authors, so the claim is capped at watchlist. The watchlist line's reason (a ...

- The sRGB encoding is a power law with an exponent of two point two
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The claim contradicts the cited definition (piecewise, linear segment near black, exponent two point four on an offset segment), so it is cut. The Colour entry's reason states the piecewise definition, which is the opposite of the claim, so it does not rest on the cut number.

- A camera has a given number of stops of dynamic range, as quoted in vendor material
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: metric with its full definition, evaluation protocol, hardware, measurement conditions the sensor standard requires.
  - Reasoning: The vendor material gives a bare figure with no protocol, and none can be recovered from it, so the claim is cut. No README entry cites vendor material. The EMVA entry rests on the standard's definitions, not on any vendor figure.

- Implicit in README reason line: joint demosaicking and denoising outperforms separate stages once the raw frame is noisy ('Why demosaicing and denoising stop being separate stages once the raw frame is noisy')
  - Owner's verdict: not examined by owner. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: dataset with split and version for the noisy comparison, input resolution and preprocessing, evaluation protocol including the noise model and levels, and whether sequential baselines were given the true noise level, hardware.
  - Reasoning: 'Stop being separate stages' is a design conclusion that holds only if joint processing measurably beats a sequential pipeline on noisy data, so it is a performance claim with no number stated. A noise-aware checkpoint exists only as a pre-trained model in the authors' deprecated Caffe repository. The maintained implementation's README (fetched) says it does not implement ...

### Section 3

- SIFT keypoints match reliably under scale, rotation, noise and viewpoint change
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: dataset with split and version, input resolution and preprocessing, model and exact checkpoint, hardware.
  - Reasoning: The reason ('the descriptor and the ratio test most matching pipelines still default to') is about provenance and adoption, not a repeatability figure.

- SuperGlue sets the best indoor and outdoor pose estimation among matching methods
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The fields contradict each other. The authors' repository README (fetched) says the released code and models were tweaked after the paper and give different numbers from those reported. It also says the paper's outdoor results used uncorrected EXIF rotations while the release corrects them. The released weights the owner counts as 'exact checkpoint' are therefore not the ...

- SuperGlue runs in real time on a modern GPU
  - Owner's verdict: cut. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, batch size, input resolution (timed setting given only in an unread appendix), framework and version with compile flags, warmup and the statistic reported (average only, no warmup or dispersion), whether preprocessing and postprocessing are inside the timer (keypoint detection, decode and resize, and the downstream robust estimator).
  - Reasoning: The owner says no fields are present and the protocol cannot be recovered. That is wrong: the paper names one GTX 1080, gives an average per-pair forward time for indoor pairs, and points to an appendix for the breakdown. The protocol can be partly recovered, so the claim is not cut. Fields are missing and the entry does not rest on the timing, so it is recorded unverified. ...

- LoFTR outperforms prior matching methods by a large margin on indoor and outdoor pose
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: none.
  - Missing fields: evaluation protocol: whether every compared matcher was scored with the same robust estimator and threshold, training data used (split not stated), hardware.
  - Reasoning: The owner says resolution and estimator settings are unpinned, but the release pins them (config fetched: RANSAC at half a pixel, confidence 0.99999, MegaDepth test resize 840). The SuperGlue release pins one pixel, and nothing reachable shows the baseline rows were rerun at LoFTR's setting. A later paper (LightGlue) reports that tuning the threshold per method moves ...

- Locally optimised RANSAC gives a two to three fold speed-up and ten to twenty per cent more inliers; also the implicit claim in the reason line 'worth refining inside the sampling loop rather than after it'
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: dataset with split and version (image pairs and their inlier ratios), input resolution and preprocessing, metric with its full definition (inlier threshold), hardware, hardware and how many of them, precision, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer, including whether the local optimisation's own cost is counted.
  - Reasoning: The abstract's wording is confirmed by search. 'Worth refining inside the loop rather than after it' is a cost-benefit claim, and it makes sense only if in-loop refinement pays for itself in samples and inliers, which is this number. The owner says the entry rests on the step 'being worth running', which is the number with the digits removed. The same group's later work ...

- MAGSAC++ is often an order of magnitude faster than its predecessor and more geometrically accurate
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: dataset split and version, input resolution and preprocessing, metric with its full definition, hardware, hardware and how many of them, precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer (correspondence generation excluded).
  - Reasoning: The wording matches the published abstract. The reason ('What a robust estimator scores with once the inlier threshold is marginalised away') is a mechanism and does not rest on the ratio.

- Well-tuned classical local features remain competitive with learned matchers once camera pose is the metric (Image Matching across Wide Baselines); also the implicit claim in the reason line 'Whether a learned ...
  - Owner's verdict: stands. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: hardware, dataset with split and version: test-split ground truth is held privately by the organisers, so the test figures can be reproduced only by the authors.
  - Reasoning: The owner argues away the missing hardware field. The ladder allows no such appeal, so the claim cannot stand. The benchmark repository README (fetched) states that test submissions 'are processed on a private test set, for which we provide images, but not the ground truth'. Only the authors can reproduce the test-set comparison, which caps it at watchlist. The README ...

- A planar pattern observed in at least two orientations suffices to recover the intrinsics
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: dataset with split and version, input resolution and preprocessing, model and exact checkpoint, training data used, hardware, evaluation protocol: two views suffice only with the skew fixed at zero, otherwise three are needed.
  - Reasoning: The owner says the entry can rest on this claim while recording it unverified. Under the ladder those two cannot hold together. What decides it is the README reason ('Where the planar calibration procedure almost every toolbox implements was specified'), which is about provenance and does not rest on the view count. The claim is therefore recorded unverified. The claim also ...

- Implicit in README reason line: a learned matcher wins on pose under the published protocols (presupposed by 'still wins')
  - Owner's verdict: not examined by owner. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: 'Still wins' presupposes the learned-matcher pose gains reported by SuperGlue and LoFTR. The SuperGlue figure is cut above because the released artefacts contradict it. The LoFTR comparison has unequal estimator settings across rows. The presupposed gain is not a usable number. The line uses it only as a report of what was published, and the entry's question still makes ...

- Watchlist line (LoFTR): 'pose gains that hinge on unstated estimator settings'
  - Owner's verdict: not examined in scope. Marshal: watchlist. Entry action: none.
  - Missing fields: evaluation protocol (robust estimator and threshold).
  - Reasoning: 'Gains' is a claim that it beats other matchers, smuggled into the line. The line already sits on the watchlist and its condition names the missing field, which is consistent with the ladder.

### Section 4

- About three per cent of test labels are wrong across ten test sets and about six per cent on the ImageNet validation split (Pervasive Label Errors)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, metric with its full definition, evaluation protocol including single-scale or test-time augmentation, hardware.
  - Reasoning: The figures are lower bounds produced by a flagging model plus crowd adjudication. The entry's reason is about rankings, not the error rate, so it does not rest on this number. The entry moves on the ranking claim instead.

- Correcting the test labels flips the ranking of two residual network sizes once the mislabelled share rises (Pervasive Label Errors)
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation, and how the mislabelled share is raised, training data used, including whether either model was retrained, hardware.
  - Reasoning: The owner watchlists the claim but keeps the entry, saying it rests on the audit procedure. The README reason is 'What happens to a benchmark ranking once the test labels themselves are corrected', which is about the ranking, not the procedure, and the ranking outcome is this number. Keeping the entry while holding back the number it is cited for is the softening the ladder ...

- Recent classifiers gain substantially less under reassessed multi-label labels than under the original ones (Are we done with ImageNet?)
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint for the full comparison set, input resolution and preprocessing per model, evaluation protocol including single-scale or test-time augmentation, and whether label-less images were excluded, hardware.
  - Reasoning: The section 4 reason 'Why relabelling a validation set changes which models look like they improved' asserts this accuracy outcome as fact, so it makes sense only if the number is true. The entry rests on it, and fields are missing, so the section 4 entry moves to the watchlist. Section 1 item eight cites the same URL with a reason about multi-object labels and is unaffected.

- A fresh ImageNet test set built to the original protocol costs every model eleven to fourteen points of top-one accuracy (Do ImageNet Classifiers Generalize to ImageNet?)
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: dataset with split and version (which new test set variant; the drop differs by variant), input resolution and preprocessing per model, evaluation protocol including single-scale or test-time augmentation, hardware.
  - Reasoning: The reason 'What a fresh test set built to the original recipe does to published accuracy' has the measured accuracy effect as its whole subject, so the entry rests on this number. The owner's note keeps the figure out of the line but does not change what the line rests on. Fields are missing, so the entry moves to the watchlist.

- Only about a third of the replication gap survives correction for selection-frequency bias (Identifying Statistical Bias in Dataset Replication)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint for the full model sweep, input resolution and preprocessing, hardware.
  - Reasoning: The reason 'Why a replacement split that looks harder may be measuring its own construction' names the selection-bias mechanism and claims only a possibility. It holds whatever the corrected magnitude, so it does not rest on the number.

- Three per cent of CIFAR-10 and ten per cent of CIFAR-100 test images have training duplicates, and replacing them costs nine to fourteen per cent relative accuracy (Do We Train on Test Data?)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint (retrieval network and evaluated classifiers), input resolution and preprocessing, metric with its full definition (near-duplicate judged by human inspection with no reproducible threshold), evaluation protocol including single-scale or test-time augmentation, hardware.
  - Reasoning: The reason ('Where test images turn out to have near duplicates sitting in the training split') rests on duplicates existing. A reader can check that by inspecting the released duplicate pairs, with no measurement protocol needed. The reason does not rest on the rate or on the accuracy drop.

- About three and a half thousand ImageNet validation images carry no reassessed label (framework dataset catalogue entry)
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The fields contradict each other. The authors' released label file (fetched over raw.githubusercontent.com) holds exactly 3163 empty lists out of 50000, not about 3500. The catalogue's citation file also points at arXiv:2002.05709, a different paper. No README entry cites the catalogue. Neither entry for the reassessed-label paper rests on the count.

### Section 5

- COCO average precision averages ten overlap thresholds (0.50 to 0.95 step 0.05) and samples 101 recall points on a monotonised precision envelope, from cocoeval.py
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Checked against cocoeval.py at master, fetched from raw.githubusercontent.com (200). setDetParams sets iouThrs to linspace(.5,.95,10), recThrs to linspace(0,1,101), four areaRng and maxDets [1,10,100]. accumulate() makes precision monotone with the backward sweep (for i in range(nd-1,0,-1)) and only then samples at recThrs. This is a protocol definition read from the ...

- COCO detections are capped at one hundred per image, from cocoeval.py (the cap component of the same claim)
  - Owner's verdict: stands. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: With useCats=1, evaluate() calls computeIoU and evaluateImg once per (imgId, catId), and each one truncates dt to maxDets[-1]. The cap is therefore one hundred per image per category, not one hundred per image. The file's own docstring says 'per image', which contradicts its code, and the draft copied the docstring. As worded the claim contradicts the implementation it ...

- An LVIS average precision and a COCO one are not comparable because the per-image detection cap differs, from lvis-api and cocoapi
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Both implementations were checked from raw.githubusercontent.com. lvis/eval.py Params uses the same iou_thrs and rec_thrs as cocoeval.py. lvis/results.py limit_dets_per_image keeps 300 detections per image across all categories. LVIS evaluates only the categories on each image's positive and negative lists, ignores false positives in not_exhaustive_category_ids, and bins ...

- Calibrating detector confidence across categories raises pooled AP by 1.7 points on LVIS, from Evaluating Large-Vocabulary Object Detectors
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation and NMS settings, training data used, hardware.
  - Reasoning: The figure is the abstract's gain on the paper's AP-pool from explicit calibration. The owner read only the abstract, and the experimental fields are not recorded. The reason line rests on the mechanism: under a per-image cap, the default AP moves when only the ranking of confidences across categories changes. The paper shows this by construction. The entry does not rest on ...

- Generalised IoU used as a regression loss improves detectors on PASCAL VOC and COCO, from Generalized Intersection over Union
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation and NMS settings, training data used, hardware.
  - Reasoning: The editor dropped this source from README section 5, and it now appears only in section 8 (Objectives). That entry rests on an analytic point: IoU is identically zero, and flat, for disjoint boxes. No measurement is needed for that. The improvement figures are not used. A fact for the editor, not a number: the section 8 reason line says 'a box loss that is not the box ...

- A fifty-one fold reduction in compute cost for an estimator that randomises more than the seed, from Accounting for Variance in Machine Learning Benchmarks
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: unit of cost and number of trainings counted per estimator, hyperparameter optimisation budget behind each estimator, task and dataset the ratio was computed on.
  - Reasoning: The ratio counts training runs across two estimator designs. It is not a timed measurement, so the seven speed fields do not describe it. The record's 'Fields present' line lists only absences, which leaves the claim with no field inventory at all. Nothing that would make the ratio checkable is recorded. The owner's statement that the ratio cannot be reproduced from the ...

- Panoptic quality factorises exactly into segmentation quality times recognition quality, with matching above an overlap of one half, from panopticapi
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Checked against panopticapi/evaluation.py from raw.githubusercontent.com. pq = iou/(tp+0.5fp+0.5fn), sq = iou/tp and rq = tp/(tp+0.5fp+0.5fn), so pq = sq*rq exactly, and all three are zero when tp is zero. A match requires iou > 0.5, where the union excludes the prediction's overlap with VOID. An unmatched prediction is ignored when its VOID plus same-class crowd overlap ...

- Boundary IoU is more sensitive to boundary error on large objects without over-penalising small ones, from Boundary IoU
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol including NMS settings, training data used, hardware.
  - Reasoning: The sensitivity demonstration's fields are not inventoried. The reason line rests on the definition: mask IoU is dominated by interior pixels as object size grows, so a worse boundary can coexist with a higher mask score. That is analytic, and the implementation is public in the Boundary IoU API. No figure is used.

- The repeated equivalence that COCO AP at IoU 0.5 is the PASCAL VOC metric
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Confirmed false. The two protocols differ in interpolation: 101 fixed recall points in cocoeval.py against every-recall-change in VOC2010 to VOC2012, or 11 points in VOC2007. They differ in the cap: COCO keeps 100 per image per category (not per image, as the note says), and VOC has no cap. They differ in ignore handling: VOC difficult flags against COCO crowd and area ...

- Implicit in README reason line for the VOC2012 devkit: the same detections score differently once 11-point interpolation is replaced by the precision envelope area
  - Owner's verdict: not examined. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The line asserts that scores differ. misc/benchmarks/05-average-precision-protocols measured this on one fixed, seeded detection set, with all eight accuracy fields and all seven speed fields stated: 77.97 for 11-point, 80.07 for all-point and 79.88 for 101-point, all at IoU 0.5. The entry rests on a number with every field present.

### Section 6

- Top-five error reported for the residual network ensemble, in Deep Residual Learning for Image Recognition
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint for each ensemble member, hardware (GPU model), evaluation protocol for the test-server entry.
  - Reasoning: The authors' repository, KaimingHe/deep-residual-networks (README fetched), releases single ResNet-50/101/152 Caffe models, not the ensemble, and says only '8 GPUs' with no model. The entry does not rest on the ensemble figure. The owner rests the entry on the degradation experiment instead, and that is ruled separately below.

- Implicit in README reason line: adding layers to a residual network stopped making training error worse (the degradation experiment, Fig. 4 and Table 2, 18/34-layer plain against residual), in Deep Residual Learning ...
  - Owner's verdict: not examined; owner asserts the entry rests on it and that it is reproducible. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, hardware.
  - Reasoning: 'Why adding layers stopped making training error worse' only makes sense if the measured comparison is true. The owner's note itself rests the entry there, with no field inventory. Present: architectures (Table 1), ImageNet 2012 train and val, 224 crops with scale and colour augmentation, top-1 error under 10-crop testing, training data, and a baseline plain net of equal ...

- Top-five error reported in ImageNet Classification with Deep Convolutional Neural Networks
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint.
  - Reasoning: The authors released no trained weights. The rows are stated row by row: single net or ensemble, 1 or 10 crops, and two ensemble members pretrained on the Fall 2011 release. That is a stated variation, not a missing protocol. 'Displaced' in the reason line refers to the field's later practice, which can be observed without this number, and 'how much of that was recipe' asks ...

- Width beating depth at matched parameter count, in Wide Residual Networks
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, input resolution and preprocessing for the large-scale rows.
  - Reasoning: The reason line is a question ('Whether depth or width was carrying the gain'), and it makes sense whatever the answer. The entry rests on the controlled design of moving one variable and holding the other, not on the figure.

- Compound scaling top-one accuracy on ImageNet, in EfficientNet
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: baseline compared against under the same recipe.
  - Reasoning: The headline B7 figure is 84.4 in arXiv v1 and the ICML version, and 84.3 in the current arXiv abstract, which is the page the README cites. No change of protocol is recorded. Two values for one claim, plus the unmatched baseline the owner already names, is the contradiction rung, so the claim is cut. The reason line names the recipe confound and does not rest on the number.

- Inference speedup over the compared scaled model (GPipe), in EfficientNet
  - Owner's verdict: cut. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The owner's cut depends on 'no batch size', but the caption of Table 4 states batch size 1 on a single core of an Intel Xeon E5-2690. Hardware, count, batch size, per-variant resolution and baseline are all present, so the protocol is partly stated and is not unrecoverable, and the cut rung does not apply. Fields are missing and the entry does not rest on speed, so the ...

- Measured latency disagreeing with FLOP count, in ShuffleNet V2
  - Owner's verdict: stands. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: warmup and the statistic reported, framework and version with compile flags, precision, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The owner ruled 'stands' while listing two missing fields, but stands requires every field. Independently, these are present: a GTX 1080Ti with cuDNN 7.0 at batch 8, and a Snapdragon 810 on a single thread at batch 1, both at 224 input. Not stated: warmup and the statistic behind batches per second, precision, and a named framework with version. The ARM half runs on an ...

- Recipe gain on the residual baseline (75.3 to 79.29 top-1), in Bag of Tricks for Image Classification
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, model and exact checkpoint (not confirmed).
  - Reasoning: The reason line rests on the ablation design, one change at a time against a retrained baseline. It does not rest on the end point.

- Owner's note under Bag of Tricks: the recipe's end point exceeds what a much deeper member of the same family reported under the older recipe
  - Owner's verdict: none given (stated in the note as fact). Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: This compares 79.29 top-1 (a single 224 centre crop from the authors' own retrained run) with a deeper network's figure as published in Deep Residual Learning. That paper reports ResNet-152 at 21.43 top-1 error under 10-crop testing (Table 3) and 19.38 under its single-model multi-scale protocol (Table 4). Whether the end point 'exceeds' depends on which protocol is picked, ...

- Top-one accuracy of the unchanged ResNet-50 under the newer procedure (80.4 at 224), in ResNet strikes back
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The owner recorded hardware as missing, but the paper states it: A1 runs 600 epochs and takes 110 hours (4.6 days) on one node of four V100 32GB GPUs. The checkpoints are published in timm (resnet50.a1_in1k and siblings). The architecture is unchanged, the data is ImageNet-1k only, train and test resolution are stated, and the baseline is the same architecture. All eight ...

- On-device latency reported for the searched mobile family, in Searching for MobileNetV3
  - Owner's verdict: watchlist. Marshal: cut. Entry action: none.
  - Missing fields: batch size, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: Measured on a single large core of a Pixel phone with the TFLite benchmark tool. Batch size, warmup and statistic, and the timer boundary are not stated. The headline latency reduction against MobileNetV2 also reads 15 percent in one deposited version and 20 percent in arXiv v4 and the ICCV version, with no change of protocol recorded. That is two values for one claim, so ...

- Implicit in README reason line: the order of normalisation, activation and addition changes what trains (pre-activation against post-activation units), in Identity Mappings in Deep Residual Networks
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, hardware.
  - Reasoning: 'Changes what trains' asserts a measured outcome: lower error and trainability at 1001 layers for the pre-activation unit under the same recipe. It only makes sense if that outcome is true. The paper's experiments ran in Caffe. The authors' repository, KaimingHe/resnet-1k-layers (README fetched), is a Torch re-implementation that releases code and no weights, and it points ...

- Implicit in README reason line: what the residual network family reaches when only the recipe and the scaling rule move, in Revisiting ResNets
  - Owner's verdict: not examined. Marshal: cut. Entry action: cut entry.
  - Missing fields: none named.
  - Reasoning: The line's protocol premise is that the architecture is held fixed. The source's own abstract says it improves the canonical ResNet with 'modern training methods, minor architectural changes and improved scaling strategies'. The ResNet-RS family adds squeeze-and-excitation and the ResNet-D stem, which is part of its additive ablation from 79.0 to 83.4. The reason only makes ...

- Implicit in README reason line: what a convolutional stack reaches once the newer recipe is held equal across the comparison, in A ConvNet for the 2020s
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: all eight accuracy fields (never inventoried in any draft).
  - Reasoning: The line asks what the stack reaches and does not assert a value. Its protocol premise matches the source's central design, a roadmap from a residual baseline retrained under the new recipe, so the premise is not contradicted. The accuracy figures were never inventoried and must not be repeated.

- Implicit in README reason line: the depthwise separable convolution replaced the mixed branch block (Xception against Inception V3 on ImageNet and JFT), in Xception
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: training data used (JFT half is a private corpus), model and exact checkpoint (not inventoried).
  - Reasoning: The replacement is the paper's own design move and the field's later practice, both observable without the accuracy margin. The line does not assert that the replacement scored higher. The JFT half of the margin can be reproduced only by the authors, and the ImageNet half was never inventoried.

### Section 7

- Top-one accuracy of the largest ViT after pretraining on a private corpus, in An Image is Worth 16x16 Words
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, training data used (JFT-300M is private).
  - Reasoning: The number can be reproduced only by the authors on a corpus nobody else holds, which is the watchlist-at-best rung. That rung matters only when the entry rests on the number, and this entry rests on the architecture: patches replace the convolutional stem.

- Top-one accuracy with the public thousand-class corpus alone, and with a distillation token, in Training data-efficient image transformers
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: baseline compared against, matched (CNN rows quoted from their own papers).
  - Reasoning: The reason line ('What distillation and augmentation buy') concerns the internal comparison, DeiT with and against without distillation under one recipe, with released checkpoints. The unmatched comparison against CNNs is the part that fails, and the entry does not rest on it.

- Headline ImageNet and COCO numbers of the hierarchical windowed design, in Swin Transformer
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: evaluation protocol: NMS settings for the HTC++ multi-scale detection headline.
  - Reasoning: The record lists 'training data used' as both present and missing. The paper does state ImageNet-22K pretraining for the classification headline; the field is misquoted by others, not missing from the source. The detection headline lacks NMS settings. The entry rests on the complexity argument, ruled separately, not on the headlines.

- A fully self-attentional network beating its residual baseline at lower FLOPs and parameters, in Stand-Alone Self-Attention in Vision Models
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: none.
  - Missing fields: model and exact checkpoint, hardware.
  - Reasoning: This is an accuracy claim at a stated FLOP and parameter budget. FLOPs are not a timed measurement, so the speed fields in the owner's list do not apply. The entry already sits on the README watchlist, and its promotion condition names released weights. Hardware is the other missing field and the line does not name it.

- Regularisation and augmentation substituting for roughly an order of magnitude more pretraining data, in How to train your ViT?
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: training data used (JFT-300M counterpart arm is private).
  - Reasoning: The vision_transformer README (fetched) confirms that over 50k AugReg checkpoints on ImageNet-21k and ImageNet-1k are public, so the trade-off under one protocol on public data is checkable. Only the JFT-300M comparison can be reproduced by the authors alone, and the reason line does not need it.

- A plain ViT reaching ResNet-level top-one accuracy in a stated epoch budget (76.5 at 90 epochs, 6 to 7 hours on TPUv3-8), in Better plain ViT baselines for ImageNet-1k
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, baseline compared against, matched (ResNet-50 90-epoch figure not rerun under the same augmentation).
  - Reasoning: The owner recorded no missing fields, but the big_vision README lists only a config (vit_s16_i1k.py) for this paper and no checkpoint. The config's docstring confirms 6 to 7 hours on TPU-v3-8 and 76.5%. The ResNet-level comparison uses a conventional baseline that was not retrained, which is the matched-baseline failure the owner applied to DeiT and MetaFormer. So the claim ...

- Accuracy of the convolution and attention hybrid across three pretraining corpora, in CoAtNet
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, training data used (JFT-3B arm is private), hardware and epoch count per number.
  - Reasoning: The owner records checkpoints as present for the public arms. No CoAtNet code or weights from the authors could be found; only timm's own-trained coatnet_rw variants and MaxViT checkpoints exist, and those are different models. The reason line ('What stacking convolution underneath attention changes as the pretraining corpus grows') rests entirely on this corpus sweep. A ...

- A pooling token mixer matching attention baselines at lower parameter and MAC counts, in MetaFormer Is Actually What You Need for Vision
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: baseline compared against, matched, hardware, batch size and warmup for throughput.
  - Reasoning: The reason line is a question, and the internal comparison that changes only the token mixer is matched. The entry does not rest on the external margins against baselines quoted from other papers.

- Stability and accuracy gain from a convolutional stem at matched FLOPs, parameters and runtime, in Early Convolutions Help Transformers See Better
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, hardware, runtime half: precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: 'Why the patch embedding stem decides whether the optimiser stays stable' rests on the measured stability finding: error across sweeps of learning rate, weight decay, optimiser and schedule. That finding has no released weights; none appear in pycls's README or model zoo, and only third-party re-implementations exist. Its hardware is not recorded. The owner is right that ...

- Implicit in README reason line: what the error rate does as corpus and model grow together, in Scaling Vision Transformers
  - Owner's verdict: not examined. Marshal: cut. Entry action: cut entry.
  - Missing fields: training data used (all arms are JFT-3B subsets, private), model and exact checkpoint.
  - Reasoning: Every data point in the scaling measurement comes from a private corpus. big_vision publishes only the config (proj/scaling_laws/train_vit_g.py) and no checkpoint. Only the authors can reproduce the number. The ladder puts that at watchlist at best, and says to cut when the entry has no other reason to exist. This reason line contains nothing except that measurement, so the ...

- Implicit in README reason line: windowing makes attention cost grow with image area instead of with its square, in Swin Transformer
  - Owner's verdict: not examined. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: This is a FLOP-count statement from the paper's operator equations: global attention carries a (hw)^2 term, and windowed attention with a fixed window size is linear in hw. It is arithmetic, not a latency claim. misc/benchmarks/07 measured the quadratic half with all seven speed fields stated, with a fitted exponent of 2.09 for attention against 0.88 for convolution.

- Implicit in README reason line: a fixed position embedding breaks as soon as the input resolution changes, in Conditional Positional Encodings for Vision Transformers
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: all eight accuracy fields for the measured accuracy drop (never inventoried).
  - Reasoning: 'Breaks' holds by construction: a fixed-length table cannot be added to a different number of tokens without interpolation. The measured accuracy drop after interpolation without fine-tuning is the empirical half. It was never inventoried, and the entry does not need it.

### Section 8

- mixup reports top-one gains on ImageNet, CIFAR-10 and CIFAR-100 over its baseline
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset split and version, input resolution and preprocessing, evaluation protocol, hardware, schedule length, the figure itself.
  - Reasoning: The abstract states no figure. The heading's 'unaugmented baseline' is wrong: the baseline is ERM with standard augmentation, without mixup. The entry rests on the interpolated target, which is a mechanism.

- CutMix reports +2.28 and +1.70 top-one on ImageNet for ResNet-50 and ResNet-101
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware, schedule length.
  - Reasoning: 'Wastes the hole unless the label moves with the pixels' is the information argument (zeroed pixels carry nothing), not the measured margin. The entry does not rest on the figures.

- AutoAugment reports 83.5 top-one on ImageNet without extra data and 1.5 percent error on CIFAR-10
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware, baseline at the same schedule.
  - Reasoning: The reason line is history: augmentation became a searched policy. It does not rest on the figure.

- RandAugment reports 85.0 top-one on ImageNet, 0.6 over the prior searched policy and 1.0 over default augmentation
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware, schedule length.
  - Reasoning: The reason line is a question ('Whether the policy search was buying anything'), and it makes sense whatever the answer. The entry does not rest on the margins.

- RandAugment reports 1.0 to 1.3 mAP over default augmentation on COCO and is within 0.3 mAP of the searched policy
  - Owner's verdict: cut. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation and NMS settings, hardware.
  - Reasoning: The protocol is partly stated and recoverable: RetinaNet with ResNet-101 and ResNet-200, 300 epochs from random initialisation, and schedules following the prior detection augmentation work. It is missing from the abstract, not unrecoverable. The owner's second ground is also wrong: a spread of 1.0 to 1.3 is 0.3 wide, which equals the 0.3 gap rather than exceeding it, and ...

- TrivialAugment reports parity with or improvement over searched policies with no search
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware.
  - Reasoning: The reason line is a question, so the entry does not rest on the figure. The owner's 'conservative direction' argument is invalid: a wrong parity result could equally hide that searched policies do survive, so it does not protect the conclusion.

- Accurate, Large Minibatch SGD: no accuracy loss up to minibatch 8192 for ResNet-50 (accuracy parity half)
  - Owner's verdict: stands. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing (recorded missing by owner, not confirmable from this container).
  - Reasoning: The owner ruled 'stands' while listing two missing fields, but stands requires every field. No checkpoint from the 8k or 256 runs was released. The baseline (256 minibatch, same epochs, 23.60 against 23.74 top-1 error), the hardware (P100s, 8 and 256) and the dataset are present. 'What else in a recipe has to move before a larger batch reaches the same accuracy' presupposes ...

- Accurate, Large Minibatch SGD: ResNet-50 trained in one hour on 256 GPUs with about 90 percent scaling efficiency (speed half)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The draft says its numbers were read from the abstract. The abstract does not state the timer boundary, so the owner's 'data loading inside, evaluation outside' has no source. The reason line does not rest on speed, and the entry action is set by the accuracy ruling. As a fact for the editor: the README title prints '1 Hour', which repeats this unverified number. voice.md ...

- SGDR reports 3.14 and 16.21 percent error on CIFAR-10 and CIFAR-100 against a fixed step schedule
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The authors' repository README (loshchil/SGDR, fetched) attributes 3.14 and 16.21 to ensembles of WRN-28-10 models. The best single-model SGDR results are 3.74 and 18.70, each a median of 2 runs. Comparing ensemble figures against a single-model step-schedule baseline means the evaluation protocol contradicts the baseline, so the claim is cut. The entry rests on defining ...

- Decoupled Weight Decay Regularization reports about 15 percent relative improvement in test error over Adam with coupled weight decay
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, evaluation protocol, hardware, search grid, absolute error rates.
  - Reasoning: The 15 percent figure could not be traced to any abstract version found; the current and v1 abstracts state no such number. The draft's provenance is therefore unconfirmed. The experiments themselves can be recovered from the public code (loshchil/AdamW-and-SGDW), so this is the missing-fields rung, not the cut rung. The entry rests on the analytic decoupling argument.

- Implicit in README reason line: label smoothing helps the classifier and hurts the student it later teaches, in When Does Label Smoothing Help?
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, hardware, evaluation protocol for the 'helps' half (quoted from other papers' results).
  - Reasoning: The line asserts two measured outcomes and only makes sense if both are true. The 'helps' half rests on a table surveying other papers' results, each under its own protocol. The 'hurts the student' half rests on the authors' own distillation runs, with no released code or weights and no stated hardware. A field is missing and the entry rests on the number. Consequence for ...

- Watchlist line (RMSNorm): 'a cheaper normalisation'
  - Owner's verdict: not examined in scope. Marshal: watchlist. Entry action: none.
  - Missing fields: hardware and how many of them, precision, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: 'Cheaper' is a speed claim and is the line's reason for watching. The condition names only an accuracy comparison and none of the seven speed fields the claim lacks for a vision workload. The entry is already on the watchlist.

### Section 9

- SimCLR reports a linear probe top-one accuracy on ImageNet matching a supervised ResNet-50
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The fields contradict. The authors' README (google-research/simclr, raw) lists 76.6 for the released ResNet50 (4x) checkpoint, but the paper quotes 76.5, so the checkpoint behind the quoted figure cannot be recovered. The 'matching' baseline is also a standard-width supervised ResNet-50 compared against a four-times-wide model under the same name. The README gives ...

- BYOL reports a linear probe top-one accuracy on ImageNet with a ResNet-50 and with a wider ResNet
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: input resolution and preprocessing, evaluation protocol (frozen layer, probe-time augmentation, probe optimiser), hardware, the baseline compared against under its own recipe.
  - Reasoning: Only the abstract was in reach and fields are missing. The reason line asks whether negatives are needed at all, which does not depend on the accuracy value.

- DINO reports a nearest neighbour accuracy with a small ViT and a linear probe accuracy with a ViT-Base
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: input resolution and preprocessing, evaluation protocol (neighbour count, distance, frozen layer), hardware.
  - Reasoning: Fields are missing. The two figures come from different backbones, which is a confound, not a field contradiction. The entry rests on centring and sharpening and on the probe becoming routine, not on either number.

- The DINOv2 model card reports nearest neighbour and linear accuracies for the same checkpoints with and without register tokens
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: input resolution and preprocessing, evaluation protocol (card says 'We refer users to the associated papers').
  - Reasoning: The card was read in full over raw. It does state hardware (A100) and software (PyTorch 2.0, xFormers 0.0.18), so the owner's 'hardware missing' is wrong. The protocol is still deferred, so the claim is not complete. The register inversion the owner reports is real (ViT-S/14: k-NN up 0.1, linear down 0.2, Oxford-H down 3.7), but the card gives no dispersion. The entry rests ...

- The DINOv2 model card states a fine-tuning gain on ImageNet-1k as a bare delta
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, the baseline compared against.
  - Reasoning: The card's sentence ('we measured +2% on ImageNet-1k classification') is attached to none of the eight listed checkpoints and has no recipe, so it cannot be tied to anything an outsider can run. The card entry's reason does not use it.

- Masked autoencoding reports a fine-tuned top-one accuracy using ImageNet-1k data only
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint for the headline (no ViT-H 448 fine-tuned checkpoint is released; released ViT-H is the 224 model), evaluation protocol detail, hardware count.
  - Reasoning: The authors' README pins the headline to ViT-H at 448, so input resolution is present, contrary to the owner. The released checkpoints are converted from TF/TPU, with 'different numerical behavior' noted, and do not include the 448 model. The entry rests on the masking mechanism, not on the accuracy.

- Do Better ImageNet Models Transfer Better reports a correlation between ImageNet accuracy and transfer accuracy
  - Owner's verdict: cut. Marshal: cut. Entry action: cut entry.
  - Missing fields: none named.
  - Reasoning: The coefficient is cut. Search confirms v1 reports r² of 0.24 and 0.86 on 13 models, while the later arXiv version and the CVPR version report r of 0.99 and 0.96 on 16 networks. The model set and the statistic both change under one identifier, and the owner misattributes the conference version to the weak figure. The reason line ('Why a frozen feature ranking and a ...

- AIM reports a frozen trunk top-one accuracy at seven billion parameters
  - Owner's verdict: watchlist. Marshal: watchlist. Entry action: none.
  - Missing fields: the baseline compared against at equal data and compute, hardware (evaluation GPU type unnamed; pretraining hardware unstated).
  - Reasoning: The owner says the weights could not be confirmed, which is now false. The apple/ml-aim aim-v1 README (raw) publishes the 7B backbone and attention-probe heads with SHA256 and an IN-1k reproduction command. The evaluation is therefore reproducible by outsiders and only the pretraining is author-only. The baseline field is still missing and the entry rests on the number, so ...

- The DINOv2 model card specifies the token count a given input size produces
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Verified on the card: 224 input with patch 14 gives 1 class token plus 256 patch tokens plus optionally 4 registers, with cropping to the nearest smaller multiple. This is a specification that one forward pass can check.

- Implicit in README reason: dense patch features decay over a long schedule and holding them steady has a cost (DINOv3)
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint for the decayed and the anchored runs, evaluation protocol and dense metric behind the decay curve (card defers to paper), training data used (LVD-1689M, drawn from 17B Instagram images, not available to others), hardware (61,440 H100 hours for ViT-7B), the baseline compared against (the run without Gram anchoring, not released).
  - Reasoning: 'Why dense patch features decay' presupposes a measured drop in dense-task quality. That is a performance claim, and the whole reason line rests on it. The measurement exists only for the authors' 7B run on a private corpus, so the last ladder row applies and the watchlist is the best it can get. It is not cut because the paper also specifies Gram anchoring, which the ...

### Section 10

- Faster R-CNN runs at five frames per second including all steps (abstract of arXiv 1506.01497)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, batch size, framework and version with compile flags, warmup and the statistic reported, timer boundary separating decode and resize from proposal NMS.
  - Reasoning: Speed fields are missing. The entry rests on proposal generation and anchor assignment, not on the frame rate.

- RetinaNet matches the speed of earlier one-stage detectors while exceeding two-stage accuracy (abstract of arXiv 1708.02002)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware and how many, precision, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: No speed field is present. The entry rests on the easy-negative imbalance mechanism.

- Mask R-CNN runs at five frames per second and adds small overhead to Faster R-CNN (abstract of arXiv 1703.06870)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing (mask paste-back) are inside the timer.
  - Reasoning: Speed fields are missing, and the reason line does not use the frame rate. The entry's actual dependency, a comparative accuracy claim, is ruled separately below.

- Implicit in README reason: the alignment of a pooled region to the pixel grid matters more than the mask head (Mask R-CNN)
  - Owner's verdict: not examined. Marshal: cut. Entry action: cut entry.
  - Missing fields: none named.
  - Reasoning: 'Matters more than' is an effect-size comparison taken from the paper's ablations, so the reason only holds if that number is true. Search of the paper's text gives these results. On the same ResNet-50-C4 model, the mask head's per-class sigmoid against softmax is worth 5.5 mask AP and RoIAlign over RoIPool about 3.3. The only comparisons that favour alignment pit RoIAlign ...

- FCOS reaches a stated AP under single-model single-scale testing with NMS as the only postprocessing (abstract of arXiv 1904.01355)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, evaluation protocol: NMS overlap and score thresholds, training data used, hardware.
  - Reasoning: Fields are missing, and the owner's list also omits hardware. The reason line asks what is lost and kept without presupposing the AP value.

- Soft-NMS raises AP against several detectors without retraining (abstract of arXiv 1704.04503)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, evaluation protocol including baseline NMS and Soft-NMS overlap, score and decay parameters, training data used, hardware.
  - Reasoning: Fields are missing. The entry rests on the suppression mechanism at an overlap threshold, not on the AP gain.

- Mask2Former reports panoptic, instance and semantic results in one architecture (abstract of arXiv 2112.01527); implicit in README reason that the three tasks stop needing three architectures
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint for the ADE20K semantic headline, evaluation protocol: single-scale or test-time augmentation for the semantic figure, the baseline compared against (specialised architectures at matched backbone and schedule).
  - Reasoning: A unified architecture that loses to the specialists does not end the need for three, so 'stop needing three different architectures' only holds if the abstract's parity-or-better claim is true. The authors' model zoo (raw) does supply checkpoints, configs, IN21k pretraining and V100 hardware for the panoptic and instance figures. Its ADE20K Swin-L row reads 56.1 ...

- YOLOv10-S is faster than a comparable transformer detector at similar AP (abstract of arXiv 2405.14458)
  - Owner's verdict: cut. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware and how many, precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing is inside the timer.
  - Reasoning: The owner's grounds for a cut are wrong. RT-DETR-R18 is a DETR-family detector and is NMS-free like YOLOv10-S, so the ratio does not set an NMS pipeline against an NMS-free one. T4 with TensorRT FP16 appears in third-party documentation, so the protocol is unread here rather than shown unrecoverable. The authors' README latency column carries only the test size. Fields are ...

- A real-time transformer detector beats comparable one-stage detectors on latency, encountered second hand inside the YOLOv10 abstract
  - Owner's verdict: watchlist. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The claim was read only through a rival's restatement, which is not a primary source. The YOLOv10 abstract the owner names as the carrier states the reverse comparison and does not contain it. None of the seven fields is recoverable from anything examined. No README entry or watchlist line exists for a watchlist verdict to attach to, and the source was left out for an ...

- Implicit in README reason: set prediction trains in a schedule a team can afford (Deformable DETR)
  - Owner's verdict: not examined. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The schedule is a recipe specification: the released main.py defaults to 50 epochs with the drop at 40. The accuracy reached in it is published with checkpoint, config and training log per row. The same page gives the AP metric, V100 hardware, a total batch of 32 and DETR baseline rows. Code confirms train2017 and val2017, multi-scale 480 to 800 training (max 1333) and ...

- Implicit in README reason: a detector trained at one overlap threshold degrades when scored at a higher one (Cascade R-CNN)
  - Owner's verdict: not examined. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: As worded, this follows from the AP definition owned by section 5. For a fixed detection set, true positives at a stricter IoU are a subset of those at a looser one, so AP cannot rise. It is checkable without any experiment and smuggles no measured number.

- README section 10 preamble: most latency figures in these sources leave preprocessing and NMS outside the timer
  - Owner's verdict: not examined. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The section's own audit does not support the count. Faster R-CNN asserts 'including all steps', which means inclusion. RetinaNet, Mask R-CNN and YOLOv10 leave the boundary undeclared, YOLOv10 has no NMS, and Soft-NMS was never timed. No source examined is shown to exclude the stages. The preamble asserts exclusion where the evidence shows only non-declaration. It is not an ...

### Section 11

- I3D reaches top-one 71.1 RGB and 74.2 two-stream on the Kinetics test set (authors' release)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, dataset with split and version (Kinetics copy not pinned).
  - Reasoning: Verified in the deepmind/kinetics-i3d README: test split, 25 fps, short side 256 bilinear, values rescaled to -1 to 1, centre 224 crop at test, and ImageNet+Kinetics against Kinetics-only columns. The reason names the origin of weight inflation and does not presuppose the accuracy.

- SlowFast R50 8x8 reaches top-one 77.0 on Kinetics-400 under 3 crops by 10 clips (authors' model zoo)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, input resolution and preprocessing (only via linked config), dataset with version.
  - Reasoning: The row is verified as stated. Fields are missing, and neither the SlowFast entry nor the model zoo entry rests on the value.

- The same X3D checkpoint scores differently at ten views and at thirty views (authors' model zoo)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, input resolution and preprocessing beyond frame length and sample rate, dataset with version.
  - Reasoning: The owner lists three missing fields and still rules stands, which breaks the ladder. 'Stands' requires every field present, and holding absent fields fixed across columns is not one of the four outcomes. The columns are verified, and all four X3D rows rise from 10-view to 30-view. The model zoo entry rests on the page's layout, not on the size of the gap.

- Kinetics-400 top-one accuracies are comparable across papers
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The dataset-version field takes different, unrecoverable values across the numbers being compared, because the videos expire and copies differ. The Kinetics entry rests on exactly this non-comparability, so the cut supports it.

- Tracktor's MOT17 result improved because the detector was retrained, with no conceptual change to the tracker
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, input resolution and preprocessing, metric implementation behind the printed tables, the baseline compared against (original iccv_19 figures are not on the page).
  - Reasoning: The admission is verbatim in the authors' README. The owner nonetheless lists missing fields and rules stands, which the ladder forbids. The owner's protocol field is also wrong: the shipped experiments/cfgs/tracktor.yaml sets public_detections: True, not private detections. The MOT17 train rows use a detector trained on those same sequences. The reason line is ...

- ByteTrack reaches MOTA 90.0 and IDF1 83.3 at 29.6 FPS (authors' model zoo)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, timer boundary for preprocessing, detector forward pass and association, evaluation protocol detail.
  - Reasoning: The README confirms the row is evaluated on MOT17 train with four training corpora mixed in. Its abstract text names a single V100, so hardware is not wholly absent. The entry does not rest on this train-split row. What it does rest on is ruled separately below.

- Implicit in README reason: discarding low scoring boxes costs identity continuity rather than precision (ByteTrack)
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: evaluation protocol: the score thresholds that define a low-scoring box, the matching threshold, and the evaluation kit, the baseline compared against: which nine trackers, and whether each was rerun on the same detections, any measurement of the precision half of the claim.
  - Reasoning: 'Why discarding ... costs identity continuity' presupposes the measured IDF1 effect, which the README states as +1 to +10 IDF1 across nine trackers. Present: ablation checkpoint, MOT17 half-val split, IDF1, CrowdHuman plus MOT17 half-train data, single V100, and an 800x1440 inference size confirmed by search. The thresholds and the nine baselines could not be confirmed from ...

- FairMOT's entire system reaches thirty frames per second under the private detector protocol, with MOTA 73.7 on MOT17 test
  - Owner's verdict: watchlist. Marshal: cut. Entry action: cut entry.
  - Missing fields: none named.
  - Reasoning: The fields contradict. The authors' README results table attaches 25.9 FPS to the MOT17 row that carries the 73.7 MOTA, and 30.5 FPS to the 2DMOT15 row. The 'up to 30 FPS' headline is a best case across workloads, not the rate of the configuration the accuracy came from. The README watchlist line rests on that frame rate, so a cut removes it from the watchlist. Keeping it ...

- MOTA is dominated by detection errors and cannot stand in for association quality
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: This is a claim about a metric's definition and decomposition, checkable with the reference implementation that the TrackEval document names as the official kit. The checkpoint and hardware fields do not apply to a scoring rule.

- Implicit in README reason: a model that ignores the order of the frames stops scoring well on Something-Something
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, training data used, hardware, the baseline compared against.
  - Reasoning: 'Stops scoring well' is an accuracy claim, and the reason line is nothing but that claim. No source in reach, including search of the dataset paper, shows an order-agnostic model measured on this benchmark, and the cited paper may not contain that experiment at all. The entry rests on a number for which no field is available.

- Implicit in README reason: temporal modelling does not have to cost an extra dimension of convolution (TSM)
  - Owner's verdict: not examined. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The cost claimed is structural: the authors' README states 'zero parameters and zero FLOPs' for the shift, checkable by reading ops/temporal_shift.py. It is a specification, not a timed speed claim, and the line asserts no latency or accuracy figure.

- README reason for PySlowFast Model Zoo: the crop and clip count at test time sits beside every accuracy the page reports
  - Owner's verdict: not examined. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The page contradicts the universal claim. The multigrid Kinetics, SSv2, Charades, AVA and ImageNet tables carry no crop and clip count, and the Charades rows link SSv2 configs. The claim holds only for the main Kinetics and X3D tables. It is not a performance number, so the ladder's entry consequence is not applied, but the line is false as worded and the editor owns the fix.

### Section 12

- Real-time novel view synthesis at high definition resolution, claimed by 3D Gaussian Splatting
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware for the frame-rate claim, precision, batch size, framework and version with compile flags, warmup and the statistic reported (a floor, not a median).
  - Reasoning: The A6000 the owner cites appears in the README only as the reference machine for a roughly 7 hour full evaluation, not for the 30 fps or better claim. Structure-from-motion preprocessing is outside the timer. The entry rests on rasterisation replacing ray marching.

- View synthesis quality of 3D Gaussian Splatting over its evaluation captures
  - Owner's verdict: watchlist. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The fields contradict. The authors' README states that the released pre-trained models come from a cleaned-up codebase with bug fixes, so their metrics 'will differ from those in the paper'. This is the same checkpoint defect the owner cut Depth Pro for. The owner's 'two scenes must be requested' statement does not appear in the authors' README. The entry does not rest on ...

- Training a radiance field in seconds, claimed by Instant Neural Graphics Primitives (also implicit in README reason: removes most of the training cost)
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: precision, batch size, framework and version with compile flags, warmup and the statistic reported, including the quality at which the timer stops, whether preprocessing and postprocessing are inside the timer (COLMAP pose estimation is outside).
  - Reasoning: The reason line's 'removes most of the training cost' is a speed claim and only holds if the number is true, so the entry rests on it. The owner never applied that test. The README states one RTX 3090. It also gives two training durations, 'under 5 seconds' and 'after around two minutes training tends to settle down', with no stated stopping criterion. A relative cost claim ...

- Per-scene view synthesis quality reported by NeRF on its synthetic and forward-facing captures
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, hardware, input resolution.
  - Reasoning: Fields are missing. The entry rests on the volume rendering formulation, not on the averaged score.

- Zero-shot cross-dataset transfer claimed by Towards Robust Monocular Depth Estimation
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware, the baseline compared against for later training mixtures.
  - Reasoning: The MiDaS README confirms the training mixture grew across releases (up to 12 datasets) under one name. The entry rests on the scale-and-shift-invariant protocol definition, not on an error value.

- Real-time operation claimed by DROID-SLAM
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing (global bundle adjustment in async mode) are inside the timer.
  - Reasoning: The README confirms an 11G inference floor, 24G for TartanAir and ETH3D-SLAM, 4x RTX-3090 for training, and frontend and backend as separate processes. The memory cost the reason line cites is an authors' stated requirement, not a timed claim. The entry does not rest on 'real-time'.

- Metric monocular depth in under a second, claimed by Depth Pro
  - Owner's verdict: cut. Marshal: cut. Entry action: cut entry.
  - Missing fields: none named.
  - Reasoning: The authors' README states the released model 're-trained ... does not match it exactly', which breaks the checkpoint field, and the 0.3 seconds is on 'a standard GPU'. The owner cut it, but the editor put Depth Pro on the README watchlist with a promotion condition. A contradiction is a cut under the ladder, not a watchlist line, so the line is removed.

- A reconstruction F-score is only defined together with its tolerance, per the ETH3D Multi-View Evaluation Program
  - Owner's verdict: stands. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Verified in the README: tolerances are a required argument, with voxel size and beam parameters as explicit options. This is a specification of the scoring program.

- Implicit in README reason: global reconstruction matches incremental accuracy (GLOMAP)
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact version of both pipelines, dataset with split and version, metric with its full definition, evaluation protocol, hardware.
  - Reasoning: The source's claim, in the deprecated colmap/glomap README, is '1-2 orders of magnitude faster, with on-par or superior reconstruction quality', with no fields. The README line is question-form ('Whether ... matches'), the pattern voice.md sanctions, so it does not presuppose the answer and the entry does not rest on the number.

- Implicit in README reason: iterative refinement replaced a single pass over the full cost volume (RAFT-Stereo)
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: every accuracy field; the only performance evidence on the authors' README is a challenge leaderboard rank, inadmissible under conventions section 6.
  - Reasoning: The line reads as the paper's design substitution, GRU refinement in place of 3D aggregation over the full volume, which is checkable from the architecture. It does not depend on a measured win, so the entry does not rest on a number.

### Section 13

- DDPM reports FID 3.17 and IS 9.46 on unconditional CIFAR-10, presented as state of the art against a baseline table
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: the baseline compared against (scored under the same metric implementation and reference statistics).
  - Reasoning: Two fields the owner lists as missing are in fact stated in hojonathanho/diffusion. Its README says the experiments ran on Google Cloud TPU v3-8, it pins tensorflow-gan for the metric, and it publishes models and samples. The claim still fails on consistency. The figure is ranked against prior models' scores taken from their own papers, which used other FID implementations ...

- DDIM gives sample quality comparable to the full step count at a small fraction of the steps, with no retraining
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: metric with its full definition, hardware.
  - Reasoning: Agreed. The DDPM-trained network is reused unchanged: the ermongroup/ddim README says it is trained with the same procedure as DDPM. However, the FID implementation and the hardware are not stated for the step sweep. The reason line is structural: the step count is chosen at sampling time over the same trained network. It does not need the quality number. The owner's note ...

- DDIM samples ten to fifty times faster in wall-clock time than DDPM (paper abstract; the repository repeats that it costs much less time and compute)
  - Owner's verdict: not examined (draft note states no wall clock is reported). Marshal: recorded unverified. Entry action: none.
  - Missing fields: precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The draft missed this speed claim. The stated range exactly matches the ratio of the full step count to the reduced step counts, so it reads as a step ratio and not as a timed measurement. No reachable source states precision, batch size, framework version, warmup or statistic. Nothing says whether the noise draw and the final conversion to pixels are inside a timer. The ...

- The aliased resizing audit: the score changes when only the resize implementation or a high-quality compression pass changes
  - Owner's verdict: stands. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: hardware.
  - Reasoning: GaParmar/clean-fid publishes almost every field: the metric code with the exact Inception port; reference statistics by dataset, split and resolution (for example FFHQ trainval70k); linked StyleGAN2 checkpoints; sample counts with repeated runs; and the PIL-bicubic and PNG baselines. Hardware is stated nowhere reachable. The comparison docs say only that a CUDA device was ...

- The audit's implementation agrees with pytorch-fid to about two parts in a million once the legacy option is set
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: docs/pytorch_fid.md names the set: 5000 StyleGAN2 samples against 5000 FFHQ images. However, the download step is a literal placeholder ('wget <to_be_hosted>.zip'), the checkpoint is unnamed and the FFHQ draw is unstated. Nobody but the authors can rerun the comparison, so the protocol is unrecoverable. The owner's restatement is also wrong in kind. The source reports an ...

- Rethinking FID: the score is biased at practical sample counts and its feature network mis-ranks text-conditioned systems
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: evaluation protocol (prompt set, rater pool, instructions, comparisons per pair), model and exact checkpoint for the systems ranked.
  - Reasoning: Agreed. The reason line names the feature network and the sample count as parts of the metric. That is carried by the published definition and code, not by a stated magnitude. The preference-ranking half has no protocol and is never quoted.

- Scaling rectified flow transformers improves human preference ratings over established formulations
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: evaluation protocol (prompt set, rater pool, instructions, number of comparisons), model and exact checkpoint for the compared systems, input resolution and preprocessing, hardware.
  - Reasoning: Agreed. The reason line rests on the objective and on the separate text and image weights, both of which are specified. The preference claim is recorded and never repeated.

- Open-weight FLUX variants are preferred by human raters over other open-weight systems
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Agreed. The repository states no evaluation, and the claim comes from a vendor announcement. No protocol is recoverable. The entry rests on the stated licences, not on the preference claim.

- Implicit in the reason line and title: classifier guidance trades diversity for fidelity ('first paid for in diversity'), and diffusion beats GANs
  - Owner's verdict: not examined. Marshal: stands. Entry action: none.
  - Missing fields: none named.
  - Reasoning: openai/guided-diffusion publishes the following. Diffusion and classifier checkpoints for each resolution. Sampling flags: step respacing, classifier scale and fp16. A TensorFlow evaluator for FID, sFID, IS, precision and recall, with reference batches. Sample batches for the guided and unguided models, and for the BigGAN-deep baseline scored with the same evaluator. The ...

- Implicit in the reason line: classifier-free guidance trades diversity away as the guidance scale rises ('what it trades away')
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, hardware.
  - Reasoning: The paper's FID/IS sweep over guidance strength uses ImageNet models that the authors never released with checkpoints or code; the draft's own link note found no authors' file. Only the authors can reproduce those figures. The entry does not rest on them: the loss of diversity follows from the construction, because the guided score targets a conditional sharpened by the ...

- Implicit in the reason line: moving diffusion into an autoencoder latent is what made text-conditioned synthesis affordable (a cost and speed claim)
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: precision, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: 'Affordable' is a cost claim, and the line only makes sense if it is true. The paper supports it with two things. The first is throughput on a single A100. The second is training compute in V100-days, converted from A100-days with an assumed speed ratio borrowed from another paper and compared against baseline compute taken from another paper. That figure is a conversion, ...

- Implicit in the reason line: a transformer backbone matches or beats the convolutional U-Net, so the convolution was not doing the work
  - Owner's verdict: not examined. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: DiT's own FID carries its fields in facebookresearch/DiT. There are released checkpoints, FID-50K through ADM's evaluator and reference batches, stated sampling steps and guidance scale, ImageNet training data, and TPU training with an A100 re-evaluation and a TF32 note. The backbone attribution is not measured. The U-Net baselines differ from DiT in latent space and ...

- Implicit in the reason line: a resize nobody can see moves the score further than a change of method does
  - Owner's verdict: not examined (the owner's stands covered only the sensitivity). Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: hardware.
  - Reasoning: The line asserts a comparison of magnitudes and rests on it entirely. The source supports it only by setting two tables side by side. The resize table is an FID between two resizings of the same real FFHQ images. The method gaps are model-against-reference scores in separate leaderboard tables. On like-for-like rows (same checkpoint, legacy against clean pipeline) the shift ...

- Watchlist line (Imagen): a frozen text encoder was argued to matter more than the image model
  - Owner's verdict: not examined (draft rejected Imagen under conventions section 6). Marshal: cut. Entry action: cut entry.
  - Missing fields: model and exact checkpoint, training data used (internal image-text set), evaluation protocol for the human ratings.
  - Reasoning: The comparison is carried by encoder and U-Net scaling runs. Those runs were trained partly on an internal image-text set, with no released weights or code, so only the authors can reproduce them. That makes the line watchlist at best, and a cut when the entry has no other reason to exist; this line gives none. Its condition ('weights or an implementation are released with ...

### Section 14

- Zero-shot ImageNet top-one of the original contrastive checkpoint as tabulated in OpenCLIP
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: dataset with split and version, evaluation protocol (which template set produced the value), training data used, hardware, baseline compared against.
  - Reasoning: The verdict is agreed but one correction is needed. The template sets are published in the same repository: src/open_clip/zero_shot_metadata.py carries the OpenAI ImageNet set and a simple set. So the protocol is not unreproducible in principle, but which set produced the tabulated value is not stated beside it. The reason line concerns named corpora, not the score.

- Sigmoid-loss checkpoint ImageNet top-one at the larger resolution as tabulated in OpenCLIP
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: dataset with split and version, input resolution and preprocessing, evaluation protocol, training data used, hardware, baseline compared against.
  - Reasoning: Agreed. The reason line is structural: the per-pair loss frees the batch from carrying the negative set. It does not use the score.

- BLIP-2 beats Flamingo on zero-shot VQAv2 (LAVIS project README)
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The fields contradict each other. The baseline is Flamingo's published zero-shot score, and Flamingo's zero-shot protocol prompts with two text-only task examples. BLIP-2's zero-shot uses no examples, so the baseline was scored under a different protocol. Flamingo weights were never released, so only its authors can reproduce the baseline. The BLIP-2 reason ('what a learned ...

- BLIP-2 zero-shot captioning score against the previous best (LAVIS project README)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol (decoding), training data used, hardware, baseline compared against (unnamed where the claim is made).
  - Reasoning: Agreed. The README states the claim with an unnamed 'previous best' and no decoding settings. The entry does not rest on it.

- LLaVA-1.5: state of the art on eleven benchmarks and about one day of training on a single eight-A100 node (repository README)
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The training-time half has more fields than the owner credits. The repository states 8x A100 (80G or 40G), global batch sizes, 336px input and a pinned framework. It has no statistic and no timer boundary: 'about one day' is a single wall-clock total of stage durations. The leading-score half compares against baselines reported under their own papers' prompts and answer ...

- Accuracy on the robustified multimodal exam ranges from the high teens to the mid twenties (MMMU repository)
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The source's statements of the range contradict each other. The MMMU repository README calls it 'accuracies ranging from'. The paper abstract states it as how much lower performance is on MMMU-Pro than on MMMU. The draft repeats the conflict: its heading reads the range as an accuracy level, while its note says 'the size of the drop is the finding'. No reading is ...

- Multi-modal gain and multi-modal leakage as defined by the vision-indispensability audit (MMStar)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint for the published rows, input resolution and preprocessing, training data used, hardware.
  - Reasoning: Stands requires every field, and the owner names four as missing. The MMStar README confirms the procedure: three result files, with image, without image, and from the base language model without image. The reason line is a 'how much' question that the procedure answers, not an asserted magnitude, so the entry does not rest on any score.

- A pocket multimodal model reaches most of the performance at a fraction of the parameters (claim made in a title)
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Agreed. A ratio with no protocol anywhere it is stated. No README entry cites the source.

- Implicit in the reason line: the LLaVA-1.5 ablation attributes gains to the connector and to the training recipe
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint (for the ablation rows).
  - Reasoning: 'Which gains came from the connector and which came from the training recipe' only makes sense if the ablation deltas are real, so the line rests on them. docs/MODEL_ZOO.md releases only the final LLaVA-1.5 checkpoints: 7B and 13B, full and LoRA. No checkpoint exists for any intermediate ablation row, so the rows the attribution is read from cannot be re-scored. The ...

- Implicit in the reason line: permuting the answer options moves a model's score (MMBench CircularEval)
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, metric with its full definition (choice extractor version), training data used, hardware.
  - Reasoning: The line rests on the effect. The authors' README states it only as a 10-20% drop that is 'common' for 'most existing VLMs', with no model named. The choice extractor is 'ChatGPT' with no version, so the metric depends on an unversioned closed service. Test-split scores come only from the authors' submission server.

### Section 15

- Post-training quantisation gives four times smaller models and a two to three times speedup (TFLite post-training quantization guide)
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Agreed. Only precision is stated; no model, part, thread count, delegate or timer is given, so the protocol is unrecoverable. The guide is not an entry, and the TFLite specification entry does not rest on it.

- Integer inference is faster than float on edge boards (XNNPACK latency tables)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: batch size, input resolution, framework and version with compile flags (no library commit), warmup and the statistic reported.
  - Reasoning: The integer rows are in the Raspberry Pi multi-threaded table. It gives the per-channel schema, the CMake build script, end2end-bench with min_time=5, randomized weights and inputs, and a date, but no commit. The owner lists the timer boundary as missing, yet the owner's own note recovers it: inputs are randomized and in memory, and only the model is timed, so both pre- and ...

- Implicit in the reason line: layers that fall back from XNNPACK run on a slower path
  - Owner's verdict: not examined. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware and how many of them, precision, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: No XNNPACK page measures the fallback path, so 'slower' is a speed direction with none of the seven fields. The line's motive is the coverage list, which does not need it, so the entry stands. Under the recorded-unverified outcome the claim is not repeated, and the word 'slower' in the line repeats it.

- Quantisation can make inference slower, and old hardware does not benefit (ONNX Runtime quantization documentation)
  - Owner's verdict: stands. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: hardware and how many of them (only instruction-set classes, no part or count), batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: The page says it in three places: 'not rare to get worse performance on old devices', 'S8S8 with QOperator will be slow on x86-64 CPUs', and on GPUs 'Older hardware will not benefit'. This is a speed claim with no measurement behind it. Stands needs all seven fields, so the owner's verdict fails the ladder. The README line offers exactly this as a reason to open the page ...

- The unsigned-by-signed eight-bit path can saturate its sixteen-bit intermediate on x86 and cost accuracy (ONNX Runtime documentation)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, training data used.
  - Reasoning: Agreed. The documentation states the mechanism (VPMADDUBSW on AVX2/AVX512) and says it is 'generally not a big issue' but gives no magnitude. The reason line does not mention it.

- Two conforming implementations of the eight-bit scheme are not bit-exact (TFLite quantization specification)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, evaluation protocol, training data used, hardware.
  - Reasoning: The specification text is confirmed: 'implementations that are not bit-exact'. It states the limits of the conformance guarantee and is not a measurement. By the owner's own list six fields are missing, so stands is not available. The entry rests on the normative scheme, not on this sentence.

- MLPerf Inference latencies are comparable across submissions (LoadGen documentation)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware and how many of them, precision, batch size, input resolution, framework and version with compile flags.
  - Reasoning: The LoadGen README states that QSL preprocessing is untimed and that decompression in the SUT is timed. Its flow post-processes the result before return, so the timer-boundary field is present. The README never makes the comparability claim, and hardware, precision, batching, resolution and framework vary by submission by design. With five fields missing the claim cannot ...

- Adaptive rounding often improves quantised accuracy (toolkit page implementing it)
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The only field given is nearest rounding as the baseline. No model, dataset, metric or protocol is stated, which is an unrecoverable protocol and so a cut, not recorded unverified. The toolkit page is not an entry. The AdaRound paper entry is ruled separately below.

- Implicit in the reason line: adaptive rounding beats rounding to nearest once calibration data exists ('the wrong default')
  - Owner's verdict: not examined. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: hardware, input resolution and preprocessing.
  - Reasoning: The line asserts that adaptive rounding is more accurate than nearest rounding and rests on that. The paper states: torchvision ResNet18; ImageNet validation top-one; symmetric 4-bit per-layer weights with float activations; 1024 unlabelled calibration images; 10k Adam iterations; five seeds; nearest rounding as the baseline. Batch-norm folding is the only preprocessing ...

- Channel permutation recovers structured-sparse accuracy without affecting run time (pruning tool documentation)
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware and how many of them, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer, dataset with split and version, metric with its full definition.
  - Reasoning: Agreed. The reason line rests on the executable sparsity pattern and the retraining recipe.

- Structured sparsity doubles matrix-unit arithmetic throughput
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware and how many of them, batch size, input resolution, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
  - Reasoning: Agreed. This is a peak-throughput property of the hardware, not a timed workload. The line says the pattern 'can execute', not that it is faster.

### Section 16

- Mean corruption error per backbone in the ImageNet-C repository table
  - Owner's verdict: cut. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: Agreed. The table is a leaderboard. The repository allows scoring either the shipped JPEGs or in-memory corruptions under one metric name, so the protocol per row is unrecoverable. Neither the suite entry nor the generator entry rests on it.

- Re-estimating batch-normalisation statistics on corrupted images moves ImageNet-C mean corruption error
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, training data used, hardware.
  - Reasoning: The figures are confirmed against the bethgelab/robustness master README abstract, and no README entry cites this source. The record has two defects. First, the draft's note repeats all four figures, which recorded unverified forbids. Second, the note says the section's warning sentence exists because of this result, so the README preamble leans on an unverified number.

- Augmentation gains do not transfer to perceptually dissimilar corruptions; README line: 'the held out corruptions that break a tuned robustness score'
  - Owner's verdict: recorded unverified. Marshal: watchlist. Entry action: move to watchlist.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, hardware.
  - Reasoning: The effect size can be reached. figs/table.png in the repository, served by raw.githubusercontent.com, gives error per augmentation on IN-C and IN-C-bar (and on the CIFAR versions), with run spread and a baseline row. The table and README name no architecture, checkpoint or preprocessing, and no hardware. The reason line rests on the effect ('break'), not on the generation ...

- Seven of nine defences accepted at one conference were reduced to low accuracy by improved attacks
  - Owner's verdict: stands. Marshal: cut. Entry action: none.
  - Missing fields: none named.
  - Reasoning: The claim as recorded contradicts the source's own fields. The authors' README abstract says 7 of 9 defences relied on obfuscated gradients, and the attacks circumvented 6 completely and 1 partially. Its table leaves the partial case at 55%, which is not low accuracy, and Na et al. is listed separately as limited robustness. Exact checkpoints for the reimplemented defences ...

- Certified robustness under randomized smoothing (certified-accuracy table)
  - Owner's verdict: stands. Marshal: recorded unverified. Entry action: none.
  - Missing fields: hardware.
  - Reasoning: The guarantee itself is a theorem and needs no fields; the number is the certified-accuracy table. locuslab/smoothing publishes the models, the noise levels, the Monte Carlo procedure with its confidence parameter, and the certification time, but names no hardware. The reason line concerns the form of a guarantee, not the table.

- Accuracy drop from the original ImageNet validation set to its rebuilt replacement
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: input resolution and preprocessing per model, metric with its full definition per model, hardware.
  - Reasoning: Agreed. The source is held by section 4, and no entry in sections 13 to 16 cites it.

- Classifier accuracy on the naturally occurring hard set; README line: 'still breaks the models that came after it'
  - Owner's verdict: recorded unverified. Marshal: cut. Entry action: cut entry.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, training data used, hardware.
  - Reasoning: The reason line extends the hard-set result to every later model with no model, checkpoint, preprocessing or protocol, so the protocol cannot be recovered. The owner's note that the entry is admitted for how the set was built is not what the line says. A later named checkpoint contradicts the universal reading. The OpenCLIP results file that section 14 relies on lists ...

- Calibration fitted in distribution degrades under dataset shift
  - Owner's verdict: recorded unverified. Marshal: recorded unverified. Entry action: none.
  - Missing fields: model and exact checkpoint, input resolution and preprocessing, training data used, hardware.
  - Reasoning: The verdict is agreed, but not the owner's rationale. The owner says the entry rests on the structural result, which would mean watchlist with four fields missing. The README line is a neutral question ('What happens to calibration...') and does not assert a direction, so it does not rest on the result.

- Implicit in the reason line: an intervention that fixes one kind of shift leaves the others untouched
  - Owner's verdict: not examined. Marshal: cut. Entry action: cut entry.
  - Missing fields: none named.
  - Reasoning: The line contradicts the source. The paper's abstract says gains on artificial robustness benchmarks can transfer to real-world shifts. It also says some methods consistently help across texture and local-statistics shifts, failing only on others such as geographic change. The geographic-change evidence comes from the StreetView StoreFronts set, which hendrycks/imagenet-r ...

- Watchlist line (AugMix): augmentation reported against the corruption suite its design was tuned near
  - Owner's verdict: draft rejected to watchlist. Marshal: watchlist. Entry action: none.
  - Missing fields: hardware, baseline compared against (its recipe).
  - Reasoning: The AugMix README publishes the checkpoint, the ImageNet recipe, the evaluation code and its mCE. Hardware and the baseline's recipe are not stated. The line's condition ('scored on a corruption family held out from its own design') has already been met by a section 16 core source: the augmentation-corruption table scores AugMix on ImageNet-C-bar. A condition that has ...
