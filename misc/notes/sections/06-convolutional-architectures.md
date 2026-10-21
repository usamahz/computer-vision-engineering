# 6. Convolutional architectures

Owner: engineer who has trained residual networks from scratch and read the ablations, suspicious of architecture claims that are training-recipe claims wearing a hat.

## Section

## 6. Convolutional architectures

Accuracy numbers across these entries were produced under different training recipes and different evaluation protocols, so the order is a dependency order and not a ranking.

### Foundations

- [A guide to convolution arithmetic for deep learning](https://arxiv.org/abs/1603.07285) - Where padding, stride and output size are worked out instead of guessed.
- [ImageNet Classification with Deep Convolutional Neural Networks](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) - Why trained features displaced designed ones, and how much of that was recipe rather than layers.
- [Network In Network](https://arxiv.org/abs/1312.4400) - Where the pointwise convolution and the pooled classifier head were argued for.
- [Very Deep Convolutional Networks](https://arxiv.org/abs/1409.1556) - Why a stack of small kernels replaced wide ones, and what the parameter bill became.
- [Going Deeper with Convolutions](https://arxiv.org/abs/1409.4842) - Why a layer stopped being one kernel size and became a set of parallel branches.

### Depth, residuals and width

- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) - Why adding layers stopped making training error worse.
- [Identity Mappings in Deep Residual Networks](https://arxiv.org/abs/1603.05027) - Why the order of normalisation, activation and addition inside a block changes what trains.
- [Wide Residual Networks](https://arxiv.org/abs/1605.07146) - Whether depth or width was carrying the gain, tested by moving one and holding the other.
- [Aggregated Residual Transformations for Deep Neural Networks](https://arxiv.org/abs/1611.05431) - What grouped convolution buys inside a residual block once parameters are held fixed.
- [Squeeze-and-Excitation Networks](https://arxiv.org/abs/1709.01507) - Why a channel reweighting block ended up inside most of the later efficient designs.

### Efficient convolutional designs

- [Xception](https://arxiv.org/abs/1610.02357) - Why the depthwise separable convolution replaced the mixed branch block it came from.
- [MobileNets](https://arxiv.org/abs/1704.04861) - Where the width and resolution multipliers that mobile deployments still tune were defined.
- [MobileNetV2](https://arxiv.org/abs/1801.04381) - Why an inverted bottleneck keeps activation memory inside a mobile budget.
- [ShuffleNet V2](https://arxiv.org/abs/1807.11164) - Why a model with fewer FLOPs can measure slower on the device it ships to.
- [EfficientNet](https://arxiv.org/abs/1905.11946) - Where compound scaling was proposed, and where the baseline recipe changed at the same time.

### Recipes against architectures

- [Bag of Tricks for Image Classification](https://arxiv.org/abs/1812.01187) - Where the recipe changes usually credited to architecture are ablated one at a time.
- [Revisiting ResNets](https://arxiv.org/abs/2103.07579) - What the residual network family reaches when only the recipe and the scaling rule move.
- [ResNet strikes back](https://arxiv.org/abs/2110.00476) - Why a published baseline accuracy reports its training year as much as its architecture.
- [A ConvNet for the 2020s](https://arxiv.org/abs/2201.03545) - What a convolutional stack reaches once the newer recipe is held equal across the comparison.

## Rejected

- [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://huggingface.co/papers/1905.11946) - Rule failed: conventions.md section 6, aggregators and paper mirrors. The page wraps a paper whose authors' own deposit is already cited, and it rots on a different schedule from the paper.
- [Convolutional Neural Networks: Architectures](https://cs231n.github.io/convolutional-networks/) - Rule failed: conventions.md section 6, course notes that restate a paper. The layer sizing arithmetic here is the same arithmetic the convolution arithmetic guide states first hand, and a disagreement would be settled against the guide rather than against the notes.
- [Train CIFAR10 with PyTorch](https://github.com/kuangliu/pytorch-cifar) - Rule failed: conventions.md section 5, admissible repositories are the authors' own, and section 6, code with no written account of what it does. A reimplementation with no paper behind it is a dependency, not a reading.
- [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993) - Rule failed: conventions.md section 9, size limit. It would have to displace Squeeze-and-Excitation Networks, and the squeeze-and-excitation block is a dependency of two later entries while dense concatenation is met far less often in production.
- [Designing Network Design Spaces](https://arxiv.org/abs/2003.13678) - Rule failed: conventions.md section 9, size limit. It would have to displace Revisiting ResNets, which makes the recipe-against-architecture separation more directly for the family an engineer actually ships.
- [Searching for MobileNetV3](https://arxiv.org/abs/1905.02244) - Rule failed: conventions.md section 9, size limit, and section 7, the evidence standard. It would have to displace EfficientNet, and its headline on-device latency figures state neither warmup and statistic nor whether preprocessing sits inside the timer.

## Claims

### Top-five error on the classification benchmark reported for the residual network entry, in Deep Residual Learning for Image Recognition

- Fields present: model and depth, dataset with split, metric with its definition, training data, baseline compared against, input resolution and preprocessing for the validation tables.
- Fields missing: exact checkpoint for each member of the submitted ensemble, hardware, evaluation protocol for the test-server entry including how multi-scale and multi-crop scoring were combined.
- Verdict: recorded unverified
- Note: The entry does not rest on this number. It rests on the degradation experiment, where a deeper plain stack reaches a higher training error than a shallower one under the same recipe, which is a within-paper comparison and reproducible. The headline ensemble figure is never repeated in the section.

### Top-five error reported in ImageNet Classification with Deep Convolutional Neural Networks

- Fields present: model, dataset with split, metric with its definition, input resolution and preprocessing, training data, hardware, baseline compared against.
- Fields missing: exact checkpoint, and the evaluation protocol shifts between rows because some are a single network and some average several networks and several crops.
- Verdict: recorded unverified
- Note: Much of the gap over the prior entries came from the recipe, the augmentation and the dropout rather than from the layer layout, which is precisely the confusion this section exists to separate. The number is not repeated.

### Width beating depth at matched parameter count, in Wide Residual Networks

- Fields present: model with its depth and widening factor, dataset with split, metric, training data, baseline compared against, evaluation protocol.
- Fields missing: hardware for the comparison rows, and the input resolution and preprocessing for the large-scale classification rows rather than the small-image rows.
- Verdict: recorded unverified
- Note: The decisive comparisons are on the small-image datasets, where the recipe differs from large-scale classification practice, so the ordering of depth against width does not transfer unexamined. The entry rests on the experimental design, not on the figure.

### Compound scaling accuracy on the classification benchmark, in EfficientNet

- Fields present: model variant, dataset with split, metric, input resolution per variant, training data, baseline compared against.
- Fields missing: a baseline trained under the same recipe, which is the field that matters here, since the scaled family carries augmentation, regularisation and optimiser choices the compared models did not have. The published and deposited versions also disagree on the headline top-one digit.
- Verdict: recorded unverified
- Note: This is the archetype the section is built to catch. The scaling rule may well be real, and the reported gain is still a joint claim about the rule and the recipe. The number is not repeated in the section, and the reason line names the confound instead.

### Inference speedup over the compared scaled model, in EfficientNet

- Fields present: hardware class, input resolution, the baseline compared against.
- Fields missing: how many devices, precision, batch size, framework and version with compile flags, warmup and the statistic reported, and whether preprocessing and postprocessing are inside the timer.
- Verdict: cut
- Note: Preprocessing and postprocessing are not stated to be inside the timer, and at the resolutions the larger variants use, resize and normalisation are not negligible. A multiplier with no batch size and no timer boundary is not a measurement, so it does not enter the list in any form.

### Measured latency disagreeing with floating point operation count, in ShuffleNet V2

- Fields present: hardware and how many, precision, batch size, input resolution, framework, the statistic reported, the baselines compared against at matched operation count.
- Fields missing: framework version with compile flags, warmup.
- Verdict: stands
- Note: The timer covers the network forward pass only, with preprocessing and postprocessing outside it, which the entry's reason line is written to survive. What stands is the qualitative claim, that ranking designs by operation count disagrees with ranking them by measured latency on a named device, and that claim is what the entry is for.

### Recipe gain on the residual baseline, in Bag of Tricks for Image Classification

- Fields present: model, dataset with split, input resolution and preprocessing, metric, evaluation protocol, training data, baseline compared against, which is the authors' own reproduction rather than a quoted figure.
- Fields missing: hardware.
- Verdict: recorded unverified
- Note: The value of the entry is the per-change ablation against one fixed baseline, not the final figure. Worth stating plainly that the end point of this recipe exceeds what a much deeper member of the same family reported under the older recipe, which is the whole argument of the subsection.

### Top-one accuracy of the unchanged residual architecture under the newer procedure, in ResNet strikes back

- Fields present: model and released checkpoint per named procedure, dataset with split, input resolution for training and for testing separately, preprocessing, metric, evaluation protocol, training data stated as the benchmark alone with no extra data and no distillation, baseline compared against as the same architecture under the original recipe.
- Fields missing: hardware for the headline row.
- Verdict: stands
- Note: The architecture is unchanged, the checkpoints are published, and the comparison is against the same architecture, so the gap is attributable to the recipe and a third party can check it. This is the one claim in the section that an architecture comparison against an older published baseline has to answer to.

### On-device latency reported for the searched mobile family, in Searching for MobileNetV3

- Fields present: hardware, precision, input resolution, framework, the baseline compared against.
- Fields missing: batch size, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
- Verdict: watchlist
- Note: Examined because the family is widely deployed and the figures are widely quoted. An entry resting on these latency figures would sit on the watchlist until the timer boundary and the statistic are stated, which is one of two reasons the source is in the rejected block rather than the section.

## Link notes

- https://arxiv.org/abs/1603.07285 - Stands for the whole set. The link checker was run on this draft and reports no dead link and no mirror, with every URL classified UNREACHABLE on a refused tunnel except the repository link, which came back BLOCKED. Both outcomes are this container's egress policy refusing CONNECT, not pages that have gone, so nothing here is recorded as dead. Every arXiv abstract page cited was instead confirmed by search with title and identifier agreeing, or from a repository README as noted below.
- https://arxiv.org/abs/2201.03545 - Identifier confirmed from the authors' own repository README at raw.githubusercontent.com/facebookresearch/ConvNeXt, which links this abstract page under the paper title, after the search budget for the session was exhausted.
- https://arxiv.org/abs/2103.07579 - Identifier confirmed from the timm source at raw.githubusercontent.com/huggingface/pytorch-image-models, which lists the title against this abstract page. The same file reconfirms the identifier for ResNet strikes back.
- https://arxiv.org/abs/1608.06993 - Rejected entry, identifier confirmed from the authors' own repository README at raw.githubusercontent.com/liuzhuang13/DenseNet. The README links the abstract page over plain HTTP and the secure form is cited here.
- https://arxiv.org/abs/2003.13678 - Rejected entry, identifier confirmed from the pycls README at raw.githubusercontent.com/facebookresearch/pycls, which also reconfirms the identifiers for the residual, aggregated residual and compound scaling papers.
- https://arxiv.org/abs/1905.02244 - Rejected entry, identifier confirmed from the mobilenet README under raw.githubusercontent.com/tensorflow/models, published by the group that trained the family.
- https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html - The conference's own abstract page, confirmed by search with the title. The same content is served under proceedings.neurips.cc and under an older slug carrying the submission number, and the hash form is the one that was confirmed, so it is the one cited. The host was not reachable from this container.
- https://proceedings.mlr.press/v97/tan19a.html - Confirmed to exist and to be the openly readable proceedings copy of the compound scaling paper, and deliberately not used. The arXiv abstract page carries the version history, and the two versions disagree on the headline digit, which is itself part of the claims record. The editor may prefer the proceedings copy; this is the only entry where that choice is live.
- https://openaccess.thecvf.com/content_CVPR_2019/html/He_Bag_of_Tricks_for_Image_Classification_with_Convolutional_Neural_Networks_CVPR_2019_paper.html - Same decision as above, confirmed by search and not used, so that the subsection cites one host throughout.
- https://huggingface.co/papers/1905.11946 - Appears only in the rejected block as the aggregator it is. Recorded here so nobody reads its presence as an admission.
- https://cs231n.github.io/convolutional-networks/ - Rejected entry. Existence confirmed through the page source in the cs231n site repository, whose front matter sets this exact permalink.
- https://github.com/kuangliu/pytorch-cifar - Rejected entry. Existence confirmed by fetching the repository README from raw.githubusercontent.com, since api.github.com refuses this session for repositories not attached to it.
- https://arxiv.org/abs/1502.03167 - Not cited. Batch normalisation is the obvious shared source between this section and section 8, whose subsection on regularisation and normalisation is where the argument belongs. This section is the earlier one and so has first claim on it, and it is declined here deliberately so that section 8 can take it. Flagged for the editor.
- https://arxiv.org/abs/2201.03545 - Collision, already resolved from the other side. The section 7 draft rejects this entry on the ground that the earlier section keeps it, so this section carries it, and the reason line here is written so that no transformer vocabulary is needed to read it.
- https://arxiv.org/abs/1905.11946 - Collision warning. Section 15 may want the compound scaling paper for a deployment argument. Earlier section keeps it. A second reason line there would have to say something different about latency rather than about scaling.

## Benchmark proposal

The claim worth measuring is that padding and stride choices change the receptive field and therefore the output geometry, in ways that silently misalign features. The folklore is that padding is a bookkeeping detail and that any choice which keeps the output size right is equivalent.

The measurement: synthesise an input with a single bright pixel at a known coordinate, then push it through a stack of strided convolutions implemented in numpy, with the kernel size, stride and padding convention varied. Three conventions are compared, symmetric padding of half the kernel size, the asymmetric convention that pads the far edge when the arithmetic does not divide evenly, and no padding at all. For each configuration, compute the centre of mass of the non-zero response, map it back to input coordinates using the stride product, and compare it against the receptive field centre predicted by the convolution arithmetic. Repeat with an even kernel size, and with an input size for which the output size formula truncates, so that trailing rows and columns are dropped. Pillow is used only to write a small side-by-side image of an impulse response against its predicted centre, so that the drift is visible as well as tabulated.

What would settle it: a table of predicted against measured input-space centres per configuration. The claim stands if odd kernels with symmetric padding land on the predicted centre exactly, while even kernels and the asymmetric convention drift by a fixed fraction of a pixel per strided stage, accumulating linearly with depth to a whole-pixel offset at the deepest stage, and if the truncating input size shifts the mapped centre again although every output tensor has the size the formula predicts. The claim fails if all configurations land on the predicted centre, or if the drift does not match the arithmetic. Quick mode runs one small input through four strided stages for every configuration and finishes in well under ten seconds on a laptop class machine with no GPU, using numpy and Pillow alone and no network access.
