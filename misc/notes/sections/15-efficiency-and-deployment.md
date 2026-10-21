# 15. Efficiency and deployment: quantisation, distillation, compilers, edge, NPU

Owner: edge inference engineer, suspicious of any speedup measured without preprocessing, at a different batch size, or on hardware nobody deploys.

## Section

## 15. Efficiency and deployment: quantisation, distillation, compilers, edge, NPU

The speedups quoted by these sources are not comparable with each other, because each was measured on different hardware, at a different batch size, with a different timer boundary.

### Quantisation

- [Building a quantization paradigm from first principles](https://github.com/google/gemmlowp/blob/master/doc/quantization.md) - Where the integer matrix multiply and its accumulator rounding are derived rather than asserted.
- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](https://arxiv.org/abs/1712.05877) - Where simulated quantisation during training and the fused integer inference pipeline were specified together.
- [TensorFlow Lite 8-bit quantization specification](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/performance/quantization_spec.md) - The normative scheme a runtime has to match, down to per-axis ranges and the zero point rules.
- [Up or Down? Adaptive Rounding for Post-Training Quantization](https://arxiv.org/abs/2004.10568) - Why rounding weights to the nearest level is the wrong default once calibration data is available.
- [A White Paper on Neural Network Quantization](https://arxiv.org/abs/2106.08295) - Where the post-training pipeline and the fine-tuning fallback are set out as one decision procedure.

### Distillation, pruning and sparsity

- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) - Where training a small model on a large model's soft outputs was first specified as a method.
- [Knowledge distillation: A good teacher is patient and consistent](https://arxiv.org/abs/2106.05237) - Why a distillation result that fails to reproduce is a schedule and augmentation problem.
- [What is the State of Neural Network Pruning?](https://arxiv.org/abs/2003.03033) - Why two pruning results with the same headline cannot be compared without a shared baseline.
- [Accelerating Sparse Deep Neural Networks](https://arxiv.org/abs/2104.08378) - The sparsity pattern a tensor core can actually execute, and the retraining recipe that reaches it.

### Compilers and runtimes

- [Open Neural Network Exchange Intermediate Representation](https://github.com/onnx/onnx/blob/main/docs/IR.md) - The normative account of what a graph means before any runtime decides how to run it.
- [Operator Schemas](https://github.com/onnx/onnx/blob/main/docs/Operators.md) - The operator semantics and version history that decide whether a model converts at all.
- [Quantize ONNX Models](https://github.com/microsoft/onnxruntime/blob/gh-pages/docs/performance/model-optimizations/quantization.md) - How a shipping runtime performs the post-training pass, including where it makes inference slower.
- [TVM](https://arxiv.org/abs/1802.04799) - Why a graph compiler searches schedules instead of calling a vendor library for every shape.
- [ExecuTorch](https://github.com/pytorch/executorch) - Where ahead-of-time export and backend delegation become the deployment unit instead of a Python process.

### Edge, accelerators and measurement

- [XNNPACK](https://github.com/google/XNNPACK) - The operator and architecture coverage that decides which layers fall back to a slower path.
- [MLComputeUnits](https://developer.apple.com/documentation/coreml/mlcomputeunits) - Why a latency figure means nothing until the processing units the model was allowed to use are named.
- [MLPerf Inference Benchmark](https://arxiv.org/abs/1911.02549) - Where inference scenarios, tail latency targets and the reporting rules are defined rather than implied.
- [LoadGen](https://github.com/mlcommons/inference/blob/master/loadgen/README.md) - Where the timer boundary around a query is fixed by code instead of by a sentence in a paper.

## Rejected

- [Knowledge Distillation Tutorial](https://github.com/pytorch/tutorials/blob/main/beginner_source/knowledge_distillation_tutorial.py) - Rule failed: conventions.md section 6, course notes that restate a paper. It is the file that confirmed the distillation paper's identifier for this draft, and it is good teaching, but a disagreement about the method gets resolved against the paper that is already admitted.
- [Awesome-Model-Quantization](https://github.com/Efficient-ML/Awesome-Model-Quantization) - Rule failed: conventions.md section 6, listicles and other lists. Linking a bibliography moves the admission problem instead of solving it, so the two quantisation entries it corroborated were admitted directly and the list itself was not.
- [LiteRT](https://github.com/google-ai-edge/LiteRT) - Rule failed: conventions.md section 6, marketing pages. The runtime ships and matters, but its front page leads with superlatives and build badges, and the part an engineer needs to read is the eight bit specification that is already admitted above.
- [OpenVINO](https://github.com/openvinotoolkit/openvino) - Rule failed: conventions.md section 6, a page with no protocol and no reproducible number is an advertisement. Its front page opens with a claim about boosting performance and routes the performance question to a benchmarks page on the vendor's commercial site, so no protocol is stated where the claim is made.
- [TensorRT](https://github.com/NVIDIA/TensorRT) - Rule failed: conventions.md section 5, admissible documentation is the maintainer's own documentation. This repository is an announcement and build page for the open source components, and the developer guide it points at sits on a host this container cannot reach, so no page could be verified.
- [FP8 Quantization: The Power of the Exponent](https://arxiv.org/abs/2208.09225) - Rule failed: conventions.md section 9, a seventh entry has to displace one of the six. It would have displaced the quantisation white paper, and it loses because the integer path is what the edge accelerators in this section execute today.
- [Ansor: Generating High-Performance Tensor Programs for Deep Learning](https://arxiv.org/abs/2006.06762) - Rule failed: conventions.md section 9, size limit and displacement. It would have displaced the compiler paper already in the subsection, which loses nothing to it on the mechanism a reader needs first, namely why a schedule is searched at all.
- [Compute Library](https://github.com/ARM-software/ComputeLibrary) - Rule failed: conventions.md section 9, size limit and displacement. It would have displaced the kernel library entry, which keeps its place because its own documentation names the runtimes that delegate to it and the quantisation schema its figures were produced under.

## Claims

### Post-training quantisation gives a model four times smaller and a two to three times speedup, from the TensorFlow Lite post-training quantization guide

- Fields present: precision, which is eight bit integer weights with either dynamic range or full integer activations.
- Fields missing: hardware and how many of them, since the table names device classes rather than parts and gives no count; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: cut
- Note: Preprocessing and postprocessing are not mentioned at all, so nothing states whether either is inside the timer, and no model, thread count or delegate is named either. This is the famous number of this area and the protocol is unstated and unrecoverable, so the figure is never repeated and the guide page was not admitted as an entry.

### Integer inference is faster than floating point inference on edge boards, from the latency tables in the XNNPACK documentation

- Fields present: hardware and how many of them, given as named boards and their system on chip, one board per column; precision, given as single precision floating point against eight bit integer with a per-channel schema; framework and version with compile flags, given as the build script, the operating system image and the benchmark command, although no library commit is named.
- Fields missing: batch size; input resolution; warmup and the statistic reported, since a minimum run time flag is set but no statistic is named; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: Preprocessing is outside the timer by construction, because the inputs are randomised tensors already resident in memory, and postprocessing is outside it too, since the harness times the model only. The entry rests on the operator and architecture coverage rather than on these figures, so the entry stands and the figures are never repeated.

### Quantisation can make inference slower, and old hardware does not benefit from it, from the ONNX Runtime quantization documentation

- Fields present: hardware and how many of them, given by instruction set rather than by part, naming vector neural network instructions on one architecture, integer tensor core support on another, and dot product instructions on a third; precision, given as the unsigned and signed eight bit combinations the runtime supports.
- Fields missing: batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: stands
- Note: No timer exists here because no figure is reported, so preprocessing and postprocessing are inside no timer at all, and the claim is qualitative by construction. It stands because it is the maintainer stating a direction of effect and its mechanism, namely the conversion overhead and the missing integer instructions, and it is the claim the benchmark proposal below tests.

### The unsigned by signed eight bit path can saturate its sixteen bit intermediate on one architecture and cost accuracy, from the ONNX Runtime quantization documentation

- Fields present: hardware, given as the architecture and the vector extensions whose multiply and add instruction saturates; baseline compared against, given as the unsigned by unsigned combination that does not saturate.
- Fields missing: model and exact checkpoint; dataset with split and version; input resolution and preprocessing; metric with its full definition; evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings; training data used.
- Verdict: recorded unverified
- Note: No latency figure accompanies it, so preprocessing and postprocessing sit inside no timer, and the seven speed fields do not apply. The mechanism is documented and actionable and the magnitude is not stated anywhere, so the mechanism is admitted and no accuracy delta is ever quoted from it.

### Two conforming implementations of the eight bit scheme are not bit-exact, from the TensorFlow Lite 8-bit quantization specification

- Fields present: metric with its full definition, in the sense that the specification defines the affine mapping, the per-axis and per-tensor ranges and the zero point constraints that conformance is judged against; baseline compared against, given as the reference kernels.
- Fields missing: model and exact checkpoint; dataset with split and version; input resolution and preprocessing; evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings; training data used; hardware.
- Verdict: stands
- Note: No timer is involved, so preprocessing and postprocessing are inside no timer here either. It stands because the specification is stating the limits of its own guarantee rather than a result, and it is load bearing downstream, since an accuracy gap attributed to quantisation may be an implementation difference between two conforming runtimes.

### MLPerf Inference latencies are comparable across submissions, from the LoadGen documentation

- Fields present: whether preprocessing and postprocessing are inside the timer, which is stated explicitly; warmup and the statistic reported, given as the scenario's target percentile and latency bound.
- Fields missing: hardware and how many of them; precision; batch size, since the scenario constrains how queries arrive but not how the system groups them; input resolution; framework and version with compile flags.
- Verdict: stands
- Note: Preprocessing is outside the timer where the query sample library holds it, which the documentation calls untimed preprocessing, while any preprocessing left inside the system under test is timed, decompression included, and postprocessing is inside the timer because a response is post processed before it is handed back as complete. That asymmetry is the reason a published MLPerf latency cannot be compared with an end-to-end camera-to-result figure.

### Adaptive rounding often improves the accuracy of the quantised model, from the adaptive rounding page of the quantisation toolkit that implements it

- Fields present: baseline compared against, given as nearest rounding.
- Fields missing: model and exact checkpoint; dataset with split and version; input resolution and preprocessing; metric with its full definition; evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings; training data used; hardware.
- Verdict: recorded unverified
- Note: No timer and no figure, so preprocessing and postprocessing are inside no timer and the seven speed fields do not apply. The word often is softening of exactly the kind conventions.md section 7 forbids, so the technique is admitted on its mechanism and the toolkit's accuracy statement is recorded and never repeated.

### Channel permutation recovers the accuracy of structured sparse networks without affecting inference run time, from the structured sparsity documentation shipped with the pruning tool

- Fields present: precision, in the sense that the sparsity pattern is two of every four weights and the arithmetic is unchanged; baseline compared against, given as the unpermuted structured sparse network.
- Fields missing: hardware and how many of them; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: Nothing states where the timer starts, so neither preprocessing nor postprocessing can be placed inside or outside it, and no latency figure is given to support the phrase about run time. The claim about accuracy recovery also names no dataset, split or metric, so the entry rests on the sparsity pattern and the retraining recipe instead.

### Structured sparsity doubles the arithmetic throughput of a matrix multiply unit, as the field repeats the claim from Accelerating Sparse Deep Neural Networks

- Fields present: precision and hardware class, in that the claim is made about an accelerator generation whose matrix units take a two of four pattern.
- Fields missing: hardware and how many of them; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: The paper could not be retrieved from this container, so no field was read at the source and the timer boundary is unknown, which means preprocessing and postprocessing cannot be placed. The entry rests on the sparsity pattern being a hardware constraint rather than on the throughput ratio, so the entry stands and the ratio is never repeated.

## Link notes

- https://arxiv.org/abs/1712.05877 - Host refused by this container's egress policy on the first and only attempt, which is policy rather than a dead page. The title, the identifier and this canonical URL were confirmed together in a framework maintainer's quantisation concept guide fetched through raw.githubusercontent.com, where the triple appears twice. The title runs well past the ceiling in voice.md section 4 and is kept whole, because a right trim would remove the integer arithmetic phrase a reader would actually search for.
- https://arxiv.org/abs/2004.10568 - Same blocked host. The identifier was confirmed from the adaptive rounding page in the toolkit published by the authors' own organisation, which links the PDF form under the same identifier rather than the abstract page. Conventions.md section 5 requires the abstract page, so the abstract form is cited; the PDF form is not named here as a URL because check_links.py classifies that path as a mirror and fails the build on it, which is the rule enforcing itself. The full title was corroborated separately.
- https://arxiv.org/abs/2106.08295 - Same blocked host. The title and identifier pair was corroborated only by a third-party bibliography, recorded plainly because every other arXiv entry in this section was confirmed against a maintainer's or an author's own file. No stronger witness was reachable from here.
- https://arxiv.org/abs/1503.02531 - Same blocked host. Title, identifier and URL confirmed together in the knowledge distillation tutorial source maintained by the framework.
- https://arxiv.org/abs/2106.05237 - Same blocked host. Title, identifier and URL confirmed together in the authors' own research codebase README. The title sits a few characters over the ceiling in voice.md section 4 and keeps its second half, because the first half alone names the whole technique rather than this treatment of it.
- https://arxiv.org/abs/2003.03033 - Same blocked host. Title, identifier and URL confirmed together in the authors' own pruning benchmark repository README.
- https://arxiv.org/abs/2104.08378 - Same blocked host. Title, identifier and URL confirmed together in the vendor's own structured sparsity README, including the bibliography entry.
- https://arxiv.org/abs/1802.04799 - Same blocked host. Title, identifier and URL confirmed together on the compiler project's own publications page in its documentation source.
- https://arxiv.org/abs/1911.02549 - Same blocked host. Title, identifier and URL confirmed together in the benchmark suite's own README, including the bibliography entry.
- https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/performance/quantization_spec.md - The rendered page moved twice, from the framework documentation site to the vendor's edge documentation site under the runtime's rename, and both destination hosts are refused here. The specification's source file was confirmed by path through raw.githubusercontent.com and is cited instead, because it is the file the rendered pages are built from.
- https://github.com/microsoft/onnxruntime/blob/gh-pages/docs/performance/model-optimizations/quantization.md - The documentation host is refused here, so the rendered URL could not be confirmed and the documentation source in the publishing branch is cited. The page's own front matter records two historical paths it redirects from, one under a how-to prefix and one directly under the performance prefix, so any older link to this page is a redirect.
- https://developer.apple.com/documentation/coreml/mlcomputeunits - Reachable and confirmed directly, returning a success status with the page title and summary intact. The older machine learning landing path for this framework returns a permanent redirect to the documentation root, so the destination is what gets cited anywhere this framework is referenced.
- https://github.com/google/gemmlowp/blob/master/doc/quantization.md - Confirmed by path through raw.githubusercontent.com. The library itself has been superseded by newer kernel libraries, and it is admitted only because the derivation in this file is the canonical one, which conventions.md section 10 permits where the lesson is the content rather than the tool.
- https://github.com/onnx/onnx/blob/main/docs/IR.md - Confirmed by path. The page heading runs past the title ceiling in voice.md section 4, so it is trimmed from the right and nothing is paraphrased.
- https://arxiv.org/abs/1807.11164 - Considered and left out rather than rejected, because it is the obvious entry for the efficient convolutional designs subsection of section 6, which is earlier and keeps it. The guidance it carries about direct latency against operation counts is the reason the kernel library entry sits where it does instead.
- https://arxiv.org/abs/1503.02531 - Collision risk with the distillation subsection of section 7, which is earlier and would keep both distillation entries if its owner claims them. If that happens this subsection drops to the floor of three entries rather than taking a replacement that fails the admission rules.
- https://arxiv.org/abs/1911.02549 - Possible collision with the protocols and reporting subsection of section 5. This section keeps it only if that owner did not, because the reason here is about the timer boundary rather than about accuracy reporting.
- Verification channels - This container's egress policy refuses almost every host, and the search budget was exhausted before a single query ran, so nothing was confirmed by search. Every URL above was confirmed either by fetching the identical owner, repository, branch and path through raw.githubusercontent.com, which is the sanctioned repository channel, or by fetching the page directly where the host is reachable. No URL was included on the strength of memory alone, and no blocked host was retried. Running check_links.py on this draft returns no dead links and no mirrors, with the arXiv entries unreachable through the tunnel, the repository documentation entries refused as automated clients, and the one reachable vendor page returning a success status.

## Benchmark proposal

Integer quantisation changes both accuracy and latency, and the sign of each depends on the
layer and the shape, so a single speedup figure for a model is not a fact about a layer. The
measurement generates, from one fixed seed, weight and activation matrices at several shapes a
convolution lowers to, a wide shallow shape from a pointwise layer, a tall thin shape from a
depthwise layer, and a square shape from a dense head, then for each shape computes the single
precision product through the library path and the eight bit product accumulated in a wider
integer and requantised, under both per-tensor and per-channel scales. Accuracy is the signal to
quantisation noise ratio of the integer result against the single precision result, which must
be bit-identical across runs. Latency is timed twice per shape, once with quantisation and
requantisation inside the timer and once with only the integer product inside, which is the gap
a vendor table hides, with warmup discarded and the median, interquartile range and ninety-fifth
percentile reported over at least seven repeats. The claim is settled if at least one shape is
slower in the integer path while at least one is faster, and the ordering of shapes by noise
ratio differs from the ordering by latency; it is refuted if both signs are the same for every
shape and both granularities. The machine is a shared cloud virtual machine with no GPU and no
neural accelerator, so this cannot measure what an integer kernel on a vector unit with dot
product instructions, a neural engine or a sparse matrix unit would deliver, and it cannot
measure kernel selection inside a runtime; it measures the mechanism, which is that quantisation
adds conversion work, changes which kernel is reachable, and does so by an amount that depends
on the shape.
