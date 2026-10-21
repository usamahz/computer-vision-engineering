# Red team, answered in writing

The red team argued for cutting entries section by section, and every argument gets an answer.
This file records the outcome of each finding against the README as it ships. An entry
that survived a cut argument says why. An entry that lost says so.

Round one ran over the first merged README with four batches of four sections. Round two
judged what the editor added or moved in response, and appears at the end.

## Round one: findings

### Section 0

- **Handheld Mobile Photography in Very Low Light** (Watchlist). Red team: cut.
  - Argument: Would enter section 2. Its reason ('A shipped low light pipeline built on a burst rather than one exposure') is close to word for word the job of the core entry 'Burst photography for high dynamic range and low-light imaging', whose reason reads 'What a shipped pipeline does instead of one exposure and one denoiser.' Section 2 also has 'Learning to See in the Dark' for very low light. Promoting it would create a ...
  - Rule cited: conventions.md section 10 (redundant rather than superseded); conventions.md section 8 (the watchlist holds items that could enter the core)
  - Answer: Accepted. Cut.

- **LoFTR** (Watchlist). Red team: reword.
  - Argument: Would enter section 3. The reason ('pose gains that hinge on unstated estimator settings') and the section 3 rejection behind it ('none of which are pinned in what is published') are contradicted by the authors' own released code. zju3dv/LoFTR src/config/default.py sets POSE_ESTIMATION_METHOD = 'RANSAC', RANSAC_PIXEL_THR = 0.5, RANSAC_CONF = 0.99999 and RANSAC_MAX_ITERS = 10000. ...
  - Rule cited: conventions.md section 7 (verdict must follow the fields actually present); section 8 (an observable condition)
  - Answer: Superseded by the evidence marshal, which moved the entry to the watchlist.

- **Stand-Alone Self-Attention in Vision Models** (Watchlist). Red team: cut.
  - Argument: Would enter section 7, where the core already has 'Exploring Self-attention for Image Recognition' ('Attention replacing convolution in one backbone with the parameter budget held fixed'). This line ('Attention replacing every convolution in a backbone') pends the same job. Promotion would create a duplicate, so it is not a pending item.
  - Rule cited: redundancy with section 7 Attention; conventions.md section 10
  - Answer: Accepted in substance. Moved to the watchlist with the condition that would promote it.

- **Root Mean Square Layer Normalization** (Watchlist). Red team: cut.
  - Argument: Would enter section 8. It is here for being off topic, not for being unverifiable. The paper, the code and its NLP measurements all exist, so by conventions section 8 it is checkable today. The owner rejected it because no vision measurement exists, which is a relevance judgement, and the watchlist 'is not a quality judgement'. The condition 'a vision benchmark compares it' names no benchmark. A vision engineer ...
  - Rule cited: conventions.md section 8 (the watchlist states what can be checked, not relevance; the condition must be specific)
  - Answer: Accepted. Cut.

- **Depth Pro** (Watchlist). Red team: cut.
  - Argument: Would enter section 12. The section 12 owner rejected it under 'fields contradict each other', and the watchlist line restates that contradiction ('released checkpoint is a retrained model, not the one measured'). Conventions section 7's ladder, applied 'with no appeal', maps 'Fields contradict each other' to Cut, not Watchlist. The editor softened the verdict, and section 7 forbids softening.
  - Rule cited: conventions.md section 7 evidence ladder (contradictory fields are cut); softening is forbidden
  - Answer: Accepted. Cut.

- **AugMix** (Watchlist). Red team: cut.
  - Argument: Would enter section 16. Its promotion condition, 'scored on a corruption family held out from its own design', was met in 2021 by an entry already in the core. The facebookresearch/augmentation-corruption README (fetched) says the paper builds ImageNet-C-bar to be perceptually dissimilar from ImageNet-C. It studies AugMix among others and shows such augmentations 'perform worse on the new dataset'. So a watchlist ...
  - Rule cited: conventions.md section 8 (the condition must be an event still to be observed, and the date is a review date); redundancy with On Interaction Between Augmentations and Corruptions
  - Answer: Accepted. Cut.

### Section 1

- **ShuffleNet V2** (none (numbered list)). Red team: cut.
  - Argument: Item 9 breaks the Start here rule that item k assumes items 1 to k-1 and nothing else. All four of the paper's guidelines are argued in terms of group convolution, channel split and shuffle, and depthwise separable layers, and they are tested against MobileNet, ShuffleNet V1 and Xception. Items 1 to 8 give none of that; it is section 6 material (Efficient convolutional designs). The section 1 owner rejected An ...
  - Rule cited: conventions.md section 3 (Start here: item k assumes only items 1 to k-1); owner-brief.md section 3 (an item needing a later section is disqualified); voice.md section 7 (a repeat needs a different reason)
  - Answer: Accepted in substance. Moved to the watchlist with the condition that would promote it.

- **Visualizing and Understanding Convolutional Networks** (none (numbered list)). Red team: cut.
  - Argument: (a) Conventions section 2 says history earns a place only where modern practice is unreadable without it. Nobody ships deconvnet visualisation or decides anything from it, and the motive in the reason ('shown instead of asserted') is curiosity, not a decision. (b) It breaks the item-k rule. The owner's own Claims block says the paper rests on 'the classification improvement over the earlier convolutional model' ...
  - Rule cited: conventions.md section 2 (history clause); conventions.md section 3 (Start here strict reading order)
  - Answer: Accepted. Cut.

- **A guide to convolution arithmetic for deep learning** (none (numbered list)). Red team: reword.
  - Argument: Section 6 opens with the same URL and the same claim: 'Where padding, stride and output size are worked out instead of guessed.' against Start here's 'Where kernel size, stride, padding and dilation turn into exact output shapes.' The README allows Start here to repeat an entry, but voice section 7 requires the repeat to carry a reason that says something different, and these two say the same thing. Once items 5 ...
  - Rule cited: voice.md section 7 (a repeat must earn a different reason); conventions.md section 11 (why, not what)
  - Answer: Accepted. Reworded.

- **Camera Calibration and 3D Reconstruction** (none (numbered list)). Red team: reword.
  - Argument: The reason is a noun phrase that lists what the page contains ('The projection model and the distortion terms ...'). It does not use any of the three shapes in voice section 1, and conventions section 11 names 'describes contents instead of giving a motive' as the failure a checker cannot catch. The entry itself stays: the 4.13.0 pin is a real release ...
  - Rule cited: voice.md section 1 (the reason is not a summary); conventions.md section 11 (why, not what)
  - Answer: Accepted. Reworded.

### Section 2

- **Recovering High Dynamic Range Radiance Maps from Photographs** (Sensors and noise). Red team: cut.
  - Argument: This is Start here item 1, same URL, and the reason makes the same claim: 'Why pixel values are not radiance until the response curve has been recovered.' against 'Where the curve from scene radiance to stored pixel value is recovered rather than assumed.' Voice section 7 bars a repeat that says nothing different. Owner-brief section 2 says the earlier section keeps a shared source. The section 1 owner's link ...
  - Rule cited: voice.md section 7; owner-brief.md section 2 (earlier section keeps a shared source)
  - Answer: Accepted. Removed from section 2. Start here keeps the source, and the list now holds each source once.

- **Light Field Photography with a Hand-Held Plenoptic Camera** (Optics and projection). Red team: cut.
  - Argument: Would a working engineer open it at this point in the path? Plenoptic capture is not in the camera stacks this path leads to, and nothing in sections 3 to 16 depends on it, so it unlocks nothing downstream (conventions section 1). The engineering lesson the reason gestures at, what aperture and focus do to the image (defocus, depth of field), is taught here through a microlens array the reader will not have. That ...
  - Rule cited: conventions.md section 2 (history clause); conventions.md section 1 (chosen for what it unlocks downstream)
  - Answer: Accepted. Cut.

- **Photographic Tone Reproduction for Digital Images** (The image signal processor). Red team: cut.
  - Argument: This is a display-side tone mapping operator from graphics, not the camera tone curve a vision engineer has to reason about or undo. Its job is already covered in the same subsection: Unprocessing Images for Learned Raw Denoising lists the tone and gamma stages that have to be inverted, and Burst photography shows what a shipped pipeline actually does for local tone mapping. The second half of the reason, 'why a ...
  - Rule cited: conventions.md section 10 (redundant with later entries in the README); voice.md section 1 (the reason claims a source role it does not have)
  - Answer: Accepted. Cut.

- **A Standard Default Color Space for the Internet** (Colour). Red team: reword.
  - Argument: This URL is the 1996 proposal, version 1.10. The host marks it obsolete and keeps it for historical purposes, and the section 2 owner's link notes admit this. The section 1 owner rejected this exact URL under conventions sections 5 and 10, and the README admits it without answering that rejection. The reason 'Where the encoding every pipeline assumes is written down' does not hold for this page: its rounded ...
  - Rule cited: conventions.md section 10 (an entry must resolve to the thing it cited); conventions.md section 5 (the live canonical source); README 'What earns a place' (live canonical copy)
  - Answer: Superseded. The entry was removed.

- **Fast Fourier Color Constancy** (Colour). Red team: reword.
  - Argument: The reason argues for the problem (illuminant estimation) rather than for this source. Any colour constancy paper could carry 'Why the illuminant has to be estimated before any colour transform downstream means anything.' That fails voice section 1's test of why to open this one instead of the next thing. The reason also says the step comes before every other colour transform, yet the entry sits last in Colour ...
  - Rule cited: voice.md section 1 (why open this instead of the next thing)
  - Answer: Accepted. Reworded.

### Section 3

- **A Generic Camera Model and Calibration Method** (Two-view and multi-view geometry). Red team: cut.
  - Argument: Its claim duplicates section 2's The Double Sphere Camera Model: 'What breaks when a wide lens is forced into a pinhole model with radial terms bolted on.' against 'Why a pinhole model breaks on a wide lens and which projection replaces it.' The Double Sphere paper evaluates this model alongside the other wide-lens models, so its job is already done. A single-camera intrinsic model is also not two-view or ...
  - Rule cited: conventions.md section 10 (made redundant by a later entry); conventions.md section 9 (a subsection is a real division, not a bin); voice.md section 1 (two lines making one claim)
  - Answer: Partly accepted. It left two-view geometry, where it did not belong, and moved to section 2 Optics and projection. It stays because its new line does a job the Double Sphere paper does not: it names the fisheye model that calibration toolboxes ship under this name, which a reader meets in code before any comparison of wide-angle models.

- **Scale-space and edge detection using anisotropic diffusion** (Sampling and filtering). Red team: cut.
  - Argument: Nothing downstream in the README depends on it, so it fails the 'chosen for what it unlocks downstream' test. The edge-preserving smoothing engineers actually ship in ISPs and depth refinement is not this partial differential equation scheme, so the entry survives on history (conventions section 2). The motive in the reason, that linear smoothing destroys boundaries, is the problem statement and is visible from ...
  - Rule cited: conventions.md section 2 (history clause); conventions.md section 1 (chosen for what it unlocks downstream)
  - Answer: Accepted. Cut.

