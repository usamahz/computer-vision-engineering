# 8. Training: objectives, augmentation, schedules, regularisation

Owner: recipe specialist in augmentation and schedules, suspicious of improvements that evaporate against a properly tuned baseline.

## Section

## 8. Training: objectives, augmentation, schedules, regularisation

### Objectives

- [When Does Label Smoothing Help?](https://arxiv.org/abs/1906.02629) - Why softening a one-hot target helps the classifier and hurts the student it later teaches.
- [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002) - What a grid of mostly background labels does to cross entropy before any architecture is blamed.
- [Generalized Intersection over Union](https://arxiv.org/abs/1902.09630) - Why a box loss that is not the box metric stops giving a gradient once the boxes stop overlapping.
- [The Lovász-Softmax loss](https://arxiv.org/abs/1705.08790) - Where optimising the overlap measure directly parts company with optimising it pixel by pixel.

### Augmentation

- [mixup](https://arxiv.org/abs/1710.09412) - Why a training target can be a blend of two labels rather than one of them.
- [CutMix](https://arxiv.org/abs/1905.04899) - Why cutting a hole in an image wastes the hole unless the label moves with the pixels.
- [AutoAugment](https://arxiv.org/abs/1805.09501) - Where augmentation stopped being a fixed list and became something searched for per dataset.
- [RandAugment](https://arxiv.org/abs/1909.13719) - Whether the policy search was buying anything a single strength setting cannot.
- [TrivialAugment](https://arxiv.org/abs/2103.10158) - Whether searched augmentation policies survive a baseline that picks one operation at random.

### Schedules and optimisation

- [SGDR: Stochastic Gradient Descent with Warm Restarts](https://arxiv.org/abs/1608.03983) - Where the cosine shaped schedule that most recipes now copy without comment was defined.
- [Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour](https://arxiv.org/abs/1706.02677) - What else in a recipe has to move before a larger batch reaches the same accuracy.
- [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101) - Why weight decay and an added squared penalty stop being the same thing under an adaptive optimiser.
- [Image classification reference training scripts](https://raw.githubusercontent.com/pytorch/vision/v0.20.0/references/classification/README.md) - Why a recipe comparison means nothing until every flag behind the baseline is written down.

### Regularisation and normalisation

- [Improving neural networks by preventing co-adaptation](https://arxiv.org/abs/1207.0580) - Where dropping units at random was introduced as a way to stop features leaning on each other.
- [Batch Normalization](https://arxiv.org/abs/1502.03167) - Why a layer whose output depends on the rest of the batch became the default everywhere.
- [Layer Normalization](https://arxiv.org/abs/1607.06450) - Where normalisation stopped depending on the batch and started depending on the feature axis.
- [Group Normalization](https://arxiv.org/abs/1803.08494) - What breaks in batch statistics once the batch on each device is too small to estimate them.
- [Rethinking "Batch" in BatchNorm](https://arxiv.org/abs/2105.07576) - The failure modes that follow from training on one set of batch statistics and testing on another.

## Rejected

- [AugMix](https://arxiv.org/abs/1912.02781) - Rule failed: conventions section 9, three to six entries per subsection. It would have displaced CutMix, and the effect it reports is a corruption suite number rather than a clean protocol one, which puts its evidence in the ground section sixteen is ordered around.
- [Instance Normalization](https://arxiv.org/abs/1607.08022) - Rule failed: conventions section 9, size limit. It would have displaced Layer Normalization, and the batch independent behaviour a reader needs at this point is already carried by the layer and group entries.
- [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515) - Rule failed: conventions section 7, the evidence standard. The case rests on dense feed-forward networks rather than on the convolutional stacks this section is about, so no measurement carrying the eight accuracy fields covers the use a reader here would make of it.
- [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) - Rule failed: conventions section 8, core admission. The operator ships in the framework, but the measurement that would justify it is not on any vision protocol, so nothing in this section's ground rests on it.
- [Designing Network Design Spaces](https://arxiv.org/abs/2003.13678) - Rule failed: owner-brief section 2, the earlier section keeps a shared source. Section six owns recipes against architectures and would hold this, so it is flagged for that owner rather than admitted twice.
- [Deep Learning Tuning Playbook](https://raw.githubusercontent.com/google-research/tuning_playbook/main/README.md) - Rule failed: conventions section 8, core admission requires a public measurement stating every field the evidence standard needs. It states at length that a baseline has to be tuned before an improvement over it is believed, which is this section's whole subject, and it reports no measurement at all, which makes it a watchlist candidate rather than an entry.
- [Albumentations](https://raw.githubusercontent.com/albumentations-team/albumentations/1.4.21/README.md) - Rule failed: conventions section 5, cite the copy the authors point at. The library is the artefact that makes the label transform explicit for boxes, masks and keypoints, and the journal paper its own citation block names could not be verified from this container, so the only verifiable URL is a file inside the repository rather than the canonical page.
- [IoU is not submodular](https://arxiv.org/abs/1809.00593) - Rule failed: conventions section 9, size limit. It would have displaced The Lovász-Softmax loss, and it corrects that paper's theoretical justification without changing anything an engineer would do differently.

## Claims

Every number below was read from the source's own abstract. The experimental sections could not be opened from this container, so any field that the abstract does not state is recorded as missing rather than assumed present.

### mixup reports top-one accuracy gains on ImageNet, CIFAR-10 and CIFAR-100 over an unaugmented baseline

- Fields present: datasets named, metric as top-one accuracy, baseline compared against as the same architecture without the augmentation.
- Fields missing: model and exact checkpoint, dataset split and version, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation, training data, hardware, the schedule length behind the quoted figure, and the figure itself, which the abstract does not state.
- Verdict: recorded unverified.
- Note: the entry earns its place for the interpolated label, not for a figure, and no figure from it is repeated in this list. Schedule length is the field most often dropped when this gain is quoted, and an augmentation that is given a longer run than its baseline is not being measured.

### CutMix reports plus 2.28 and plus 1.70 top-one accuracy points on ImageNet for ResNet-50 and ResNet-101

- Fields present: model family, dataset, metric as top-one accuracy, training data, baseline compared against as the same two architectures without the augmentation.
- Fields missing: exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware, schedule length.
- Verdict: recorded unverified.
- Note: the baseline is retrained rather than lifted from another paper, which is the right shape for this comparison. Schedule length is still the field that decides whether the gain belongs to the augmentation or to the extra training the augmentation needs.

### AutoAugment reports 83.5 percent top-one accuracy on ImageNet without extra data, and 1.5 percent error on CIFAR-10

- Fields present: dataset, metric as top-one accuracy, training data stated as no extra data.
- Fields missing: model and exact checkpoint for the headline figure, input resolution and preprocessing, evaluation protocol, hardware, and a baseline compared against at the same schedule.
- Verdict: recorded unverified.
- Note: the abstract does not name the architecture behind the headline figure, so that figure and the gain usually quoted beside it for a residual baseline are not the same experiment and cannot be subtracted from one another.

### RandAugment reports 85.0 percent top-one accuracy on ImageNet, 0.6 points over the prior searched policy and 1.0 points over a default augmentation pipeline

- Fields present: dataset, metric as top-one accuracy, baselines named as the prior searched policy and as a default augmentation pipeline.
- Fields missing: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware, schedule length.
- Verdict: recorded unverified.
- Note: the entry rests on the search space being reduced to a strength setting that can be tuned on the target task, which is a structural claim rather than a numeric one. The 0.6 point margin over the searched policy is the one that decides whether the search was worth running, and it is six tenths of the margin against the weaker baseline that gets quoted instead.

### RandAugment reports 1.0 to 1.3 mAP over a default augmentation pipeline on COCO detection, and within 0.3 mAP of the searched policy

- Fields present: dataset, metric named as mAP, baseline named as a default augmentation pipeline.
- Fields missing: model and exact checkpoint, input resolution and preprocessing, evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings, training data split, hardware.
- Verdict: cut.
- Note: a detection figure quoted as mAP with no protocol is exactly what section five refuses, and the protocol is not recoverable from the abstract. A spread of 1.0 to 1.3 reported against a 0.3 gap to the alternative is also a range wider than the difference it is being used to settle. The numbers are not repeated anywhere in this list and the entry does not rest on them.

### TrivialAugment reports parity with or improvement over searched augmentation policies while running no search

- Fields present: datasets, metric as top-one accuracy, the methods compared against, and the absence of a search phase, which removes the search budget from the comparison.
- Fields missing: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware.
- Verdict: recorded unverified.
- Note: the entry rests on the comparison being run at equal cost rather than on any figure, which is the conservative direction for a claim of this shape: a parity result that is wrong understates the trivial baseline and so cannot manufacture the conclusion the entry is cited for. No figure from it is repeated.

### Accurate, Large Minibatch SGD reports no accuracy loss up to a minibatch of 8192, ResNet-50 trained in one hour on 256 GPUs, and about 90 percent scaling efficiency from 8 to 256 GPUs

- Fields present: model as ResNet-50, dataset, metric as top-one accuracy, training data, hardware with its count, baseline compared against as the small minibatch run, and a matched epoch protocol.
- Fields missing: exact checkpoint, input resolution and preprocessing.
- Verdict: stands.
- Note: the baseline here is the retuned one, which is the thing this section exists to check, and the claim the entry rests on is that the learning rate must be rescaled and warmed up rather than that any particular number was reached. For the speed half, hardware and count, batch size and the statistic are stated while precision, framework version and compile flags are not; the one hour figure is wall clock for the whole training run, so data loading and preprocessing are inside the timer and evaluation is outside it.

### SGDR reports 3.14 percent and 16.21 percent error on CIFAR-10 and CIFAR-100 against a fixed step schedule

- Fields present: datasets, metric as error rate, training data, baseline compared against as a step schedule.
- Fields missing: model and exact checkpoint, input resolution and preprocessing, evaluation protocol, hardware, and the epoch budget at which each compared schedule was tuned.
- Verdict: recorded unverified.
- Note: restarts change how many epochs a run is allowed, so a schedule comparison that does not hold the budget fixed and does not re-search the step schedule's learning rate at that same budget is measuring two things at once. The entry earns its place for defining the cosine shape that later recipes copy.

### Decoupled Weight Decay Regularization reports about 15 percent relative improvement in test error over Adam with coupled weight decay

- Fields present: metric as relative test error, baseline compared against as Adam with the coupled penalty.
- Fields missing: model and exact checkpoint, dataset with split and version for the headline figure, input resolution and preprocessing, evaluation protocol, hardware, and the search grid behind the comparison.
- Verdict: recorded unverified.
- Note: a 15 percent relative improvement with no absolute error rate and no named dataset is not checkable, because relative to a weak enough starting point it is almost free. The accompanying claim that the best learning rate and the best decay factor become more independent implies a search over both, which is the retuned baseline shape this section demands, but the grid itself is not stated in the abstract; the entry rests on the decoupling argument rather than on the figure.

## Link notes

- https://arxiv.org/abs/1906.02629, https://arxiv.org/abs/1708.02002, https://arxiv.org/abs/1902.09630, https://arxiv.org/abs/1705.08790, https://arxiv.org/abs/1710.09412, https://arxiv.org/abs/1905.04899, https://arxiv.org/abs/1805.09501, https://arxiv.org/abs/1909.13719, https://arxiv.org/abs/2103.10158, https://arxiv.org/abs/1608.03983, https://arxiv.org/abs/1706.02677, https://arxiv.org/abs/1711.05101 - arxiv.org refuses every automated client from this container, with the connection rejected before any response, so none of these could be opened here. Each title and identifier pairing was confirmed by search, with the title returned against the identifier and the submission history quoted back.
- https://arxiv.org/abs/1207.0580, https://arxiv.org/abs/1502.03167, https://arxiv.org/abs/1607.06450, https://arxiv.org/abs/1803.08494 - the search budget for this pass ran out before these four were reached, so the title and identifier pairings were confirmed instead from the citations inside the framework's own module sources, fetched at a pinned release tag. Those sources are published by the maintainers of the layers in question, which makes the pairing a first party one rather than a search snippet.
- https://arxiv.org/abs/2105.07576 - the title and identifier pairing was confirmed from the paper reference table inside the authors' own detection library documentation, fetched at a pinned release tag. One author of the library is an author of the paper, so this is a first party pairing.
- https://arxiv.org/abs/1809.00593 - confirmed only as a title returned against this identifier in a single search result, and that result pointed at the PDF rather than the abstract page. It appears in the rejected block only, so nothing in the section rests on it, but the confirmation is thinner than for the entries above and should be rechecked before it is ever promoted.
- https://raw.githubusercontent.com/pytorch/vision/v0.20.0/references/classification/README.md - raw.githubusercontent.com is the one repository host reachable from here, so the recipe is cited as a file inside the repository at a pinned release tag rather than through the rendered repository page. The pin is deliberate: the recipe on the default branch changes without notice and a reading path that cites a moving recipe cites nothing. The rendered host and the GitHub API both refuse this container, the API because repository access has not been attached to this session, so repository existence was established by fetching the file itself.
- https://arxiv.org/abs/1805.09501 - the framework's own augmentation source cites the PDF for this one. The abstract page is cited here instead, under conventions section 5, because the abstract page carries the version history. That history matters for this entry: the title changed between versions, from policies to strategies, and the trimmed title avoids inheriting either wording.
- https://arxiv.org/abs/1705.08790 - the title carries a non-ASCII character in the method name. The URL is ASCII and the title is left exactly as the source spells it, per voice.md section 4.
- https://arxiv.org/abs/1207.0580 - the source title runs past the soft ceiling of sixty characters, so it is trimmed from the right rather than paraphrased, which drops the words naming feature detectors. The method name does not appear in the source title at all, so there is nothing shorter to keep.
- Collision with section 6 - mixup and CutMix are plausible entries for the recipes against architectures subsection of section six. Section six is earlier and keeps them under owner-brief section 2. If that owner claims them, this augmentation subsection drops to three entries and the replacements come from the rejected block, with AugMix the first candidate.
- Collision with section 10 - Focal Loss for Dense Object Detection and Generalized Intersection over Union both belong to the detector literature section ten covers. Section eight is the earlier section and keeps them, cited here for what each loss assumes about the label rather than for the detectors built on them, so section ten should pick differently.
- Collision with section 5 - the RandAugment detection figure is cut here rather than discussed, because the protocol that would make a mAP number checkable is section five's ground.
- Checker outcome for this draft, over twenty-six unique URLs: zero DEAD, zero MIRROR, zero REDIRECT, zero BLOCKED, three OK and twenty-three UNREACHABLE. The three OK results are the raw.githubusercontent.com files. All twenty-three UNREACHABLE results are arxiv.org, every one of them the proxy answering 403 to CONNECT before any request reached the host, which is this container's egress policy rather than a page that has gone. Confirmation routes for each are given above.

## Benchmark proposal

The claim worth measuring is the one every pipeline repeats without testing: that a geometric
augmentation applied to the image is safe so long as the transform is mild, and that a
horizontal flip in particular is free. The measurement generates synthetic scenes from a fixed
seed, each placing a few asymmetric markers on a background with Pillow, and gives each scene a
label set of one axis aligned box per marker plus a pair of named keypoints that differ only by
handedness. The same transforms, flip, rotation, shear and random resized crop, are then
applied twice, once to the image alone and once to the image and its label set together, and
the benchmark computes the intersection over union between the naive label and the correctly
transformed one, the share of boxes that leave the frame, and the share of keypoint pairs whose
handedness is now wrong. Quick mode runs a few hundred scenes with numpy and Pillow only, no
network and no GPU, and finishes well inside ten seconds. The claim is refuted if the median box
intersection over union under rotation and crop falls far enough that the untransformed label
no longer selects its own marker, and it is refuted more sharply if the flip case leaves every
box intersection over union at exactly one while the handedness error rate goes to one,
because that is a label which is completely wrong under a geometric check that reports no
error at all.
