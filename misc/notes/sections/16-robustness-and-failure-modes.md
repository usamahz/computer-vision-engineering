# 16. Robustness and failure modes: distribution shift, adversarial, bias, safety

Owner: robustness researcher, suspicious of any robustness claim evaluated only on the corruption benchmark it was tuned against.

## Section

## 16. Robustness and failure modes: distribution shift, adversarial, bias, safety

A score on a corruption suite measures the suite as much as the model, so nothing below is comparable across suites.

### Distribution shift

- [Natural Adversarial Examples](https://arxiv.org/abs/1907.07174) - Why a test set filtered against one checkpoint still breaks the models that came after it.
- [The Many Faces of Robustness](https://arxiv.org/abs/2006.16241) - Why an intervention that fixes one kind of shift leaves the others untouched.
- [WILDS](https://arxiv.org/abs/2012.07421) - Where the difference between subpopulation shift and domain generalisation is made concrete.
- [Measuring Robustness to Natural Distribution Shifts](https://arxiv.org/abs/2007.00644) - Whether a corruption suite score predicts behaviour under real shift.

### Corruptions and synthetic perturbation

- [Benchmarking Neural Network Robustness to Common Corruptions](https://arxiv.org/abs/1903.12261) - Where the corruption suite and the error metric everyone quotes were defined.
- [make_imagenet_c.py](https://raw.githubusercontent.com/hendrycks/robustness/master/ImageNet-C/create_c/make_imagenet_c.py) - What each corruption name actually computes before a score is attributed to a model.
- [On Interaction Between Augmentations and Corruptions](https://github.com/facebookresearch/augmentation-corruption) - Where the held out corruptions that break a tuned robustness score come from.
- [3D Common Corruptions](https://github.com/EPFL-VILAB/3DCommonCorruptions) - Why a corruption applied uniformly over pixels cannot happen in a real scene.

### Adversarial robustness

- [Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572) - Why a tiny perturbation flips a prediction and how cheaply one is found.
- [Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083) - Where the threat model a defence has to state was written down.
- [Obfuscated Gradients Give a False Sense of Security](https://arxiv.org/abs/1802.00420) - How defences that only break the attacker's gradient get taken apart.
- [On Adaptive Attacks to Adversarial Example Defenses](https://arxiv.org/abs/2002.08347) - What an evaluation has to do before accuracy under attack means anything.
- [Certified Adversarial Robustness via Randomized Smoothing](https://arxiv.org/abs/1902.02918) - What a guarantee looks like once the norm and the noise level are stated.

### Bias, calibration and safety

- [FairFace](https://github.com/joojs/fairface) - What an audit set has to balance before a disparity between groups can be measured.
- [Fitzpatrick17k](https://github.com/mattgroh/fitzpatrick17k) - Why a clinical image classifier has to be scored separately by skin type.
- [FRVT](https://github.com/usnistgov/frvt) - Where the protocol that deployed face recognition is submitted to is specified.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) - Why a confidence score is not a probability until it is fitted to be one.
- [Can You Trust Your Model's Uncertainty?](https://arxiv.org/abs/1906.02530) - What happens to calibration once the test data stops matching the training data.

## Rejected

- [ImageNet-C Leaderboard](https://github.com/hendrycks/robustness#imagenet-c-leaderboard) - Rule failed: leaderboards and benchmark trackers, conventions section six. The suite's own repository carries a ranking table of mean corruption error, which is a snapshot of a protocol being gamed; the corruption implementation from the same repository is admitted instead.
- [RobustBench](https://github.com/RobustBench/robustbench) - Rule failed: leaderboards and benchmark trackers, conventions section six. The repository exists to maintain a standing ranking and its model zoo, and the attack methodology papers it ranks against are the admissible readings.
- [AugMix](https://github.com/google-research/augmix) - Rule failed: the evidence standard and the core bar, conventions section seven and section eight. The training section rejected it for its own size limit and pointed here, but the entry would rest on a mean corruption error from the suite whose corruption family its operations were selected against, quoted without preprocessing or the baseline's recipe, which makes it a watchlist line rather than a core entry.
- [ImageNetV2](https://github.com/modestyachts/ImageNetV2) - Rule failed: section collision, owner brief section two. The dataset section already admits the paper behind these test sets under splits and leakage, so the earlier section keeps the source and this section does not restate it with a thinner reason.
- [Robustness Metrics](https://github.com/google-research/robustness_metrics) - Rule failed: code without a paper, conventions section six. The repository documents an interface rather than a measurement, so the reading a reader would need is the calibration paper, which is already admitted.
- [Temperature Scaling](https://github.com/gpleiss/temperature_scaling) - Rule failed: code without a written account, conventions section six. The repository states that it is unmaintained and points elsewhere, and the method's own paper carries the protocol.
- [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox) - Rule failed: code without a paper, conventions section six. It is a library that reimplements attacks defined elsewhere, and a reader settling a disagreement needs the attack papers rather than the wrapper.

## Claims

### Mean corruption error for a residual backbone on ImageNet-C, as tabulated in the suite's own repository

- Fields present: model backbone, training data, dataset, metric, input resolution, baseline comparison through the clean error column.
- Fields missing: model and exact checkpoint; input resolution and preprocessing beyond the stated side length, including interpolation, crop and whether the shipped JPEG images or in-memory corruptions were scored; evaluation protocol, meaning the severity averaging and the normalising reference; training data used per row, since the rows differ by recipe; hardware.
- Verdict: cut
- Note: the table is a leaderboard and is rejected by rule, so none of its values are repeated in the section. The repository itself states that scoring the shipped JPEG images is preferred to computing corruptions in memory, which means two groups can report the same metric name from different pixels.

### Replacing batch normalization statistics with statistics of the corrupted images moves ImageNet-C mean corruption error, as stated in the authors' own repository abstract

- Fields present: model, dataset, metric, evaluation protocol including the number of adaptation samples, baseline using unadapted statistics.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; training data used; hardware.
- Verdict: recorded unverified
- Note: recorded once here and never repeated. The abstract reports mean corruption error falling from 76.7 per cent to 62.2 per cent for a residual baseline and from 56.5 per cent to 51.0 per cent for an augmentation-trained model, with no weight updated. A suite score that moves by that much when only the activation statistics change is a property of the evaluation protocol, not of the model, which is the reason this section carries a warning sentence.

### Augmentation gains do not transfer to perceptually dissimilar corruptions, as claimed by the held out suite's repository

- Fields present: dataset definitions for the held out corruption suites with their corruption types and severity count, metric, evaluation protocol through the stated distance measure between augmentations and corruptions, baseline given by the same augmentations scored on the original suite.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; training data used; hardware; the effect size itself, because the paper's tables are on a host this container cannot reach.
- Verdict: recorded unverified
- Note: the entry rests on the generation code for the held out corruptions, not on a number, so the missing effect size does not move it to the watchlist. This is the claim the section's benchmark proposal measures directly.

### Seven of nine defences accepted at a single conference were reduced to low accuracy by improved attacks

- Fields present: threat model with norm and radius per row, dataset per row, metric as accuracy under the authors' own attack, baseline as each defence's own reported robustness, evaluation protocol described per defence.
- Fields missing: exact checkpoints for the rows where the defence authors released no weights; training data used; hardware.
- Verdict: stands
- Note: the headline is a count of defences rather than an accuracy, and every row carries its norm and radius, which is why it survives the ladder. The one defence that held is named, and the authors say they could not defeat it without leaving its threat model, which is the correct form for a negative result.

### Certified robustness radius under randomized smoothing

- Fields present: norm, noise standard deviation, dataset, metric as certified accuracy with an abstention option, evaluation protocol as a Monte Carlo certification with a stated failure probability.
- Fields missing: none in the authors' own statement of the guarantee.
- Verdict: stands
- Note: the guarantee is stated in one norm only, and the certificate is probabilistic with an abstention rate. A radius quoted without the norm, the noise level and the failure probability is cut on sight, because those three are the claim and the radius alone is decoration.

### Accuracy drop between the original ImageNet validation set and its rebuilt replacement

- Fields present: dataset construction with three test sets, their selection frequency protocols and their revision identifiers, baseline as the original validation set, breadth of models evaluated.
- Fields missing: the drop itself with per-model input resolution and preprocessing, because the paper is hosted on an author's server this container cannot reach; metric definition per model; hardware.
- Verdict: recorded unverified
- Note: examined because it is the number everybody quotes for natural shift, not because anything here rests on it. The source is kept by the dataset section after a collision, and no figure from it appears in this section.

### Classifier accuracy on the naturally occurring hard set, as quoted for natural shift

- Fields present: dataset with its class list, baseline given by the residual network whose predictions the dataset's own presentation shows, metric as single label accuracy.
- Fields missing: model and exact checkpoint for the quoted figures; input resolution and preprocessing; evaluation protocol; training data used; hardware.
- Verdict: recorded unverified
- Note: the field that decides what the number means is not on the ladder at all, namely the model whose failures selected the images. An accuracy on this set is partly a statement about that selection model's family, so the entry is admitted for how the set was built and not for any published figure.

### Calibration fitted in distribution degrades under dataset shift

- Fields present: methods compared, datasets including the corruption suites and a rotated digit set, metric family, evaluation protocol as a shift sweep with held out out-of-distribution test sets, baseline as the uncalibrated maximum likelihood network.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; training data used; hardware.
- Verdict: recorded unverified
- Note: the structural result is what the entry rests on, that a calibration fix validated on clean data does not survive the shift, so the absence of a reproducible single figure does not sink it.

## Link notes

- WebSearch was unavailable for this draft: the per-turn budget is shared across all sixteen owners and was exhausted before this section ran. Every identifier below was therefore confirmed by reading the authors' own repository through raw.githubusercontent.com, which is the only reachable confirmation route left, and the title and identifier appear together in the fetched file in each case.
- https://api.github.com - returns 403 for every repository in this session because repository access is gated per session, so repository existence was confirmed by a two hundred response from raw.githubusercontent.com on the repository's own README instead.
- https://arxiv.org/abs/1903.12261 - title to identifier agreement confirmed in hendrycks/robustness README. arxiv.org itself is blocked by this container's egress policy, which is policy and not link rot.
- https://arxiv.org/abs/2006.16241 - confirmed in hendrycks/imagenet-r README, which links the title to the identifier and carries the matching citation block.
- https://arxiv.org/abs/2012.07421 - confirmed in p-lambda/wilds README, which links the main paper to the identifier.
- https://arxiv.org/abs/2007.00644 - confirmed in modestyachts/imagenet-testbed README and its citation block. Title trimmed from the right to drop the trailing field name, which leaves it unambiguous.
- https://arxiv.org/abs/1412.6572 - identifier is attached to the title in the attack table of Harry24k/adversarial-attacks-pytorch, and to the same method in the cleverhans tutorials list.
- https://arxiv.org/abs/1706.06083 - title and identifier appear together in the obfuscated gradients README and in MadryLab/mnist_challenge, which states the title in full.
- https://arxiv.org/abs/1802.00420 - confirmed in the authors' own anishathalye/obfuscated-gradients README, whose heading is the paper title.
- https://arxiv.org/abs/2002.08347 - title confirmed in the authors' own wielandbrendel/adaptive_attacks_paper README; identifier confirmed by the RobustBench README, which cites the same work at that identifier. Two sources were needed because the authors' README carries the title without a link.
- https://arxiv.org/abs/1902.02918 - confirmed in the authors' own locuslab/smoothing README, whose heading is the paper title.
- https://arxiv.org/abs/1706.04599 - confirmed in gpleiss/temperature_scaling, which names the title at that identifier. The repository is in Rejected and the paper is admitted.
- https://arxiv.org/abs/1906.02530 - confirmed in the uncertainty benchmark README inside google-research/google-research, which states the full title at that identifier. The title is kept with its question mark because that punctuation is the source's own and the trailing half is the subtitle.
- https://raw.githubusercontent.com/hendrycks/robustness/master/ImageNet-C/create_c/make_imagenet_c.py - cited deliberately as the raw file rather than the repository page, because the entry is about what the corruption functions compute. Verified with a two hundred response.
- https://github.com/modestyachts/ImageNetV2 - considered as the artefact for the rebuilt test sets, because the paper is served from an author's own server this container cannot reach. Dropped on a collision: the dataset section already admits that paper under splits and leakage, the earlier section keeps it, and the naturally occurring hard set takes the opening slot here instead. Recorded in Rejected.
- https://arxiv.org/abs/1907.07174 - title to identifier agreement confirmed in the authors' own hendrycks/natural-adv-examples README, whose heading is the paper title and whose first line links that identifier.
- https://github.com/google-research/augmix - collision flag resolved the other way than expected: the training section rejected this for its own size limit and pointed at this section, and it is rejected here on the evidence standard rather than admitted, so neither section carries it and it belongs on the watchlist.
- https://github.com/facebookresearch/augmentation-corruption - repository cited rather than the paper, since the README states the title but carries no identifier and the generation code for the held out suites is the artefact.
- https://github.com/EPFL-VILAB/3DCommonCorruptions - the authors' project page is linked from this README, and that page would be preferred, but its host is unreachable here so the page could not be confirmed and the repository is cited instead.
- https://github.com/usnistgov/frvt - the issuing body's own repository, carrying the evaluation application programming interface documents. The demographic effects report itself is published on a NIST host that this container cannot reach, so the report is not cited and no figure from it is used.
- Left out for want of confirmation, each a source that would otherwise have been considered: the commercial gender classification audit published in a conference proceedings whose host refused every request; the NIST demographic effects report; the ObjectNet dataset page; and the first adversarial examples paper, where only an attribution to the authors at an identifier could be found and not the title itself. None of these is recorded as dead. All are hosts this container cannot reach, or an agreement that could not be shown without WebSearch.
- misc/scripts/check_links.py on this draft: twenty six unique URLs, zero DEAD, zero MIRROR, twelve
  UNREACHABLE, all of them arxiv.org abstract pages refused at the proxy, twelve BLOCKED, all of
  them github.com repository pages refused to an automated client, and two OK on
  raw.githubusercontent.com. Every UNREACHABLE and BLOCKED result was confirmed to exist by the
  repository route described above, so none of them is link rot.
- Hosts probed once each and found unreachable or refusing: arxiv.org, nvlpubs.nist.gov, pages.nist.gov, proceedings.mlr.press, objectnet.dev, zenodo.org, openreview.net, wilds.stanford.edu, 3dcommoncorruptions.epfl.ch, gendershades.org, api.github.com, github.com. Only raw.githubusercontent.com answered.

## Benchmark proposal
The claim worth measuring is that a pipeline tuned against one corruption does not transfer to
a held out corruption, so a corruption suite score measures the suite as much as the model.
The measurement needs no weights. Generate a deterministic two class set of synthetic greyscale
images from a fixed seed, one class carrying low frequency blobs and the other carrying high
frequency stripes at matched total energy, then classify with a fixed hand written statistic,
the ratio of high band to low band energy from a small separable convolution, thresholded. The
tunable part is the preprocessing and the threshold, which is what an engineer tunes in
practice: a blur radius, a median filter radius, a resize with its resampling filter from
Pillow, and a re-encode quality, searched over a small declared grid.

Tune that grid to maximise accuracy on one corruption only, additive pixel noise, then score
three pipelines, the untuned one, the one tuned on noise and the one tuned on the held out
corruption, against both corruptions at every severity, reported per severity rather than as
one average, because averaging over severities is where the effect hides. The claim is settled
in its favour if the gain from tuning on noise keeps less than half of itself on the held out
corruption, or goes negative, while tuning on the held out corruption recovers it, and settled
against if most of the gain transfers. Quick mode uses sixty images per class at sixty four
pixels square and three severities, finishing well under ten seconds on the machine named in
the benchmark brief, with numpy and Pillow alone, no GPU and no network at run time. What it
measures is the tuning transfer effect on a synthetic classifier, and explicitly not any
published robustness number: no checkpoint is downloaded, no mean corruption error is
reproduced, and the corruptions are the benchmark's own rather than a published suite.