- **A Combined Corner and Edge Detector** (Features and correspondence). Red team: keep but weakest.
  - Argument: No rule failure and no redundancy, so there is no case to cut. It is the weakest entry because the next entry gives the detector and descriptor most matching pipelines actually call, and the learned entries replace hand-built detection entirely. It holds its place only because the autocorrelation score survives in corner refinement and in keypoint ranking for binary features, and the path never covers those ...
  - Rule cited: none failed
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Ceres Solver** (Estimation and bundle adjustment). Red team: keep but weakest.
  - Argument: No case to cut: it is maintainer documentation with a written account, not a bare dependency. It is the weakest line in the subsection because its reason, 'What a sparse nonlinear least squares problem looks like once it has to be written down and solved', names neither a mistake prevented nor a question settled. The URL is the documentation home page rather than the modelling and robust-loss pages a reader ...
  - Rule cited: voice.md section 1 (weakest of the three reason shapes)
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

### Section 4

- **ILSVRC** (The datasets that set the terms). Red team: cut.
  - Argument: The section 1 owner rejected this exact URL under conventions section 6 (leaderboards and benchmark trackers). The page is a hub to the yearly challenge pages, results, workshops and an evaluation server. The reason claims 'the access terms that come before any download', but the section 4 owner's own link notes put the terms at image-net.org/download.php, which was deliberately not cited because only its ...
  - Rule cited: conventions.md section 6 (leaderboards); voice.md section 1 (the reason must be true of the source); voice.md section 7 (one subject twice in a subsection)
  - Answer: Accepted. Cut.

- **ImageNet Large Scale Visual Recognition Challenge** (The datasets that set the terms). Red team: cut.
  - Argument: Start here item 6 is the same URL, and its reason already covers the task definition and the scoring rule. The section 4 reason's 'top-five rule' is that same scoring rule. Its other half, 'what that choice throws away', is the job of Start here item 8 and of From ImageNet to Image Classification in the next subsection. That leaves the line no unique job. Owner-brief section 2 says the earlier section keeps a ...
  - Rule cited: owner-brief.md section 2 (earlier section keeps a shared source); voice.md section 7 (prefer not to repeat)
  - Answer: Accepted. Removed from section 4. Start here keeps the source, and the list now holds each source once.

- **Microsoft COCO: Common Objects in Context** (The datasets that set the terms). Red team: reword.
  - Argument: Title only. Voice section 4 says to drop a trailing subtitle after a colon when the first half is unambiguous, and 'Microsoft COCO' is unambiguous here, because the other COCO entries are named cocoeval.py and COCO 2018 Panoptic Segmentation Task API. The reason is fine.
  - Rule cited: voice.md section 4 (titles)
  - Answer: Accepted. Reworded.

- **Are we done with ImageNet?** (Annotation and label noise). Red team: cut.
  - Argument: Start here item 8 is the same URL. The section 4 reason, 'Why relabelling a validation set changes which models look like they improved', makes the same claim as Pervasive Label Errors in Test Sets two lines below it: 'What happens to a benchmark ranking once the test labels themselves are corrected.' Owner-brief section 2 says the earlier section keeps a shared source, and the section 1 owner's collision note ...
  - Rule cited: owner-brief.md section 2; voice.md section 7 (prefer not to repeat); redundancy with Pervasive Label Errors in Test Sets
  - Answer: Accepted. Removed from section 4. Start here keeps the source, and the list now holds each source once.

- **From ImageNet to Image Classification** (Annotation and label noise). Red team: reword.
  - Argument: The reason, 'What human annotators answer when asked the question the benchmark assumes has one answer', repeats Start here item 8's 'What the single label per image assumption hides'. The paper's unique job is something else: it shows how the crowd validation and selection step that built the benchmark decided which images and labels survived. Identifying Statistical Bias in Dataset Replication, in the next ...
  - Rule cited: voice.md section 1 (why open this instead of the next thing); redundancy with Start here item 8
  - Answer: Accepted. Reworded.

- **Identifying Statistical Bias in Dataset Replication** (Splits, leakage and duplication). Red team: keep but weakest.
  - Argument: No case to cut: it is the reply that removes the adaptive-overfitting reading of the entry above it, and the subsection is at the floor of three. It is the weakest entry because it matters only to an engineer who builds a replacement test set, and its argument is a statistical correction resting on a model of annotator selection rather than a procedure the reader runs.
  - Rule cited: none failed
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **The Dataset Nutrition Label** (Documentation and audit). Red team: cut.
  - Argument: Its own reason defines it relative to the entry above ('A shorter documentation format for datasets whose full datasheet will never be written'). That describes a format, which is contents, and gives no motive to open it once Datasheets for Datasets is in hand. It is not specific to vision, no later entry in the README uses it, and a working engineer at section 4 gains nothing from it that Datasheets does not ...
  - Rule cited: conventions.md section 11 (why, not what); voice.md section 1; redundancy with Datasheets for Datasets
  - Answer: Accepted. Cut.

- **Lessons from Archives** (Documentation and audit). Red team: cut.
  - Argument: The reason names a profession ('curating and documenting a collection already exists as a profession'). It does not name a source role, a mistake prevented or a question settled. The paper argues for adopting archival practice at an institutional level and gives an engineer no procedure that Datasheets for Datasets does not. A working engineer would not open it at this point in the path. Consequence the editor ...
  - Rule cited: voice.md section 1 (the three reason shapes); conventions.md section 1 (chosen for what it unlocks downstream)
  - Answer: Accepted. Cut.

### Section 5

