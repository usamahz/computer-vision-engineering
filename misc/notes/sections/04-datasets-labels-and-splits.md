# 4. Datasets, labels and splits: where ground truth comes from and how it lies

Owner: data-centric researcher who has audited label quality, suspicious of any result that ignores label noise or split leakage.

## Section

## 4. Datasets, labels and splits: where ground truth comes from and how it lies

The label error rates and replication gaps quoted from this subject are estimates produced by a model and a crowd protocol rather than counts, and two of the entries below disagree about how much of a replicated test set's extra difficulty is real.

### The datasets that set the terms

- [The PASCAL Visual Object Classes (VOC) Challenge](http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf) - Where the annotation guidelines and the difficult flag that later benchmarks inherited were written down.
- [ImageNet Large Scale Visual Recognition Challenge](https://arxiv.org/abs/1409.0575) - How one label per image and the top-five rule were settled on, and what that choice throws away.
- [ILSVRC](https://image-net.org/challenges/LSVRC/) - Which images belong to which year of the challenge, and the access terms that come before any download.
- [Microsoft COCO: Common Objects in Context](https://arxiv.org/abs/1405.0312) - What counts as one instance, and when a region is marked as crowd instead of labelled.
- [LVIS](https://openaccess.thecvf.com/content_CVPR_2019/html/Gupta_LVIS_A_Dataset_for_Large_Vocabulary_Instance_Segmentation_CVPR_2019_paper.html) - Why annotating every instance of every category stops being affordable once the list has a long tail.

### Annotation and label noise

- [From ImageNet to Image Classification](https://arxiv.org/abs/2005.11295) - What human annotators answer when asked the question the benchmark assumes has one answer.
- [Are we done with ImageNet?](https://arxiv.org/abs/2006.07159) - Why relabelling a validation set changes which models look like they improved.
- [Human uncertainty makes classification more robust](https://arxiv.org/abs/1908.07086) - Where annotator disagreement is kept as signal instead of being voted away.
- [Confident Learning](https://arxiv.org/abs/1911.00068) - How a label error estimate is produced, and the noise assumption it rests on.
- [Pervasive Label Errors in Test Sets](https://arxiv.org/abs/2103.14749) - What happens to a benchmark ranking once the test labels themselves are corrected.

### Splits, leakage and duplication

- [Do We Train on Test Data? Purging CIFAR of Near-Duplicates](https://arxiv.org/abs/1902.00423) - Where test images turn out to have near duplicates sitting in the training split.
- [Do ImageNet Classifiers Generalize to ImageNet?](https://proceedings.mlr.press/v97/recht19a) - What a fresh test set built to the original recipe does to published accuracy.
- [Identifying Statistical Bias in Dataset Replication](https://arxiv.org/abs/2005.09619) - Why a replacement split that looks harder may be measuring its own construction.

### Documentation and audit

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) - The documentation to demand before trusting a dataset, in a form somebody can actually fill in.
- [The Dataset Nutrition Label](https://arxiv.org/abs/1805.03677) - A shorter documentation format for datasets whose full datasheet will never be written.
- [Lessons from Archives](https://arxiv.org/abs/1912.10389) - Where curating and documenting a collection already exists as a profession with its own rules.
- [Large image datasets: A pyrrhic win for computer vision?](https://openaccess.thecvf.com/content/WACV2021/html/Birhane_Large_Image_Datasets_A_Pyrrhic_Win_for_Computer_Vision_WACV_2021_paper.html) - What an audit of a shipped vision dataset finds inside it, consent included.

## Rejected

- [The Pascal Visual Object Classes (VOC) Challenge](https://www.microsoft.com/en-us/research/publication/the-pascal-visual-object-classes-voc-challenge/) - Rule failed: conventions.md section 5, an aggregator's landing page cited where the authors' own copy exists. The challenge organisers host the paper on the challenge's own site, which is the copy a disagreement gets resolved against.
- [Microsoft COCO: Common Objects in Context](https://vision.ucsd.edu/sites/default/files/publications/pdfs/Microsoft%20COCO%20Common%20Objects%20in%20Context.pdf) - Rule failed: conventions.md section 5, a third-party PDF copy where the authors' own deposit exists. A departmental file tree rots on its own schedule and carries no version history.
- [Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks](https://neurips.cc/virtual/2021/22763) - Rule failed: conventions.md section 6, video lectures and talks. The page is a venue front end for a recorded presentation wrapped around a paper hosted elsewhere, and nothing on it is quotable or diffable.
- [From ImageNet to Image Classification: Contextualizing Progress on Benchmarks](https://icml.cc/virtual/2020/poster/53132) - Rule failed: conventions.md section 6, aggregators and paper mirrors. A venue poster page adds a layer that can go stale while the authors' own deposit stays correct.
- [Identifying Statistical Bias in Dataset Replication](https://par.nsf.gov/servlets/purl/10194573) - Rule failed: conventions.md section 6, aggregators and paper mirrors. A funder's public access repository holds a deposited copy of a paper whose authors publish it themselves.
- [imagenet2012_real](https://www.tensorflow.org/datasets/catalog/imagenet2012_real) - Rule failed: conventions.md section 6, aggregators and paper mirrors restating a primary source. The catalogue entry describes the reassessed labels but its citation block points at a different arXiv identifier, which is the added layer of error the rule exists to keep out.
- [ciFAIR](https://cvjena.github.io/cifair/) - Rule failed: conventions.md section 6, leaderboards and benchmark trackers. The authors' own download page carries a ranking next to the data, and the protocol definition in the paper is admissible where the ranking is not.
- [Do ImageNet Classifiers Generalize to ImageNet?](https://www.csail.mit.edu/node/7067) - Rule failed: conventions.md section 6, aggregators and paper mirrors. An institutional announcement page about a paper is not the paper and does not carry the experimental section.

## Claims

### Roughly three per cent of test labels are wrong on average across ten benchmark test sets, and about six per cent on the ImageNet validation split, from Pervasive Label Errors in Test Sets

- Fields present: dataset with split and version; training data used; baseline compared against.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; metric with its full definition; evaluation protocol including single-scale or test-time augmentation and the non-maximum suppression settings; hardware.
- Verdict: recorded unverified
- Note: the rate is the output of a confident-learning pass over an ensemble of pretrained models followed by crowd adjudication, so it estimates errors among the candidates that pass surfaced rather than counting errors in the split, and the recall of the flagging step is unmeasured. What counts as an error is a crowd majority over a flagged shortlist, and the quorum, worker screening and tie-breaking are not specified tightly enough to reproduce, so the figure is a lower bound on a quantity whose definition depends on the flagging model. The entry stands on the audit procedure and no reason line repeats the number.

### Correcting the test labels flips the ranking of two residual network sizes once the mislabelled share rises, from Pervasive Label Errors in Test Sets

- Fields present: dataset with split and version; metric with its full definition; baseline compared against.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; evaluation protocol including single-scale or test-time augmentation; training data used; hardware.
- Verdict: watchlist
- Note: this is the claim a reader would carry away, and the missing fields are the ones that decide it, since a ranking flip between two members of the same family turns on preprocessing and on whether either model was retrained once the labels changed. The claim is held back rather than the entry, which rests on the audit procedure instead. It becomes statable once the checkpoints, the preprocessing and the retraining decision are published alongside the corrected labels.

### Recent classifiers gain substantially less under reassessed multi-label validation labels than under the original ones, from Are we done with ImageNet?

- Fields present: dataset with split and version; metric with its full definition; training data used; baseline compared against.
- Fields missing: model and exact checkpoint for the full comparison set; input resolution and preprocessing per model; evaluation protocol including single-scale or test-time augmentation; hardware.
- Verdict: recorded unverified
- Note: reassessed accuracy counts a prediction correct when it falls inside a multi-label set, which is a different metric on a different label set from single-label top-one, so the gap between the two is not a measurement of one quantity moving. Part of the validation split carries no reassessed label and has to be dropped, which changes the denominator, and a quoted reassessed number that does not say whether those images were dropped is not comparable with another one.

### A fresh ImageNet test set built to the original protocol costs every model eleven to fourteen points of top-one accuracy, from Do ImageNet Classifiers Generalize to ImageNet?

- Fields present: dataset with split and version; model and exact checkpoint; metric with its full definition; training data used; baseline compared against.
- Fields missing: input resolution and preprocessing per model; evaluation protocol including single-scale or test-time augmentation; hardware.
- Verdict: recorded unverified
- Note: the drop reproduces, but the authors' own reading of it, that the replacement images are slightly harder rather than that the original test set was overfitted, is contested by the next claim, which attributes most of the gap to bias in the replication procedure. The number is recorded here and never repeated in a reason line, because quoting it as evidence of adaptive overfitting is exactly the inference the replication-bias work removes.

### Only about a third of that gap survives correction for selection-frequency bias in the replication, from Identifying Statistical Bias in Dataset Replication

- Fields present: dataset with split and version; metric with its full definition; evaluation protocol including the estimator and its assumptions; training data used; baseline compared against.
- Fields missing: model and exact checkpoint for the full model sweep; input resolution and preprocessing; hardware.
- Verdict: recorded unverified
- Note: the corrected residual is an estimate under a stated model of annotator selection rather than a measurement, and it inherits every field the replication it corrects was missing. Two primary sources now give different magnitudes for the same effect, which is why no reason line in this section carries either figure and why the subsection keeps both entries instead of the earlier one alone.

### Three per cent of the CIFAR-10 test split and ten per cent of the CIFAR-100 test split have duplicates in the training split, and replacing them costs trained networks nine to fourteen per cent relative accuracy, from Do We Train on Test Data?

- Fields present: dataset with split and version; training data used; baseline compared against.
- Fields missing: model and exact checkpoint; input resolution and preprocessing; metric with its full definition; evaluation protocol including single-scale or test-time augmentation; hardware.
- Verdict: recorded unverified
- Note: a near duplicate is settled by human inspection of a retrieval shortlist, so the duplicate rate has no reproducible threshold and is a lower bound set by whatever the retrieval step surfaced. The relative accuracy figure also mixes several network families whose checkpoints are not pinned, so it describes a spread rather than an effect size. The mechanism underneath it is what this section's benchmark measures directly, with the model held fixed so that nothing but the split can move.

### About three and a half thousand ImageNet validation images carry no reassessed label, from a framework dataset catalogue entry for the reassessed labels

- Fields present: dataset with split and version.
- Fields missing: metric with its full definition; evaluation protocol including single-scale or test-time augmentation; model and exact checkpoint; input resolution and preprocessing; training data used; hardware; baseline compared against.
- Verdict: cut
- Note: the page stating the count cites a different arXiv identifier from the paper it describes, so the protocol behind the count is unrecoverable from the source quoting it. The quantity matters because it sets the denominator for every reassessed accuracy figure, which is precisely why it may not be taken from a secondary page, and the catalogue entry is rejected above for the same reason.

## Link notes

- http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf - The host refuses automated clients from this container, which returns a connection failure rather than an HTTP status, so the URL was confirmed by search instead, with the title and the challenge's own path agreeing. The challenge homepage on the same host could not be confirmed and is therefore not cited, so this single URL carries both the dataset paper and the official page role for PASCAL VOC.
- https://image-net.org/challenges/LSVRC/ - Same host refusal, confirmed by search with the page title agreeing. Cited as the official page rather than the paper because the per-year challenge data definitions live there and not in the paper.
- https://image-net.org/download.php - Access restriction a reader will hit, recorded rather than cited. The full dataset and the common subsets sit behind a login and an agreement to terms that limit use to non-commercial research and education, with the hosting universities reserving the right to end access at any time. It is not an entry because the only page state search could confirm for it is the logged-out one.
- https://cocodataset.org - Left out. Neither the home page nor the download page could be confirmed from this container, so the official COCO page does not appear and the dataset paper carries that ground alone, which leaves the split composition question that only the official page answers unanswered in this section. Separately a collision: the detection evaluation page on that host is section five's ground and section five keeps it.
- https://proceedings.mlr.press/v97/recht19a - Preferred over the arXiv abstract page under conventions.md section 5, which asks for a conference page where the authors' canonical copy is openly readable. The arXiv deposit was used to check that the title and the identifier agree, and it carries the version history if the proceedings page ever moves.
- https://openaccess.thecvf.com/content_CVPR_2019/html/Gupta_LVIS_A_Dataset_for_Large_Vocabulary_Instance_Segmentation_CVPR_2019_paper.html - Published conference version preferred over the arXiv deposit for the same reason. The official LVIS dataset page named inside that paper could not be confirmed from this container and is not cited.
- https://openaccess.thecvf.com/content/WACV2021/html/Birhane_Large_Image_Datasets_A_Pyrrhic_Win_for_Computer_Vision_WACV_2021_paper.html - Published conference version preferred over the arXiv deposit for the same reason.
- Withdrawn dataset, no URL given. The eighty million tiny images collection, which is the source the CIFAR splits were drawn from, was withdrawn by its maintainers following the audit cited in Documentation and audit, and the page carrying the withdrawal notice could not be confirmed from this container, so it is recorded here without a link. Anyone tracing CIFAR provenance hits this, and the lineage is why that audit sits in this section rather than in section sixteen.
- Entry count, Splits, leakage and duplication. Three entries rather than four. The companion CIFAR-10 replication study belongs there as the shorter read before the ImageNet one, but its arXiv identifier could not be confirmed before this container's search budget ran out, and an unconfirmed identifier does not go in a draft. Three is the floor and the subsection still covers duplication, replication and the measurement bias in replication.
- Ordering decision, The datasets that set the terms. The official challenge page sits after the challenge paper rather than before it, because the page's data descriptions assume the task and label definitions the paper states.
- Collision, Datasheets for Datasets. It is also the obvious entry for the bias and audit material in section sixteen. Section four is earlier and keeps it.
- Collision, LVIS. Also a candidate for section ten. Section four keeps it as a dataset entry, and section ten should cite the detector work rather than the dataset paper.
- Every arXiv citation here is the abstract page rather than the PDF that search returned first, under conventions.md section 5. No URL in this draft is recorded as dead, because every host in it returns a connection failure from inside this container rather than a status code, which is the egress policy and not a dead page.

## Benchmark proposal

Near duplicate leakage between splits inflates a score with no change to the model. The model is
held exactly fixed by making it a nearest neighbour classifier over a fixed feature, downsampled
grey levels, with the training split as its only parameters, so nothing about the model can move
between conditions. Synthetic greyscale images are generated from a fixed seed with
`numpy.random.default_rng`, a few hundred per split in quick mode, as class prototypes plus
per-image noise. Near duplicates are produced with Pillow by re-encoding a training image as JPEG,
resizing it down and back, and shifting it by one pixel, so a leaked test item is visually the same
image and byte-identical to nothing. Two test splits of identical size and identical class balance
are built, one with no near duplicate of any training image and one where a swept fraction of items
are near duplicates of training images, at nought, one twentieth, one tenth and one quarter.
Accuracy on both splits is reported at each fraction, alongside what an exact byte hash and an exact
pixel comparison report as duplicates on the same contaminated split. The claim is settled if
accuracy on the contaminated split rises monotonically with the contamination fraction while the
clean split's accuracy stays bit-identical across runs and across fractions, and if the byte hash
and the pixel comparison both report no duplicates while the inflated score sits there, which would
show that the deduplication step a team actually runs cannot see the leak that moved the number. It
is refuted if the two accuracies stay within the run to run spread, which is zero here because the
accuracy computation is deterministic, in which case the mechanism needs a stronger duplicate than a
re-encode and the folklore is wrong in the other direction. Everything runs on CPU with numpy and
Pillow alone, with no network access at run time, and quick mode finishes well inside ten seconds.
