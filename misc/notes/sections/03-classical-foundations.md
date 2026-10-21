# 3. Classical foundations: filtering, features, multi-view geometry

Owner: multi-view geometry engineer who has implemented bundle adjustment, suspicious of the claim that learning made geometry obsolete.

## Section

## 3. Classical foundations: filtering, features, multi-view geometry

The matching entries are ordered by what each one assumes rather than by which one wins, and the published comparisons between them were mostly run with the robust estimator tuned for one side only.

### Sampling and filtering

- [Computer Vision: Algorithms and Applications](https://szeliski.org/Book/) - Where the resampling and pyramid machinery the later papers assume is derived in one place.
- [The Laplacian Pyramid as a Compact Image Code](https://persci.mit.edu/pub_abstracts/pyramid83_abs.html) - Why a smoothing filter and a decimation step have to be chosen together rather than in turn.
- [Finding Edges and Lines in Images](https://dspace.mit.edu/handle/1721.1/6939) - Where an edge operator is derived from stated criteria instead of asserted as a kernel.
- [Feature Detection with Automatic Scale Selection](https://people.kth.se/~tony/papers/cvap198.pdf) - How the scale a detector responds at stops being a hand-set parameter.
- [Scale-space and edge detection using anisotropic diffusion](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1988/5318.html) - Why linear smoothing destroys the boundary it was meant to help locate.

### Features and correspondence

- [A Combined Corner and Edge Detector](https://bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf) - Where the local autocorrelation test behind most corner detectors is defined.
- [Distinctive Image Features from Scale-Invariant Keypoints](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) - Where the descriptor and the ratio test most matching pipelines still default to were set out.
- [SuperPoint](https://arxiv.org/abs/1712.07629) - What replaces a hand-designed detector once the keypoints themselves are learned from warps.
- [SuperGlue](https://arxiv.org/abs/1911.11763) - What replaces the nearest neighbour heuristic once correspondence is posed as an assignment.
- [Image Matching across Wide Baselines](https://arxiv.org/abs/2003.01587) - Whether a learned matcher still wins once pose is the metric and every stage is tuned equally.

### Two-view and multi-view geometry

- [A Flexible New Technique for Camera Calibration](https://www.microsoft.com/en-us/research/project/a-flexible-new-technique-for-camera-calibration-2) - Where the planar calibration procedure almost every toolbox implements was specified.
- [A Generic Camera Model and Calibration Method](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf) - What breaks when a wide lens is forced into a pinhole model with radial terms bolted on.
- [Determining the epipolar geometry and its uncertainty](https://www.microsoft.com/en-us/research/publication/determining-epipolar-geometry-uncertainty-review) - Why the recovered fundamental matrix depends on coordinate normalisation and on the cost chosen.
- [Recognising Panoramas](https://www.cs.ubc.ca/~lowe/papers/brown03.pdf) - How homographies, robust fitting and a joint refinement combine into one working pipeline.

### Estimation and bundle adjustment

- [Random Sample Consensus](https://www.sri.com/publication/artificial-intelligence-pubs/random-sample-consensus-a-paradigm-for-model-fitting-with-applications-to-image-analysis-and-automated-cartography/) - Where fitting a model by rejecting most of the data was first stated as a method.
- [Locally Optimized RANSAC](https://cmp.felk.cvut.cz/ftp/articles/matas/chum-dagm03.pdf) - Why a consensus set is worth refining inside the sampling loop rather than after it.
- [MAGSAC++](https://arxiv.org/abs/1912.05909) - What a robust estimator scores with once the inlier threshold is marginalised away.
- [Bundle Adjustment - A Modern Synthesis](https://dumas.ccsd.cnrs.fr/IMAG/inria-00590128v1) - Where the cost, the sparse normal equations and the gauge freedom are set out together.
- [Ceres Solver](https://ceres-solver.org/) - What a sparse nonlinear least squares problem looks like once it has to be written down and solved.

## Rejected

- [Multiple View Geometry in Computer Vision](https://www.robots.ox.ac.uk/~vgg/hzbook/) - Rule failed: the book carve-out, conventions.md section 5, which admits a book only where the author hosts the canonical copy openly. The page carries errata, figures and a pair of sample chapters, so the thing a reader is actually sent to is a purchase page, and the geometry it would have supplied is carried instead by the epipolar review and the calibration entries.
- [A Performance Evaluation of Local Descriptors](https://www.cse.unr.edu/~bebis/CS491Y/Papers/Schmid05.pdf) - Rule failed: primary sources only, conventions.md section 5, read with owner-brief rule two on third-party copies. Every copy I could confirm is a university course handout and neither author nor publisher hosts an open one, so the descriptor comparison is left out rather than cited from a lecture folder.
- [LoFTR](https://arxiv.org/abs/2104.00680) - Rule failed: the evidence standard, conventions.md section 7, a field missing where the entry would rest on the number. The pose result turns on the robust estimator and its inlier threshold and on the input resolution, none of which are pinned in what is published, so it is a watchlist claim and not a core entry.
- [An Efficient Solution to the Five-Point Relative Pose Problem](https://www-users.cse.umn.edu/~hspark/CSci5980/nister.pdf) - Rule failed: no third-party PDF mirror where an official copy exists, owner-brief rule two. The minimal solver belongs in this subsection on merit, and the only openly readable copies I could confirm are course scans, so it is absent for want of a citable host rather than for want of value.
- [In Defense of the Eight-Point Algorithm](https://www.cse.unr.edu/~bebis/CS485/Handouts/hartley.pdf) - Rule failed: no third-party PDF mirror where an official copy exists, owner-brief rule two. The normalisation argument it makes is already carried by the epipolar review that the section does cite, and the only copies I could confirm are course handouts.
- [Bundle Adjustment - A Modern Synthesis](https://ais-lab.di.unimi.it/Teaching/SIA/Old/IntelligentSystems_2003_2004/Documents/Vision/02_TriggsMcLauchRichard_Bundle%20Adjustment%20-%20A%20Modern%20Synthesis.pdf) - Rule failed: no third-party PDF mirror where an official copy exists, owner-brief rule two. This is a course copy of a paper the authors deposited in their own institutional repository, and the deposit is what the section cites.
- [Bundle Adjustment in the Large](https://grail.cs.washington.edu/projects/bal) - Rule failed: three to six entries per subsection and the displacement rule, conventions.md section 9. It would have had to displace the solver documentation, and a reader who has not yet written the normal equations down learns less from a problem set than from the thing that solves it.
- [Scale-Space Filtering](https://mlanthology.org/ijcai/1983/witkin1983ijcai-scale/) - Rule failed: aggregators and paper mirrors, conventions.md section 6. Scale space as a working idea starts here, and the only landing page I could confirm wraps the proceedings paper rather than hosting it, which also means the host is not on the link checker's mirror list and the machine would have passed it.

## Claims

### SIFT keypoints match reliably under scale, rotation, noise and viewpoint change

- Fields present: metric with its full definition, keypoint repeatability and the nearest neighbour ratio acceptance rate, both defined in the text; evaluation protocol, synthetic transformations applied to a fixed image set with no detection postprocessing stage involved; training data used, none; baseline compared against, matching without the ratio test.
- Fields missing: dataset with split and version; input resolution and preprocessing; model and exact checkpoint; hardware.
- Verdict: recorded unverified
- Note: the entry rests on the descriptor and the ratio test being what later pipelines default to, not on a repeatability figure, so no number is repeated. The transformations are synthetic warps of an unnamed image set, which is exactly the missing split, and a repeatability curve measured that way does not transfer to a real baseline.

### SuperGlue sets the best indoor and outdoor pose estimation among matching methods

- Fields present: model and exact checkpoint, the indoor and outdoor weight files published in the authors' repository; dataset, ScanNet indoors and MegaDepth outdoors, named in the repository; training data used, the same two; baseline compared against, nearest neighbour matching on identical keypoints.
- Fields missing: input resolution and preprocessing, the repository exposes a resize flag with three modes and the default differs between the two released models; evaluation protocol, the robust estimator and its inlier threshold are not pinned, and that setting dominates a pose number; metric with its full definition; hardware.
- Verdict: recorded unverified
- Note: the entry stands on the assignment formulation, not on the pose figure, so the number is not repeated. A pose comparison in which the estimator is tuned for the learned matcher and left at a default for the classical baseline is not a comparison of matchers, and the missing evaluation protocol field is where that hides.

### SuperGlue runs in real time on a modern GPU

- Fields present: none of the seven.
- Fields missing: hardware and how many of them; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: cut
- Note: preprocessing and postprocessing are not inside the timer for a claim phrased this way, and for this method the postprocessing is the robust estimator, which is the part of the pipeline a geometry user actually pays for. The protocol is unstated in everything reachable from here, so the claim is cut and the phrase is never repeated.

### LoFTR outperforms prior matching methods by a large margin on indoor and outdoor pose

- Fields present: dataset, ScanNet, MegaDepth, HPatches and InLoc, named; model and exact checkpoint, weights published in the authors' repository; baseline compared against, named method families.
- Fields missing: input resolution and preprocessing; evaluation protocol including the robust estimator settings; metric with its full definition; training data used, stated as the same datasets but without a split; hardware.
- Verdict: watchlist
- Note: an entry for this method would rest on the pose figure, and the field that decides that figure is the estimator setting, so it cannot enter the core on what is published. This is the reason the method is in the rejected block rather than in the section.

### Locally optimised RANSAC gives a two to three fold speed-up and ten to twenty per cent more inliers

- Fields present: baseline compared against, plain RANSAC; the model families fitted, epipolar geometry and homography; metric in part, the inlier count and the number of samples drawn.
- Fields missing, accuracy: dataset with split and version; input resolution and preprocessing; metric with its full definition; model and exact checkpoint; hardware.
- Fields missing, speed: hardware and how many of them; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: the speed-up is expressed as a ratio of samples drawn rather than wall clock, so there is no timer boundary to declare at all. That makes it more portable than a latency figure and it also means it must never be repeated as one. The entry rests on the local optimisation step being worth running inside the loop, not on the ratio.

### MAGSAC++ is often an order of magnitude faster than its predecessor and more geometrically accurate

- Fields present: dataset, six public sets for homography and fundamental matrix fitting, named in the paper; baseline compared against, the predecessor and other robust estimators.
- Fields missing, accuracy: split and version; input resolution and preprocessing; metric with its full definition; hardware.
- Fields missing, speed: hardware and how many of them; precision; batch size; input resolution; framework and version with compile flags; warmup and the statistic reported; whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: the entry rests on the scoring function removing the inlier threshold, which is a mechanism and not a timing result. Preprocessing here is the feature matching that produces the correspondences, and it is certainly outside any timer reported for the estimator, so the quoted ratio describes a fraction of the work a caller pays for.

### Well-tuned classical local features remain competitive with learned matchers once camera pose is the metric

- Fields present: dataset with split, the benchmark's own photo-tourism scenes with a published validation and test division; metric with its full definition, pose error thresholded on rotation and translation and then aggregated; evaluation protocol, a modular pipeline in which every stage is tuned on the validation split and the same robust estimator is exposed to every method; baseline compared against, classical detectors and descriptors against several learned methods; model and exact checkpoint, the public release of each method; training data used, as published for each learned method.
- Fields missing: hardware, which the accuracy claim does not rest on.
- Verdict: stands
- Note: this is the claim the section is ordered around, and it is the reason the matching entries carry a warning rather than a ranking. The earlier tables that put learned matchers ahead held one estimator setting fixed across methods, and tuning per method moves the order. The paper body was not reachable from this container, so the fields above were checked against the abstract and the public benchmark release and the aggregate figures are not repeated.

### A planar pattern observed in at least two orientations suffices to recover the intrinsics

- Fields present: metric with its full definition, reprojection error under the maximum likelihood criterion; evaluation protocol, a closed-form initialisation followed by nonlinear refinement, both described in the report; baseline compared against, photogrammetric calibration that needs a known three dimensional target and self-calibration that needs none.
- Fields missing: dataset with split and version; input resolution and preprocessing; model and exact checkpoint; training data used; hardware.
- Verdict: recorded unverified
- Note: this is the famous claim in the area and it is structural, about degrees of freedom, rather than numeric, which is why the entry can rest on it while the report's own reprojection figures are not repeated. The experimental section was not reachable from this container, so the dataset fields are recorded as missing rather than assessed.

## Link notes

- Nothing in this section could be fetched directly. The container's egress policy answers 403 to CONNECT for almost every host, including arxiv.org, szeliski.org, hal.science, ijcai.org and api.github.com, so every URL below was confirmed by web search with the title and the identifier agreeing, or by fetching a file from raw.githubusercontent.com. The policy refusals are not link rot and are not recorded as dead.
- https://szeliski.org/Book/ - The book carve-out rests on this page. Confirmed by search against the author's own site, which describes the published second edition alongside a free PDF; the page itself refused the connection. The same book is a plausible entry for sections 1 and 2, so the collision is flagged for the editor and the earlier section keeps it if it wants it.
- https://persci.mit.edu/pub_abstracts/pyramid83_abs.html - The authors' laboratory abstract page is cited rather than the PDF beside it, matching the rule that the abstract page carries the record. The journal version is behind a publisher paywall.
- https://dspace.mit.edu/handle/1721.1/6939 - This is the institutional technical report, not the later journal article, which is paywalled. The report is the primary derivation of the criteria and the operator, so it is cited in its own right rather than as a substitute.
- https://www2.eecs.berkeley.edu/Pubs/TechRpts/1988/5318.html - The authors' institutional report series page. A metadata record for the journal version also exists in a second university repository and was rejected in favour of this one because the report is openly readable and the record is not.
- https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf - An author self-archive at his current institution rather than the address printed in the paper, which no longer appears in search results. A national research registry marks the published article as not open access, so this copy is an author deposit and not a publisher copy.
- https://www.microsoft.com/en-us/research/project/a-flexible-new-technique-for-camera-calibration-2 - Two separate pages exist on the same host for this work, a project page and a technical report page. The project page is cited. The host refuses automated clients.
- https://www.microsoft.com/en-us/research/publication/determining-epipolar-geometry-uncertainty-review - Same host, same refusal. An institutional deposit of the identical report exists in the French open archive and a PDF of the report sits on this host as well; the publication page is cited because it carries the record.
- https://dumas.ccsd.cnrs.fr/IMAG/inria-00590128v1 - This is the authors' own institutional deposit, record inria-00590128, served under a laboratory portal of the French open archive rather than under the archive's main domain, which was unreachable from here. It looks like a third-party host and is not one. The deposit's own title field misspells Adjustment; the entry uses the published spelling and a hyphen in place of the dash in the title.
- https://ceres-solver.org/ - Confirmed from the maintainers' own repository README, fetched over raw.githubusercontent.com, which names this site as the project's documentation. The README links the http form, so expect one redirect to https.
- https://arxiv.org/abs/1712.07629 - The identifier was confirmed from the authors' own repository README for the companion method, which names this abstract page for the keypoint detector. Search budget ran out before a second independent confirmation, so the pairing of title and identifier rests on that repository.
- https://arxiv.org/abs/1911.11763, https://arxiv.org/abs/2003.01587, https://arxiv.org/abs/1912.05909 - Titles and identifiers confirmed by search. Abstract pages are cited, never the PDF. A conference open-access page also exists for the robust estimator and was passed over in favour of the abstract page because that page carries the version history.
- https://bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf, https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf, https://www.cs.ubc.ca/~lowe/papers/brown03.pdf, https://cmp.felk.cvut.cz/ftp/articles/matas/chum-dagm03.pdf, https://people.kth.se/~tony/papers/cvap198.pdf - Conference archive of the publishing society, and author or laboratory pages. Confirmed by search with title and author agreeing. These are PDFs because no abstract landing page exists on the same hosts.
- https://www.sri.com/publication/artificial-intelligence-pubs/random-sample-consensus-a-paradigm-for-model-fitting-with-applications-to-image-analysis-and-automated-cartography/ - The authors' institution hosts the publication record. Two near-identical paths exist on that host, one with a numeric suffix; the unsuffixed path is cited. The journal version is paywalled.
- Reader front ends and aggregators for several of these papers turned up in every search, including arXiv HTML front ends and a paper-anthology host. They are deliberately absent from the section. One of them, the anthology host, is not on the link checker's mirror list, which is worth telling whoever maintains that list.
- Sources I wanted and could not cite: the five-point relative pose solver, the eight-point normalisation paper, the descriptor performance evaluation and the original scale-space filtering paper. In each case the only openly readable copies I could confirm were course handouts or an aggregator wrapper, so they are in the rejected block instead.
- Collisions with later sections: incremental structure from motion and the reconstruction pipelines built on it belong to section 12 and are left alone here, including the large-scale bundle adjustment problem set, which is rejected above on the size limit rather than claimed.
- Ordering decisions that are not obvious from reading top to bottom. The book sits first in the opening subsection because the carve-out puts it there as the thing that makes the papers readable, not because it matters most. Anisotropic diffusion sits last in that subsection because it reads as a reply to linear scale space and is unreadable before it. Calibration comes before the epipolar review because the review assumes a camera model, and the panorama pipeline comes last in its subsection because it is the first entry that uses robust fitting and a joint refinement together, which hands the reader straight into the next subsection. The four subsection names are the brief's skeleton unchanged.
- misc/scripts/check_format.py did not exist when this draft was written, so the entry grammar, reason lengths and banned vocabulary were checked against voice.md by hand and by a throwaway script. misc/scripts/check_links.py exists but cannot classify anything useful from inside this container, because every host would come back blocked or unreachable.

## Benchmark proposal

The claim, in the form a practitioner repeats without thinking: a box blur is a cheap Gaussian, because a blur of equal support removes the same detail and repeating the box a few times converges on the Gaussian anyway, so the choice is an optimisation detail rather than a change to the image.

The measurement generates a synthetic step edge and a pair of closely spaced edges at known subpixel positions from a fixed seed, then blurs each with a separable Gaussian, with a box kernel of the same support width, with a box matched on its second moment, and with three successive box passes. Four quantities are computed from the blurred profiles: the maximum absolute profile difference normalised by edge contrast, the ten to ninety per cent rise distance, the subpixel edge position recovered from the zero crossing of the second derivative, and whether the two nearby edges stay separable in the second derivative at all. Pillow's own Gaussian and box filters run on the same arrays as a cross-check, so that a finding is not an artefact of the kernels written for the benchmark.

The claim is settled in favour of the folklore if the normalised profile difference stays a small fraction of the edge contrast and the recovered edge position agrees to within a small fraction of a pixel in every condition. It is broken if the recovered edge position shifts, or if the two-edge case resolves under one filter and not the other, and then the size of the shift and the support width at which the two-edge case collapses are the findings to report. Everything is synthetic, small, one and two dimensional, and needs only numpy and Pillow, so the quick mode runs a single support width at a reduced repeat count and finishes well inside ten seconds with no network access and no GPU.
