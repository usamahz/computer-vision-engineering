# 2. Image formation: optics, sensors, the ISP, colour, noise

Owner: camera and image signal processor engineer who has tuned a sensor pipeline, suspicious of any work that treats an image as a clean array of numbers that fell from the sky.

## Section

## 2. Image formation: optics, sensors, the ISP, colour, noise

### Optics and projection

- [The Double Sphere Camera Model](https://arxiv.org/abs/1807.08957) - Why a pinhole model breaks on a wide lens and which projection replaces it.
- [High-Quality Computational Imaging Through Simple Lenses](https://www.cs.ubc.ca/labs/imager/tr/2013/SimpleLensImaging/SimpleLensImaging_Heide2013.pdf) - Where a lens stops being a clean transform and becomes a blur that varies with position and colour.
- [Light Field Photography with a Hand-Held Plenoptic Camera](https://graphics.stanford.edu/papers/lfcamera/) - What an aperture is actually sampling, and what focus becomes once that sampling is recorded.

### Sensors and noise

- [EMVA Standard 1288](https://www.emva.org/standards-technology/emva-1288/emva-standard-1288-downloads/) - Where dynamic range, read noise and quantum efficiency get definitions a measurement can falsify.
- [Recovering High Dynamic Range Radiance Maps from Photographs](https://pauldebevec.com/Research/HDR/) - Why pixel values are not radiance until the response curve has been recovered.
- [Practical Poissonian-Gaussian noise modeling and fitting](https://webpages.tuni.fi/foi/sensornoise.html) - Why noise in a raw frame depends on the signal, and how that dependence is fitted from one frame.
- [Learning to See in the Dark](https://arxiv.org/abs/1805.01934) - What is left to work with when almost no photons arrived, and what a stock pipeline does to it.

### The image signal processor

- [High-quality linear interpolation for demosaicing](https://www.microsoft.com/en-us/research/publication/high-quality-linear-interpolation-for-demosaicing-of-bayer-patterned-color-images/) - Where the linear demosaicing baseline that later methods are measured against is specified.
- [Deep Joint Demosaicking and Denoising](https://groups.csail.mit.edu/graphics/demosaicnet) - Why demosaicing and denoising stop being separate stages once the raw frame is noisy.
- [Photographic Tone Reproduction for Digital Images](https://users.cs.utah.edu/docs/techreports/2002/pdf/UUCS-02-001.pdf) - Where a tone curve comes from, and why a scene cannot reach a display unmodified.
- [Unprocessing Images for Learned Raw Denoising](https://arxiv.org/abs/1811.11127) - Which pipeline stages have to be inverted before processed images can stand in for raw ones.
- [Burst photography for high dynamic range and low-light imaging](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/) - What a shipped pipeline does instead of one exposure and one denoiser.

### Colour

- [A Standard Default Color Space for the Internet](https://www.w3.org/Graphics/Color/sRGB.html) - Where the encoding every pipeline assumes is written down as a piecewise curve rather than a power law.
- [ITU-R BT.709](https://www.itu.int/rec/R-REC-BT.709) - Where the primaries and the camera encoding curve that most video silently assumes are specified.
- [ITU-R BT.2100](https://www.itu.int/rec/R-REC-BT.2100) - Which transfer functions a high dynamic range signal may carry, and what display it assumes.
- [ICC Specifications](https://www.color.org/icc_specs2.xalter) - How a colour space travels between two pipelines that agree on pixels and disagree on colour.
- [Fast Fourier Color Constancy](https://arxiv.org/abs/1611.07596) - Why the illuminant has to be estimated before any colour transform downstream means anything.

## Rejected

- [Handheld Mobile Photography in Very Low Light](https://research.google/pubs/handheld-mobile-photography-in-very-low-light/) - Rule failed: conventions.md section 8, the core needs a shipped implementation an outsider can run and a public measurement stating every field. The pipeline exists only inside one vendor's phone camera application and ships no dataset, unlike the burst photography entry, which publishes the burst dataset its results were computed on, so this is a watchlist candidate rather than a core entry.
- [Unprocessing Images for Learned Raw Denoising](https://arxiv.org/pdf/1811.11127) - Rule failed: conventions.md section 5, the arXiv carve-out admits the abstract page and not the PDF. The abstract page carries the version history, and a direct PDF hides which revision a reader is holding.
- [EMVA1288](https://en.wikipedia.org/wiki/EMVA1288) - Rule failed: conventions.md section 5, primary sources only, and section 6, restatement. An encyclopaedia summary of a freely downloadable standard adds a layer of error over a document the standards body hands out at no cost.
- [High-quality linear interpolation for demosaicing of Bayer-patterned color images](https://www.cs.toronto.edu/~lindell/teaching/2529/reading/Demosaicing_ICASSP04.pdf) - Rule failed: conventions.md section 5, a course site rehost is neither the authors' copy nor the publisher's. The authors' own institution publishes this paper on its research listing, so a teaching path copy adds a host that rots on its own schedule and carries no version history.
- [High-quality linear interpolation for demosaicing](https://www.microsoft.com/en-us/research/?p=158092) - Rule failed: owner-brief section 5, a permanent redirect is cited at its destination rather than at the form that redirects. This query string permalink reaches the right page, and the link checker recorded one hop to the slug form, which is what the section cites.
- [EMVA Standard 1288 Release A2.01](https://zenodo.org/record/1402251) - Rule failed: conventions.md section 10, an entry must resolve to the live canonical document. This is an archived copy of a release the standards body has twice superseded, and citing it would teach a reader the wrong noise and dynamic range definitions.
- [High-Quality Computational Imaging Through Simple Lenses video](https://vimeo.com/61495125) - Rule failed: conventions.md section 6, video lectures and talks. The results are in the paper, which is diffable and quotable, and the video carries no cross-channel deconvolution detail the paper omits.
- [Deep Image Demosaicking using a Cascade of Convolutional Residual Denoising Networks](https://arxiv.org/abs/1803.05215) - Rule failed: conventions.md section 9, the subsection is full at its budget. It would have had to displace Deep Joint Demosaicking and Denoising, which it cannot, because the earlier work is the one that states the joint problem and publishes the hard patch mining that makes the training set honest.

## Claims

### Peak signal to noise ratio gain over bilinear demosaicing, quoted on the research listing for the linear demosaicing filter

- Fields present: metric with its name, baseline compared against, a second comparison against another linear method.
- Fields missing: dataset with split and version, input resolution and preprocessing, evaluation protocol, training data used, hardware, metric with its full definition.
- Verdict: recorded unverified
- Note: Demosaicing peak signal to noise ratio is computed against a reference that was itself produced by mosaicking an already processed colour image, so the reference is an ISP output and not ground truth. The entry stands on the filter being the baseline later work is measured against, not on the figure, and the figure is not repeated in the section.

### Noise in a raw frame is a Poissonian-Gaussian process whose variance is affine in the signal, with two parameters sufficient to describe it

- Fields present: metric with its full definition as a variance model, the fitting procedure, a published tool that reproduces the fit on a single image, the clipping behaviour at both ends of the range.
- Fields missing: hardware, and the sensor and exposure conditions behind the authors' example raw data are named on the page rather than fully specified.
- Verdict: stands
- Note: This is a mechanism claim rather than an accuracy claim, and it is the one this section proposes to measure, because the benchmark can generate data whose true noise parameters are known by construction.

### A denoiser trained on raw noise synthesised by inverting the pipeline outperforms one trained on noise added after processing

- Fields present: dataset, metric, baseline compared against, training data used, the inversion stages listed in full.
- Fields missing: hardware, model and exact checkpoint, evaluation protocol in the detail the ladder requires.
- Verdict: recorded unverified
- Note: The container's egress policy blocked the paper itself, so the experimental section could not be read here and no figure from it is repeated anywhere in this draft. The entry stands on the stage-by-stage inversion recipe, which is checkable from the abstract page and from the noise model it builds on, not on the comparison.

### The burst pipeline produces a finished twelve megapixel image in about four seconds on device

- Fields present: input resolution, and the statement that the measurement was taken on the handset rather than on a workstation.
- Fields missing: hardware and count, precision, batch size, framework and version with compile flags, warmup and the statistic reported, whether preprocessing and postprocessing are inside the timer.
- Verdict: recorded unverified
- Note: Preprocessing and postprocessing are almost certainly outside the timer here, since capture, motion metering and the exposure decision happen before the stated interval and encoding happens after it, but the publication listing does not say so, which is exactly why the number is not repeated in the entry. No handset model, no clock and no repeat count are given.

### The pipeline operates down to about three tenths of a lux

- Fields present: metric named as scene illuminance, a baseline of unaided human vision, the hardware class as one vendor's handsets.
- Fields missing: metric with its full definition, evaluation protocol, dataset with split and version, hardware and count.
- Verdict: watchlist
- Note: Scene illuminance at the subject is not a protocol, and no public capture set accompanies the claim, so nobody outside the authors' group can run the comparison. Enters the core when a burst set captured at the stated illuminance is published with the metering parameters.

### The sRGB encoding is a power law with an exponent of two point two

- Fields present: the specification's own definition, which is piecewise, with a linear segment near black and an exponent of two point four on the curved segment.
- Fields missing: none, the definition is published.
- Verdict: cut
- Note: The figure of two point two describes the effective exponent of the resulting display behaviour and is not the encoding, so code that applies a single power law disagrees with the standard near black, which is exactly where sensor noise lives. The normative text is sold by the standards body and could not be opened from this container, so the openly readable deposit is what the entry cites.

### A camera has a given number of stops of dynamic range, as quoted in vendor material

- Fields present: none that the ladder recognises, the figure arrives as a bare number.
- Fields missing: metric with its full definition, evaluation protocol, hardware, and the measurement conditions the sensor standard requires, namely temperature, illumination spectrum, exposure time and the saturation and noise floor definitions.
- Verdict: cut
- Note: The standard in this section exists precisely so this claim can be stated checkably, and a figure quoted without those conditions is not comparable between two cameras, let alone between a camera and a published model's assumptions.

## Link notes

- Verification method for every URL in this draft: WebSearch in standard mode, confirming that the title, the identifier where one exists and the host agree before the URL was written down. This container's egress policy refuses nearly every host, so no URL here was confirmed by fetching it. Hosts that failed DNS resolution outright on one attempt each: szeliski.org, helpx.adobe.com, www.w3.org, www.cs.ubc.ca. The GitHub API path offered for repository checks returned 403 through the proxy for three candidate repositories, so no repository is cited in this section and nothing rests on one. One run of the repository link checker over this draft classified twenty four unique URLs as zero dead, zero mirror, one redirect and the rest unreachable, every unreachable case being the proxy refusing the tunnel rather than a missing page, which is the policy the brief describes and not link rot.
- https://arxiv.org/abs/1807.08957, https://arxiv.org/abs/1805.01934, https://arxiv.org/abs/1811.11127, https://arxiv.org/abs/1611.07596 - all four cited as abstract pages, never as PDFs. Each identifier was confirmed against its title and author list through search. Searches surfaced arXiv front ends and aggregator landing pages for all four; those hosts are rejected by rule and by the link checker's blocklist, so none appears here, including in the Rejected block.
- https://www.itu.int/rec/R-REC-BT.709 and https://www.itu.int/rec/R-REC-BT.2100 - version independent recommendation pages, cited deliberately because they carry the version history. BT.709-6 of June two thousand and fifteen and BT.2100-3 of February two thousand and twenty five are the versions in force, and the superseded editions are listed on the same pages. ITU recommendation texts are free to download, so neither of these sits behind a paywall.
- https://www.emva.org/standards-technology/emva-1288/emva-standard-1288-downloads/ - the standards body's download page rather than a release specific PDF path, because Release four replaced Release three point one and split the document into a General module and a Linear module. The standard is free and published under a Creative Commons licence that permits redistribution without modification. A near duplicate page with a trailing numeral in the path also exists, and the Zenodo archive of the oldest release is rejected above.
- https://www.w3.org/Graphics/Color/sRGB.html - the host marks this deposit as retained for historical purposes, and the normative standard is IEC 61966-2-1, which is sold through the IEC web store and is the one paywalled document this section depends on. The deposit is cited because it is the openly readable text of the definition and the equations in it are the ones pipelines implement. The current openly readable restatement in the web platform's colour specification would be preferable, but its canonical URL could not be confirmed before the search budget for this turn was exhausted, so it is not cited.
- https://www.color.org/icc_specs2.xalter - three spellings of this page surfaced in search, with and without the extension that the consortium's site uses. The landing page is cited rather than the specification PDF because the PDF path names a single revision and the page tracks the amendment history.
- https://users.cs.utah.edu/docs/techreports/2002/pdf/UUCS-02-001.pdf - the authors' institutional technical report, openly readable. The journal version of the same work is paywalled, and the only other openly readable copies found were course site rehosts, which are rejected by rule.
- https://www.cs.ubc.ca/labs/imager/tr/2013/SimpleLensImaging/SimpleLensImaging_Heide2013.pdf - the laboratory's own copy. The containing directory is described in search results as the project page, but it could not be confirmed as a page in its own right because the host does not resolve from here, so the confirmed PDF path is cited instead.
- https://webpages.tuni.fi/foi/sensornoise.html - the authors' own model and tool page, cited under the paper's trimmed title because the journal version is paywalled and this page is the artefact a reader actually needs, carrying the estimator that fits the two parameter model to a single raw image.
- https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/ - the publication listing. One oddity: the listing's author list is shorter than the citation published on the project's own dataset site, so the two official sources disagree about authorship. An older numeric publication path for the same page also exists and redirects, and the slug form is cited.
- https://www.microsoft.com/en-us/research/publication/high-quality-linear-interpolation-for-demosaicing-of-bayer-patterned-color-images/ - the destination of a permanent redirect. The query string permalink for the same page is the only form that surfaced in search, the link checker followed it in one hop, and the slug form above is what the section cites, as the brief requires for a permanent redirect. This was also the one URL in this draft the checker could actually reach from here.
- https://groups.csail.mit.edu/graphics/demosaicnet - the project page, which carries the abstract, the citation and the data pointers. Search also returned an institutional repository copy of the same paper, which was not preferred because the project page is the authors' own.
- Collisions flagged for the editor. Camera calibration and lens distortion estimation are left to section 3, which owns calibration in its coverage duty, so no calibration paper appears here even though lens distortion is an optics subject. The openly hosted textbook treatment of image formation was left out on two grounds at once: it would collide with section 1 and section 3, and its host does not resolve from this container, so the URL could not be verified to the standard the brief sets. The high dynamic range radiance map entry touches tone mapping, which section 13 may also want for its evaluation subsection; this section keeps it because the response curve, not the display mapping, is why it is here.

## Benchmark proposal

The claim under test is that sensor noise is signal dependent, so one denoising or normalisation
constant chosen in the midtones is wrong at both ends of the exposure range. The measurement
generates a noise free linear test frame in numpy from a recorded seed, holding a low contrast
texture patch and an intensity ramp, scales it across exposures from a handful of electrons per
pixel up to near saturation, and forms each observed frame as a Poisson draw on the photon count
plus a zero mean Gaussian read term, with a fixed gain mapping electrons to code values and
clipping applied at both ends the way a sensor applies it. Pillow writes a few inspection frames
and does nothing else. For every exposure the benchmark estimates the noise standard deviation per
intensity bin, fits the affine variance model, then denoises each frame twice with the same local
averaging operator, once with a single standard deviation fitted at the middle exposure, which is
the assumption under test, and once with the per pixel standard deviation the affine model implies.
The headline is the median residual root mean square error against the noise free reference at the
darkest, middle and brightest exposure, with the interquartile range across seeds, and the timer
covers only the estimation and filtering, not the data generation.

What would settle it: the claim holds if the fitted slope of variance against signal is clearly
positive and the fixed constant's residual rises at both ends while the signal dependent one stays
flat, with the direction of the failure reported separately at each end, because the fixed constant
over-smooths the dark frames and flattens the low contrast patch, then under-denoises the bright
ones and leaves the ramp visibly noisy. If the slope cannot be distinguished from zero, or the two
residual curves lie on top of each other across the sweep, the claim does not hold on this data and
the section says so in the first sentence of the analysis. Quick mode uses small tiles, three
exposures and one seed, and finishes well inside ten seconds. Everything is synthetic and built at
run time from the recorded seed, so no network access is needed and nothing beyond numpy and Pillow
is imported.
