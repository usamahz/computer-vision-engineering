# 13. Generative vision: diffusion, editing, control

Owner: generative modelling specialist, suspicious of a distributional image metric standing in for anything a user cares about.

## Section

## 13. Generative vision: diffusion, editing, control

The distributional scores in this section are not comparable across implementations, so a small gap between two published numbers is not a result.

### Diffusion foundations

- [Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) - Where the forward corruption and the learned reverse process were first written down as one construction.
- [Generative Modeling by Estimating Gradients of the Data Distribution](https://arxiv.org/abs/1907.05600) - Why sampling can be driven by the gradient of a log density that is never normalised.
- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) - Where the noise prediction objective that almost every later system trains against is fixed.
- [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456) - Why the discrete noise schedule and the score view are the same continuous process.
- [Flow Matching Guide and Code](https://arxiv.org/abs/2412.06264) - What changes in training and sampling when the path from noise to data is a straight line.

### Samplers and guidance

- [Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) - Why the step count is a sampler choice rather than a property of the trained network.
- [Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) - Where steering samples with a separate classifier was first paid for in diversity.
- [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) - Why the guidance scale in every text conditioned interface exists and what it trades away.
- [Elucidating the Design Space of Diffusion-Based Generative Models](https://arxiv.org/abs/2206.00364) - Which parts of a sampler can be swapped without retraining the network.

### Latent and text conditioned systems

- [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) - Why moving the process into an autoencoder latent is what made text conditioned synthesis affordable.
- [Stable Diffusion v1 Model Card](https://github.com/CompVis/stable-diffusion/blob/main/Stable_Diffusion_v1_Model_Card.md) - What the first widely loaded checkpoint was trained on and what its own authors say it fails at.
- [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748) - Whether the convolutional backbone was ever the part doing the work.
- [Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) - Where the straight path objective meets separate weights for text and image tokens.
- [FLUX](https://github.com/black-forest-labs/flux) - Where the open weight variants state the licence that decides whether a product can ship.

### Control, editing and evaluation

- [SDEdit](https://arxiv.org/abs/2108.01073) - How far an image can be changed by adding noise and letting the reverse process finish.
- [Prompt-to-Prompt Image Editing with Cross Attention Control](https://arxiv.org/abs/2208.01626) - Why the cross attention maps are the handle for changing one object and keeping the rest.
- [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) - How a spatial condition attaches to a frozen checkpoint without retraining it.
- [GANs Trained by a Two Time-Scale Update Rule](https://arxiv.org/abs/1706.08500) - Where the distributional score that generative results are quoted in was defined.
- [On Aliased Resizing and Surprising Subtleties in GAN Evaluation](https://arxiv.org/abs/2104.11222) - Why a resize nobody can see moves the score further than a change of method does.
- [Rethinking FID](https://arxiv.org/abs/2401.09603) - What the feature network and the sample count contribute to the number before the images do.

## Rejected

- [Imagen](https://arxiv.org/abs/2205.11487) - Rule failed: conventions section 6, papers without code where the entry's claim depends on the missing half. No weights, no implementation and no reference statistics, so the text conditioning result cannot be rerun outside the group that produced it.
- [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242) - Rule failed: conventions section 6, papers without code where the claim depends on the missing half. The official repository publishes the evaluation dataset and no implementation of the method, and the subject fidelity claim is the whole of the entry.
- [SDXL](https://arxiv.org/abs/2307.01952) - Rule failed: conventions section 9, three to six entries per subsection. Would have displaced FLUX in Latent and text conditioned systems, and FLUX is kept because its repository states the licence terms a shipping decision turns on.
- [DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps](https://arxiv.org/abs/2206.00927) - Rule failed: conventions section 9, three to six entries per subsection. Would have displaced the design space entry, which treats the solver, the schedule and the preconditioning as one set of choices rather than one of them.
- [InstructPix2Pix: Learning to Follow Image Editing Instructions](https://arxiv.org/abs/2211.09800) - Rule failed: conventions section 9, three to six entries per subsection. Would have displaced Prompt-to-Prompt, which supplies the attention mechanism its training pairs were generated with and is therefore the earlier read.
- [FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space](https://arxiv.org/abs/2506.15742) - Rule failed: conventions section 9, three to six entries per subsection. Would have displaced the conditional control entry, which gives a mechanism attachable to a checkpoint a reader already has rather than a system to adopt whole.
- [Improved Precision and Recall Metric for Assessing Generative Models](https://arxiv.org/abs/1904.06991) - Rule failed: conventions section 9, three to six entries per subsection. Would have displaced the rethinking entry, which puts the feature network and the sample count in one place instead of splitting the metric critique across two reads.
- [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) - Rule failed: conventions section 6, a repository with no written account of what it does is a dependency rather than a reading. Its sampler and scheduler behaviour cannot be argued against any specification, which is exactly what a reader needs when two interfaces disagree.
- [Diffusers](https://github.com/huggingface/diffusers) - Rule failed: conventions section 9, three to six entries per subsection. Admissible as framework documentation, but it would have displaced the Stable Diffusion v1 model card, which states training data and stated limits that the library's pipeline pages do not.

## Claims

### Denoising diffusion probabilistic models report a Fréchet Inception Distance of 3.17 and an Inception Score of 9.46 on unconditional CIFAR-10

- Fields present: model and exact checkpoint; dataset with split; metric named with the sample count it was computed over; training data used; baseline compared against.
- Fields missing: metric with its full definition, because the feature extractor port and the resize path inside the metric implementation are not stated in a form another implementation can match; input resolution and preprocessing of the reference statistics, including whether they come from the train or the test split; hardware.
- Verdict: recorded unverified
- Note: the entry rests on the training objective, not on the score, so the number is not repeated in the section. The same two figures are quoted downstream as a comparison target, which is the error this section's last subsection exists to block.

### Denoising diffusion implicit models claim that a small fraction of the training step count gives comparable sample quality with no retraining

- Fields present: model and exact checkpoint, which is the network trained for the denoising diffusion baseline and reused unchanged; dataset with split; metric named; evaluation protocol as a sweep over step counts; baseline compared against, which is the ancestral sampler at the full step count.
- Fields missing: metric with its full definition, with the same implementation gap as the claim above; hardware.
- Verdict: recorded unverified
- Note: no wall clock is reported, so nothing is inside a timer and the question of preprocessing and postprocessing does not arise. Step count is not latency, because a guided sampler pays for more than one network evaluation per step, and the structural half of the claim survives without any number.

### The aliased resizing audit claims the score changes when the only difference is the resize implementation or a high quality compression pass

- Fields present: metric with its full definition including the feature extractor and the exact port of its weights; the preprocessing path under test, which is the variable; reference statistics published for named datasets and splits; code and precomputed statistics published by the authors.
- Fields missing: none that the claim rests on.
- Verdict: stands
- Note: the claim admitted here is a sensitivity, not a level, so no table value is repeated. This is the claim the section's benchmark proposal measures locally, because a sensitivity is the one property of this metric a laptop can check without downloading network weights.

### The same audit states that its implementation agrees with another widely used one to about two parts in a million once the matching option is set

- Fields present: both implementations named by repository; the option that makes them agree; metric with its full definition; reference statistics.
- Fields missing: dataset with split and version for that particular comparison; the sample count it was computed over.
- Verdict: recorded unverified
- Note: the tolerance is quoted on the authors' own page without the dataset it was measured on, so it is recorded and not repeated. It matters only as a contrast, since the gap between implementations is orders larger when the resize path is left unmatched.

### The rethinking entry claims the standard distributional score is biased at practical sample counts and that its feature network mis-ranks text conditioned systems

- Fields present: metric with its full definition, including the named encoder checkpoint and the kernel; code published by the authors; sample count treated as a variable rather than a constant.
- Fields missing: evaluation protocol for the human preference comparison the ranking argument leans on, specifically the prompt set, the rater pool, the instructions given and the number of comparisons per pair.
- Verdict: recorded unverified
- Note: the entry earns its place for naming the feature network and the sample count as parts of the metric rather than parts of the images. The preference correlation half is the part a reader should not quote, and it is the half with no protocol.

### Scaling rectified flow transformers claims improved human preference ratings over established formulations

- Fields present: model family with its sizes; training objective and the noise sampling change under test; the direction of the claim; baseline compared against, named as a formulation rather than a checkpoint.
- Fields missing: evaluation protocol, specifically the prompt set, the rater pool, the instructions, the number of comparisons and any significance treatment; model and exact checkpoint for the systems compared against; input resolution and preprocessing for the compared samples.
- Verdict: recorded unverified
- Note: the entry rests on the rectified flow objective and the separate text and image streams, both of which are specified, so the preference claim is recorded and never repeated. A preference number with no rater pool and no prompt set is not weaker evidence than a distributional score, it is a different kind of nothing.

### The open weight FLUX variants are preferred by human raters over other open weight systems

- Fields present: none that can be checked. The repository documents the variants, their intended use and their licences, and states no evaluation.
- Fields missing: metric with its full definition; evaluation protocol including prompt set and rater pool; dataset with split; model and exact checkpoint for everything compared against; sample count; hardware.
- Verdict: cut
- Note: the claim circulates from a vendor announcement, which is a marketing page by rule and could not be reached from this container in any case. The entry cites the repository for weights, licences and reference sampling code, which is all the repository claims.

## Link notes

- Verification channel for every URL in this draft: the turn's WebSearch budget was spent before this section was drafted, and arxiv.org, openreview.net, huggingface.co and the vendor hosts all refuse CONNECT from this container, so each identifier was confirmed by fetching a file over raw.githubusercontent.com in which the title and the identifier appear together. Mapping: 1503.03585 from Sohl-Dickstein/Diffusion-Probabilistic-Models; 1907.05600 and 2011.13456 from ermongroup/ncsn; 2006.11239 from hojonathanho/diffusion; 2010.02502 from ermongroup/ddim; 2105.05233 from openai/guided-diffusion; 2206.00364 from NVlabs/edm; 2112.10752 from CompVis/latent-diffusion; 2212.09748 from facebookresearch/DiT; 2403.03206 from the diffusers documentation tree; 2412.06264 from facebookresearch/flow_matching; 2108.01073 from ermongroup/SDEdit; 2208.01626 from google/prompt-to-prompt; 2302.05543 from lllyasviel/ControlNet; 1706.08500 from bioinf-jku/TTUR; 2104.11222 from GaParmar/clean-fid; 2401.09603 from google-research/google-research; 2205.11487 from LuChengTHU/dpm-solver; 2208.12242 from google/dreambooth; 2211.09800 from timothybrooks/instruct-pix2pix; 2307.01952 from Stability-AI/generative-models; 2206.00927 from LuChengTHU/dpm-solver; 1904.06991 from kynkaat/improved-precision-and-recall-metric; 2506.15742 from black-forest-labs/flux.
- https://arxiv.org/abs/2207.12598 - identifier confirmed from the Stable Diffusion repository and card, which link it as the guidance method the checkpoints were trained for; the title was confirmed separately from a third-party implementation's citation block, since no file from the authors states it. The arXiv abstract page is cited, not that implementation.
- https://arxiv.org/abs/2011.13456 - the authors' own repository points at openreview.net/forum?id=PxTIG12RRHS as the canonical link. The arXiv abstract page is cited instead because it carries the version history and is the identifier the work is cited by, and because the OpenReview host could not be reached to confirm the forum identifier resolves.
- https://arxiv.org/abs/2104.11222 - the authors' repository links their own project page on a university host as the paper link. Not cited, because that host could not be reached from this container and the arXiv abstract page carries the version history.
- https://arxiv.org/abs/2412.06264 - cited in place of the original flow matching paper, whose identifier could not be confirmed from any file reachable here. The rule is to leave an unconfirmed URL out, so it is out; this deposit is the same authors' guide published alongside the reference library, and it covers the straight path construction the rectified flow entries depend on.
- Left out for the same reason: the work on what the feature network's class structure contributes to the distributional score. The clean resizing repository cites it by identifier and by author but no file reachable here states its title, so it is not in the draft. The rethinking entry covers the feature network and the sample count.
- https://github.com/CompVis/stable-diffusion/blob/main/Stable_Diffusion_v1_Model_Card.md - the card is cited as the file in the authors' own repository rather than the weight page on the model host, because that host refuses CONNECT here. The file was fetched and its heading is the title used.
- https://github.com/black-forest-labs/flux and https://github.com/huggingface/diffusers and https://github.com/AUTOMATIC1111/stable-diffusion-webui - each confirmed by fetching a file from the repository rather than by the GitHub API, which is gated to repositories attached to this session and answers 403 otherwise.
- The paper landing pages on the model host appear inside the documentation used for confirmation. None is cited anywhere in this draft; they are aggregator pages by rule.
- Collision check: every identifier in this draft was grepped against the other fifteen section drafts as delivered, and none of them appears in another section. The nearest risk was the distributional score's origin paper and the aliased resizing audit against section 5's How a metric misleads, but that subsection is confined to detection metrics, so both stay here. If section 5 later admits either, this section drops it and keeps the rethinking entry, which is the one tied to text conditioned systems.
- Ordering note for Control, editing and evaluation, which is the one subsection whose order is not self-evident: the three editing entries run in order of how much machinery each needs, from noising an existing image, to reaching into the attention maps, to training a side branch. The three evaluation entries are independent of them and run definition, then resize sensitivity, then feature network and sample count. Where the two halves are genuinely independent the shorter read goes first.
- misc/scripts/check_links.py was run against this draft. Every URL classified UNREACHABLE or BLOCKED because the container's egress policy refuses CONNECT to all of these hosts; nothing classified DEAD or MIRROR. The classification is a property of this container, not of the pages, and the confirmation route is the mapping in the first note.
- Paper full texts could not be opened from here, so the Claims block names fields from the authors' own repositories, model cards and documentation. Verdicts are the conservative reading wherever a field could not be checked, and no examined number is repeated in the section.

## Benchmark proposal

The claim worth measuring is that a distributional image metric moves under changes a viewer
cannot see, so a small difference in it is not evidence of anything. The measurement generates
two synthetic image sets from a fixed seed with numpy, builds a cheap fixed feature map for
every image rather than a learned network, which is a small bank of separable derivative and
oriented band filters pooled over a coarse grid into a few dozen dimensions, fits a Gaussian to
each set and computes the Fréchet distance between them with a numpy eigendecomposition. It then
recomputes the candidate set's score after changes no viewer can see, each applied through
Pillow and each reported alongside the mean and maximum absolute pixel difference it caused: a
round trip through a different resampling filter at the same output size, a re-encode at near
lossless compression quality, and a change in the number of samples drawn from the same
generator. The claim is settled against the field's folklore if the shift caused by a resampling
filter swap or a near lossless re-encode is at least as large as the shift caused by a visible
change held as a control, such as a slight blur or a contrast change, and larger than the
metric's own spread across seeds at a fixed sample count, while the pixel difference it caused
stays below a stated threshold. The benchmark measures the metric's sensitivity to its own
pipeline and not the published metric itself: no network weights may be downloaded here, the
feature map is fixed and arbitrary, and no absolute value it prints is comparable to any
published score. Quick mode runs a few hundred small images and finishes well inside ten
seconds.
