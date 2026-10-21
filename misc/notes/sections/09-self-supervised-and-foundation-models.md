# 9. Self-supervised learning and vision foundation models

Owner: self-supervised learning specialist, suspicious of linear-probe numbers presented as general capability.

## Section

## 9. Self-supervised learning and vision foundation models

The frozen feature accuracies behind these entries were measured under different probe protocols and are not comparable with each other.

### Contrastive learning

- [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748) - Where the objective that almost every later pretext task reuses is first written down.
- [A Simple Framework for Contrastive Learning of Visual Representations](https://arxiv.org/abs/2002.05709) - Why the augmentation list, not the loss, decides what the representation keeps.
- [Momentum Contrast for Unsupervised Visual Representation Learning](https://arxiv.org/abs/1911.05722) - How the supply of negatives gets decoupled from the batch that has to fit in memory.
- [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](https://arxiv.org/abs/2005.10242) - Separates the two things a contrastive loss does and makes each one measurable on its own.

### Self-distillation and masked modelling

- [Bootstrap your own latent](https://arxiv.org/abs/2006.07733) - Whether a joint embedding method needs negatives at all to stay off a constant output.
- [Exploring Simple Siamese Representation Learning](https://arxiv.org/abs/2011.10566) - Which single operation keeps a Siamese network from collapsing to one vector.
- [Barlow Twins](https://arxiv.org/abs/2103.03230) - Avoiding collapse by decorrelating the embedding axes instead of pushing pairs apart.
- [Emerging Properties in Self-Supervised Vision Transformers](https://arxiv.org/abs/2104.14294) - Where centring and sharpening stand in for negatives and the nearest neighbour probe becomes routine.
- [BEiT: BERT Pre-Training of Image Transformers](https://arxiv.org/abs/2106.08254) - What a masked prediction target inherits from the tokeniser that produced it.
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377) - Why reconstructing pixels teaches anything once most of the image is hidden from the encoder.

### Vision foundation models and weights

- [DINOv2](https://arxiv.org/abs/2304.07193) - Where the scaling work moves from the objective to the curation of the pretraining corpus.
- [Model Card for DINOv2](https://github.com/facebookresearch/dinov2/blob/main/MODEL_CARD.md) - Which checkpoint carries which licence, and which probe produced each frozen feature number.
- [DINOv3](https://arxiv.org/abs/2508.10104) - Why dense patch features decay over a long schedule and what holding them steady costs.
- [Model Card for DINOv3](https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md) - Where the terms stop being permissive and the satellite trained weights are listed apart.

### Evaluating representations

- [Do Better ImageNet Models Transfer Better?](https://arxiv.org/abs/1805.08974) - Why a frozen feature ranking and a fine-tuned ranking of the same backbones disagree.
- [Revisiting Self-Supervised Visual Representation Learning](https://arxiv.org/abs/1901.09005) - How far the ranking of pretext tasks moves when only the backbone underneath changes.
- [How Well Do Self-Supervised Models Transfer?](https://openaccess.thecvf.com/content/CVPR2021/html/Ericsson_How_Well_Do_Self-Supervised_Models_Transfer_CVPR_2021_paper.html) - Where many shot accuracy stops predicting detection and dense prediction.
- [A Large-scale Study of Representation Learning with the Visual Task Adaptation Benchmark](https://arxiv.org/abs/1910.04867) - Where the adaptation protocol is fixed so that two representations can be compared at all.
- [Understanding Dimensional Collapse in Contrastive Self-supervised Learning](https://arxiv.org/abs/2110.09348) - What the spectrum of an embedding exposes that a probe accuracy hides.

## Rejected

- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/pdf/2111.06377) - Rule failed: conventions section 5, the abstract page is cited and the PDF is not. The PDF is the same deposit without the version history that tells a reader which revision a quoted number came from.
- [Masked Autoencoders Are Scalable Vision Learners](https://huggingface.co/papers/2111.06377) - Rule failed: conventions section 6, aggregators and paper mirrors. A hub page wrapping a paper hosted on arXiv adds nothing to the authors' deposit and rots on its own schedule.
- [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](https://icml.cc/virtual/2020/poster/53658) - Rule failed: conventions section 6, video lectures and talks, and section 5, not the authors' canonical copy. A venue listing with a recorded talk is not what a disagreement about the uniformity metric gets settled against.
- [INTRODUCING DINOV3](https://ai.meta.com/research/dinov3/) - Rule failed: conventions section 6, a vendor announcement that paraphrases the card. It carries neither the licence text nor the evaluation protocol, both of which the repository holds in full.
- [SimSiam](https://mmselfsup.readthedocs.io/en/stable/papers/simsiam.html) - Rule failed: conventions section 6, course notes and other pages that restate a paper already admitted. A framework's paper page drifts from the paper and is not the artefact an argument is resolved against.
- [Scalable Pre-training of Large Autoregressive Image Models](https://arxiv.org/abs/2401.08541) - Rule failed: conventions section 7, the ladder's last row. The frozen trunk headline rests on a two billion image corpus and a seven billion parameter run nobody outside the authors can repeat, so watchlist at best, and the weights repository could not be confirmed from this container.
- [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243) - Rule failed: conventions section 9, three to six entries per subsection. It would have displaced Barlow Twins in the self-distillation subsection, and Barlow Twins keeps the slot because decorrelation is the one collapse mechanism nothing else in this section covers.

## Claims

### SimCLR reports a linear probe top-one accuracy on ImageNet matching a supervised ResNet-50

- Fields present: model and exact checkpoint as a ResNet-50 with stated width, dataset with split as the ImageNet-1k training and validation sets, metric with its full definition as top-one accuracy, training data used as unlabelled ImageNet-1k, the baseline compared against as a supervised ResNet-50, evaluation protocol named as linear evaluation on frozen features.
- Fields missing: input resolution and preprocessing at probe time, evaluation protocol detail, meaning which frozen layer the features were taken from, whether augmentation is applied while the probe trains, and the probe's own optimiser and schedule, hardware.
- Verdict: recorded unverified
- Note: assessed from the abstract text confirmed by search, because the egress policy of this container blocks arxiv.org and the experimental section could not be opened. The protocol lives in an appendix rather than with the number, which is why the figure survives in the wild stripped of the three fields that make it checkable.

### BYOL reports a linear probe top-one accuracy on ImageNet with a ResNet-50 and with a wider ResNet

- Fields present: model and exact checkpoint as a ResNet-50 and a stated larger variant, dataset with split as ImageNet-1k, metric with its full definition as top-one accuracy, training data used, evaluation protocol named as linear evaluation.
- Fields missing: input resolution and preprocessing at probe time, evaluation protocol detail including the frozen layer and probe-time augmentation, hardware, the baseline compared against stated with its own recipe rather than as a quoted figure.
- Verdict: recorded unverified
- Note: abstract text only, same blocked host. Two numbers from two different backbone widths are routinely quoted side by side with contrastive results whose probe recipe differs, which is a comparison the fields as published do not support.

### DINO reports a nearest neighbour accuracy with a small ViT and a linear probe accuracy with a ViT-Base

- Fields present: model and exact checkpoint as a small ViT and a ViT-Base with stated patch size, dataset with split as ImageNet-1k, metric with its full definition as top-one accuracy, training data used, evaluation protocol named as nearest neighbour classification in one case and linear evaluation in the other.
- Fields missing: input resolution and preprocessing, evaluation protocol detail, meaning the neighbour count and distance used by the nearest neighbour probe and the frozen layer both probes read, hardware.
- Verdict: recorded unverified
- Note: abstract text only. The two headline figures come from two different backbones at two different patch sizes, so the published gap between the nearest neighbour probe and the linear probe is confounded with the model it was measured on and cannot be read as a property of either probe.

### The DINOv2 model card reports nearest neighbour and linear accuracies for the same checkpoints with and without register tokens

- Fields present: model and exact checkpoint as the named torch hub entry points with and without registers, dataset with split as ImageNet-1k and the Oxford hard retrieval split, metric with its full definition as top-one accuracy and mean average precision, training data used as LVD-142M, the baseline compared against as the same backbone without registers.
- Fields missing: input resolution and preprocessing, evaluation protocol, which the card defers to the papers in one sentence, so the neighbour count, the probe recipe and the probe-time augmentation are all absent from the page carrying the numbers, hardware.
- Verdict: recorded unverified
- Note: read in full from raw.githubusercontent.com. For the small backbone the nearest neighbour score rises with registers while the linear score falls, and the nearest neighbour retrieval score falls further than either moved, so the two probes order the same pair of checkpoints differently on the same page. The ranking inversion is recorded as the thing to measure and the figures are not repeated in the list.

### The DINOv2 model card states a fine-tuning gain on ImageNet-1k as a bare delta

- Fields present: training data used, model type.
- Fields missing: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, hardware, the baseline compared against.
- Verdict: cut
- Note: the card says a gain of about two points was measured, with no recipe, no split, no checkpoint and no metric definition attached. Seven of the eight fields are absent and the protocol is unrecoverable from the page, so the number never appears in the list and is not used to argue that fine-tuning is or is not worth it.

### Masked autoencoding reports a fine-tuned top-one accuracy using ImageNet-1k data only

- Fields present: model and exact checkpoint as a plain ViT-Huge, dataset with split as ImageNet-1k, metric with its full definition as top-one accuracy, training data used as ImageNet-1k alone, the baseline compared against as other methods restricted to the same data.
- Fields missing: input resolution and preprocessing, which matters because the headline uses a higher test resolution than the probe numbers it is quoted beside, evaluation protocol detail, hardware.
- Verdict: recorded unverified
- Note: abstract text only, so the test resolution is recorded as a missing field rather than asserted. This is a fine-tuning number and gets quoted against linear probe numbers from the contrastive line, which is the single most common category error in this part of the field.

### Do Better ImageNet Models Transfer Better reports a correlation between ImageNet accuracy and transfer accuracy

- Fields present: model and exact checkpoint as a stated set of classification backbones, dataset with split as a stated set of downstream classification datasets, metric with its full definition, evaluation protocol separated into fixed feature extraction and fine-tuning, the baseline compared against.
- Fields missing: nothing by name, but the field values contradict each other across versions of the same artefact.
- Verdict: cut
- Note: the later arXiv abstract gives correlation coefficients near unity while the first version and the conference version give a coefficient of determination of about a quarter for fixed features and about six sevenths for fine-tuning. Which number a reader repeats depends on which version they opened, so the coefficient is cut. The entry stands on the finding both versions share, that fixed feature ranking and fine-tuned ranking of the same backbones disagree.

### AIM reports a frozen trunk top-one accuracy at seven billion parameters

- Fields present: model and exact checkpoint as a stated parameter count, dataset with split as ImageNet-1k, metric with its full definition as top-one accuracy, evaluation protocol named as a frozen trunk, training data used as a corpus of about two billion images.
- Fields missing: input resolution and preprocessing, evaluation protocol detail for the head fitted on the frozen trunk, hardware, the baseline compared against at equal data and equal compute.
- Verdict: watchlist
- Note: abstract text only. The corpus is not available to anyone outside the authors and the run is not repeatable at that scale, which is the ladder's last row, so the entry did not enter the core. It would enter if the weights and the frozen trunk evaluation script were published and confirmable.

### The DINOv2 model card specifies the token count a given input size produces

- Fields present: all fields the claim has, since it is a specification rather than a measurement. Model and exact checkpoint as the named torch hub entry points, input resolution and preprocessing as a stated square input and a patch size of fourteen, the definition as one class token plus the patch grid plus four optional register tokens, and the stated cropping behaviour when the input is not a multiple of the patch size.
- Fields missing: none.
- Verdict: stands
- Note: checkable by loading the checkpoint and counting the output tokens, with no protocol to argue about. Recorded as the contrast case, because it is the only claim in this section that an engineer can falsify in one line.

## Link notes

- https://arxiv.org/abs/1807.03748, https://arxiv.org/abs/2002.05709, https://arxiv.org/abs/1911.05722, https://arxiv.org/abs/2005.10242, https://arxiv.org/abs/2006.07733, https://arxiv.org/abs/2011.10566, https://arxiv.org/abs/2103.03230, https://arxiv.org/abs/2104.14294, https://arxiv.org/abs/2106.08254, https://arxiv.org/abs/2111.06377, https://arxiv.org/abs/2304.07193, https://arxiv.org/abs/2508.10104, https://arxiv.org/abs/1805.08974, https://arxiv.org/abs/1901.09005, https://arxiv.org/abs/1910.04867, https://arxiv.org/abs/2110.09348 - arxiv.org is refused at the egress proxy of this container on every request, which is policy and not link rot. Each identifier was confirmed by search returning the same title and the same arXiv number together, and each is cited as the abstract page rather than the PDF. None of these is recorded as dead or unreachable.
- https://github.com/facebookresearch/dinov2/blob/main/MODEL_CARD.md, https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md - github.com and api.github.com both answer with a refusal for repositories not attached to this session. Both cards were instead retrieved in full from raw.githubusercontent.com on the main branch and read end to end, which is what the licence, the checkpoint list and the probe names in the entries rest on. The DINOv2 card carries the Apache licence and the DINOv3 card points at a bespoke licence held in the same repository, so the two families are not interchangeable in a product.
- https://openaccess.thecvf.com/content/CVPR2021/html/Ericsson_How_Well_Do_Self-Supervised_Models_Transfer_CVPR_2021_paper.html - the host is refused by the same policy. The URL was returned verbatim by search alongside the exact paper title, and the conference open access page is preferred over the arXiv deposit under the rule that a publisher copy the authors host openly wins. The arXiv identifier for the same work is 2011.13377, held in reserve if the open access path ever moves.
- https://arxiv.org/pdf/2111.06377, https://huggingface.co/papers/2111.06377, https://icml.cc/virtual/2020/poster/53658, https://ai.meta.com/research/dinov3/, https://mmselfsup.readthedocs.io/en/stable/papers/simsiam.html - rejected sources, kept in the draft so the rejection is auditable. Every one of these hosts is also refused by the egress policy, so none was fetched, and each URL came back from search with its title attached. Rejections whose host sits on the mirror or restatement blocklist in check_links.py were deliberately described by host in prose rather than linked, so that running the link checker over this draft does not fail on a link that exists to document a refusal.
- Ordering decision in Contrastive learning: the momentum contrast entry sits after the simple framework entry although it was deposited earlier, because the queue and the momentum encoder read as an answer to the batch size problem the earlier entry exposes. Date order is banned and this is the dependency order.
- Five titles sit over the sixty character soft ceiling and are kept whole, because each is a full title with no subtitle to drop, and trimming from the right at a word boundary removes the phrase a reader would search for, namely the simple framework title, the momentum contrast title, alignment and uniformity, the visual task adaptation benchmark, and dimensional collapse. The one title trimmed is the DINOv2 card, whose own heading lists the four model sizes after the words kept here.
- Scope boundary with section 14: image-text contrastive pretraining is theirs, so nothing here links a language supervised model, and the lineage in this section is image only throughout. The register token work that the DINOv2 card depends on would be a collision with section 7 and is left to them.
- misc/scripts/check_format.py does not exist in this checkout, so the draft was checked against voice.md by hand and with a local script over the entry lines. misc/scripts/check_links.py was not run against the live network, because every host in the draft is refused by the container's egress policy and the run would report the whole file as unreachable.

## Benchmark proposal

The claim is that a linear probe and a nearest neighbour probe both measure frozen representation quality and therefore rank two representations the same way, which is what every frozen feature accuracy quoted as capability quietly assumes. The DINOv2 card already contradicts it on a single page, where adding register tokens to the small backbone moves the nearest neighbour score up, the linear score down, and the nearest neighbour retrieval score further down than either, so the folklore is testable and likely wrong as a ranking instrument.

The measurement generates a labelled synthetic image set with numpy and Pillow from a fixed seed, then builds two feature maps of it with no training at all, one whose classes are separated by a hyperplane but spread widely within each class, and one whose classes are separated by a two factor code that no hyperplane cuts. Both are scored with a ridge regression linear probe fitted on a training split and with a cosine nearest neighbour probe against that same split, reporting the two by two accuracy table over seven seeds with its interquartile range. It settles the claim only if the ranking of the two representations inverts between the probes, with each probe's margin wider than its own seed to seed interquartile range; a difference in absolute accuracy between the probes settles nothing, because that difference is expected and is not a ranking. A second pass repeats the table with unit norm scaling and feature centring switched on and off at probe time, since those are the choices a published linear probe number usually leaves unstated, and a ranking that also moves with them shows the protocol is load bearing and the number alone is not evidence. Quick mode runs ten classes, six hundred training and three hundred test images at thirty-two by thirty-two with a sixty-four dimensional feature map, which finishes well inside ten seconds on the virtual machine named in the benchmark brief, needs no network at run time and imports nothing beyond numpy and Pillow.