- **LVIS: A Dataset for Large Vocabulary Instance Segmentation** (Protocols and reporting). Red team: cut.
  - Argument: This is the same paper section 4 already carries as [LVIS](https://openaccess.thecvf.com/content_CVPR_2019/html/Gupta_LVIS_A_Dataset_for_Large_Vocabulary_Instance_Segmentation_CVPR_2019_paper.html). Only the URL differs. The README's own admission rule says Start here may repeat an entry and no other section may. Owner-brief section 2 says the earlier section keeps a shared source, and the section 4 draft's link ...
  - Rule cited: README 'What earns a place': no section except Start here may repeat an entry; owner-brief section 2 (earlier section keeps); conventions section 5 (prefer the conference page over arXiv)
  - Answer: Accepted. Cut.

- **Boundary IoU API** (Segmentation and dense metrics). Red team: cut.
  - Argument: The paper one line above already does this job. The other paper-plus-code pairs in this section earn their second line by naming a detail that only the code settles. cocoeval.py fixes recall sampling and the detection cap, and panopticapi fixes void and crowd handling. This line names no such detail. 'What moves in the reported score when ... swaps mask overlap for boundary overlap' is the paper's experimental ...
  - Rule cited: conventions section 10 (a later entry makes it redundant) and section 11 'why not what'; voice section 1 (name the thing it is the source of)
  - Answer: Accepted. Cut.

- **A Metric Learning Reality Check** (How a metric misleads). Red team: cut.
  - Argument: It is cited from a subfield that appears nowhere else in the path. Deep metric learning, retrieval embeddings, Recall@K and MAP@R are never introduced, so a reader at section 5 has no context for its tables. Its stated job, that reported gains vanish once the protocol is held fixed, is already done in this README by Accounting for Variance in Machine Learning Benchmarks (section 5), by ResNet strikes back and Bag ...
  - Rule cited: conventions section 1 (a path, not a library) and section 10 (redundant); the 'would a working engineer at this point open it' test
  - Answer: Accepted. Cut.

- **The PASCAL Visual Object Classes Challenge 2012 Development Kit** (What the detection metrics compute). Red team: reword.
  - Argument: The reason line misnames the change it is cited for. The VOC2007 rule already averages the interpolated precision, which is the monotone envelope, at eleven sampled recall levels. The VOC2010 to 2012 rule takes the exact area under that same envelope at every unique recall. So interpolation was never 'replaced by the precision envelope area'. Only the sampling changed. The section 5 draft's own benchmark proposal ...
  - Rule cited: voice section 1 (the reason must name what the source is the source of, and accurately); conventions section 11 'why not what'
  - Answer: Accepted. Reworded.

- **The PASCAL Visual Object Classes Challenge 2012 Development Kit** (What the detection metrics compute). Red team: keep but weakest.
  - Argument: There is no case to cut in this subsection. This is still its weakest entry. cocoeval.py and the VOC2007 kit already carry the 'same name, different number' lesson between them, and the all-point rule is restated by Open Images evaluation protocols in the next subsection. It survives because it is the only primary definition of all-point AP, and the section's own benchmark measures it as the third protocol. It ...
  - Rule cited: weakest entry in a subsection with no case to cut
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Diagnosing Error in Object Detectors** (How a metric misleads). Red team: keep but weakest.
  - Argument: This is the next entry to cut. TIDE, the next line, uses the same error taxonomy, runs on COCO, LVIS and VOC output files through maintained code, and isolates each error type's contribution where Hoiem's analysis on the VOC2007 protocol could not. The reason line is a priority credit ('first broken into'), not a motive to open the page. It survives only because conventions section 10 protects a superseded paper ...
  - Rule cited: conventions section 2 (history earns a place only where modern practice is unreadable without it) and section 10 (redundant versus superseded)
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

### Section 6

- **A guide to convolution arithmetic for deep learning** (Foundations). Red team: cut.
  - Argument: Same URL as Start here item 4, with the same claim. Start here reads 'Where kernel size, stride, padding and dilation turn into exact output shapes.' This line reads 'Where padding, stride and output size are worked out instead of guessed.' That is a strict subset of the first. Voice section 7 allows a cross-section repeat only when the second line says something different, and this one does not. Owner-brief ...
  - Rule cited: voice section 7 (a repeat must earn a different reason line); owner-brief section 2; conventions section 10 (redundant)
  - Answer: Accepted. Removed from section 6. Start here keeps the source, and the list now holds each source once.

- **Network In Network** (Foundations). Red team: cut.
  - Argument: The reason is a credit line ('were argued for'), not a motive. Both ideas it credits reach the reader through later entries. Going Deeper with Convolutions, two lines down, uses the one by one reduction and the globally pooled head and explains both in its own text. Deep Residual Learning uses the pooled head again. Nobody ships NIN, and modern practice is readable without it, so conventions section 2 removes the ...
  - Rule cited: conventions section 2 (history only where modern practice is unreadable without it); voice section 1
  - Answer: Accepted. Cut.

- **ImageNet Classification with Deep Convolutional Neural Networks** (Foundations). Red team: reword.
  - Argument: The second half of the reason, 'how much of that was recipe rather than layers', promises an answer this paper does not give. The owner's own Claims note says the recipe and layer contributions were confounded here, and that separating them is what Bag of Tricks and ResNet strikes back in the same section are for. Kept as written, the line sends the reader to the wrong source for the question. Reword, don't cut: ...
  - Rule cited: voice section 1 (name the question it settles, not one it raises); conventions section 11 'why not what'
  - Answer: Accepted. Reworded.

- **ShuffleNet V2** (Efficient convolutional designs). Red team: cut.
  - Argument: Same URL as Start here item 9, with the same claim. Start here says counted operations do not predict latency. This line says fewer FLOPs can measure slower on device. Voice section 7 needs a different reason for a repeat, and the section 1 draft's link notes flag this exact paper against section 6 under owner-brief section 2: 'Section 1 keeps all five, so each of those owners picks something else'. No later ...
  - Rule cited: voice section 7; owner-brief section 2 (flagged by the section 1 owner); conventions section 10
  - Answer: Accepted in substance. Moved to the watchlist with the condition that would promote it.

- **Xception** (Efficient convolutional designs). Red team: keep but weakest.
  - Argument: This is the weakest surviving entry. Its reason is lineage history ('replaced the mixed branch block it came from'). An engineer opens MobileNets, the next line, to learn what a depthwise separable layer costs, and that paper derives the cost from scratch. Xception survives only as the bridge from the Inception module, and that bridge matters only while Going Deeper with Convolutions stays in Foundations. It also ...
  - Rule cited: conventions section 2 (history); conventions section 3 (least prior context first)
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Squeeze-and-Excitation Networks** (Depth, residuals and width). Red team: reword.
  - Argument: The reason is an adoption verdict ('ended up inside most of the later efficient designs'), which is the praise-through-verbs failure conventions section 11 names. Measured against this README it is also false. Of the five core efficient designs, only EfficientNet uses the block. Xception, MobileNets and MobileNetV2 do not, ShuffleNet V2 has it only as an optional variant, and MobileNetV3 is on the watchlist. The ...
  - Rule cited: conventions section 11 (praise leaks through verbs); voice section 1 (not a verdict)
  - Answer: Accepted. Reworded.

- **Wide Residual Networks** (Depth, residuals and width). Red team: keep but weakest.
  - Argument: This is the weakest entry here. The owner's own Claims note concedes that the decisive depth-against-width comparisons are on small-image datasets under a recipe unlike large-scale practice, 'so the ordering of depth against width does not transfer unexamined'. So the question the reason line promises to settle is not settled for this path's reader. EfficientNet asks the same question at the benchmark scale. It ...
  - Rule cited: conventions section 7 (the entry's question is not settled for the reader's setting); redundancy with EfficientNet
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Revisiting ResNets** (Recipes against architectures). Red team: cut.
  - Argument: The reason, 'when only the recipe and the scaling rule move', is contradicted by the paper's own abstract, which describes the model family as modern training methods plus 'minor architectural changes' plus new scaling strategies. The architecture moved too, so the entry cannot separate recipe from architecture, and that separation is this subsection's only purpose. ResNet strikes back, the next line, does the ...
  - Rule cited: conventions section 10 (redundant); conventions section 7 (an unaudited claim the entry implicitly rests on); voice section 1 (an accurate reason)
  - Answer: Accepted. Cut.

- **A ConvNet for the 2020s** (Recipes against architectures). Red team: reorder.
  - Argument: The paper is a step-by-step 'modernisation' of a ResNet toward Swin Transformer. Every step (patchify stem, stage ratios, inverted bottleneck, large depthwise kernels, layer normalisation) is justified by reference to Swin, and the baseline recipe is the transformer recipe (AdamW, mixup, CutMix, RandAugment, stochastic depth, label smoothing). Swin is in section 7 and the recipe parts are in section 8. A reader ...
  - Rule cited: conventions section 3 (section N must assume nothing after it: 'has to', not 'would benefit from')
  - Answer: Accepted. Moved, and the line reworded.

### Section 7

- **Neural Machine Translation by Jointly Learning to Align and Translate** (Attention). Red team: cut.
  - Argument: The reason is pure history ('Where attention begins as ...'). No later entry in sections 7 to 16 uses additive alignment over recurrent states. The next line, Attention Is All You Need, defines the operator every vision transformer in this README uses, and it is readable without this paper. Conventions section 2 admits history only where modern practice is unreadable without it, and that is not the case here. The ...
  - Rule cited: conventions section 2 (history only where modern practice is unreadable without it)
  - Answer: Accepted. Cut.

- **Exploring Self-attention for Image Recognition** (Attention). Red team: cut.
  - Argument: Five separate failures. (1) The title is the paper's but the URL is a repository, and the entry's claim is the paper's. The link note says the arXiv identifier could not be confirmed, but it is 2004.13621 and the paper also sits on the CVF open access site, so conventions section 5 points at the paper. (2) The reason is a content fragment, 'Attention replacing convolution ...', which conventions section 11 'why ...
  - Rule cited: conventions section 5 (primary source, the paper's own page); conventions section 7 and 8 (an unaudited comparison the entry rests on); conventions section 11 'why not what'; redundancy with the watchlist line
  - Answer: Accepted. Cut.

- **Do Vision Transformers See Like Convolutional Neural Networks?** (Vision transformers). Red team: cut.
  - Argument: This is a representation-similarity analysis, and no engineering decision follows from reading it. Its central findings come from models pretrained on a private corpus, the same ground the README uses to send AIM to the watchlist ('a corpus nobody else holds'). The draft has no Claims entry for it. The reason line says where the differences sit, which is a description of contents, not why to open it. A working ...
  - Rule cited: conventions section 7 ladder (data nobody else has); conventions section 11 'why not what'; would an engineer open it
  - Answer: Accepted. Cut.

- **An Image is Worth 16x16 Words** (Vision transformers). Red team: reword.
  - Argument: 'Nothing convolutional is left' is contradicted two entries later. Early Convolutions Help Transformers See Better rests on the point that the patchify stem is a stride-p convolution with a p-by-p kernel, and every framework implements it that way. As written, the README contradicts itself inside one subsection. The motive should be the patch-sequence formulation, not a claim about convolution that does not hold.
  - Rule cited: voice section 1 (the reason must be true of the source); internal consistency of the README
  - Answer: Accepted. Reworded.

- **Scaling Vision Transformers** (Data, scale and distillation). Red team: cut.
  - Argument: The reason, 'What the error rate does as corpus and model grow', rests entirely on scaling numbers trained on a private three-billion-image corpus. The authors' big_vision README lists only a training config for this paper and no checkpoint (checked on raw.githubusercontent.com). So no outsider can check the measurement, which fails the third core condition in conventions section 8. Under the section 7 ladder, a ...
  - Rule cited: conventions section 7 ladder (reproducible only by the authors); conventions section 8 (core needs a public measurement); consistency with the AIM watchlist line
  - Answer: Accepted. Cut.

- **Better plain ViT baselines for ImageNet-1k** (Data, scale and distillation). Red team: reword.
  - Argument: This entry carries the only claim in section 7 the audit marked 'stands', so it stays. Its line, though, describes contents ('names its epoch count and its hardware') and makes an unfalsifiable claim about other work ('which most comparisons leave implicit'). The reason to open it is the question it settles: a plain transformer reaching a residual baseline on the public corpus in a short stated schedule. The ...
  - Rule cited: conventions section 11 'why not what'; voice section 1 (name the question it settles)
  - Answer: Accepted. Reworded.

- **CoAtNet** (Hierarchies and hybrids). Red team: cut.
  - Argument: No official code or weights were ever released. timm's from-scratch implementation says so in its header: 'without any official pretrained weights it's difficult to confirm a 100% match'. That contradicts the draft's Claims field 'model and exact checkpoint for the public corpus arms'. The reason, 'as the pretraining corpus grows', rests on the largest arm, whose corpus is private. The owner's own note says the ...
  - Rule cited: conventions section 7 ladder (field missing, entry rests on the number: watchlist); conventions section 8 (shipped implementation and public measurement)
  - Answer: Accepted in substance. Moved to the watchlist with the condition that would promote it.

- **Pyramid Vision Transformer** (Hierarchies and hybrids). Red team: keep but weakest.
  - Argument: This is the weakest surviving entry. Swin Transformer, the next line, gives the same hierarchical backbone and is the one detection codebases ship. PVT's reason ('dense prediction needs a feature pyramid') leans on feature pyramid networks and dense heads, which the path introduces only in section 10. It survives because cutting it as well as CoAtNet would drop the subsection below three, and because ...
  - Rule cited: redundancy with Swin Transformer; mild forward dependency on section 10 under conventions section 3
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

### Section 8

- **Generalized Intersection over Union** (Objectives). Red team: reorder.
  - Argument: Both the section 5 and section 8 drafts carried this entry. Owner-brief section 2 says the earlier section keeps it, and section 5 is earlier. In section 5 it sits next to the IoU definitions it generalises and needs nothing else, so the point is about the metric: overlap gives no ordering for disjoint boxes. In section 8 it is a box-regression loss read before any detector exists, since detectors arrive in ...
  - Rule cited: owner-brief section 2 (earlier section keeps); conventions section 3 (dependency order)
  - Answer: Accepted. Moved, and the line reworded.

- **The Lovász-Softmax loss** (Objectives). Red team: keep but weakest.
  - Argument: This is the weakest entry in Objectives. It is a segmentation-specific loss read before segmentation appears in section 10. Its theoretical justification is corrected by the owner's own rejected entry, IoU is not submodular. It rarely appears in the recipes this README cites. It survives because the subsection would otherwise fall below three, and because it is the only entry that sets optimising the metric ...
  - Rule cited: weakest entry; mild forward dependency on section 10
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **TrivialAugment** (Augmentation). Red team: cut.
  - Argument: Three of five lines in this subsection settle one question: whether a policy search is worth running. RandAugment asks 'Whether the policy search was buying anything a single strength setting cannot', and TrivialAugment asks 'Whether searched augmentation policies survive a baseline that picks one operation at random'. The owner's Claims notes rest both on the same structural equal-cost argument. RandAugment is ...
  - Rule cited: conventions section 10 (a later or adjacent entry makes it redundant); conventions section 1 (a path, not a library)
  - Answer: Accepted. Cut.

- **Image classification reference training scripts** (Schedules and optimisation). Red team: reword.
  - Argument: The line preaches a lesson ('Why a recipe comparison means nothing until every flag ... is written down') that the page never argues. The page is a log of commands. That lesson is already the job of ResNet strikes back (section 6) and Better plain ViT baselines (section 7). What this page is the source of is the exact flags behind each torchvision checkpoint: the step schedule against the cosine and warmup ...
  - Rule cited: voice section 1 (name the thing it is the source of); conventions section 11 'why not what'
  - Answer: Accepted. Reworded.

- **SGDR: Stochastic Gradient Descent with Warm Restarts** (Schedules and optimisation). Red team: keep but weakest.
  - Argument: This is the weakest entry in Schedules, with no case to cut. Its own mechanism, warm restarts, is not what the cited recipes use. They use one cosine cycle with warmup. The owner's Claims note records that its schedule comparison was not budget-matched. It survives as the citable definition of the cosine curve that the torchvision flags name.
  - Rule cited: weakest entry in a subsection with no case to cut
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Improving neural networks by preventing co-adaptation** (Regularisation and normalisation). Red team: cut.
  - Argument: The reason is a history credit ('Where dropping units at random was introduced'). The modern recipes in this README turn dropout off. DeiT trains with dropout at zero, and the torchvision ResNet and ViT commands set no dropout. What they regularise with is stochastic depth, which the README never gives. A reader has already met dropout as part of the recipe in section 6's ImageNet Classification entry. Under ...
  - Rule cited: conventions section 2 (history); conventions section 9 (displacement: a slot spent on a technique the cited recipes switch off)
  - Answer: Accepted. Cut.

- **Batch Normalization** (Regularisation and normalisation). Red team: reword.
  - Argument: 'Became the default everywhere' is an adoption verdict, the praise-through-verbs failure conventions section 11 names. The paper also cannot say why it was adopted, since its own internal-covariate-shift motive is the part later work disputed. The reason to open it is the specified train and test behaviour of a batch-dependent layer, including the running averages, which is what Group Normalization and Rethinking ...
  - Rule cited: conventions section 11 (praise); voice section 1 (not a verdict)
  - Answer: Accepted. Reworded.

- **Rethinking "Batch" in BatchNorm** (Regularisation and normalisation). Red team: reword.
  - Argument: 'The failure modes that follow from ...' describes contents: the paper has failure modes in it. It gives no motive. Voice section 1 asks for the mistake it prevents, and the mistake is shipping a model that validated with one set of batch statistics and runs with another. Keep the entry and fix the line.
  - Rule cited: conventions section 11 'why not what'; voice section 1 (name the mistake it prevents)
  - Answer: Accepted. Reworded.

### Section 9

- **Representation Learning with Contrastive Predictive Coding** (Contrastive learning). Red team: cut.
  - Argument: The reason claims the objective is reused by 'almost every later pretext task', and section 9 itself shows that is false. Of the later section 9 entries only SimCLR and MoCo reuse InfoNCE. BYOL, SimSiam, Barlow Twins, DINO, BEiT, MAE, DINOv2 and DINOv3 do not. Without that claim, all the line offers is provenance ('first written down'), and history earns a place only where modern practice is unreadable without ...
  - Rule cited: conventions.md s2 (history only where modern practice is unreadable without it); voice.md s1 (the reason must name what the source is actually the source of, and this claim is false inside the section); conventions.md s10 (redundant with SimCLR and MoCo for the loss definition)
  - Answer: Rejected, and the reason rewritten. The popularity claim was false and is gone. The entry stays because it is where the InfoNCE objective is written down, and SimCLR, MoCo and CLIP all train with it later in the path.

- **Alignment and Uniformity on the Hypersphere** (Contrastive learning). Red team: reword.
  - Argument: The reason starts with a verb that describes what the paper does ('Separates ... and makes ...'). That is a contents summary, not a motive to open it, the 'Describes contents' row of the voice.md s1 table. What an engineer actually takes from it is a pair of label-free embedding diagnostics. That overlaps 'Understanding Dimensional Collapse in Contrastive Self-supervised Learning' in Evaluating representations ...
  - Rule cited: voice.md s1 and conventions.md s11 (why, not what); voice.md s4 (trim titles from the right); conventions.md s10 (redundant with Dimensional Collapse)
  - Answer: Accepted. Reworded.

- **Barlow Twins** (Self-distillation and masked modelling). Red team: cut.
  - Argument: The subsection is full at six. Barlow Twins is neither self-distillation (no teacher) nor masked modelling (no masking), so it sits in a subsection whose name does not cover it. The reason is a method summary ('Avoiding collapse by decorrelating ...'), which describes contents. The collapse lesson is already delivered by BYOL (whether negatives are needed), SimSiam (which single operation prevents collapse) and ...
  - Rule cited: voice.md s1 (why, not what); conventions.md s9 (a subsection is a real division of the subject, not a bin); conventions.md s10 (made redundant by BYOL, SimSiam, DINO and Dimensional Collapse)
  - Answer: Accepted. Cut.

- **BEiT: BERT Pre-Training of Image Transformers** (Self-distillation and masked modelling). Red team: reword.
  - Argument: The entry itself is defensible, since MAE reads as a reply to it, but the title breaks a rule. 'BEiT' is unambiguous in the README, so the subtitle after the colon should go. The editor applies this trim elsewhere (FCOS, Mask2Former, YOLOv10, RAFT), so leaving it here is inconsistent.
  - Rule cited: voice.md s4 (drop a trailing subtitle after a colon when the first half is unambiguous)
  - Answer: Accepted. Retitled to BEiT.

- **Model Card for DINOv2** (Vision foundation models and weights). Red team: reword.
  - Argument: The reason line misstates the card. I read it in full from raw.githubusercontent.com on main, and it gives one licence, 'Apache License 2.0', for all eight checkpoints, so 'Which checkpoint carries which licence' has nothing to point at. 'Which probe produced each frozen feature number' is half true. The table names probe types (k-NN, linear, linear 4 layers, multiscale, nearest neighbor), but the card says 'We ...
  - Rule cited: voice.md s1 (the reason must be true of the source and name what it is the source of); conventions.md s7 (the line implies a protocol the card does not carry)
  - Answer: Accepted. Reworded.

- **DINOv3** (Vision foundation models and weights). Red team: keep but weakest.
  - Argument: Weakest entry, with no case to cut. The subsection is four entries on one model family from one lab. The paper's lesson (dense patch features decay over a long schedule, and Gram anchoring holds them) is a training-dynamics result for whoever trains at seven-billion-parameter scale. An engineer at this point loads a checkpoint, and the DINOv3 card already gives the licence, the satellite weights, the token counts ...
  - Rule cited: would a working engineer at this point open it; partial overlap with Model Card for DINOv3
  - Answer: Noted. The evidence marshal moved it to the watchlist.

- **Revisiting Self-Supervised Visual Representation Learning** (Evaluating representations). Red team: cut.
  - Argument: The pretext tasks whose ranking it measures (rotation, exemplar, jigsaw, relative patch location) appear nowhere in the README, so a reader cannot interpret 'how far the ranking of pretext tasks moves'. It needs context the path never supplies. Those tasks are obsolete, so this is history that no current practice depends on. Its general lesson, that a representation ranking is an artefact of backbone and ...
  - Rule cited: conventions.md s2 (history without a modern practice that needs it); conventions.md s10 (redundant with three entries in the same subsection); conventions.md s3 (assumes context the path never gives)
  - Answer: Accepted. Cut.

- **A Large-scale Study of Representation Learning with the Visual Task Adaptation Benchmark** (Evaluating representations). Red team: reword.
  - Argument: Title only. At 88 characters it is the longest title in batch C, against a 60-character soft ceiling. voice.md s4 says to keep the community name where that is what people search for (the YOLOv3 precedent), and the community name is VTAB. The owner's justification (trimming from the right removes the searchable phrase) is an argument for the community name, not for the full title. The same inconsistency affects ...
  - Rule cited: voice.md s4 (sixty-character soft ceiling, prefer the community name when it is the searchable one)
  - Answer: Accepted. Reworded.

### Section 10

- **Cascade R-CNN** (Detector families). Red team: keep but weakest.
  - Argument: Weakest entry, with no case to cut. It is the least likely of the four to be opened by an engineer shipping a latency-bound detector, because multi-stage refinement rarely ships. The threshold mismatch it addresses is partly visible already through section 5's cocoeval.py, where AP is averaged over overlap thresholds. It survives because its reason names a concrete failure that section 5 does not explain: a ...
  - Rule cited: would a working engineer at this point open it
  - Answer: Noted as the weakest in its subsection. Kept as written.

- **Deformable DETR** (Set prediction and anchor-free designs). Red team: keep but weakest.
  - Argument: Weakest entry, with no case to cut. 'A schedule a team can afford' is a vague stake, and it does not name the mechanism every later DETR-family detector inherits: sparse attention to a few sampled points around reference points, across scales. It survives because without it DETR reads as untrainable at a practical budget. The reason should name the mechanism.
  - Rule cited: voice.md s2 (vague stakes, by convention); voice.md s1 (name the thing it is the source of)
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Fully Convolutional Networks for Semantic Segmentation** (Segmentation). Red team: cut.
  - Argument: The reason is a history claim ('first became'), and history earns a place only where modern practice is unreadable without it. The next entry, U-Net, is a self-contained account of a fully convolutional encoder-decoder with skip connections, and it is the one that ships in medical and industrial segmentation. Mask R-CNN's mask head and Mask2Former's per-pixel decoder are both readable without FCN. Counterargument ...
  - Rule cited: conventions.md s2 (history only where modern practice is unreadable without it); conventions.md s10 (U-Net does its job for an engineer)
  - Answer: Accepted. Cut.

- **Segment Anything** (Segmentation). Red team: reword.
  - Argument: 'What a mask model can do when ...' is a capability showcase that describes contents rather than giving a reason to open it. Adopters get two facts wrong: the masks carry no class, and one ambiguous point prompt returns several candidate masks with predicted quality scores to choose from. The line should name that mistake.
  - Rule cited: voice.md s1 (name the mistake it prevents, not what it contains); conventions.md s11 (why, not what)
  - Answer: Accepted. Reworded.

- **NonMaxSuppression** (Postprocessing and what ships). Red team: reword.
  - Argument: I read the operator text from docs/Operators.md on main via raw.githubusercontent.com. It specifies three things: boxes under score_threshold are removed; a box is suppressed only when its IoU is strictly greater than iou_threshold, so a box exactly at the threshold is kept; and center_point_box selects corner [y1,x1,y2,x2] or centre [x_center,y_center,width,height] layout. It says nothing about ordering among ...
  - Rule cited: voice.md s1 (the reason must be true of the source); README 'What earns a place' (no repeated entry outside Start here); owner-brief.md s2 (the earlier section keeps a shared source)
  - Answer: Accepted. Reworded.

- **Detectron2** (Postprocessing and what ships). Red team: reword.
  - Argument: Weakest entry in the subsection. It is cited at the repository root. Its README (read via raw) is a library landing page with marketing lines ('state-of-the-art detection and segmentation algorithms', 'trains much faster') and no paper: the citation is a @misc pointing back at the repository. That is the same vendor-content objection the owner used to reject Ultralytics, and a repository root with no written ...
  - Rule cited: conventions.md s6 (a repository with no written account is a dependency, not a reading; vendor content); conventions.md s11 (why, not what: the root page does not show what the reason promises)
  - Answer: Accepted. Reworded.

### Section 11

- **RAFT** (Temporal modelling). Red team: reword.
  - Argument: The reason says RAFT estimates 'the motion field that a flow-fed temporal model consumes', but no entry in the README consumes it. Quo Vadis' flow stream uses a classical TV-L1 estimator, and R(2+1)D, TSM and SlowFast are RGB-only, so the reason invents a dependency. As the first entry it should need the least context, yet it assumes the optical flow problem, brightness constancy and correlation cost volumes. The ...
  - Rule cited: voice.md s1 (the reason must be true); conventions.md s3 (first entry needs the least context; no look-forward)
  - Answer: Accepted. Reworded.

- **TSM: Temporal Shift Module for Efficient Video Understanding** (Temporal modelling). Red team: reword.
  - Argument: Title rule: 'TSM' is unambiguous in the README, so the subtitle after the colon should go. The title also sits exactly on the 60-character ceiling. Separately, TSM is built on and evaluated against TSN, which the reader only meets in the next subsection (see order problems).
  - Rule cited: voice.md s4 (drop a trailing subtitle after a colon when the first half is unambiguous)
  - Answer: Accepted. Reworded.

- **A Closer Look at Spatiotemporal Convolutions** (Temporal modelling). Red team: keep but weakest.
  - Argument: Weakest entry, with no case to cut. It overlaps TSM, since both answer what temporal modelling has to cost: factorise the space-time filter, or shift channels. Of the two, whether the filter is solid or factorised is the design point an engineer is least likely to revisit. It survives because it defines the video backbones engineers actually load from torchvision (r3d, mc3, r2plus1d).
  - Rule cited: conventions.md s10 (partial overlap with TSM); would a working engineer at this point open it
  - Answer: Noted as the weakest in its subsection. Kept as written.

- **UCF101** (Video datasets and their protocols). Red team: cut.
  - Argument: The reason calls its own value history: 'the split protocol behind the older action recognition numbers'. History is admitted only where modern practice is unreadable without it, and nothing later in the README depends on UCF101, because Kinetics, Something-Something and the model zoo carry the current protocols. The owner records HMDB51, the other half of the classic pair, as missing, so that protocol is only ...
  - Rule cited: conventions.md s2 (no inclusion for historical importance alone); voice.md s1 (name the mistake it prevents)
  - Answer: Accepted. Cut.

- **Tracking without bells and whistles** (Tracking). Red team: keep but weakest.
  - Argument: Weakest entry, with no case to cut. Its reason (how much of a tracking score belongs to the detector) is the same confound that MOT16's public detection protocol exists to control and that HOTA splits into detection and association terms, so three entries carry one confound. The sharpest form of the lesson, the admission that later gains came from a retrained detector with no change to the tracker, is in the ...
  - Rule cited: conventions.md s10 (partial overlap with MOT16 and HOTA)
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking** (Tracking metrics). Red team: keep but weakest.
  - Argument: Weakest entry, with no case to cut. Half of this source is the DukeMTMC multi-camera dataset, which its maintainers withdrew in 2019 over consent concerns, the same kind of failure section 4's 'Large image datasets: A pyrrhic win' audits. A reader who follows the title's 'a Data Set' finds nothing to download. (The withdrawal is from my own knowledge; it was not checked from this container.) IDF1 itself is ...
  - Rule cited: conventions.md s10 (part of the cited artefact withdrawn); voice.md s4 (title length)
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

### Section 12

- **Pyramid Stereo Matching Network** (Depth and stereo). Red team: cut.
  - Argument: The owner's own Link notes name this as the entry the stereo taxonomy would displace. Its reason ('What a cost volume looks like once the whole stereo pipeline is trained end to end') describes contents, and this paper is not the source of what it names. End-to-end regression over a 3D cost volume came first in GC-Net (arXiv 1703.04309). PSMNet's own contribution is pyramid pooling and stacked hourglass ...
  - Rule cited: voice.md s1 (name what it is the source of; why, not what); owner's own displacement note in misc/notes/sections/12-3d.md Link notes
  - Answer: Accepted. Cut.

- **COLMAP** (Structure from motion). Red team: reword.
  - Argument: 'Most reconstruction work still calibrates against' is a popularity claim that cannot be falsified. It is the enthusiasm-through-verbs leak that conventions.md s11 warns about, and the banned 'popular' and 'influential' in all but name. 'Calibrates against before anything else runs' is also ambiguous: camera calibration, or a benchmark baseline? Keep the repository, since it is the artefact people run, and its ...
  - Rule cited: voice.md s2 (praise and popularity vocabulary); conventions.md s11 (praise leaking through verbs)
  - Answer: Accepted. Reworded.

- **OpenMVG** (Structure from motion). Red team: cut.
  - Argument: Its job, global pose averaging as separate steps, is the job of 'Global Structure-from-Motion Revisited', whose reason is about solving rotation and translation separately. That pipeline now ships inside COLMAP: the COLMAP README asks users of 'the global SfM pipeline (GLOMAP)' to cite it, and the owner notes the glomap repository redirects there. So the tool readers already run, plus the paper, covers both ...
  - Rule cited: conventions.md s10 (redundant with the GLOMAP paper and the COLMAP repository); conventions.md s6 (code without the paper the claim depends on)
  - Answer: Accepted. Cut.

- **ORB-SLAM3** (Simultaneous localisation and mapping). Red team: reword.
  - Argument: 'The feature based system most robotics stacks still start from' is a popularity claim that cannot be falsified, and 'with the map handling made explicit' is vague. The distinctive lesson is the multi-map system: when tracking is lost it starts a new map and merges it back on revisit, plus visual-inertial initialisation. The reason should name that. Its position as first entry is also questionable, because it ...
  - Rule cited: voice.md s2 (popularity vocabulary); conventions.md s11 (praise through verbs); voice.md s1 (name the mistake it prevents)
  - Answer: Accepted. Reworded.

- **LSD-SLAM** (Simultaneous localisation and mapping). Red team: cut.
  - Argument: It is cited as a repository for a method claim ('what tracking looks like when image intensities replace keypoints'), and the paper is not linked. The README (read via raw) names the ECCV paper without a link, says it was tested on Ubuntu 12.04 with ROS fuerte and Ubuntu 14.04 with ROS indigo, and says 'building without ROS is not supported'. Both platforms are long end-of-life, so this is neither a reading nor ...
  - Rule cited: conventions.md s6 (code without the paper the claim depends on); conventions.md s10 (deprecated tooling; redundant with Direct Sparse Odometry)
  - Answer: Accepted. Cut.

- **Instant Neural Graphics Primitives** (Radiance fields and splatting). Red team: reword.
  - Argument: 'Removes most of the training cost' restates the training-time claim that the owner's own Claims block recorded as unverified. Precision, batch size, framework and the reported statistic are missing, and the timer starts after poses exist, which costs more than the training being advertised. The ladder says a recorded-unverified number is never repeated, and a quantity written in words is still the claim. The ...
  - Rule cited: conventions.md s7 (a recorded-unverified number is never repeated); conventions.md s4 (no numbers in reasons, in spirit); conventions.md s5 (prefer the authors' canonical copy)
  - Answer: Accepted. Reworded.

- **MultiNeRF** (Radiance fields and splatting). Red team: cut.
  - Argument: This is one code release covering three papers (Mip-NeRF 360, Ref-NeRF, RawNeRF). Its own README says 'This is not an officially supported Google product' and 'This is research code'. It is cited for ideas from mip-NeRF 360 (unbounded scenes) and mip-NeRF (anti-aliasing), and neither paper is linked, so the claim depends on the missing half. A reader lands on JAX install instructions. For an engineer heading to ...
  - Rule cited: conventions.md s6 (code without the paper the claim depends on); conventions.md s5 (cite the paper when the claim is a method claim)
  - Answer: Accepted. Cut.

### Section 13

- **Deep Unsupervised Learning using Nonequilibrium Thermodynamics** (Diffusion foundations). Red team: cut.
  - Argument: The reason is a priority claim: 'first written down'. That is a fact about history, not a reason to open it. Denoising Diffusion Probabilistic Models, two lines below, restates the forward process, the reverse process and the variational bound in its own background section. Every later entry in the README is written against that version, and nothing downstream needs the thermodynamic framing. Conventions section ...
  - Rule cited: conventions.md section 2 (history earns a place only where modern practice is unreadable without it); section 3 (first entry needs least context); voice.md section 1 (motive, not provenance)
  - Answer: Accepted. Cut.

- **Denoising Diffusion Probabilistic Models** (Diffusion foundations). Red team: reword.
  - Argument: Keep the entry and fix the reason. 'The noise prediction objective that almost every later system trains against' is an unsupported claim of popularity, and this section contradicts it. The straight path entry in this same subsection trains a velocity, and so do Scaling Rectified Flow Transformers and FLUX in Latent and text conditioned systems. Elucidating the Design Space trains a preconditioned denoiser. A ...
  - Rule cited: voice.md section 2 (vague stakes and unfalsifiable claims) and conventions.md section 3 (importance is not a reason); internal contradiction with later entries
  - Answer: Accepted. Reworded.

- **Flow Matching Guide and Code** (Diffusion foundations). Red team: cut.
  - Argument: This is a book-length tutorial by the flow matching group that restates their earlier paper, so it is course material standing in for a paper. The owner's link notes say it was admitted only because the original paper's identifier could not be confirmed, which is a verification gap, not a reason to admit a restatement. A primary paper that does exactly the job of the reason line ('the path from noise to data is a ...
  - Rule cited: conventions.md section 5 book carve-out (admissible only where no paper plays its role); section 6 (course notes that restate a paper)
  - Answer: Accepted. Cut.

- **Diffusion Models Beat GANs on Image Synthesis** (Samplers and guidance). Red team: cut.
  - Argument: The reason is about classifier guidance, which needs a separate classifier trained on noisy images and is not used by any system in this section. 'Was first paid for in diversity' is a priority claim. The next entry, Classifier-Free Diffusion Guidance, re-derives classifier guidance in its own background, and its reason ('what it trades away') carries the same fidelity-against-diversity lesson. That is two lines ...
  - Rule cited: conventions.md section 2 (history only where modern practice is unreadable without it); redundancy with Classifier-Free Diffusion Guidance
  - Answer: Accepted. Cut.

- **Elucidating the Design Space of Diffusion-Based Generative Models** (Samplers and guidance). Red team: reword.
  - Argument: The reason makes the same point as the DDIM line at the top of the subsection. 'Which parts of a sampler can be swapped without retraining' and 'step count is a sampler choice rather than a property of the trained network' are one lesson. What only this paper gives is the split of the noise schedule, the network preconditioning, the loss weighting and the solver into separately priced decisions, some on the ...
  - Rule cited: conventions.md section 11 (why, not what) and redundancy with the Denoising Diffusion Implicit Models reason
  - Answer: Accepted. Reworded.

- **FLUX** (Latent and text conditioned systems). Red team: cut.
  - Argument: The entry fails the core admission test twice. FLUX.1 has no paper or specification; the repository's only citation is the Kontext paper, which the owner rejected. There is also no measurement: the owner's own Claims block finds 'Fields present: none that can be checked' and cuts the preference claim. Imagen and DreamBooth were sent to the watchlist for missing one of the three conditions; FLUX misses two. What ...
  - Rule cited: conventions.md section 8 (core needs a paper or spec, an implementation and a public measurement); section 6 (a repository with no written account is a dependency); redundancy with section 9 model cards
  - Answer: Accepted in substance. Moved to the watchlist with the condition that would promote it.

- **Stable Diffusion v1 Model Card** (Latent and text conditioned systems). Red team: reword.
  - Argument: 'The first widely loaded checkpoint' is a popularity justification, the banned 'popular' without the word, and conventions section 3 calls importance unfalsifiable. The card's real value is that it names its corpus subsets (laion2B-en, laion-high-resolution, laion-aesthetics v2 5+ with its watermark and size filters) and its own failure list. The card also names the CLIP ViT-L/14 text encoder, which the README ...
  - Rule cited: voice.md section 2 (praise and popularity vocabulary); conventions.md section 3 (importance is not a reason)
  - Answer: Accepted. Reworded.

- **Adding Conditional Control to Text-to-Image Diffusion Models** (Control, editing and evaluation). Red team: reword.
  - Argument: Fix the title only. The method is known and searched as ControlNet, and the paper's title does not contain the name. Voice section 4 says to keep the method name in that case, and the README follows that rule elsewhere (SDEdit, FCOS, RAFT, SuperGlue). Keep the reason line.
  - Rule cited: voice.md section 4 (keep the method name when the title buries it)
  - Answer: Accepted. Retitled to ControlNet, the name it is searched by.

- **Rethinking FID** (Control, editing and evaluation). Red team: keep but weakest.
  - Argument: Weakest of the six. The section preamble already gives the conclusion of its reason line ('depend on the feature network, the sample count'), so a reader gets nothing from the line that the preamble did not say. The half of the paper that goes beyond the preamble, the mis-ranking of text conditioned systems against human preference, is the half the owner's Claims block records as having no protocol and says ...
  - Rule cited: redundancy with the section 13 preamble; conventions.md section 7 (the distinctive claim is recorded unverified)
  - Answer: Noted as the weakest in its subsection. Kept as written.

### Section 14

- **Learning Transferable Visual Models From Natural Language Supervision** (Contrastive image-text pretraining). Red team: reword.
  - Argument: Fix the title only. The paper is known and searched as CLIP, and the title buries the name. A reader who searches the page for CLIP lands on 'Model Card: CLIP' and 'OpenCLIP' and never on the paper that defines it. Voice section 3 asks for one spelling per concept so that search inside the page works. The same rule applies in this section to 'Sigmoid Loss for Language Image Pre-Training' (SigLIP), 'Visual ...
  - Rule cited: voice.md section 4 (method name when the title buries it) and section 3 (search inside the page)
  - Answer: Accepted. Reworded.

- **LAION-5B** (Contrastive image-text pretraining). Red team: reword.
  - Argument: 'What an openly released image-text corpus is made of' describes contents, and it is also out of date. LAION took the corpus offline in December 2023 after the Stanford Internet Observatory found links to CSAM that its filtering had let through, and released it again in August 2024 as Re-LAION-5B with those links removed (laion.ai/blog/relaion-5b). The cut case is that DataComp, the next entry, documents a pool ...
  - Rule cited: conventions.md section 11 and voice.md section 1 (why, not what); conventions.md section 10 (a claim that no longer holds)
  - Answer: Accepted. Reworded.

- **Flamingo** (Generative vision-language models). Red team: cut.
  - Argument: There are no weights or code from the authors, and no measurement with its fields. The owner's rejected block refuses the only first-party page as marketing. Section 13 sent Imagen to the watchlist for the same missing half, so a consistent list sends this one too. Its reason ('a frozen language model was made to read images without retraining either half') does the same job as BLIP-2's line ('both the image ...
  - Rule cited: conventions.md section 8 (core needs an implementation and a public measurement), consistent with the Imagen watchlist decision; redundancy with BLIP-2
  - Answer: Accepted in substance. Moved to the watchlist with the condition that would promote it.

- **Improved Baselines with Visual Instruction Tuning** (Generative vision-language models). Red team: reword.
  - Argument: Its reason ('which gains came from the connector and which came from the training recipe') overlaps Prismatic VLMs two lines later ('the connector, the encoder and the data were varied one at a time'), which is the controlled version of the same question. What this entry has that Prismatic lacks is that it is the recipe later open models reproduce, as the owner's InstructBLIP rejection says, and the base ...
  - Rule cited: redundancy with Prismatic VLMs; conventions.md section 3 (a later entry reads as a reply to an earlier one, so state the dependency)
  - Answer: Superseded by the evidence marshal, which moved the entry to the watchlist.

- **Molmo and PixMo** (Open weights and model cards). Red team: reword.
  - Argument: Its motive ('weights and the data behind them released together, so a leakage check needs nobody's cooperation') is the same as OpenCLIP's line above it ('training corpus is named, which is what makes an overlap audit possible'). What only Molmo shows, and what an engineer comparing it with Visual Instruction Tuning needs, is that its instruction and caption data came from human annotators rather than being ...
  - Rule cited: redundancy with OpenCLIP in the same subsection
  - Answer: Accepted. Reworded.

- **Llama 3.2-Vision** (Open weights and model cards). Red team: reword.
  - Argument: This is the weakest entry in the subsection. Its reason rests on one field, a December 2023 data cutoff, used as a contamination check, while the subsection's own benchmark entries argue for measurement over dates. The card's benchmark table was computed with 'our internal evaluations library', so its protocol is unstated. What an engineer has to learn from this card before loading it is not on the line. The ...
  - Rule cited: voice.md section 1 (name the question it settles); conventions.md section 7 (the card's numbers carry no protocol)
  - Answer: Accepted. Reworded.

- **Benchmarking Benchmark Leakage in Large Language Models** (Benchmarks and contamination). Red team: cut.
  - Argument: This is not a vision source. The authors' README (GAIR-NLP/benbench) frames the work 'through the lens of mathematical reasoning tasks', detects leakage from perplexity and n-gram accuracy on GSM8K and MATH, needs model logits, and shows a leaderboard image. Nothing in it touches an image. The vision version of the job is already done by MMStar, the line above, whose multi-modal leakage metric the owner's own ...
  - Rule cited: redundancy with MMStar and section 4 Splits, leakage and duplication; conventions.md section 2 (what this reader needs); voice.md section 1 (why, not what)
  - Answer: Accepted. Cut.

- **MMMU** (Benchmarks and contamination). Red team: reword.
  - Argument: 'The multimodal exam most reports quote' rests on popularity without crediting the source with anything; voice section 1 accepts 'everyone quotes' only when the line names what the source defines. The second half, 'the answer extraction rule the quoting drops', is the job VLMEvalKit does on the next line ('where the prompt template and the answer extraction... actually live'). What ties MMMU to the path is that ...
  - Rule cited: redundancy with VLMEvalKit; conventions.md section 3 (importance is not a reason)
  - Answer: Accepted. Reworded.

- **Are We on the Right Way for Evaluating Large Vision-Language Models?** (Benchmarks and contamination). Red team: reword.
  - Argument: Fix the title only. It is 68 characters, over the 60-character soft ceiling, and it is a question. The owner kept it whole because a question cannot be trimmed, but voice section 4 offers the other route: use the method name when the paper is known by it. The owner's own rejected block and link notes call it the MMStar entry, and the repository is MMStar-Benchmark/MMStar.
  - Rule cited: voice.md section 4 (sixty-character ceiling; keep the method name)
  - Answer: Accepted. Retitled to MMStar, the benchmark the paper builds.

### Section 15

- **Building a quantization paradigm from first principles** (Quantisation). Red team: cut.
  - Argument: The next two entries already do its job. Its headings (affine map, zero exactly representable, quantising a matrix multiplication, implementation) are the derivation that 'Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference' sets out in its own quantised-inference section. That paper comes from the same group and cites gemmlowp as its implementation. The TensorFlow Lite ...
  - Rule cited: conventions.md section 10 (deprecated tooling and redundancy retirement); redundancy with the integer-arithmetic paper and the TensorFlow Lite specification
  - Answer: Accepted. Cut.

- **Distilling the Knowledge in a Neural Network** (Distillation, pruning and sparsity). Red team: reword.
  - Argument: Keep the entry and fix the reason. 'First specified as a method' is a priority claim, and the paper's own abstract contradicts it by crediting Caruana and collaborators with compressing an ensemble into a single model. What this paper actually contributes, and what a reader comes for, is the softmax temperature as the control on what transfers.
  - Rule cited: voice.md section 1 (motive, not provenance); factual accuracy of the reason
  - Answer: Accepted. Reworded.

- **What is the State of Neural Network Pruning?** (Distillation, pruning and sparsity). Red team: keep but weakest.
  - Argument: Weakest in the subsection. Its lesson, that results are incomparable without a shared baseline, is already taught three times: section 5's 'A Metric Learning Reality Check', and section 6's 'ResNet strikes back' and 'Revisiting ResNets'. Its subject is mostly unstructured pruning, which none of the runtimes in the next two subsections turn into latency. The only sparsity that pays at runtime here is the ...
  - Rule cited: redundancy with section 5 and section 6 recipe entries; conventions.md section 2 (what a working engineer needs)
  - Answer: Noted as the weakest in its subsection. Kept as written.

- **Operator Schemas** (Compilers and runtimes). Red team: cut.
  - Argument: This is the only document repeated across numbered sections outside Start here. Section 10 already cites the same file at https://github.com/onnx/onnx/blob/main/docs/Operators.md#NonMaxSuppression, and README 'What earns a place' says 'Start here may repeat an entry... No other section may.' Its stated job, 'version history that decide whether a model converts at all', is done by the IR entry above it. IR.md's ...
  - Rule cited: README 'What earns a place' (no repeats outside Start here); voice.md section 7; redundancy with the ONNX IR entry
  - Answer: Accepted. Removed from section 15. The ONNX operator document is cited once, at the NonMaxSuppression anchor in section 10.

- **MLComputeUnits** (Edge, accelerators and measurement). Red team: cut.
  - Argument: The page is an enum reference. Its whole content is the abstract 'The set of processing-unit configurations the model can use to make predictions' and four cases (all, cpuAndGPU, cpuAndNeuralEngine, cpuOnly), fetched from Apple's documentation JSON. The reason promises a 'Why' that the page never argues; that is the reader's own inference. The same lesson, that latency must name what it ran on, is already given ...
  - Rule cited: voice.md section 1 (the reason must be true of the source); redundancy with the section 15 preamble and ShuffleNet V2
  - Answer: Rejected, and the reason rewritten. The page is short because the lesson is short: a Core ML latency figure depends on a setting with four values, and a figure that does not name the value cannot be reproduced. That is section 15's suspicion stated as an official setting.

- **XNNPACK** (Edge, accelerators and measurement). Red team: reword.
  - Argument: The reason claims the page decides 'which layers fall back to a slower path'. The README says nothing about fallback; that happens inside the runtime's delegate. The README also says it 'is not intended for direct use by deep learning practitioners', so the maintainers themselves cast it as a dependency. What the page does give is a list of CPU architectures and operators, plus latency tables the owner records as ...
  - Rule cited: conventions.md section 6 (a repository is a dependency, not a reading); voice.md section 1 (the reason must be true of the source)
  - Answer: Accepted. Reworded.

### Section 16

- **Measuring Robustness to Natural Distribution Shifts** (Distribution shift). Red team: reword.
  - Argument: This is the weakest line in the subsection as written. 'Whether a corruption suite score predicts behaviour under real shift' overlaps The Many Faces of Robustness, which also tests whether fixes transfer across kinds of shift. It also depends on the corruption suite, which is defined only in the next subsection (see order problems). What only this paper gives a working engineer is effective robustness: most ...
  - Rule cited: conventions.md section 11 (why, not what) and redundancy with The Many Faces of Robustness
  - Answer: Accepted. Reworded.

- **On Interaction Between Augmentations and Corruptions** (Corruptions and synthetic perturbation). Red team: reword.
  - Argument: The title is the paper's but the URL is the repository, which breaks the voice section 4 rule that repositories are titled with the thing. The reason ('held out corruptions that break a tuned robustness score') also asserts the paper's measured finding, which the owner could not read and recorded unverified, while the entry claims to rest only on code. The obstacle is gone. The paper is arXiv 2102.11273, ...
  - Rule cited: voice.md section 4 (titles); conventions.md section 5 (cite the paper when the claim is the paper's); section 7 (a reason resting on an unverified finding)
  - Answer: Accepted. Reworded.

- **3D Common Corruptions** (Corruptions and synthetic perturbation). Red team: keep but weakest.
  - Argument: Weakest in the subsection. The held-out-suite lesson is already carried by the augmentation-corruption entry above it. The reason overclaims: 'cannot happen in a real scene' is false for additive noise, which section 2's Poissonian-Gaussian entry treats as a real sensor property. It survives because it is the only entry whose corruptions follow scene geometry (motion blur, depth of field, fog by depth) and the ...
  - Rule cited: voice.md section 1 (the reason must be accurate); partial redundancy with the held-out corruption entry
  - Answer: Noted as the weakest in its subsection. Kept, with the line sharpened.

- **Towards Deep Learning Models Resistant to Adversarial Attacks** (Adversarial robustness). Red team: reword.
  - Argument: 'Where the threat model a defence has to state was written down' undersells the reason to open it and half-duplicates the adaptive attacks line. What an engineer needs from this paper is that projected gradient adversarial training is the defence the owner's Obfuscated Gradients claim names as the one that held. That is the dependency the next two entries read against.
  - Rule cited: voice.md section 1 (name the thing it is the source of)
  - Answer: Accepted. Reworded.

- **On Adaptive Attacks to Adversarial Example Defenses** (Adversarial robustness). Red team: cut.
  - Argument: This repeats the job of the line above. 'Obfuscated Gradients Give a False Sense of Security' already shows how published defences fail honest evaluation, and its claim is the only one in the subsection with a 'stands' verdict. This paper breaks more defences and teaches the same lesson, and its reason ('what an evaluation has to do before accuracy under attack means anything') is the moral of the earlier paper. ...
  - Rule cited: conventions.md section 10 (retire when a later or earlier entry makes it redundant); redundancy with Obfuscated Gradients
  - Answer: Accepted. Cut.

- **FRVT** (Bias, calibration and safety). Red team: cut.
  - Argument: The cited page does not contain what the reason says. The README (fetched) is a directory index of validation packages. Each one links to an API PDF on pages.nist.gov, which the owner could not reach, so the protocol named in the reason is not in the cited page. The evaluation has also been renamed: the README itself says FRTE and FATE. A submission harness is a dependency for vendors, not a reading for an ...
  - Rule cited: conventions.md section 6 (a repository with no written account is a dependency); voice.md section 1 (the reason must be true of the source)
  - Answer: Accepted. Cut.

- **Fitzpatrick17k** (Bias, calibration and safety). Red team: cut.
  - Argument: Its job, scoring a classifier separately per group before claiming accuracy, is the job FairFace does on the line above. The README does not ship the images. It says to fetch them from the original atlas URLs, notes 'some of the links are broken', and offers a request form instead, so an outsider cannot rerun the audit as published. The README also admits that Fitzpatrick labelling of diseased skin is subjective. ...
  - Rule cited: conventions.md section 8 (an implementation an outsider can run); redundancy with FairFace
  - Answer: Accepted. Cut.

## Round one: dependency order

- Section 1, none (numbered list): If item 5 survives, it sits above item 6 even though its experiments are top-five comparisons on the ImageNet challenge splits, which item 6 defines. This breaks 'item k assumes items 1 to k-1'.
  - Answer: Resolved. Item five was cut, so the inversion no longer exists.

- Section 1, none (numbered list): ShuffleNet V2 at item 9 assumes group convolution, depthwise separable layers and channel shuffle from section 6. No position inside Start here fixes this, because no Start here item provides that material. The only fix is removal (see findings).
  - Answer: Accepted. ShuffleNet V2 left Start here; MLPerf Inference Benchmark took the deployment slot and assumes no architecture.

- Section 2, Colour: The image signal processor comes before Colour, but Unprocessing Images for Learned Raw Denoising inverts white balance gains, the colour correction matrix and the sRGB curve, all of which the reader first meets in Colour. Fast Fourier Color Constancy says the illuminant must be estimated before any downstream colour transform, yet it sits last. A reader ...
  - Answer: Accepted. Colour now comes before The image signal processor.

- Section 2, Sensors and noise: Learning to See in the Dark is a learned raw-to-output pipeline, and its reason ('what a stock pipeline does to it') assumes the ISP stages introduced only in the next subsection. It belongs in The image signal processor after Unprocessing Images for Learned Raw Denoising. Interplay: once the Recovering High Dynamic Range Radiance Maps cut is applied, ...
  - Answer: Accepted in substance. The line now concerns what survives in a raw frame, which needs only the noise model before it.

- Section 3, Two-view and multi-view geometry: Recognising Panoramas names 'robust fitting and a joint refinement' in its own reason, and those are introduced only in the next subsection (Random Sample Consensus, Bundle Adjustment - A Modern Synthesis). The owner's note admits it 'hands the reader straight into the next subsection', which means it is read before what it depends on. Move it to ...
  - Answer: Partly accepted. Recognising Panoramas stays in two-view geometry, and its line now concerns homography drift alone, which needs nothing from the estimation subsection to read.

- Section 4, The datasets that set the terms: The LVIS paper appears twice outside Start here: in section 4 as 'LVIS' (openaccess.thecvf.com URL) and in section 5 as 'LVIS: A Dataset for Large Vocabulary Instance Segmentation' (https://arxiv.org/abs/1908.03195). That is two titles and two URLs for one paper. README 'What earns a place' says no section other than Start here may repeat an entry. ...
  - Answer: Accepted. LVIS appears once, in section 4.

- Section 6, Recipes against architectures: A ConvNet for the 2020s is a step-by-step move from a ResNet toward Swin Transformer (section 7), trained on the transformer recipe whose parts are defined in section 8. A section 6 reader has to look forward, which fails the conventions section 3 test. Bag of Tricks and ResNet strikes back also lean on section 8 techniques (cosine decay, label ...
  - Answer: Accepted. A ConvNet for the 2020s moved to section 7, after Swin Transformer.

- Section 6, Efficient convolutional designs: Xception sits first but needs the most prior context: it assumes the Inception module from Going Deeper with Convolutions. MobileNets derives the depthwise separable cost from scratch. Conventions section 3 puts the entry needing the least context first. MobileNetV2 replies to MobileNets, not to Xception, so moving MobileNets up breaks nothing. ...
  - Answer: Accepted. MobileNets now comes first and Xception second.

- Section 7, Vision transformers: Conditional Positional Encodings for Vision Transformers adds its encoding to DeiT models trained with the DeiT recipe and reports against DeiT. Early Convolutions Help Transformers See Better also follows the DeiT recipe. DeiT (Training data-efficient image transformers) sits in the next subsection, so this subsection reads ahead of its own dependency. ...
  - Answer: Accepted. Training data-efficient image transformers moved into Vision transformers, ahead of the entries that build on it.

- Section 7, Data, scale and distillation: Distillation is assumed before the path defines it. DeiT's reason line and this subsection's name lean on it, and section 8's label smoothing line ('hurts the student it later teaches') does too, but the defining source, Distilling the Knowledge in a Neural Network, sits in section 15. The augmentation policies that DeiT and How to train your ViT? trade ...
  - Answer: Accepted differently. The DeiT line now introduces the teacher network itself, and the label smoothing line no longer mentions a student, so neither needs section 15 first.

- Section 8, Regularisation and normalisation: Batch Normalization and Layer Normalization sit in section 8, but section 6 depends on BN: Deep Residual Learning puts BN after every convolution, and Identity Mappings' reason line is literally about 'the order of normalisation, activation and addition'. Section 7's transformer block and MetaFormer's 'block around it' depend on LN. The section 6 draft ...
  - Answer: Rejected. Deep Residual Learning describes the normalisation it uses in its own text, so section 6 does not have to read section 8 first. The batch normalisation paper stays with training, where its train and test behaviour is the lesson.

- Section 8, Objectives: The editor reversed owner-brief section 2 twice. Focal Loss was in the section 8 draft and moved to the later section 10. Generalized Intersection over Union was in the section 5 draft and landed in the later section 8. The result is a detection box loss read before any detector exists. Applied consistently: GIoU returns to section 5 What the detection ...
  - Answer: Accepted for GIoU, which returned to section 5. Rejected for Focal Loss, which stays in section 8: its line concerns class imbalance in a dense grid of positions, which reads without any detector architecture.

- Section 10, Postprocessing and what ships: Soft-NMS comes before the specification of the operation it modifies. Its reason ('Why a neighbouring object disappears at one overlap threshold and survives at another') is about hard greedy suppression, which the ONNX NonMaxSuppression text defines, and the specification is also the shorter read. The first entry should need the least context.
  - Answer: Accepted. The ONNX specification now comes before Soft-NMS.

- Section 11, Temporal modelling: TSM is built on TSN and evaluated against it as its 2D baseline with segment sampling. SlowFast's reason presupposes clip sampling. But TSN and the clip-sampling protocol arrive only in the next subsection, 'Video datasets and their protocols', so the reader has to look forward. The README's own trunk logic is measurement before architecture. Fix: put ...
  - Answer: Accepted. Video datasets and their protocols now comes before Temporal modelling.

- Section 11, Temporal modelling: RAFT sits first but is the highest-context entry. It assumes brightness constancy and correlation cost volumes, and nothing in sections 1 to 10 supplies either; the owner's premise that section 3 does is false in the README. None of the four RGB entries needs RAFT, and Quo Vadis describes its own classical flow input. Unless a flow-definition entry is ...
  - Answer: Accepted. RAFT moved to section 12, where RAFT-Stereo and DROID-SLAM build on it.

- Section 11, Tracking: Tracking comes before Tracking metrics. Tracktor ('how much of a tracking score belongs to the detector') and ByteTrack ('identity continuity rather than precision') are therefore read before MOTA, the public and private detection split, IDF1 and HOTA are defined. This is weaker than the TSM case, because each paper explains its own metrics, but it ...
  - Answer: Accepted. Tracking metrics now comes before Tracking.

- Section 12, Simultaneous localisation and mapping: 'A Photometrically Calibrated Benchmark For Monocular Visual Odometry' defines the response, vignetting and exposure model that Direct Sparse Odometry consumes; the DSO paper defers to it for calibration. The benchmark is also the shorter read, yet it sits after DSO. ORB-SLAM3, which assumes inertial preintegration and a multi-map system, is a weak ...
  - Answer: Accepted. The photometric benchmark now comes before Direct Sparse Odometry.

- Section 12, Depth and stereo: RAFT-Stereo (and DROID-SLAM in the next subsection) are built directly on section 11's RAFT. conventions.md s3 says sections 10 to 14 do not depend on each other, so a reader who branches from the trunk straight to section 12 meets RAFT-Stereo without its base. Either record the cross-family dependency or give RAFT-Stereo a reason that stands without ...
  - Answer: Accepted. RAFT now sits in section 12 directly before RAFT-Stereo.

- Section 13, Latent and text conditioned systems: Section 13 assumes section 14, which breaks conventions section 3 ('must assume nothing after it'). The Stable Diffusion v1 Model Card (fetched) describes the checkpoint as using 'a fixed, pretrained text encoder (CLIP ViT-L/14)' trained on laion2B-en and laion-aesthetics subsets. CLIP and LAION-5B are introduced only in section 14's first subsection. ...
  - Answer: Rejected. The text-conditioned entries name a pretrained text encoder as a component, and reading them needs only the fact that one exists. How it was trained is section 14's subject, and nothing in section 13 depends on it.

- Section 13, Control, editing and evaluation: The distributional score is defined by 'GANs Trained by a Two Time-Scale Update Rule' in the last subsection, but the section reads in its terms from the start. The preamble warns about it, 'Diffusion Models Beat GANs on Image Synthesis' and 'Classifier-Free Diffusion Guidance' state their trade-offs in it, and DDPM's results are quoted in it. The ...
  - Answer: Accepted. The score definitions now open the section in their own subsection.

- Section 14, Contrastive image-text pretraining: 'Sigmoid Loss for Language Image Pre-Training' replies directly to the CLIP paper's loss. It does not depend on LAION-5B or DataComp, and it is a much shorter read than either. Conventions section 3 puts genuinely independent entries shortest first and later entries as replies to earlier ones, so it belongs second, not last.
  - Answer: Accepted. The sigmoid loss now comes second, directly after the paper whose loss it replaces.

- Section 15, Distillation, pruning and sparsity: Distillation is defined here in section 15, but earlier sections assume it. Section 7's 'Data, scale and distillation' includes 'Training data-efficient image transformers' ('What distillation and augmentation buy'). Section 8's 'When Does Label Smoothing Help?' reasons about 'the student it later teaches'. A reader at section 7 has to look forward to ...
  - Answer: Accepted differently, as for item nine: no earlier line now assumes distillation is already known.

- Section 16, Distribution shift: 'Measuring Robustness to Natural Distribution Shifts' has a reason ('Whether a corruption suite score predicts behaviour under real shift') that needs the corruption suite and its error metric. Those are defined only in the next subsection, by 'Benchmarking Neural Network Robustness to Common Corruptions' and 'make_imagenet_c.py'. Moving the entry after ...
  - Answer: Partly accepted. The line now asks only whether robustness to synthetic perturbation predicts robustness to natural shift, which needs no suite definition.

## Round one: coverage gaps

A gap is filled only with a source whose URL and identifier were verified from this container,
by the arXiv identifier and title appearing together in the authors' own repository or by
search. A gap that could not be filled that way stays open and is listed in misc/notes/status.md.

- Section 2, The image signal processor: no entry covers lossy encoding, the last stage every dataset image in section 4 passed through. That means JPEG chroma subsampling and block quantisation, and video codecs for section 11. Nothing in the README touches it before section 16's corruption code ...
  - Answer: Not filled. The ITU-T T.81 page could not be pinned to a verified catalogue entry from this container, and a guessed URL breaks the first rule. Open: needs a verified canonical URL for the JPEG specification.

- Section 2, Optics and projection or Sensors and noise: owner-brief section 3 lists exposure as section 2 coverage, but no entry covers exposure-time effects on geometry and appearance: motion blur, and rolling-shutter readout that is not simultaneous across rows. Section 11 tracking and section ...
  - Answer: Not filled. No primary rolling shutter source could be verified from this container. Open.

- Section 3, Sampling and filtering (or Start here): every sampling entry is theory, and none shows that the resize implementations engineers call disagree on antialiasing and pixel-centre convention, which is the main source of preprocessing mismatch between training and serving. The only README ...
  - Answer: Filled. On Aliased Resizing moved to section 3 Sampling and filtering, with a line about library disagreement.

- Section 3, Features and correspondence: no binary detector or descriptor (FAST, BRIEF, ORB). Section 12's ORB-SLAM3 line ('The feature based system most robotics stacks still start from') assumes them, so section 12 currently depends on material the trunk never gives. No owner's Rejected block ...
  - Answer: Not filled. No canonical copy of a binary descriptor paper could be verified. Open, and ORB-SLAM3's line no longer leans on the term.

- Section 4, Splits, leakage and duplication: near-duplicate purging covers only copies at the pixel level. Nothing covers grouped or temporal leakage: splitting by the unit that will be new at deployment, such as scene, subject, capture session, video or time. Benchmark 04 shows that hash ...
  - Answer: Not filled as an entry. Benchmark four measures grouped leakage directly. Open for a primary source.

- Section 4, Documentation and audit: nothing tells an engineer that the dataset downloaded today is not the one a paper trained on. Examples are the withdrawal of the source behind CIFAR, ImageNet's filtering of person categories and its face-blurred release, and terms of access. The section 4 ...
  - Answer: Not filled. The withdrawal notices could not be verified. Open.

- Section 1, Start here: if items 5 and 9 are cut, two of the exactly ten slots must be refilled with items that assume only what comes before them. The owner-brief duty 'what deployment costs' then loses its only timing lesson, because item 10 covers system debt, not measurement. It needs a ...
  - Answer: Filled. MLPerf Inference Benchmark took the deployment slot and the AlexNet paper took the learned feature slot.

- Section 5, What the detection metrics compute or Protocols and reporting: no entry tells an engineer how to choose or report the operating point a shipped detector actually runs at. Every metric in the section integrates over confidence thresholds, and the section 10 draft's benchmark assumes ...
  - Answer: Not filled. Benchmark ten measures the operating point against the suppression threshold. Open for a primary source.

- Section 5, Segmentation and dense metrics: the subsection covers panoptic and boundary scores but nothing defines semantic segmentation mean IoU. In particular, nothing covers per-class IoU accumulated over the whole split's confusion matrix versus a per-image average, or the ignore label, which ...
  - Answer: Not filled. The Cityscapes metric page could not be verified. Open.

- Section 6, any subsection: nothing connects section 3's sampling and pyramid material to strided convolutional downsampling. Without it, an engineer cannot explain why a CNN's prediction flips under a one-pixel shift or crop jitter, which matters for video and letterboxing. Primary source: ...
  - Answer: Filled with Making Convolutional Networks Shift-Invariant Again.

- Section 7, Vision transformers: nothing covers the high-norm artefact tokens that ViTs store in background patches, or register tokens. The section 9 draft's link notes hand this to section 7 explicitly ('The register token work that the DINOv2 card depends on would be a collision with section 7 ...
  - Answer: Filled with Vision Transformers Need Registers in section 7.

- Section 8, Augmentation or Schedules and optimisation: nothing explains the train-test resolution discrepancy, where random-resized-crop changes apparent object size so the best test resize differs from the training crop. The torchvision recipe cited in this very section trains at one crop size ...
  - Answer: Filled with Fixing the train-test resolution discrepancy.

- Section 8, Regularisation and normalisation: stochastic depth (drop path) is the regulariser in every modern recipe the README cites (DeiT, Swin Transformer, A ConvNet for the 2020s, ResNet strikes back), and the README never defines it. It is the natural displacement for the proposed dropout ...
  - Answer: Filled with Deep Networks with Stochastic Depth, which displaced the dropout paper.

- Section 8, Schedules and optimisation: nothing covers reduced-precision training. Every modern command in the cited torchvision recipe sets AMP, yet no entry explains fp16 underflow, loss scaling or master weights, and section 15 covers only inference-side precision. Primary source: Mixed ...
  - Answer: Filled with Mixed Precision Training.

- Section 9, register tokens. The DINOv2 card splits its checkpoints into with-register and without-register variants, and DINOv3 builds registers in. The section 9 owner left 'Vision Transformers Need Registers' (https://arxiv.org/abs/2309.16588, identifier confirmed by search) to section 7, but ...
  - Answer: Filled in section 7, which comes first. The DINOv2 card line now points at which checkpoints carry registers.

- Section 9, adapting a frozen backbone. Both DINO cards say to fine-tune only as a last resort, but no entry says when full fine-tuning hurts, especially under shift, or how to adapt instead (linear probe, then fine-tune). Candidate: 'Fine-Tuning can Distort Pretrained Features and Underperform ...
  - Answer: Not filled. The fine-tuning distortion paper was not verified independently. Open.

- Section 9, missing warning label. The owner's preamble (frozen feature accuracies come from different probe protocols and are not comparable) was dropped in the merge. Sections 10, 13, 15 and 16 keep theirs. This is the first legitimate preamble case in voice.md s5, and it is the section's ...
  - Answer: Accepted. The probe protocol warning is restored as the section 9 preamble.

- Section 10, single-stage grid detectors. No SSD or YOLO lineage appears in the README, so YOLOv10, the only real-time detector entry, is read without its base, and that lineage is what most shipped detectors descend from. The owner dropped SSD (https://arxiv.org/abs/1512.02325) and the third ...
  - Answer: Filled with SSD and YOLOv3.

- Sections 10 and 11, propagating a mask through time. Video object segmentation has no entry. Its only candidate was rejected by the section 10 owner as section 11's subject and by the section 11 owner as section 10's, so neither owner judged it on merit. The editor must assign it to one section ...
  - Answer: Not filled. No verified candidate. Open.

- Section 11, attention or masked-pretrained video backbones. Temporal modelling ends at convolutional designs. The one attention candidate was rejected on the premise that section 7 owns video attention, but section 7 carries no video entry, and its draft explicitly left the video reading to ...
  - Answer: Filled with TimeSformer.

- Section 11, what optical flow is and how it is scored. RAFT is read cold. The owner assumed section 3 supplies brightness constancy, but README section 3 has no flow entry, and no entry defines end-point error or a flow protocol. Candidate: 'A Database and Evaluation Methodology for Optical ...
  - Answer: Partly addressed. RAFT moved to section 12 with a line that defines what it estimates. The flow benchmark paper could not be verified. Open.

- Section 12, the classical stereo pipeline and its scoring. The first entry's reason presupposes classical cost aggregation, which nothing introduces, and semi-global style matching is what most shipped depth cameras and OpenCV's stereo still run. The owner left the dense two-frame taxonomy and ...
  - Answer: Not filled. No canonical copy could be verified. Open.

- Section 12, the trajectory error protocol. Every SLAM number is quoted as absolute trajectory error or relative pose error, and the photometric benchmark's reason ('before a trajectory error means anything') leans on a metric the README never defines. The owner deferred KITTI and the TUM RGB-D ...
  - Answer: Not filled. The trajectory benchmark could not be verified. Open.

- Section 13, Samplers and guidance: there is no entry on few-step distillation of a diffusion model. That is how shipping systems actually cut sampling cost, and the FLUX entry's open schnell variant is itself step-distilled. DDIM and EDM cover only training-free samplers, and the rejected ...
  - Answer: Filled with Consistency Models.

- Section 13, Control, editing and evaluation: no entry measures whether an image matches its prompt. The section's own suspicion is that a distributional score stands in for what a user cares about, yet all three evaluation entries are about that score. Any candidate (a text-image alignment score ...
  - Answer: Filled with GenEval.

- Section 14, Benchmarks and contamination: nothing measures hallucination, meaning objects asserted that are not in the image, the main failure of a deployed captioning or VQA model. Candidate: POPE, https://arxiv.org/abs/2305.10355 (authors' repo RUCAIBox/POPE, HTTP 200). It is in no owner's ...
  - Answer: Filled with POPE.

- Section 14, Open weights and model cards: the README admits official model cards as a source class and cites five of them (Stable Diffusion v1, CLIP, Llama 3.2-Vision, DINOv2, DINOv3), but no entry says what a card must contain, including disaggregated evaluation. The section 14 owner deferred ...
  - Answer: Filled with Model Cards for Model Reporting, placed in section 4 so it comes before every model card in the list.

- Section 15, Edge, accelerators and measurement: the section heading promises NPU, but no entry explains how a graph is partitioned between a neural accelerator and the CPU, which operators and layouts an NPU accepts, or what falls back. XNNPACK is CPU only, and MLComputeUnits only names the ...
  - Answer: Filled with Apple Neural Engine Transformers.

- Section 15, Quantisation: every entry concerns integer schemes for convolutional networks. Sections 7, 9, 13 and 14 put attention models at the centre, yet nothing covers why their activation outliers, softmax and normalisation layers break per-tensor eight-bit quantisation. SmoothQuant ...
  - Answer: Filled with SmoothQuant.

- Section 16, Adversarial robustness: all five entries use digital norm-ball threat models. Nothing covers the physically realisable attack (a printed patch or sticker in the scene), which is the adversarial threat a deployed camera system actually faces and which a norm bound does not describe. ...
  - Answer: Filled with Adversarial Patch.

- Section 16, Bias, calibration and safety: calibration is covered, but rejecting inputs the model should not answer is not. There is no out-of-distribution detection or abstention baseline, which is the standard safety mechanism in deployed vision. Candidate: A Baseline for Detecting ...
  - Answer: Filled with A Baseline for Detecting Misclassified and Out-of-Distribution Examples.
