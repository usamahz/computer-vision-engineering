# 7. Attention, vision transformers and hybrids

Owner: attention-against-convolution comparisons, tracked one at a time, suspicious of any comparison run at unequal compute or unequal data.

## Section

## 7. Attention, vision transformers and hybrids

The accuracy numbers behind these sources were produced on different pretraining corpora and under different recipes, so the order of entries carries no comparison.

### Attention

- [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) - Where attention begins as an alignment over a sequence rather than a layer in a vision stack.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Where the scaled dot product operator and the position encoding it needs are defined.
- [Non-local Neural Networks](https://arxiv.org/abs/1711.07971) - What a global attention block costs once it is dropped into a convolutional stack.
- [On the Relationship between Self-Attention and Convolutional Layers](https://arxiv.org/abs/1911.03584) - Whether an attention layer can express a convolution at all, which decides what a comparison means.
- [Exploring Self-attention for Image Recognition](https://github.com/hszhao/SAN) - Attention replacing convolution in one backbone with the parameter budget held fixed.

### Vision transformers

- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) - Where a patch sequence replaces the convolutional stem and nothing convolutional is left.
- [Conditional Positional Encodings for Vision Transformers](https://arxiv.org/abs/2102.10882) - Why a fixed position embedding breaks as soon as the input resolution changes.
- [Early Convolutions Help Transformers See Better](https://arxiv.org/abs/2106.14881) - Why the patch embedding stem decides whether the optimiser stays stable.
- [Do Vision Transformers See Like Convolutional Neural Networks?](https://arxiv.org/abs/2108.08810) - Where the two families differ inside the network rather than on the metric everyone quotes.

### Data, scale and distillation

- [Training data-efficient image transformers](https://arxiv.org/abs/2012.12877) - What distillation and augmentation buy when the pretraining corpus is held to a public one.
- [How to train your ViT?](https://arxiv.org/abs/2106.10270) - Where augmentation, corpus size and compute are traded against each other under one protocol.
- [Scaling Vision Transformers](https://arxiv.org/abs/2106.04560) - What the error rate does as corpus and model grow together rather than one at a time.
- [Better plain ViT baselines for ImageNet-1k](https://arxiv.org/abs/2205.01580) - A recipe that names its epoch count and its hardware, which most comparisons leave implicit.
- [Vision Transformer and MLP-Mixer Architectures](https://github.com/google-research/vision_transformer) - Which checkpoint was pretrained on which corpus, stated for each released file.

### Hierarchies and hybrids

- [Pyramid Vision Transformer](https://arxiv.org/abs/2102.12122) - Why dense prediction needs a feature pyramid that a single scale token grid cannot give.
- [Swin Transformer](https://arxiv.org/abs/2103.14030) - Where windowing makes attention cost grow with image area instead of with its square.
- [CoAtNet](https://arxiv.org/abs/2106.04803) - What stacking convolution underneath attention changes as the pretraining corpus grows.
- [MetaFormer Is Actually What You Need for Vision](https://arxiv.org/abs/2111.11418) - Whether the attention operator or the block around it is doing the work.

## Rejected

- [Stand-Alone Self-Attention in Vision Models](https://arxiv.org/abs/1906.05909) - Rule failed: conventions section 7 ladder, a field missing and the entry resting on the number, plus conventions section 8 requiring an implementation someone outside the authors' group can run. The entry would exist for its matched budget comparison against a residual baseline, and that comparison is reported in floating point operations and parameter counts with no released checkpoint and no implementation from the authors, so the verdict is watchlist rather than core.
- [A ConvNet for the 2020s](https://arxiv.org/abs/2201.03545) - Rule failed: owner brief section 2, where the same source is the natural entry for two sections the earlier section keeps it. Section 6 owns convolutional architectures and the recipe papers that reassigned credit, so the modernised convolutional baseline belongs there and only the comparison belongs here.
- [MobileViT](https://arxiv.org/abs/2110.02178) - Rule failed: conventions section 9, three to six entries per subsection with six full. It would have displaced CoAtNet in Hierarchies and hybrids, and CoAtNet stays because its corpus sweep is what makes the hybrid argument checkable rather than a mobile latency claim measured on one vendor's accelerator.
- [MLP-Mixer: An all-MLP Architecture for Vision](https://arxiv.org/abs/2105.01601) - Rule failed: conventions section 9, the subsection size limit. It would have displaced MetaFormer Is Actually What You Need for Vision, and MetaFormer stays because it changes only the token mixer inside a fixed block shape, which is the comparison this section exists to police.
- [An Image is Worth 16x16 Words](https://arxiv.org/pdf/2010.11929) - Rule failed: conventions section 5, the abstract page is cited and not the PDF because the abstract page carries the version history. The same work enters the section through its abstract page instead, and the PDF link is what search offered first.
- [vit-pytorch](https://github.com/lucidrains/vit-pytorch) - Rule failed: conventions section 5, which admits the authors' own repository and not a third party reimplementation. Nothing in it is the artefact any claim in this section rests on.
- [An Empirical Study of Training Self-Supervised Vision Transformers](https://arxiv.org/abs/2104.02057) - Rule failed: owner brief section 3 coverage boundary. The instability it diagnoses is real and the pretext task is section 9's ground, so admitting it here would duplicate that section and pull self-supervised pretraining into a subsection about supervised data scale.

## Claims

### Top-one accuracy of the largest vision transformer after pretraining on a private corpus, as stated in An Image is Worth 16x16 Words

- Fields present: dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, hardware as accelerator core days, the baseline compared against, which was pretrained on the same corpus.
- Fields missing: model and exact checkpoint, since the weights for the private corpus arm were not released; training data used, which is named but not auditable because the corpus is not public and its composition and duplication against the evaluation split cannot be inspected by anyone outside.
- Verdict: recorded unverified
- Note: The number is not repeated anywhere in the section and the entry stands on the operator and the patch embedding instead. The convolutional baseline in that table did get the same pretraining corpus, which is the one thing most later comparisons drop.

### Top-one accuracy reachable with the public thousand-class corpus alone, and with a distillation token, as stated in Training data-efficient image transformers

- Fields present: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, training data used, hardware with wall clock.
- Fields missing: the baseline compared against, in the sense that the convolutional entries in the comparison tables are quoted from their own publications, so their epoch count, augmentation policy and regularisation are not the recipe applied to the transformer.
- Verdict: recorded unverified
- Note: The trainability claim is checkable because code and checkpoints exist. The attention against convolution reading of the same tables is not, because only one side of it was retrained.

### Headline classification and detection numbers of the hierarchical windowed design, as stated in Swin Transformer

- Fields present: model and exact checkpoint, dataset with split and version, input resolution, metric, training data used, the baseline compared against for the backbone swap tables.
- Fields missing: evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings for the detection number, which uses multi-scale testing inside a heavier detection framework; training data used for the classification headline, which is quoted as the thousand-class benchmark while the pretraining corpus is the larger labelled superset.
- Verdict: recorded unverified
- Note: The backbone swap tables, where a convolutional backbone and this one are trained inside the same detection framework at a similar budget, are the matched part and are the reason the entry is here. The headline is not matched and is not repeated.

### A fully self-attentional residual network beating its baseline at lower floating point operation and parameter counts, as stated in Stand-Alone Self-Attention in Vision Models

- Fields present: dataset with split and version, metric with its full definition, training data used, the baseline compared against at the same depth and recipe, floating point operation and parameter counts.
- Fields missing: model and exact checkpoint, hardware, framework and version with compile flags, batch size, warmup and the statistic reported.
- Verdict: watchlist
- Note: Fewer floating point operations is not lower latency, and no timing is reported, so neither the accuracy nor the cost half can be rerun outside the authors' group. Preprocessing and postprocessing do not arise because no timer is reported at all. This is why the paper sits in Rejected rather than in Attention.

### Regularisation and augmentation substituting for roughly an order of magnitude more pretraining data, as stated in How to train your ViT?

- Fields present: model and exact checkpoint for the released sweep, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, hardware, epoch and compute budget stated per run, the baseline compared against inside the sweep.
- Fields missing: training data used, for the private corpus arm only, which is the arm the order of magnitude claim is measured against.
- Verdict: recorded unverified
- Note: The public corpus half of the sweep is reproducible from the released checkpoints and the released training code, which is rare in this subsection. The cross corpus half is the part no outsider can check, and it is the half the headline sentence rests on.

### A plain vision transformer reaching residual network level top-one accuracy in a stated epoch budget, as stated in Better plain ViT baselines for ImageNet-1k

- Fields present: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, training data used, hardware with wall clock, the baseline compared against at the same epoch count.
- Fields missing: none
- Verdict: stands
- Note: This is the one claim in the section where the epoch count, the accelerator and the wall clock are all stated next to the number, and the training code is published, so the claim may be stated in notes. The convolutional baseline is the conventional ninety epoch recipe rather than a rerun under the same augmentation, which the note records and which does not move the verdict because the claim is about the transformer side.

### Accuracy of the convolution and attention hybrid across three pretraining corpora, as stated in CoAtNet

- Fields present: model and exact checkpoint for the public corpus arms, dataset with split and version, input resolution, metric with its full definition, evaluation protocol, the baseline compared against.
- Fields missing: training data used, for the largest arm, whose corpus is private and roughly an order of magnitude larger than the public one; hardware and epoch count are not restated alongside each of the three numbers.
- Verdict: recorded unverified
- Note: The three numbers are quoted together as if they were one scaling curve, and the corpus changes between them, so the comparison with any single corpus baseline is unequal data rather than unequal architecture.

### A pooling token mixer matching attention baselines at lower parameter and multiply-accumulate counts, as stated in MetaFormer Is Actually What You Need for Vision

- Fields present: model and exact checkpoint, dataset with split and version, input resolution and preprocessing, metric with its full definition, training data used, parameter and multiply-accumulate counts, the baseline compared against by name.
- Fields missing: the baseline compared against in the matched sense, since the transformer and multilayer perceptron baselines are quoted from their own papers rather than retrained under this recipe; hardware, batch size and warmup for the throughput reading.
- Verdict: recorded unverified
- Note: The internal comparison, where only the token mixer changes and the rest of the block is fixed, is matched and is why the entry earns its place. The external comparison against quoted baselines is not, and the margins there are small enough that the recipe difference could account for them.

### Stability and accuracy gain from a convolutional stem at matched floating point operations, parameters and runtime, as stated in Early Convolutions Help Transformers See Better

- Fields present: dataset with split and version, input resolution and preprocessing, metric with its full definition, evaluation protocol, training data used, the baseline compared against, which is the same model with one transformer block removed so that the budget matches.
- Fields missing: model and exact checkpoint, since no weights accompany the study; framework and version with compile flags, and the hardware, for the runtime half of the match.
- Verdict: recorded unverified
- Note: The budget match is stated as a design constraint rather than demonstrated with a timing table, so the runtime claim has no declared timer boundary and nothing can be said about whether preprocessing and postprocessing sit inside it. The stability finding does not depend on the runtime half.

## Link notes

- https://arxiv.org/abs/1409.0473 - Confirmed by search that the identifier and the title agree. The host refuses automated clients from this container, so the abstract page itself was not fetched. The search result set also surfaced ar5iv and web3 front ends for the same identifier, both rejected as mirrors.
- https://arxiv.org/abs/1706.03762 - Confirmed by search. Mirror candidates for the same identifier, including an aggregator paper page and an arXiv HTML front end, were rejected by rule rather than by preference.
- https://arxiv.org/abs/1711.07971 - Confirmed by search. The authors' own implementation lives in a separate video repository and is not cited here, because the entry rests on the operator rather than on the code. Possible collision with section 11, which owns temporal modelling and may want the same paper for its video results; the attention operator reading is the one kept here, and the video reading is left to that owner.
- https://arxiv.org/abs/1911.03584 - Confirmed by search, which also named the authors' code repository. The ICLR listing for the same work is a conference programme page rather than an openly hosted canonical copy, so the abstract page is cited. Search ranked an arXiv HTML reader front end for this identifier above the abstract page; that host sits on the link checker's mirror list and is refused by rule, and it is named here rather than linked because a mirror link anywhere in a file fails the build.
- https://github.com/hszhao/SAN - The repository exists and its own heading, fetched through raw.githubusercontent.com, matches the title used here. The repository is cited rather than a paper page because the arXiv identifier for this work could not be confirmed before the search budget for this session ran out, and because the matched budget claim depends on the code and the custom kernels that the repository carries. The authors host a copy of the paper on their own academic page and link it from this repository, which is where a reader lands next.
- https://arxiv.org/abs/2010.11929 - Confirmed by search. The conference version sits on an open review platform and the authors' own deposit is the arXiv page, which carries the version history, so the abstract page is cited. The PDF link for the same identifier is in Rejected. An aggregator paper page on a model hosting site and a generated summary site both carried this title and identifier in the search results, and both are refused by rule; they are named here rather than linked, because an aggregator link in a draft is an aggregator link whatever block it sits in.
- https://arxiv.org/abs/2102.10882 - Confirmed by search, which also showed that the latest revision is the conference version. Title kept in full because the shorter community name for this method is not in the title.
- https://arxiv.org/abs/2106.14881 - Confirmed by search. A conference proceedings PDF exists for the same work and was not cited, because it is a PDF rather than a landing page with version history.
- https://arxiv.org/abs/2108.08810 - Confirmed by search. The search result pointed at a versioned abstract page and the versionless form is cited, per the rule against version suffixes.
- https://arxiv.org/abs/2012.12877 - Confirmed by search. Title trimmed from the right at the soft ceiling, which drops the distillation half of the title; the reason line carries that half instead.
- https://arxiv.org/abs/2106.10270 - Confirmed by search. This work was later published in a journal whose landing page is on an open review platform; the identifier for that page could not be confirmed from this container, so the abstract page is cited. Title trimmed from the right at the question mark.
- https://arxiv.org/abs/2106.04560 - Confirmed by search. A vendor research publication page carries the same title and was not cited, because it is a listing entry rather than the authors' deposit with version history.
- https://arxiv.org/abs/2205.01580 - Confirmed by search. A conference PDF on a proceedings host carries the same title and was not cited for the same reason.
- https://github.com/google-research/vision_transformer - Verified by fetching the repository README through raw.githubusercontent.com, which returned the heading used as the title here and the list of papers and corpora the released checkpoints belong to. The GitHub API is not reachable from this container, so repository existence was confirmed this way instead. That README is also what confirmed the identifier and title for the all perceptron architecture listed in Rejected.
- https://arxiv.org/abs/2102.12122 - Confirmed by search, which also named the authors' repository. Title trimmed from the right, dropping the subtitle.
- https://arxiv.org/abs/2103.14030 - Confirmed by search. Several framework documentation pages restate this paper and none is cited, because documentation that restates a paper is not the artefact.
- https://arxiv.org/abs/2106.04803 - Confirmed by search. Title is the method name, which the paper's own title carries first.
- https://arxiv.org/abs/2111.11418 - Confirmed by search, which also named the authors' repository; the repository was additionally reachable through raw.githubusercontent.com. The paper is cited rather than the repository because the entry rests on the ablation rather than on the code.
- https://arxiv.org/abs/2201.03545 and https://arxiv.org/abs/2104.02057 - Both identifiers and titles were confirmed by fetching the authors' own repository READMEs through raw.githubusercontent.com, since search was unavailable by then. Both appear only in Rejected.
- Cross section collisions, checked against the drafts present at delivery: the vision transformer abstract page also appears in the section 1 draft, but only inside that draft's Rejected block on the ground that an item in Start here may not need section 7, so there is no live collision and this section keeps it. The modernised convolutional baseline named in Rejected here is carried live by the section 6 draft, which records the same resolution from its side, so the two drafts agree on who keeps it. No other URL in this section appears in any other draft.
- Blocked hosts, recorded once rather than retried: arxiv.org refuses the proxy in this container with a policy denial on CONNECT, as do the publisher and framework documentation hosts. The GitHub API answers with a policy denial as well. None of these is a dead link and none is recorded as one.
- What this draft could not verify: the experimental sections of the papers themselves were not readable from this container, so every field inventory in Claims comes from the abstract as confirmed by search, from the authors' repository documentation, and from the paper's own tables as reported in those sources. The evidence marshal should re-read the experimental sections for the three claims whose verdicts turn on whether a convolutional baseline shared the recipe, which are the distillation claim, the pooling token mixer claim and the hierarchical windowed design claim.

## Benchmark proposal

The claim is that attention cost grows with the square of the token count while convolution cost grows linearly in it, so a comparison of the two operators at one input resolution says nothing about the same comparison at another resolution. The measurement generates one synthetic image from a fixed seed, resizes it with Pillow across a sweep of input resolutions, embeds non-overlapping patches of fixed side into a fixed channel width with one matrix multiply, and then times two forward operators on the resulting token grid in numpy at single precision. The first is a single-head self-attention pass that materialises the full score matrix and normalises it; the second is a dense convolution of fixed support over the same spatial grid at the same channel width. Resizing and patch embedding sit outside the timer and are measured separately, because folding them in is the usual way this comparison is made to flatter one side. Seven repeats after two discarded warmup iterations, median as the headline with interquartile range and ninety-fifth percentile, thread counts set explicitly and recorded, and a straight line fitted to the logarithm of the measured median against the logarithm of the token count for each operator.

Settling it means two things at once: the fitted exponent for attention lands near two and the one for convolution near one across the swept range, and the crossover token count, below which attention is the cheaper operator and above which it is not, falls inside the range of resolutions production systems actually use. The result that breaks the claim is an attention exponent near one over the whole sweep, which would say the score matrix is not where the time goes at these sizes and that the comparison is dominated by memory traffic instead; that outcome goes in the first sentence of the analysis if it happens. Quick mode sweeps the small end of the token grid with three repeats and finishes inside ten seconds, and the full run extends the sweep to the largest grid that fits in memory on the named machine.
