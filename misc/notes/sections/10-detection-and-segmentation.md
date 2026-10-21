# 10. Detection and segmentation

Owner: practitioner who has shipped a detector into production, suspicious of any latency figure that excludes non-maximum suppression.

## Section

## 10. Detection and segmentation

Most of the latency figures in these sources exclude preprocessing and non-maximum suppression, so the speeds quoted across them are not comparable.

### Detector families

- [Faster R-CNN](https://arxiv.org/abs/1506.01497) - Where proposal generation moved inside the network and anchors became the assignment rule.
- [Feature Pyramid Networks for Object Detection](https://arxiv.org/abs/1612.03144) - Why a box of a given size is assigned to one pyramid level rather than another.
- [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002) - What dense anchor assignment does to the ratio of easy negatives during training.
- [Cascade R-CNN](https://arxiv.org/abs/1712.00726) - Why a detector trained at one overlap threshold degrades when scored at a higher one.

### Set prediction and anchor-free designs

- [FCOS](https://arxiv.org/abs/1904.01355) - What a detector loses and keeps when the anchor box and its hyperparameters are removed.
- [Adaptive Training Sample Selection](https://arxiv.org/abs/1912.02424) - Whether anchor-free and anchor-based detectors differ in anything but how positives are chosen.
- [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872) - Where bipartite matching replaces both the anchor grid and the duplicate removal pass.
- [Deformable DETR](https://arxiv.org/abs/2010.04159) - What set prediction needs before it trains in a schedule a team can afford.

### Segmentation

- [Fully Convolutional Networks for Semantic Segmentation](https://arxiv.org/abs/1411.4038) - Where a classification backbone first became a dense per-pixel predictor.
- [U-Net](https://arxiv.org/abs/1505.04597) - Why skip connections between encoder and decoder decide how sharp a mask boundary is.
- [Mask R-CNN](https://arxiv.org/abs/1703.06870) - Why the alignment of a pooled region to the pixel grid matters more than the mask head.
- [Mask2Former](https://arxiv.org/abs/2112.01527) - Where semantic, instance and panoptic outputs stop needing three different architectures.
- [Segment Anything](https://arxiv.org/abs/2304.02643) - What a mask model can do when the prompt rather than a fixed class list defines the target.

### Postprocessing and what ships

- [Soft-NMS](https://arxiv.org/abs/1704.04503) - Why a neighbouring object disappears at one overlap threshold and survives at another.
- [NonMaxSuppression](https://github.com/onnx/onnx/blob/main/docs/Operators.md#NonMaxSuppression) - Where the tie-breaking and box format rules a runtime actually applies are written down.
- [Detectron2](https://github.com/facebookresearch/detectron2) - Where the postprocessing defaults behind several published numbers are readable as code.
- [YOLOv10](https://arxiv.org/abs/2405.14458) - Where duplicate removal is trained away instead of timed out of the latency budget.

## Rejected

- [Panoptic Segmentation](https://arxiv.org/abs/1801.00868) - Rule failed: owner-brief section 2, where the same source is the obvious best entry for two sections the earlier section keeps it. The load-bearing contribution is the panoptic quality metric, which section 5 owns, so this section cites the architectures that produce panoptic output instead.
- [MMDetection](https://github.com/open-mmlab/mmdetection) - Rule failed: conventions section 9, three to six entries per subsection and a further entry has to displace one of them. It would have displaced Detectron2, which stays because it is the authors' own implementation of four of the papers already cited here.
- [Ultralytics](https://github.com/ultralytics/ultralytics) - Rule failed: conventions section 6, code without a paper where the entry's claim depends on the missing half, compounded by conventions section 6 on content farms, because the training walkthroughs published under its documentation domain are vendor content marketing rather than framework documentation. The model generations it ships have no written account that states the evaluation protocol or the timer boundary behind its published tables.
- [SAM 2](https://github.com/facebookresearch/sam2) - Rule failed: conventions section 3, a section may assume every section before it and must assume nothing after it. Its subject is video segmentation and memory across frames, which section 11 owns.
- [DETR reference implementation](https://github.com/facebookresearch/detr) - Rule failed: conventions section 9, three to six entries per subsection. It would have displaced Deformable DETR and adds no written account of the method that the paper does not already carry.
- [torchvision](https://github.com/pytorch/vision) - Rule failed: owner-brief section 5, a URL you cannot verify does not go in the draft. The operator reference page documenting its non-maximum suppression kernels sits on a host that refused this container's automated client, and the search budget ran out before the page title and path could be confirmed, so the operator semantics are cited from the ONNX specification instead.

## Claims

### Faster R-CNN runs at five frames per second including all steps, as stated in the abstract of arXiv 1506.01497

- Fields present: input resolution and preprocessing partially, in that the proposal count per image is stated; hardware, named only as a single graphics processor; whether preprocessing and postprocessing are inside the timer, asserted by the phrase including all steps.
- Fields missing: precision; batch size; framework and version with compile flags; warmup and the statistic reported.
- Verdict: recorded unverified
- Note: including all steps is the strongest timer wording of any claim in this section, and it is still not a declared boundary, because it does not separate image decoding and resizing from the proposal-stage non-maximum suppression that the same sentence folds into the figure. The paper's experimental section could not be read from this container, so the four missing fields are missing from the evidence available rather than proven absent, and the number is not repeated in the section.

### RetinaNet matches the speed of earlier one-stage detectors while exceeding two-stage accuracy, as stated in the abstract of arXiv 1708.02002

- Fields present: none of the seven, beyond the implicit claim that two systems were timed the same way.
- Fields missing: hardware and how many of them; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: a speed-parity claim is a latency claim with the number removed, so it inherits every missing field and adds the risk that the two pipelines being compared decode, resize and suppress differently. The abstract does not say whether preprocessing or box decoding and non-maximum suppression are inside either timer, and the entry stands on the training-time diagnosis of foreground and background imbalance rather than on the speed sentence.

### Mask R-CNN runs at five frames per second and adds small overhead to Faster R-CNN, as stated in the abstract of arXiv 1703.06870

- Fields present: hardware, named only as a single graphics processor; the baseline compared against.
- Fields missing: precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: the abstract does not say whether preprocessing and postprocessing are inside the timer, and for a mask head the postprocessing question is sharper than for a box detector, because pasting each mask back to image resolution is a per-instance cost that grows with the number of surviving detections and therefore with the suppression threshold. The entry rests on region alignment to the pixel grid, not on the frame rate.

### FCOS reaches a stated average precision under single-model single-scale testing with non-maximum suppression as the only postprocessing, as stated in the abstract of arXiv 1904.01355

- Fields present: model and backbone family; metric, defined in section 5; evaluation protocol in part, in that single-model and single-scale testing are named and non-maximum suppression is named as the only postprocessing step; baseline compared against, being the anchor-based dense detector.
- Fields missing: exact checkpoint; dataset split and version; input resolution and preprocessing; the non-maximum suppression settings themselves; training data used.
- Verdict: recorded unverified
- Note: this is the most carefully worded accuracy claim in the section, because it names the postprocessing stage rather than leaving it implicit, and it is still short of the protocol field, since naming non-maximum suppression without its overlap and score thresholds does not let anybody reproduce the score. This is an accuracy claim and not a speed claim, so the seven speed fields do not apply to it.

### Soft-NMS raises average precision on the detection benchmarks against several detectors without retraining, as stated in the abstract of arXiv 1704.04503

- Fields present: metric, defined in section 5; baseline compared against, named as three detector configurations; dataset names.
- Fields missing: model and exact checkpoint; dataset split and version; input resolution and preprocessing; evaluation protocol including the overlap, score and decay parameters of both the baseline suppression and the replacement; training data used.
- Verdict: recorded unverified
- Note: the independent variable here is the postprocessing itself, which makes the absent suppression parameters disqualifying for reuse rather than merely untidy, because a gain reported against an untuned baseline threshold is a gain against a badly chosen operating point. The abstract also claims the same computational cost as the baseline suppression without stating hardware, batch size or whether the comparison was timed at all, so there is no speed claim here that can be examined.

### Mask2Former reports panoptic, instance and semantic results on two datasets in one architecture, as stated in the abstract of arXiv 2112.01527

- Fields present: metric names, all three defined in section 5; dataset names.
- Fields missing: model and exact checkpoint, since the backbone that produced each figure is not named in the abstract; dataset split and version; input resolution and preprocessing; evaluation protocol including single-scale or test-time augmentation; training data used, including the pretraining corpus of the backbone; baseline compared against.
- Verdict: recorded unverified
- Note: three numbers on three tasks from one abstract, with no backbone attached to any of them, cannot be matched to a downloadable checkpoint, and dense semantic scores in particular are routinely reported with multi-scale testing that the headline does not mention. The entry rests on the unification of mask classification across the three tasks, which is an architectural claim.

### YOLOv10-S is faster than a comparable transformer detector at similar average precision, as stated in the abstract of arXiv 2405.14458

- Fields present: dataset name; input resolution, recoverable from the authors' own repository table.
- Fields missing: hardware and how many of them; precision; batch size; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: cut
- Note: this is a cross-paper latency ratio between one pipeline that performs non-maximum suppression and one that does not, and neither side's timer boundary is declared in a form that makes the two comparable, so the protocol is unstated and the comparison is not recoverable from the sources available. The authors' own repository table, read directly, carries a latency column with the test size as the only one of the seven speed fields present, which is the same defect in a more visible place. The mechanism, consistent dual assignments that remove the suppression stage from the deployed graph, keeps the entry in the core; the ratio is cut and is not repeated anywhere in the section.

### A real-time transformer detector beats comparable one-stage detectors on latency, as encountered second hand inside the YOLOv10 abstract

- Fields present: none of the seven in the form available.
- Fields missing: hardware and how many of them; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: watchlist
- Note: the only form of this claim reachable from this container was a competitor's summary of it, which is not a source, and a latency claim read through a rival's comparison table is exactly the shape of number this section exists to distrust. Enters the core when the authors' own paper and its timing protocol are read directly, with the timer boundary and the hardware stated.

## Link notes

- https://arxiv.org/abs/1506.01497, https://arxiv.org/abs/1612.03144, https://arxiv.org/abs/1708.02002, https://arxiv.org/abs/1712.00726, https://arxiv.org/abs/1904.01355, https://arxiv.org/abs/1912.02424, https://arxiv.org/abs/2005.12872, https://arxiv.org/abs/2010.04159, https://arxiv.org/abs/1411.4038, https://arxiv.org/abs/1505.04597, https://arxiv.org/abs/1703.06870, https://arxiv.org/abs/1801.00868, https://arxiv.org/abs/2112.01527, https://arxiv.org/abs/2304.02643, https://arxiv.org/abs/1704.04503, https://arxiv.org/abs/2405.14458 - arxiv.org is refused at the proxy CONNECT stage from this container, so the link checker classifies every one of them UNREACHABLE with a tunnel refusal rather than DEAD, which is an egress policy and not link rot. Each abstract page was confirmed by search, with the title and the arXiv identifier agreeing in the result set, and the YOLOv10 identifier was confirmed a second time by reading the authors' own repository README, which links the same abstract page.
- https://github.com/onnx/onnx/blob/main/docs/Operators.md#NonMaxSuppression - github.com is also refused at CONNECT, so the link checker returns BLOCKED for every github.com URL cited or rejected here. The file and the NonMaxSuppression anchor were confirmed by reading docs/Operators.md on the main branch over raw.githubusercontent.com, which is reachable. The operator text pins two things a production reader needs and no paper states: boxes are suppressed only when the overlap is strictly greater than the threshold, so a box exactly at the threshold is kept, and the box layout attribute distinguishes a corner convention from a centre and extent convention, so the same threshold in two runtimes can select different boxes.
- https://github.com/facebookresearch/detectron2 - confirmed over raw.githubusercontent.com. Licence read from the repository's own licence file as Apache License, Version 2.0. The README states it is the successor to two earlier repositories from the same group, so older papers in this section point at predecessors that are no longer the maintained artefact.
- https://arxiv.org/abs/2405.14458 and the YOLOv10 repository - the repository is licensed under the GNU Affero General Public License, version 3, because its code base is built on the Ultralytics code base, and its README now opens by directing readers to a successor project from the same group. Both facts argue for citing the paper rather than the repository, and the licence matters to anybody who intends to ship the code rather than read it.
- https://github.com/open-mmlab/mmdetection - confirmed over raw.githubusercontent.com. Licence is Apache License, Version 2.0, with the copyright notice ending several years before the present, which is consistent with low-activity maintenance rather than active development. Recorded because a reader choosing a detection framework for production is choosing a maintenance commitment.
- https://github.com/ultralytics/ultralytics - confirmed over raw.githubusercontent.com. Licence read from the repository's own licence file as the GNU Affero General Public License, version 3, which is a stronger obligation than most teams assume when they install the package. Its documentation domain was refused at CONNECT and was not cited.
- api.github.com - returned a session policy refusal for every repository queried, so repository existence was confirmed by fetching a known file from each repository over raw.githubusercontent.com instead, which succeeded for every repository cited or rejected here.
- Collision with section 5 - section 5 owns IoU, average precision and panoptic quality, so no entry here restates a metric definition, and the panoptic task definition paper is left to section 5 under the owner-brief rule that the earlier section keeps a shared source.
- Candidates left out for lack of verification - the search budget for this session was exhausted part way through verification, so several strong candidates whose arXiv identifiers could not be confirmed were dropped rather than guessed. They are the single-shot multibox detector, the third YOLO technical report, the keypoint-based anchor-free detector known as objects as points, the real-time transformer detector, the predecessor of Mask2Former, the atrous convolution segmentation line, the learned replacement for non-maximum suppression, the SAM 2 paper, and the MMDetection toolbox paper. Any of them is a candidate for a later pull request once its identifier can be confirmed.

## Benchmark proposal

The claim is that the non-maximum suppression threshold moves the precision-recall curve and
therefore the operating point a product ships, which the field repeats while treating the
threshold as a default copied out of a configuration file. The measurement builds two synthetic
detection sets from a fixed seed, a sparse scene family and a crowded family whose ground-truth
boxes genuinely overlap, perturbs each ground-truth box into several scored duplicates and adds
scored false positives, then varies nothing but the overlap threshold of a greedy numpy
suppression pass across a declared sweep. At each threshold it computes the precision-recall
curve at a fixed matching overlap, the all-point interpolated average precision, and separately
the precision and the recall at one fixed score threshold, because the second pair is what ships
and the first number is what a paper reports. What settles it is a stated effect size on both.
If average precision barely moves across the sweep while precision and recall at the fixed score
threshold move by a wide margin, and the crowded family moves further than the sparse one, the
claim holds in the form that matters, namely that a threshold chosen to protect a reported
average precision is not the threshold that protects the shipped operating point; if both move
together and the two families agree, the folklore is wrong and the default is defensible. Pillow
renders one contact sheet of a crowded scene before and after suppression at the ends of the
sweep so the duplicate pattern is inspectable rather than asserted, the suppression pass is
timed with its boundary written down and reported beside the accuracy columns, and quick mode
runs a reduced sweep on the smaller family inside ten seconds with no network access and no GPU.
