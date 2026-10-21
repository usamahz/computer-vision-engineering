# Link verification

The link verifier confirms that every URL resolves to the live canonical source of the title it
is attached to, records redirects and blocked hosts, and rejects mirrors where an official copy
exists.

## Why there are two kinds of check

The build container's egress policy refuses connections to almost every host this list cites,
including arxiv.org, github.com web pages, pytorch.org and university sites. A refusal there is
policy, not a dead page, so the live check could not run from the machine that built the list.
Two checks therefore exist and they answer different questions.

- Identity, done here. Each URL was matched to its title by a method that does not need the
  host: the arXiv identifier and title appearing together in the authors' own repository
  README fetched from raw.githubusercontent.com, a 200 from the raw path behind a GitHub file
  link, or a web search that returns the exact URL with the exact title.
- Liveness, done in CI. `misc/scripts/check_links.py` runs on every push and weekly from a GitHub
  runner with open egress, separates dead from unreachable from blocked, and fails the build
  and opens an issue on a dead link or a mirror.

## Round one, over the first merged README

URLs in scope: 327. Reported: 327. confirmed 317, non_canonical 9, mismatch 0, unconfirmed 1.

Every URL that was not simply confirmed, and what happened to it:

- non canonical: https://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf
  - Evidence: An exact-URL search for host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf returned nothing on that host, so this path is not confirmed. Search restricted to robots.ox.ac.uk shows the VOC site now lives at https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/ ('The PASCAL Visual Object ...
  - Outcome: Replaced with the organisers' current landing page, https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/pubs/everingham10.html.

- non canonical: https://github.com/hszhao/SAN
  - Evidence: The repository exists: raw README 200, heading 'Exploring Self-attention for Image Recognition', owned by the first author. But the title names the paper, and the repository is only its code. The owner's link note says the repository was chosen only because the arXiv ID could not be confirmed. ...
  - Outcome: Entry cut by the red team; the paper's claim was cited through a repository.

- non canonical: https://huggingface.co/papers/2310.03744
  - Evidence: This is a Hugging Face Papers aggregator page for the same work. The LLaVA README places [HF](https://huggingface.co/papers/2310.03744) next to the arXiv paper link. The draft already rejects it on these grounds.
  - Outcome: Not in the shipped README: the URL appears only in a draft's rejected block, where it was already refused for this reason.

- non canonical: https://arxiv.org/pdf/2311.16502.pdf
  - Evidence: This is an arXiv /pdf/ path. The MMMU README links exactly this PDF under this title. The draft's rejection already substitutes the abstract page.
  - Outcome: Not in the shipped README: the URL appears only in a draft's rejected block, where it was already refused for this reason.

- non canonical: https://www.deepmind.com/blog/tackling-multiple-tasks-with-a-single-visual-language-model
  - Evidence: Moved page. WebSearch shows the post (Apr 28 2022, Flamingo) indexed on deepmind.google at /blog/... and /discover/blog/.... The deepmind.com URL is the legacy host.
  - Outcome: Not in the shipped README: the URL appears only in a draft's rejected block, where it was already refused for this reason.

- non canonical: https://openai.com/blog/clip/
  - Evidence: Moved page. A WebSearch restricted to openai.com returns 'CLIP: Connecting text and images' at openai.com/index/clip/. openai/CLIP README still links the old /blog/clip/ path.
  - Outcome: Not in the shipped README: the URL appears only in a draft's rejected block, where it was already refused for this reason.

- non canonical: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/performance/quantization_spec.md
  - Evidence: The raw file at master returns 200 and its heading matches the title. It is a legacy docs source file, though. WebSearch shows the maintained spec now published as 'LiteRT 8-bit quantization specification' on developers.google.com/edge/litert/... (also ...
  - Outcome: Kept. The maintainer's own source file is confirmed at its path; the renamed published page could not be pinned to a verified URL. Recorded so the next review can move it.

- non canonical: https://github.com/microsoft/onnxruntime/blob/gh-pages/docs/performance/model-optimizations/quantization.md
  - Evidence: The raw file on gh-pages returns 200 with heading '# Quantize ONNX Models'. It is the Jekyll source of the docs site, with front matter and a TOC placeholder. WebSearch shows the published page 'Quantize ONNX Models' at onnxruntime.ai/docs/performance/model-optimizations/quantization.html.
  - Outcome: Replaced with the published documentation page, https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html.

- non canonical: https://raw.githubusercontent.com/hendrycks/robustness/master/ImageNet-C/create_c/make_imagenet_c.py
  - Evidence: This raw file URL returns 200, but it is a raw rehost path rather than the repository page. The draft cites it deliberately, while the editor's README uses the blob URL.
  - Outcome: Already cited in the README as the blob page, which is the canonical form; the raw path was the draft's.

- unconfirmed: https://api.github.com
  - Evidence: This is not a reading and has no title, so there is nothing to match against a source. curl to api.github.com/repos/quic/aimet answered 403 from this container, which reproduces the note's claim. It is listed only so that no URL is skipped.
  - Outcome: Not an entry. A diagnostic mention in a draft's link notes.

## Added in review

Every source the editor added after round one was confirmed before it went in. Eleven arXiv
identifiers were matched to their titles in the authors' own repository READMEs: registers
2309.16588, SmoothQuant 2211.10438, POPE 2305.10355, anti-aliased networks 1904.11486,
Consistency Models 2303.01469, GenEval 2310.11513, FixRes 1906.06423, the out-of-distribution
baseline 1610.02136, SSD 1512.02325, stochastic depth 1603.09382 and TimeSformer 2102.05095.
Mixed Precision Training 1710.03740, YOLOv3 1804.02767, Model Cards for Model Reporting
1810.03993 and Adversarial Patch 1712.09665 were confirmed by search returning the exact
abstract page with the exact title. CSS Color Module Level 4 was confirmed at its W3C address.
The Apple Neural Engine repository README was fetched directly.

## Hosts that refuse automated clients

Publishers and vendor documentation commonly answer 401, 403, 406 or 429 to a script while
serving a browser. `check_links.py` reports those as BLOCKED and does not fail the build on
them, because a checker that calls them dead trains everyone to ignore it. The hosts most
likely to do so for this list are the arXiv abstract pages under load, research.google,
microsoft.com research pages and developer.apple.com.

## Canonical URL changes

URLs that changed between an owner's draft and the README, because the verifier found the
canonical copy elsewhere. `misc/scripts/build_changelog.py` reads this list, so that a moved URL is
counted as the same entry rather than as one removal and one addition. Raw file URLs that became
the repository's own file page are normalised by the script and are not listed.

- `http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf` became `https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/pubs/everingham10.html`
- `https://github.com/microsoft/onnxruntime/blob/gh-pages/docs/performance/model-optimizations/quantization.md` became `https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html`
- `https://www.w3.org/Graphics/Color/sRGB.html` became `https://www.w3.org/TR/css-color-4/`
