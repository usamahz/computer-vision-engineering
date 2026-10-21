# 1. Start here: the minimum mental model

Owner: staff engineer who onboards vision hires, ordering the ten by what the next item needs, suspicious of anything that assumes a background the reader has not been given yet.

## Section

## 1. Start here: the minimum mental model

1. [Recovering High Dynamic Range Radiance Maps from Photographs](https://pauldebevec.com/Research/HDR/) - Where the curve from scene radiance to stored pixel value is recovered rather than assumed.
2. [Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) - The projection model and the distortion terms a calibration routine actually solves for.
3. [A Pixel Is Not A Little Square](https://www.alvyray.com/Memos/CG/Microsoft/6_pixel.pdf) - Why treating a sample as a little square breaks resampling and alignment.
4. [A guide to convolution arithmetic for deep learning](https://arxiv.org/abs/1603.07285) - Where kernel size, stride, padding and dilation turn into exact output shapes.
5. [Visualizing and Understanding Convolutional Networks](https://arxiv.org/abs/1311.2901) - What a learned filter responds to, shown instead of asserted.
6. [ImageNet Large Scale Visual Recognition Challenge](https://arxiv.org/abs/1409.0575) - Where the accuracy figures everyone quotes get their task definition and their scoring rule.
7. [Understanding deep learning requires rethinking generalization](https://arxiv.org/abs/1611.03530) - Why fitting the training labels and generalising are separate events.
8. [Are we done with ImageNet?](https://arxiv.org/abs/2006.07159) - What the single label per image assumption hides when a picture holds several objects.
9. [ShuffleNet V2](https://arxiv.org/abs/1807.11164) - Why counted operations do not predict latency and what has to be timed on the target device.
10. [Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/) - Where the costs that arrive after a model ships are named as engineering debt.

## Rejected

- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) - Rule failed: conventions section 3, a section may assume nothing after it, and this needs section 7. It was considered for the learned feature slot at item five, where a reader has no attention operator, no patch embedding and no sense of what the data scale argument is replying to, so the item would have to be read forwards to be read at all.
- [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934) - Rule failed: conventions section 3, forward dependency on section 12. Volume rendering through a learned field is unreadable before posed cameras, and item two gives only the projection model, not reconstruction.
- [A Standard Default Color Space for the Internet - sRGB](https://www.w3.org/Graphics/Color/sRGB.html) - Rule failed: conventions section 5 admission for standards and section 10 on citing the thing that is actually live. The openly readable copy carries its own obsolescence notice and points at IEC 61966-2-1, which is not openly readable, so neither URL is a live canonical source a reader can check the transfer function against.
- [The Pascal Visual Object Classes (VOC) Challenge](https://www.microsoft.com/en-us/research/publication/the-pascal-visual-object-classes-voc-challenge/) - Rule failed: conventions section 3, forward dependency on sections 5 and 10. Average precision with an overlap threshold is the right source for what a detection metric computes, and a reader at item six has no detector, no overlap measure and no non-maximum suppression, so the item would teach the protocol of a task that has not been introduced.
- [Do ImageNet Classifiers Generalize to ImageNet?](https://arxiv.org/abs/1902.10811) - Rule failed: conventions section 9 size limit, ten items and no eleventh. It would have displaced item ten, and item ten keeps the slot because a new test set teaches that a benchmark number travels badly, while the deployment item teaches the pipeline, feedback and consumer failures that arrive even when the number travels fine.
- [A guide to convolution arithmetic for deep learning](https://arxiv.org/pdf/1603.07285) - Rule failed: conventions section 5, the abstract page is cited and not the PDF, because the abstract page carries the version history. This paper has two deposited versions, so the distinction is load bearing rather than cosmetic.
- [ImageNet Large Scale Visual Recognition Challenge (ILSVRC)](https://image-net.org/challenges/LSVRC/) - Rule failed: conventions section 6, leaderboards and benchmark trackers. The challenge site is the right place for the protocol and the wrong place for the ranking, and the entry a reader needs is the paper that defines the task and the metric, which item six already carries.

## Claims

### The sRGB transfer function is a single power law with an exponent of two point two, as repeated whenever item one comes up

- Fields present: the exponent as quoted, and the direction of the mapping as usually implied.
- Fields missing: metric with its full definition, evaluation protocol, baseline compared against.
- Verdict: cut
- Note: the specification's own curve is piecewise, a linear segment near black followed by an offset power segment above it, so the quoted single exponent contradicts the document it is attributed to. The openly readable copy also records a rounding correction made during standardisation, which is a second reason the bare constant has no protocol behind it. Cut rather than recorded unverified, because the fields contradict each other rather than merely being absent.

### The camera response curve is recoverable from several differently exposed photographs only up to one global scale factor, in the radiance map paper at item one

- Fields present: metric with its full definition, meaning relative radiance identifiable up to a single multiplicative constant; evaluation protocol, meaning a least squares fit across exposures with a smoothness term under an assumption of reciprocity; baseline compared against, in that the recovery is demonstrated for both photochemical and digital imaging; training data used, which does not apply because no parameters are learned from a corpus.
- Fields missing: model and exact checkpoint, which does not apply; dataset with split and version, since the scenes are the authors' own; input resolution and preprocessing; hardware.
- Verdict: stands
- Note: this is an identifiability statement rather than a measurement, so the absent fields cannot contradict it and the section repeats no figure from it. The entry rests on it, because the whole of item one is the claim that a stored pixel value is an encoding of radiance and not radiance. The evidence marshal may prefer recorded unverified on the strength of the absent fields, and the entry survives either verdict.

### The classification improvement over the earlier convolutional model reported in the feature visualisation paper at item five

- Fields present: dataset with split and version, as the challenge validation and test splits of that year; metric with its full definition, as top-five error; evaluation protocol in outline, with multiple crops and model combination named as variants; baseline compared against, as the earlier convolutional model; training data used, as the same year's training split.
- Fields missing: model and exact checkpoint, input resolution and preprocessing per reported row, hardware.
- Verdict: recorded unverified
- Note: presence was assessed from the abstract and from the bibliographic record that search returned, because this container cannot reach the paper's full text, so the experimental section was not read. The entry rests on the visualisation method rather than on the error figure, and the reason line carries no figure.

### Convolutional networks fit randomly labelled training data to zero training error, in the paper at item seven

- Fields present: dataset with split and version, as the training splits of the small image corpus and of the large recognition corpus; metric with its full definition, as training error under randomised labels and randomised pixels; evaluation protocol, as the same recipes run with and without explicit regularisers; training data used, as the randomised training splits; baseline compared against, as the same architectures on true labels.
- Fields missing: model and exact checkpoint, input resolution and preprocessing, hardware.
- Verdict: recorded unverified
- Note: the full text was not reachable from this container, so the three absent fields are recorded rather than argued away. The entry rests on the qualitative result that fitting and generalising come apart, which is what item seven has to install before item eight can say anything about labels, and no figure from the paper is repeated.

### The human top-five error figure quoted from the challenge paper at item six

- Fields present: dataset with split and version; metric with its full definition, as top-five error; evaluation protocol in outline, as a trained annotator working a sampled subset.
- Fields missing: model and exact checkpoint, which cannot exist because an annotator cannot be re-run; input resolution and preprocessing; training data used; hardware; baseline compared against.
- Verdict: watchlist
- Note: the figure is reproducible only by the group that ran that annotation exercise, which the ladder places at watchlist at best. The watchlist verdict attaches to the claim and not to the entry, since item six stands on the task and metric definitions, which are fully specified in the same paper.

### The latency comparisons in the efficient design paper at item nine, including the mobile rows

- Fields present: hardware and count in part, as one desktop graphics processor and an ARM device that is described rather than named; input resolution; the reported statistic as a throughput figure.
- Fields missing: precision; batch size; framework and version with compile flags; warmup and the dispersion of the reported statistic; whether preprocessing and postprocessing are inside the timer.
- Verdict: watchlist
- Note: on the timer boundary, nothing in the material that could be verified from this container puts image decode, resize, normalisation or any postprocessing inside the timer, so every figure should be read as the network forward pass alone. The unnamed mobile device makes those rows reproducible only by the authors. The entry rests on the mechanism, that memory access cost and degree of parallelism break the operation count as a latency proxy, and it quotes no figure.

### The re-scored validation accuracy reported against the reassessed labels at item eight

- Fields present: dataset with split and version, as the original validation split carrying a separately distributed reassessed annotation; metric with its full definition, as accuracy against a multi-label annotation with unlabelled examples excluded; evaluation protocol, as re-scoring existing classifiers without retraining; baseline compared against, as the original labels.
- Fields missing: model and exact checkpoint for each re-scored classifier, input resolution and preprocessing, training data used, hardware.
- Verdict: recorded unverified
- Note: the exclusion of the few thousand images that received no label under the new procedure is part of the protocol, and a re-scoring that quietly keeps them is not comparable, which is exactly the lesson item eight is in the path to teach. The entry rests on the existence and direction of the label disagreement, not on the accuracy figure.

### The accuracy drop on the rebuilt test set, from the paper rejected for the size limit

- Fields present: dataset with split and version, as new test sets built by replaying the original collection procedure; metric with its full definition, as top-one accuracy on the new and the original sets; evaluation protocol, as the same models scored on both; training data used, as unchanged; baseline compared against, as the original test sets.
- Fields missing: model and exact checkpoint for each scored model, input resolution and preprocessing, hardware.
- Verdict: recorded unverified
- Note: examined because it is the figure people reach for whenever benchmark overfitting is argued, and the count of examined numbers is the evidence that the bar was real. Recorded here and quoted nowhere, and the paper was rejected for the size limit rather than for the number.

## Link notes

- Verification route for the whole section. This container's egress policy refused every direct fetch attempted. The unversioned alias of the projection documentation page returned no HTTP status at all through the proxy, and the repository endpoint of the GitHub API returned 403, so the API route was unavailable too and nothing here was confirmed by fetching it. The link checker run on this draft classifies every URL as UNREACHABLE with a refused tunnel, and reports no dead link and no mirror. Every URL in this draft was confirmed by standard web search in which the source's own title, its identifier where it has one, and the host agreed across independent results. No URL was included on the strength of a guessed path.
- https://arxiv.org/abs/1603.07285, https://arxiv.org/abs/1311.2901, https://arxiv.org/abs/1409.0575, https://arxiv.org/abs/1611.03530, https://arxiv.org/abs/2006.07159, https://arxiv.org/abs/1807.11164 - each confirmed by title, arXiv identifier and author list agreeing across results, and cited in abstract page form. Reader front ends and rehosts surfaced for all six, including ar5iv, alphaxiv, academia.edu, deepai, bibsonomy and several aggregator landing pages, and all were rejected under conventions section 6. For the convolution arithmetic guide the PDF path was the top result and is rejected above in favour of the abstract page.
- https://pauldebevec.com/Research/HDR/ - the authors' own project page, chosen over course-hosted copies of the paper at Princeton, Waterloo and WPI, over a `mail.pauldebevec.com` host variant of the same abstract page, and over the conference history archive entry. The project page was preferred to the abstract page on the same host because it carries the publication record and the radiance map downloads.
- https://www.alvyray.com/Memos/CG/Microsoft/6_pixel.pdf - the memo itself on the author's own site, cross-checked against that site's own index of computer graphics memos, which lists it as the numbered technical memo with the later voxel subtitle added. Course-hosted copies at Princeton and Northwestern were rejected as rehosts. This is a PDF rather than a landing page because the memo has no landing page of its own; the index page is one level up and names it.
- https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html - version pinned deliberately. The unversioned `4.x` alias could not be confirmed from this container, and the only other module page search could confirm by exact path was an old release. The pinned page was confirmed by a domain-restricted search in which the page heading, the projection relation and the radial and tangential distortion text all matched. A reader checking later will find the alias page carrying the same content; the pin is the version that was verified, and it should be revisited when the documentation moves.
- https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/ - the authors' own institutional publication page. The conference proceedings paper file was confirmed by search, but the hash-based proceedings abstract page could not be, and the brief prefers a landing page over a PDF, so the publication page is cited.
- https://www.microsoft.com/en-us/research/publication/the-pascal-visual-object-classes-voc-challenge/ and https://image-net.org/challenges/LSVRC/ - appear only in the rejected block, both confirmed by title and host agreeing in search. The official dataset site for the first of those could not be confirmed from this container at all, which is one more reason it is not cited as a live source here.
- URLs left out for want of confirmation, named so that the next owner does not repeat the work: the course notes page for convolutional networks on `cs231n.github.io`, the book site for multiple view geometry under `robots.ox.ac.uk`, the development kit documentation under `host.robots.ox.ac.uk`, and the author-hosted textbook on `szeliski.org`. Search returned no result that confirmed any of those paths, so they are absent rather than caveated, including from the rejected block where two of them would otherwise have been useful examples.
- Collisions to flag for later owners, under owner-brief section 2. The projection model page overlaps section 3 on two-view geometry and section 12 on reconstruction. The challenge paper overlaps section 4 on datasets and section 5 on evaluation. The reassessed label paper overlaps section 4 on annotation and label noise. The efficient design paper overlaps section 6 on efficient convolutional designs and section 15 on measurement. The radiance map paper overlaps section 2 on the image signal processor and colour. Section 1 keeps all five, so each of those owners picks something else.

## Benchmark proposal

The claim under test is the one the field repeats without thinking, that an image is an array of
numbers and the array is the scene. Measured against it: one synthetic linear light scene is
generated from a fixed seed with `numpy.random.default_rng`, holding both a bright highlight
region and a deep shadow region, and then encoded twice, once through the piecewise curve with a
linear segment near black and once through a plain power law. Both encodings are quantised to
eight bit, and the benchmark reports per channel the median and the maximum absolute difference
in code levels, plus the fraction of pixels differing by more than one level. The second half
repeats the comparison through an operation rather than a display, halving the image with Pillow
in the encoded domain and again in linear light before re-encoding, and reports the difference
between those two orders overall and restricted to a high contrast edge mask.

What would count as settling it: the claim holds if the two encodings differ by more than one code
level across a large fraction of pixels and the two downscale orders differ by more than one code
level at edges, and it fails if every difference sits at or below one level, which would mean the
transfer function is cosmetic for downstream arithmetic. Both outputs are accuracy style and have
to be bit identical between runs on the same machine. Nothing is timed, so no timer boundary is
declared, and the machine comes from the shared harness banner rather than being typed. Numpy and
Pillow only, no GPU and no network at run time, and the quick mode runs one small scene so that it
finishes well inside ten seconds.
