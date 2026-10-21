# 14. Vision-language models

Owner: vision-language specialist, suspicious of benchmark contamination and of any evaluation whose test set sat on the open web before the model was trained.

## Section

## 14. Vision-language models

Scores in this section are not comparable between papers, because the prompt template and the answer extraction rule differ and are almost never reported.

### Contrastive image-text pretraining

- [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) - Where classification by text prompt was defined, and what it needs from the caption corpus.
- [LAION-5B](https://arxiv.org/abs/2210.08402) - What an openly released image-text corpus is made of, down to the filtering that built it.
- [DataComp](https://arxiv.org/abs/2304.14108) - What changes when the training recipe is frozen and only the data is allowed to move.
- [Sigmoid Loss for Language Image Pre-Training](https://arxiv.org/abs/2303.15343) - Why the contrastive loss stops forcing the batch size to carry the whole negative set.

### Generative vision-language models

- [Flamingo](https://arxiv.org/abs/2204.14198) - How a frozen language model was made to read images without retraining either half.
- [BLIP-2](https://arxiv.org/abs/2301.12597) - What a learned query bottleneck buys when both the image encoder and the language model stay frozen.
- [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485) - Where the instruction data for a conversational image model was synthesised rather than collected.
- [Improved Baselines with Visual Instruction Tuning](https://arxiv.org/abs/2310.03744) - Which gains came from the connector and which came from the training recipe.
- [Prismatic VLMs](https://arxiv.org/abs/2402.07865) - Where the connector, the encoder and the data were varied one at a time instead of all at once.

### Open weights and model cards

- [Model Card: CLIP](https://github.com/openai/CLIP/blob/main/model-card.md) - What the people who trained an image-text model say it was not built to do.
- [OpenCLIP](https://github.com/mlfoundations/open_clip) - Checkpoints whose training corpus is named, which is what makes an overlap audit possible at all.
- [Molmo and PixMo](https://arxiv.org/abs/2409.17146) - Weights and the data behind them released together, so a leakage check needs nobody's cooperation.
- [Llama 3.2-Vision](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD_VISION.md) - A card that states a knowledge cutoff, which is the field an evaluation date has to be checked against.

### Benchmarks and contamination

- [MMBench](https://arxiv.org/abs/2307.06281) - Why permuting the answer options moves the score of a model that supposedly knows the answer.
- [MMMU](https://arxiv.org/abs/2311.16502) - The multimodal exam most reports quote, and the answer extraction rule the quoting drops.
- [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) - Where the prompt template and the answer extraction that a reported score depends on actually live.
- [Are We on the Right Way for Evaluating Large Vision-Language Models?](https://arxiv.org/abs/2403.20330) - How much of a multimodal score survives when the image is removed from the input.
- [Benchmarking Benchmark Leakage in Large Language Models](https://arxiv.org/abs/2404.18824) - A way to measure whether a test set was in the training corpus without holding the corpus.

## Rejected

- [Improved Baselines with Visual Instruction Tuning](https://huggingface.co/papers/2310.03744) - Rule failed: aggregators and paper mirrors. The page wraps a paper the authors deposit on arXiv themselves, adds nothing to it, and rots on its own schedule.
- [MMMU Leaderboard](https://mmmu-benchmark.github.io/#leaderboard) - Rule failed: leaderboards and benchmark trackers. A ranking is a snapshot of a protocol being gamed, and the protocol definition is already admitted in its place.
- [MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI](https://arxiv.org/pdf/2311.16502.pdf) - Rule failed: the arXiv carve-out admits the abstract page, not the PDF. The benchmark's own repository links the PDF, so the abstract page was substituted because it carries the version history.
- [Tackling multiple tasks with a single visual language model](https://www.deepmind.com/blog/tackling-multiple-tasks-with-a-single-visual-language-model) - Rule failed: marketing pages for closed models. No model card, no weights and no evaluation protocol, so nothing in it can be checked against the paper it announces.
- [CLIP: Connecting text and images](https://openai.com/blog/clip/) - Rule failed: blogspam and content farms. A vendor post paraphrasing a paper drops the ablation table, which is the only part that settles an argument about where the result came from.
- [Multimodal Foundation Models: From Specialists to General-Purpose Assistants](https://arxiv.org/abs/2309.10020) - Rule failed: listicles and other lists. A survey moves the admission problem somewhere else instead of solving it, and the entries worth reading are admitted directly.
- [CVPR 2023 Tutorial on Large Multimodal Models](https://youtu.be/mkI7EPD1vp8) - Rule failed: video lectures and talks. Not searchable, not quotable and not diffable, and nothing in it is absent from the papers already admitted.
- [Qwen2.5-VL Technical Report](https://arxiv.org/abs/2502.13923) - Rule failed: the three to six entry limit per subsection. It would have displaced the Llama vision card, and it lost because a technical report with an undisclosed training corpus is not a model card and cannot support a contamination check.
- [MMMU-Pro: A More Robust Multi-discipline Multimodal Understanding Benchmark](https://arxiv.org/abs/2409.02813) - Rule failed: the three to six entry limit per subsection. It would have displaced MMMU, and it lost because its vision-indispensability finding overlaps the MMStar entry while MMMU remains the dependency both are read against.
- [Reproducible scaling laws for contrastive language-image learning](https://arxiv.org/abs/2212.07143) - Rule failed: the three to six entry limit per subsection. It would have displaced DataComp, and it lost because DataComp holds the recipe fixed and moves only the data, which is the question this section needs answered.
- [InstructBLIP](https://arxiv.org/abs/2305.06500) - Rule failed: the three to six entry limit per subsection. It would have displaced the improved visual instruction tuning baselines, and it lost because the baselines paper is the recipe later open models actually reproduce.

## Claims

### Zero-shot ImageNet top-one accuracy for the original contrastive checkpoint, as tabulated in the OpenCLIP repository

- Fields present: model and exact checkpoint; input resolution; metric named as top-one accuracy; training data named as the closed web image-text set
- Fields missing: dataset with split and version; preprocessing; evaluation protocol, specifically the prompt template set and whether prompt ensembling was used; training data used, in the sense of a corpus anyone can inspect; hardware; baseline compared against
- Verdict: recorded unverified
- Note: for a zero-shot classifier the prompt template set is the protocol, so a number without it is not reproducible even in principle. Because the training corpus was never released, overlap between it and the evaluation split cannot be ruled out by anyone outside the lab that trained it.

### Sigmoid-loss checkpoint ImageNet top-one accuracy at the larger input resolution, as tabulated in the OpenCLIP repository

- Fields present: model and exact checkpoint; input resolution; metric named as top-one accuracy; training data named as a closed multilingual web corpus; samples seen
- Fields missing: dataset with split and version; preprocessing; evaluation protocol including the prompt template set; training data used, in the inspectable sense; hardware; baseline compared against
- Verdict: recorded unverified
- Note: the entry rests on the loss function rather than the score, so the number is recorded and never repeated. The training corpus is undisclosed, which is the normal case in this subsection and the reason the training data field is named missing rather than present.

### Zero-shot VQAv2 accuracy of the frozen-encoder generative model against the earlier few-shot model, as stated on the authors' project page

- Fields present: dataset named; metric family named as visual question answering accuracy; baseline compared against
- Fields missing: model and exact checkpoint, since the language model variant is not named in the claim; dataset with split and version, so test-dev against validation is unrecoverable; input resolution and preprocessing; metric with its full definition, including the multi-annotator agreement rule and answer normalisation; evaluation protocol, including prompt template and decoding settings; training data used, which is undisclosed for the baseline; hardware
- Verdict: recorded unverified
- Note: the comparison is between two systems whose evaluation prompts are both unstated, and visual question answering accuracy is sensitive to answer normalisation alone. The entry stands on the connector design, not on this pair of numbers.

### Captioning score of the frozen-encoder generative model against the previous best, as stated on the authors' project page

- Fields present: dataset named; metric family named; baseline compared against
- Fields missing: dataset with split and version; input resolution and preprocessing; metric with its full definition, including the tokeniser and the consensus variant; evaluation protocol, including decoding settings such as beam width and length penalty; training data used; hardware; model and exact checkpoint
- Verdict: recorded unverified
- Note: a consensus-based captioning metric changes materially with the tokeniser and the beam settings, neither of which is stated. The captioning corpora are also web-sourced, so overlap with the caption test images is possible and unmeasured.

### Training completed in about one day on a single eight-accelerator node, with leading scores across eleven benchmarks, as stated in the authors' repository

- Fields present: hardware and count
- Fields missing: precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; and on the accuracy side, dataset with split and version for each benchmark, metric definitions, evaluation protocol including prompt template and decoding, and the baseline per benchmark
- Verdict: recorded unverified
- Note: preprocessing and postprocessing are not inside any declared timer, because no timer boundary is declared at all. The figure is a single wall-clock training duration with no repeats and no dispersion, so it is a planning estimate rather than a measurement.

### Accuracy falling to between the high teens and the mid twenties per cent on the robustified multimodal exam, as stated on the benchmark's own repository

- Fields present: dataset with split and version; metric named as accuracy; evaluation protocol partly, in that the vision-only input setting and the optical character recognition prompt and chain-of-thought variants are named; baseline compared against, being the same models on the original exam
- Fields missing: model and exact checkpoint, since the range spans unnamed models; input resolution and preprocessing; metric with its full definition, in particular the answer extraction rule; decoding settings; training data used, which is undisclosed for every proprietary model inside the range; hardware
- Verdict: recorded unverified
- Note: the size of the drop is the finding, and it is consistent with shortcut answering rather than with a capability change. Because the training data field is missing for every model in the range, contamination of the original exam cannot be excluded as a contributor to the number the drop is measured from.

### Multi-modal gain and multi-modal leakage as defined by the vision-indispensability audit

- Fields present: metric with its full definition; dataset with split and version; evaluation protocol, in that each model is scored with visual input, without visual input, and as its base language model without visual input; baseline compared against, being the language-model-only score
- Fields missing: model and exact checkpoint for the published rows; input resolution and preprocessing; training data used, which is undisclosed for the audited models and is the condition the audit exists to work around; hardware
- Verdict: stands
- Note: the claim admitted here is a measurement procedure, not a score, and the procedure is fully specified down to the three result files a submission must provide. It is the only entry in this section whose central claim can be checked without any access to a training corpus.

### A pocket multimodal model reaching most of the performance at a small fraction of the parameters, as the claim appears in a title

- Fields present: the parameter ratio, and nothing else
- Fields missing: model and exact checkpoint; dataset with split and version; input resolution and preprocessing; metric with its full definition; evaluation protocol; training data used; hardware; baseline compared against
- Verdict: cut
- Note: a performance ratio asserted in a title, with no protocol attached anywhere the claim is repeated, is decoration. It is recorded here only because the changelog counts examined numbers.

## Link notes

- Egress policy for this container refuses a CONNECT to almost every publisher host. `arxiv.org`, `huggingface.co`, `github.com` and `visualqa.org` all failed, and the proxy status endpoint reports them as policy denials rather than dead pages. None of them is recorded as a dead link.
- The run's shared WebSearch budget was exhausted before the first query of this section, so no search-based confirmation was available. Every arXiv identifier below was instead confirmed by finding the title and the identifier together inside a citation block or paper link served from `raw.githubusercontent.com`, which is the authors' own deposit of the pairing.
- https://arxiv.org/abs/2103.00020 - confirmed from `openai/CLIP` README and the `mlfoundations/open_clip` citation block.
- https://arxiv.org/abs/2210.08402 and https://arxiv.org/abs/2304.14108 - confirmed from the `mlfoundations/open_clip` README and the `mlfoundations/datacomp` citation block.
- https://arxiv.org/abs/2303.15343 - confirmed from the `google-research/big_vision` paper list, which is the training lab's own repository.
- https://arxiv.org/abs/2204.14198 - confirmed from the `mlfoundations/open_flamingo` citation block. The team that trained Flamingo publishes an announcement post rather than an abstract link, and that post is rejected above as marketing, so the reimplementation's citation was used for the pairing instead.
- https://arxiv.org/abs/2301.12597 - confirmed from `salesforce/LAVIS` and its `projects/blip2` page. The full title was not needed because the subtitle after the colon was trimmed under the title rule.
- https://arxiv.org/abs/2304.08485 and https://arxiv.org/abs/2310.03744 - confirmed from the `haotian-liu/LLaVA` README and its citation block.
- https://arxiv.org/abs/2402.07865 - confirmed from the `TRI-ML/prismatic-vlms` README badge and citation block.
- https://arxiv.org/abs/2409.17146 - confirmed from the `allenai/molmo` citation block.
- https://arxiv.org/abs/2307.06281, https://arxiv.org/abs/2311.16502, https://arxiv.org/abs/2403.20330 and https://arxiv.org/abs/2404.18824 - confirmed from the `open-compass/MMBench`, `MMMU-Benchmark/MMMU`, `MMStar-Benchmark/MMStar` and `GAIR-NLP/benbench` repositories respectively.
- The MMMU and MMStar repositories both link their papers as `arxiv.org/pdf/...pdf`. The abstract page was substituted in both cases under the arXiv carve-out, and the MMMU PDF link is listed in the rejected block so the substitution is on the record.
- https://github.com/open-compass/VLMEvalKit - the README links its report as `www.arxiv.org`; the entry cites the repository itself, because the prompt templates and the answer extraction code are the artefact being cited rather than the report.
- `api.github.com/repos/...` answers 403 for every repository not attached to this session, so repository and file existence was confirmed with a 200 from `raw.githubusercontent.com` on a file inside each repository. That is how the two `github.com/.../blob/...` card URLs and the two repository URLs were verified.
- Collision with section 4. Model cards as a documentation practice, and the datasheet literature behind them, sit in section 4's documentation and audit subsection by ownership, so the general card paper was left to them and only cards published by the training teams appear here. The LAION-5B dataset paper may also be wanted by section 4's datasets subsection; the earlier section keeps it if so, and the slot here would go to the scaling laws paper rejected above. Checked against the delivered drafts for sections one to ten: no URL in this section appears in any of them.
- Collision with section 9. Image-only self-supervision and its contrastive lineage are left to section 9 entirely. Nothing here cites a pretext-task paper, and the contrastive entries are image-text only.
- The MMStar paper's title is a question and runs past the sixty character soft ceiling. It was kept in full because the title rule forbids paraphrase and a question cannot be trimmed from the right without changing its sense.
- `misc/scripts/check_links.py` on this draft reports PASS with no dead link and no mirror. Every URL lands in UNREACHABLE or BLOCKED, which is the egress policy described above and not a property of any page. The four GitHub URLs come back BLOCKED with a refused automated client, and each was confirmed instead by a 200 from the matching `raw.githubusercontent.com` path.
- The checker does not classify `huggingface.co/papers` as a mirror host, so the rejected paper-wrapper URL above passes its blocklist. Worth adding to `MIRROR_HOSTS`, since the rejection here had to be made by hand.
- VQAv2 was wanted as the first benchmark entry, because it is where the visual question answering protocol and the language-prior problem were defined. Its identifier could not be confirmed from any reachable authors' repository, and the official dataset host was unreachable, so it was left out rather than guessed.

## Benchmark proposal

The claim worth measuring is the folklore that contamination can only be assessed by whoever holds the model, together with its corollary that a substring grep is enough once you do hold the corpus. The measurement generates a synthetic caption corpus and a synthetic evaluation set from one fixed seed, then injects a known subset of evaluation items back into the corpus in two forms, verbatim and as near duplicates produced by case and punctuation changes, word order jitter and token substitution, each item paired with a small synthetic image whose near-duplicate copy is requantised and resaved through Pillow. Two audits then run with no model present. The first is an exact audit over normalised character and word shingles held in a hash set. The second scores shingle overlap alongside an average hash of the image, swept across thresholds. The run reports recall and precision for each injection form and, separately, the false positive rate measured on the clean portion of the corpus, with every accuracy-style figure bit-identical across runs on the same seed.

The claim is settled in favour of auditability if the verbatim injections are recovered essentially completely and the near-duplicate injections are recovered at a rate well clear of the clean-portion false positive floor at a single usable threshold. It is settled against the grep corollary, which is the likelier outcome and the more useful finding, if near-duplicate recall at the exact-match threshold sits near zero while the shingle and image-hash audit recovers those same items, because real leakage arrives as paraphrase and rescaled imagery rather than as a copy. Either way the result is obtained without a forward pass, which is the part of the claim that matters for auditing a model whose corpus nobody will publish.
