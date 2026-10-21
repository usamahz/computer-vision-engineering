# Computer Vision Engineering

![](misc/banner-calibration-chessboard.avif)

[![Links](https://github.com/usamahz/computer-vision-engineering/actions/workflows/links.yml/badge.svg)](https://github.com/usamahz/computer-vision-engineering/actions/workflows/links.yml) [![Quality](https://github.com/usamahz/computer-vision-engineering/actions/workflows/quality.yml/badge.svg)](https://github.com/usamahz/computer-vision-engineering/actions/workflows/quality.yml) [![Entries](https://img.shields.io/badge/entries-243-1f6feb)](#contents) [![Benchmarks](https://img.shields.io/badge/benchmarks-16%20runnable-1f6feb)](misc/benchmarks/common/README.md) [![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

Shipping a vision system means knowing what a pixel measured, what a metric counted, and which number in a paper will survive contact with a camera. This is the reading that gets there, from a photon hitting a sensor to a model running in production, in the order that makes the next piece legible.

**Scope.** Image formation through deployment: sensors and optics, classical geometry, data and evaluation, the architectures and training that sit on them, the task families built from them, and what breaks in production. Not robotics control, not graphics for its own sake, and not general machine learning without a vision consequence.

**Evidence.** Primary sources only: the paper, the specification, the official model card, the repository, or the documentation of whoever maintains the tool. Every number behind an entry carries all the fields set out in [What earns a place](#what-earns-a-place), or it is not used, and [misc/notes/changelog.md](misc/notes/changelog.md) counts what was checked and what was turned away.

**Proof.** Every section ends in a benchmark under [misc/benchmarks/](misc/benchmarks/common/README.md): the source, the pinned environment, the machine, the raw numbers and the analysis, all committed. Run them.

Section 1 is a path through the rest. Read it top to bottom before using the numbered sections as a reference. The rules the list is built to are in [misc/notes/conventions.md](misc/notes/conventions.md).

## Contents

- [1. Start here: the minimum mental model](#1-start-here-the-minimum-mental-model)
- [2. Image formation: optics, sensors, the ISP, colour, noise](#2-image-formation-optics-sensors-the-isp-colour-noise)
  - [Optics and projection](#optics-and-projection)
  - [Sensors and noise](#sensors-and-noise)
  - [Colour](#colour)
  - [The image signal processor](#the-image-signal-processor)
- [3. Classical foundations: filtering, features, multi-view geometry](#3-classical-foundations-filtering-features-multi-view-geometry)
  - [Sampling and filtering](#sampling-and-filtering)
  - [Features and correspondence](#features-and-correspondence)
  - [Calibration and two-view geometry](#calibration-and-two-view-geometry)
  - [Estimation and bundle adjustment](#estimation-and-bundle-adjustment)
- [4. Datasets, labels and splits: where ground truth comes from and how it lies](#4-datasets-labels-and-splits-where-ground-truth-comes-from-and-how-it-lies)
  - [The datasets that set the terms](#the-datasets-that-set-the-terms)
  - [Annotation and label noise](#annotation-and-label-noise)
  - [Splits, leakage and duplication](#splits-leakage-and-duplication)
  - [Documentation and audit](#documentation-and-audit)
- [5. Evaluation: IoU, mAP, protocols, and the ways a metric misleads](#5-evaluation-iou-map-protocols-and-the-ways-a-metric-misleads)
  - [What the detection metrics compute](#what-the-detection-metrics-compute)
  - [Protocols and reporting](#protocols-and-reporting)
  - [Segmentation and dense metrics](#segmentation-and-dense-metrics)
  - [How a metric misleads](#how-a-metric-misleads)
- [6. Convolutional architectures](#6-convolutional-architectures)
  - [Foundations](#foundations)
  - [Depth, residuals and width](#depth-residuals-and-width)
  - [Efficient convolutional designs](#efficient-convolutional-designs)
  - [Recipes against architectures](#recipes-against-architectures)
- [7. Attention, vision transformers and hybrids](#7-attention-vision-transformers-and-hybrids)
  - [Attention](#attention)
  - [Vision transformers](#vision-transformers)
  - [Data and recipes](#data-and-recipes)
  - [Hierarchies and hybrids](#hierarchies-and-hybrids)
- [8. Training: objectives, augmentation, schedules, regularisation](#8-training-objectives-augmentation-schedules-regularisation)
  - [Objectives](#objectives)
  - [Augmentation](#augmentation)
  - [Schedules and optimisation](#schedules-and-optimisation)
  - [Regularisation and normalisation](#regularisation-and-normalisation)
- [9. Self-supervised learning and vision foundation models](#9-self-supervised-learning-and-vision-foundation-models)
  - [Contrastive learning](#contrastive-learning)
  - [Self-distillation and masked modelling](#self-distillation-and-masked-modelling)
  - [Vision foundation models and weights](#vision-foundation-models-and-weights)
  - [Evaluating representations](#evaluating-representations)
- [10. Detection and segmentation](#10-detection-and-segmentation)
  - [Detector families](#detector-families)
  - [Set prediction and anchor-free designs](#set-prediction-and-anchor-free-designs)
  - [Segmentation](#segmentation)
  - [Postprocessing and what ships](#postprocessing-and-what-ships)
- [11. Video: temporal modelling and tracking](#11-video-temporal-modelling-and-tracking)
  - [Video datasets and their protocols](#video-datasets-and-their-protocols)
  - [Temporal modelling](#temporal-modelling)
  - [Tracking metrics](#tracking-metrics)
  - [Tracking](#tracking)
- [12. 3D: depth, stereo, SfM, SLAM, radiance fields and splatting](#12-3d-depth-stereo-sfm-slam-radiance-fields-and-splatting)
  - [Depth and stereo](#depth-and-stereo)
  - [Structure from motion](#structure-from-motion)
  - [Simultaneous localisation and mapping](#simultaneous-localisation-and-mapping)
  - [Radiance fields and splatting](#radiance-fields-and-splatting)
- [13. Generative vision: diffusion, editing, control](#13-generative-vision-diffusion-editing-control)
  - [What the scores measure](#what-the-scores-measure)
  - [Diffusion and its samplers](#diffusion-and-its-samplers)
  - [Latent and text-conditioned systems](#latent-and-text-conditioned-systems)
  - [Control and editing](#control-and-editing)
- [14. Vision-language models](#14-vision-language-models)
  - [Contrastive image-text pretraining](#contrastive-image-text-pretraining)
  - [Generative vision-language models](#generative-vision-language-models)
  - [Open weights and model cards](#open-weights-and-model-cards)
  - [Benchmarks and contamination](#benchmarks-and-contamination)
- [15. Efficiency and deployment: quantisation, distillation, compilers, edge, NPU](#15-efficiency-and-deployment-quantisation-distillation-compilers-edge-npu)
  - [Quantisation](#quantisation)
  - [Distillation, pruning and sparsity](#distillation-pruning-and-sparsity)
  - [Compilers and runtimes](#compilers-and-runtimes)
  - [Edge, accelerators and measurement](#edge-accelerators-and-measurement)
- [16. Robustness and failure modes: distribution shift, adversarial, bias, safety](#16-robustness-and-failure-modes-distribution-shift-adversarial-bias-safety)
  - [Distribution shift](#distribution-shift)
  - [Corruptions and synthetic perturbation](#corruptions-and-synthetic-perturbation)
  - [Adversarial robustness](#adversarial-robustness)
  - [Bias, calibration and safety](#bias-calibration-and-safety)
- [Watchlist](#watchlist)
  - [Images, geometry and convolutional designs](#images-geometry-and-convolutional-designs)
  - [Attention and self-supervision](#attention-and-self-supervision)
  - [Tasks and generative systems](#tasks-and-generative-systems)
- [What earns a place](#what-earns-a-place)
- [License](#license)

## 1. Start here: the minimum mental model

Each entry assumes only the ones before it, so the order is the instruction.

1. [Recovering High Dynamic Range Radiance Maps from Photographs](https://pauldebevec.com/Research/HDR/) - Why a stored pixel value says nothing about radiance until the camera's response curve is known.
2. [Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) - Which distortion terms a calibration routine solves for, and so which lens errors it leaves in.
3. [A Pixel Is Not A Little Square](https://www.alvyray.com/Memos/CG/Microsoft/6_pixel.pdf) - Why treating a sample as a little square breaks every resampling and alignment step after it.
4. [A guide to convolution arithmetic for deep learning](https://arxiv.org/abs/1603.07285) - Why a padding or stride choice moves where each output value sits on the input grid.
5. [ImageNet Large Scale Visual Recognition Challenge](https://arxiv.org/abs/1409.0575) - Where the task definition and the scoring rule behind a top-one accuracy figure are written down.
6. [ImageNet Classification with Deep Convolutional Neural Networks](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) - What a convolution stack trained end to end on a labelled benchmark learns in place of designed features.
7. [Understanding deep learning requires rethinking generalization](https://arxiv.org/abs/1611.03530) - Why fitting the training labels and generalising to new images are separate events.
8. [Are we done with ImageNet?](https://arxiv.org/abs/2006.07159) - What the single label per image assumption hides when a picture holds several objects.
9. [MLPerf Inference Benchmark](https://arxiv.org/abs/1911.02549) - Why a latency figure needs a scenario, a tail percentile and a timer boundary before it can be compared.
10. [Hidden Technical Debt in Machine Learning Systems](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/) - Where the costs that arrive after a model ships are named, from entangled features to unseen consumers.

Reproduce it: [misc/benchmarks/01-transfer-function-pixels](misc/benchmarks/01-transfer-function-pixels/README.md), one scene encoded through two transfer curves becomes two different arrays.

## 2. Image formation: optics, sensors, the ISP, colour, noise

### Optics and projection

- [High-Quality Computational Imaging Through Simple Lenses](https://www.cs.ubc.ca/labs/imager/tr/2013/SimpleLensImaging/SimpleLensImaging_Heide2013.pdf) - Why a real lens blurs differently across the frame and across colour channels.
- [A Generic Camera Model and Calibration Method](https://users.aalto.fi/~kannalj1/calibration/Kannala_Brandt_calibration.pdf) - Which polynomial fisheye model a toolbox means when it offers Kannala-Brandt.
- [The Double Sphere Camera Model](https://arxiv.org/abs/1807.08957) - What a wide-angle model has to trade between fitting the lens and inverting the projection in closed form.

### Sensors and noise

- [EMVA Standard 1288](https://www.emva.org/standards-technology/emva-1288/emva-standard-1288-downloads/) - Where dynamic range, read noise and quantum efficiency get definitions a measurement can falsify.
- [Practical Poissonian-Gaussian noise modeling and fitting](https://webpages.tuni.fi/foi/sensornoise.html) - Why raw noise grows with the signal, and how that dependence is fitted from a single frame.
- [Learning to See in the Dark](https://arxiv.org/abs/1805.01934) - What survives in a raw frame when almost no photons arrived.

### Colour

- [Fast Fourier Color Constancy](https://arxiv.org/abs/1611.07596) - Why white balance is an estimate of the illuminant with an error of its own, not a fixed gain.
- [CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/) - Where the piecewise sRGB curve and its conversions to other spaces are kept in a maintained standard.
- [ITU-R BT.709](https://www.itu.int/rec/R-REC-BT.709) - Which primaries and camera encoding curve an unlabelled video frame is assumed to use.
- [ITU-R BT.2100](https://www.itu.int/rec/R-REC-BT.2100) - Which transfer functions a high dynamic range signal may carry, and the display each one assumes.
- [ICC Specifications](https://www.color.org/icc_specs2.xalter) - How a colour space travels between two pipelines that agree on pixels and disagree on colour.

### The image signal processor

- [High-quality linear interpolation for demosaicing](https://www.microsoft.com/en-us/research/publication/high-quality-linear-interpolation-for-demosaicing-of-bayer-patterned-color-images/) - Where the linear demosaicing baseline that later methods are scored against is specified.
- [Unprocessing Images for Learned Raw Denoising](https://arxiv.org/abs/1811.11127) - Which camera pipeline stages, in which order, a processed image is walked back through to resemble raw.
- [Burst photography for high dynamic range and low-light imaging](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/) - Why a phone camera aligns and merges a burst of short frames in place of one long exposure.

Reproduce it: [misc/benchmarks/02-signal-dependent-noise](misc/benchmarks/02-signal-dependent-noise/README.md), noise that grows with the signal, and a denoiser tuned at one exposure failing at the others.

## 3. Classical foundations: filtering, features, multi-view geometry

### Sampling and filtering

- [Computer Vision: Algorithms and Applications](https://szeliski.org/Book/) - Where the resampling and pyramid machinery the later papers assume is derived in one place.
- [The Laplacian Pyramid as a Compact Image Code](https://persci.mit.edu/pub_abstracts/pyramid83_abs.html) - Why a smoothing filter and a decimation step have to be chosen together.
- [On Aliased Resizing and Surprising Subtleties in GAN Evaluation](https://arxiv.org/abs/2104.11222) - Why the same resize call returns different pixels from different libraries.
- [Finding Edges and Lines in Images](https://dspace.mit.edu/handle/1721.1/6939) - Which criteria the Canny operator is derived from, and what each one trades against the others.
- [Feature Detection with Automatic Scale Selection](https://people.kth.se/~tony/papers/cvap198.pdf) - How a detector picks the scale it responds at from the image itself.

### Features and correspondence

- [A Combined Corner and Edge Detector](https://bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf) - Why the Harris corner test rejects edges and responds only where two gradients meet.
- [Distinctive Image Features from Scale-Invariant Keypoints](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) - Where the scale-invariant descriptor and the nearest neighbour ratio test are defined.
- [SuperPoint](https://arxiv.org/abs/1712.07629) - How a keypoint detector is trained from synthetic shapes and homographic warps of real images.
- [SuperGlue](https://arxiv.org/abs/1911.11763) - How correspondence is posed as an assignment between two sets of keypoints.
- [Image Matching across Wide Baselines](https://arxiv.org/abs/2003.01587) - How a matching benchmark scores features by the camera pose they recover, not by match counts.

### Calibration and two-view geometry

- [A Flexible New Technique for Camera Calibration](https://www.microsoft.com/en-us/research/project/a-flexible-new-technique-for-camera-calibration-2) - Where the planar target calibration that toolboxes implement is specified.
- [Determining the epipolar geometry and its uncertainty](https://www.microsoft.com/en-us/research/publication/determining-epipolar-geometry-uncertainty-review) - Why a recovered fundamental matrix depends on coordinate normalisation and on the cost minimised.
- [Recognising Panoramas](https://www.cs.ubc.ca/~lowe/papers/brown03.pdf) - Why homographies estimated pair by pair drift apart across a panorama.

### Estimation and bundle adjustment

- [Random Sample Consensus](https://www.sri.com/publication/artificial-intelligence-pubs/random-sample-consensus-a-paradigm-for-model-fitting-with-applications-to-image-analysis-and-automated-cartography/) - Where fitting a model by rejecting most of the data is first stated as a method.
- [Locally Optimized RANSAC](https://cmp.felk.cvut.cz/ftp/articles/matas/chum-dagm03.pdf) - Where the leading hypothesis is refined by local optimisation inside the sampling loop.
- [MAGSAC++](https://arxiv.org/abs/1912.05909) - How a robust estimator scores a model when the inlier threshold is marginalised away.
- [Bundle Adjustment - A Modern Synthesis](https://dumas.ccsd.cnrs.fr/IMAG/inria-00590128v1) - Where the cost, the sparse normal equations and the gauge freedom are set out together.
- [Ceres Solver](https://ceres-solver.org/) - Which linear solver and robust loss a bundle adjustment needs before it runs on real data.

Reproduce it: [misc/benchmarks/03-gaussian-against-box-blur](misc/benchmarks/03-gaussian-against-box-blur/README.md), a box blur inverting contrast at frequencies where a Gaussian stays positive.

## 4. Datasets, labels and splits: where ground truth comes from and how it lies

### The datasets that set the terms

- [The PASCAL Visual Object Classes (VOC) Challenge](https://www.robots.ox.ac.uk/~vgg/projects/pascal/VOC/pubs/everingham10.html) - Where the annotation guidelines and the difficult flag that later benchmarks inherited are written down.
- [Microsoft COCO](https://arxiv.org/abs/1405.0312) - What counts as one instance, and when a region is marked as crowd and not labelled.
- [LVIS](https://openaccess.thecvf.com/content_CVPR_2019/html/Gupta_LVIS_A_Dataset_for_Large_Vocabulary_Instance_Segmentation_CVPR_2019_paper.html) - Why a long-tail vocabulary is labelled federated, with each image checked for only some categories.

### Annotation and label noise

- [From ImageNet to Image Classification](https://arxiv.org/abs/2005.11295) - How the crowd validation step that built the benchmark decided which images and labels survived.
- [Human uncertainty makes classification more robust](https://arxiv.org/abs/1908.07086) - Where annotator disagreement is kept as a soft label and not voted away.
- [Confident Learning](https://arxiv.org/abs/1911.00068) - How a label error estimate is produced, and the noise assumption it rests on.
- [Pervasive Label Errors in Test Sets](https://arxiv.org/abs/2103.14749) - How test set label errors are flagged by a model and then confirmed by human review.

### Splits, leakage and duplication

- [Do We Train on Test Data? Purging CIFAR of Near-Duplicates](https://arxiv.org/abs/1902.00423) - Why a test image can sit in the training split as a near copy that no checksum catches.
- [Do ImageNet Classifiers Generalize to ImageNet?](https://proceedings.mlr.press/v97/recht19a) - How a fresh test set is rebuilt from the original collection procedure, and where that procedure cannot be repeated.
- [Identifying Statistical Bias in Dataset Replication](https://arxiv.org/abs/2005.09619) - Why a replacement test set can differ from the original through its own selection step.

### Documentation and audit

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) - Which questions about collection, consent and maintenance a dataset has to answer before it is trusted.
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) - What a model card has to report, results split by group included, before a checkpoint is trusted.
- [Large image datasets: A pyrrhic win for computer vision?](https://openaccess.thecvf.com/content/WACV2021/html/Birhane_Large_Image_Datasets_A_Pyrrhic_Win_for_Computer_Vision_WACV_2021_paper.html) - What an audit of a shipped vision dataset finds inside it, consent included.

Reproduce it: [misc/benchmarks/04-near-duplicate-leakage](misc/benchmarks/04-near-duplicate-leakage/README.md), the same classifier scored under a random split and a group split.

## 5. Evaluation: IoU, mAP, protocols, and the ways a metric misleads

These protocols are different metrics that share a name, and a score produced under one says nothing about a score produced under another.

### What the detection metrics compute

- [Generalized Intersection over Union](https://arxiv.org/abs/1902.09630) - Why overlap cannot rank two candidate boxes that both miss the target.
- [The PASCAL Visual Object Classes Challenge 2007 Development Kit](https://host.robots.ox.ac.uk/pascal/VOC/voc2007/htmldoc/index.html) - Where the overlap threshold and the eleven point interpolated average precision are specified.
- [The PASCAL Visual Object Classes Challenge 2012 Development Kit](https://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html) - Why sampling precision at eleven recall points and integrating it exactly give different scores.
- [cocoeval.py](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py) - Where a COCO average precision is fixed in code, from recall sampling to the per-image detection cap.

### Protocols and reporting

- [LVIS API](https://github.com/lvis-dataset/lvis-api) - Why an average precision from this scorer is not comparable with one from the COCO protocol.
- [Open Images evaluation protocols](https://storage.googleapis.com/openimages/web/evaluation.html) - What a protocol does with a label hierarchy and with boxes that cover a group of objects.
- [Accounting for Variance in Machine Learning Benchmarks](https://arxiv.org/abs/2103.03098) - Whether a gap between two reported scores survives the randomness that produced both.

### Segmentation and dense metrics

- [Panoptic Segmentation](https://arxiv.org/abs/1801.00868) - Where one score covering stuff and things is defined so that segmentation and recognition errors separate.
- [COCO 2018 Panoptic Segmentation Task API](https://github.com/cocodataset/panopticapi) - How void pixels and crowd regions are handled in the code that computes panoptic quality.
- [Boundary IoU](https://arxiv.org/abs/2103.16562) - Why a mask score can rise while the boundary a viewer looks at gets worse.

### How a metric misleads

- [Diagnosing Error in Object Detectors](https://dhoiem.cs.illinois.edu/projects/detectionAnalysis/) - Which kinds of error one average precision folds together, from localisation to background.
- [TIDE](https://arxiv.org/abs/2008.08115) - Why two detectors with one headline score can need different fixes.
- [Evaluating Large-Vocabulary Object Detectors](https://arxiv.org/abs/2102.01066) - How average precision moves when only the calibration of scores across categories changes.

Reproduce it: [misc/benchmarks/05-average-precision-protocols](misc/benchmarks/05-average-precision-protocols/README.md), one set of detections scored under four published average precision protocols.

## 6. Convolutional architectures

### Foundations

- [Very Deep Convolutional Networks](https://arxiv.org/abs/1409.1556) - Why a stack of small kernels can replace one wide kernel, and what the parameter bill becomes.
- [Going Deeper with Convolutions](https://arxiv.org/abs/1409.4842) - Where a layer becomes parallel branches of several kernel sizes, with pointwise reductions to pay for them.
- [Making Convolutional Networks Shift-Invariant Again](https://arxiv.org/abs/1904.11486) - Why a strided network's output can change under a one-pixel shift, and where a blur before subsampling goes.

### Depth, residuals and width

- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) - Where the identity shortcut around a stack of layers is introduced, with the training failure it targets.
- [Identity Mappings in Deep Residual Networks](https://arxiv.org/abs/1603.05027) - Which order of normalisation, activation and addition a residual block uses, and what reaches the shortcut.
- [Wide Residual Networks](https://arxiv.org/abs/1605.07146) - Whether depth or width carries a residual network, tested on small images by moving one at a time.
- [Aggregated Residual Transformations for Deep Neural Networks](https://arxiv.org/abs/1611.05431) - Where grouped convolution enters the residual block as a third axis beside depth and width.
- [Squeeze-and-Excitation Networks](https://arxiv.org/abs/1709.01507) - What a channel reweighting block computes, and what it costs when added to an existing backbone.

### Efficient convolutional designs

- [MobileNets](https://arxiv.org/abs/1704.04861) - Where the cost of a depthwise separable layer is derived and the width and resolution multipliers are defined.
- [Xception](https://arxiv.org/abs/1610.02357) - How the multi-branch block of the Inception family reduces to depthwise separable convolution.
- [MobileNetV2](https://arxiv.org/abs/1801.04381) - Why an inverted bottleneck keeps activation memory inside a mobile budget.

### Recipes against architectures

- [Bag of Tricks for Image Classification](https://arxiv.org/abs/1812.01187) - Where the recipe changes usually credited to architecture are ablated one at a time.
- [EfficientNet](https://arxiv.org/abs/1905.11946) - Where compound scaling is proposed alongside a baseline recipe that changed at the same time.
- [ResNet strikes back](https://arxiv.org/abs/2110.00476) - Why a published baseline accuracy reports its training recipe as much as its architecture.

Reproduce it: [misc/benchmarks/06-padding-stride-geometry](misc/benchmarks/06-padding-stride-geometry/README.md), tensor shapes that match the formula while the feature moves.

## 7. Attention, vision transformers and hybrids

Most comparisons in this section use unequal pretraining data or compute, so the order of entries is a reading order and not a ranking.

### Attention

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Where the scaled dot product operator and the position encoding it needs are defined.
- [Non-local Neural Networks](https://arxiv.org/abs/1711.07971) - What a global attention block costs when it is dropped into a convolutional stack.
- [On the Relationship between Self-Attention and Convolutional Layers](https://arxiv.org/abs/1911.03584) - Whether an attention layer can express a convolution, which decides what comparing the two means.

### Vision transformers

- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) - Where an image becomes a sequence of patch tokens fed to an unmodified transformer encoder.
- [Training data-efficient image transformers](https://arxiv.org/abs/2012.12877) - How a vision transformer is trained on a public corpus with a teacher network and heavy augmentation.
- [Conditional Positional Encodings for Vision Transformers](https://arxiv.org/abs/2102.10882) - Why a fixed position embedding has to be interpolated when the input resolution changes.
- [Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) - Why a trained vision transformer stores high-norm tokens in background patches, and where extra tokens give them room.

### Data and recipes

- [How to train your ViT?](https://arxiv.org/abs/2106.10270) - How augmentation, corpus size and compute trade against each other under one protocol.
- [Better plain ViT baselines for ImageNet-1k](https://arxiv.org/abs/2205.01580) - How much of the gap between a plain vision transformer and a convolutional baseline was recipe.
- [Vision Transformer and MLP-Mixer Architectures](https://github.com/google-research/vision_transformer) - Which checkpoint was pretrained on which corpus, stated for each released file.

### Hierarchies and hybrids

- [Pyramid Vision Transformer](https://arxiv.org/abs/2102.12122) - Why dense prediction needs a feature pyramid that a single-scale token grid cannot give.
- [Swin Transformer](https://arxiv.org/abs/2103.14030) - How windowed attention makes cost grow with image area and not with its square.
- [A ConvNet for the 2020s](https://arxiv.org/abs/2201.03545) - What a convolutional network reaches when it borrows the transformer recipe and block design step by step.
- [MetaFormer Is Actually What You Need for Vision](https://arxiv.org/abs/2111.11418) - Whether the attention operator or the block around it is doing the work.

Reproduce it: [misc/benchmarks/07-attention-against-convolution-scaling](misc/benchmarks/07-attention-against-convolution-scaling/README.md), attention and convolution cost fitted over a token count sweep.

## 8. Training: objectives, augmentation, schedules, regularisation

### Objectives

- [When Does Label Smoothing Help?](https://arxiv.org/abs/1906.02629) - What label smoothing does to the clusters a classifier forms in its penultimate layer.
- [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002) - What a dense grid of mostly background positions does to cross entropy, and how the loss is reweighted.
- [The Lovász-Softmax loss](https://arxiv.org/abs/1705.08790) - Why optimising an overlap measure directly differs from optimising it pixel by pixel.

### Augmentation

- [mixup](https://arxiv.org/abs/1710.09412) - Why a training target can be a blend of two labels.
- [CutMix](https://arxiv.org/abs/1905.04899) - Why a pasted region is wasted unless the label is mixed in proportion to its area.
- [AutoAugment](https://arxiv.org/abs/1805.09501) - Where augmentation becomes a policy searched for each dataset.
- [RandAugment](https://arxiv.org/abs/1909.13719) - Whether a policy search buys anything that a single strength setting cannot.
- [Fixing the train-test resolution discrepancy](https://arxiv.org/abs/1906.06423) - Why random-resized crops make the right test resolution differ from the training crop size.

### Schedules and optimisation

- [SGDR](https://arxiv.org/abs/1608.03983) - Where the cosine schedule that recipes reuse without its restarts is defined.
- [Accurate, Large Minibatch SGD](https://arxiv.org/abs/1706.02677) - Where the linear learning rate scaling rule and gradual warmup are stated for large batches.
- [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101) - Why weight decay and an added squared penalty stop being equivalent under an adaptive optimiser.
- [Mixed Precision Training](https://arxiv.org/abs/1710.03740) - Why half-precision training keeps a single-precision copy of the weights and scales the loss.
- [Image classification reference training scripts](https://github.com/pytorch/vision/blob/v0.20.0/references/classification/README.md) - Where the exact flags behind each reference checkpoint are written down.

### Regularisation and normalisation

- [Batch Normalization](https://arxiv.org/abs/1502.03167) - Why a layer whose output depends on the rest of the batch behaves differently in training and inference.
- [Layer Normalization](https://arxiv.org/abs/1607.06450) - Where normalisation moves from the batch axis to the feature axis.
- [Group Normalization](https://arxiv.org/abs/1803.08494) - What breaks in batch statistics when each device holds too few images to estimate them.
- [Rethinking "Batch" in BatchNorm](https://arxiv.org/abs/2105.07576) - Why a model scores differently when its test-time batch statistics are not the ones it trained with.
- [Deep Networks with Stochastic Depth](https://arxiv.org/abs/1603.09382) - Where whole residual blocks are dropped at random during training, the regulariser behind drop path.

Reproduce it: [misc/benchmarks/08-augmentation-label-geometry](misc/benchmarks/08-augmentation-label-geometry/README.md), three ways of handling a box label under five augmentations.

## 9. Self-supervised learning and vision foundation models

Frozen feature accuracies in this section come from different probe protocols and cannot be compared across entries.

### Contrastive learning

- [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748) - Where the InfoNCE objective shared by the contrastive methods below is written down.
- [SimCLR](https://arxiv.org/abs/2002.05709) - Why the augmentation list, not the loss, decides what the representation keeps.
- [MoCo](https://arxiv.org/abs/1911.05722) - How the supply of negatives is decoupled from the batch that has to fit in memory.
- [Alignment and Uniformity on the Hypersphere](https://arxiv.org/abs/2005.10242) - Which two properties a contrastive loss trades, each measurable without a downstream task.

### Self-distillation and masked modelling

- [Bootstrap your own latent](https://arxiv.org/abs/2006.07733) - Whether a joint embedding method needs negatives to stay off a constant output.
- [Exploring Simple Siamese Representation Learning](https://arxiv.org/abs/2011.10566) - Which single operation keeps a Siamese network from collapsing to one vector.
- [DINO](https://arxiv.org/abs/2104.14294) - Where centring and sharpening stand in for negatives and the nearest neighbour probe becomes routine.
- [BEiT](https://arxiv.org/abs/2106.08254) - What a masked prediction target inherits from the tokeniser that produced it.
- [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377) - Why reconstructing pixels teaches anything when most of the image is hidden from the encoder.

### Vision foundation models and weights

- [DINOv2](https://arxiv.org/abs/2304.07193) - Where the scaling work moves from the objective to the curation of the pretraining corpus.
- [Model Card for DINOv2](https://github.com/facebookresearch/dinov2/blob/main/MODEL_CARD.md) - Which checkpoints carry registers, and which probe produced each frozen feature number.
- [Model Card for DINOv3](https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md) - Where the licence terms stop being permissive and the satellite-trained weights are listed apart.

### Evaluating representations

- [How Well Do Self-Supervised Models Transfer?](https://openaccess.thecvf.com/content/CVPR2021/html/Ericsson_How_Well_Do_Self-Supervised_Models_Transfer_CVPR_2021_paper.html) - Where many-shot linear accuracy stops predicting detection and dense prediction.
- [VTAB](https://arxiv.org/abs/1910.04867) - Where the adaptation protocol is fixed so that two representations can be compared.
- [Understanding Dimensional Collapse in Contrastive Self-supervised Learning](https://arxiv.org/abs/2110.09348) - What the spectrum of an embedding exposes that a probe accuracy hides.

Reproduce it: [misc/benchmarks/09-linear-probe-against-nearest-neighbour](misc/benchmarks/09-linear-probe-against-nearest-neighbour/README.md), two probes ranking the same representations in opposite orders.

## 10. Detection and segmentation

Most latency figures in this section leave preprocessing and non-maximum suppression outside the timer, so they compare neither with each other nor with a deployed system.

### Detector families

- [Faster R-CNN](https://arxiv.org/abs/1506.01497) - Where proposals move inside the network and anchors become the assignment rule.
- [SSD](https://arxiv.org/abs/1512.02325) - How a single pass predicts boxes from default anchors on several feature maps at once.
- [Feature Pyramid Networks for Object Detection](https://arxiv.org/abs/1612.03144) - Why a box of a given size is assigned to one pyramid level and not another.
- [YOLOv3](https://arxiv.org/abs/1804.02767) - How a grid-based single-stage detector predicts boxes at three scales from one network.
- [Cascade R-CNN](https://arxiv.org/abs/1712.00726) - Why a detector trained at one overlap threshold degrades when scored at a higher one.

### Set prediction and anchor-free designs

- [FCOS](https://arxiv.org/abs/1904.01355) - What a detector loses and keeps when the anchor box and its hyperparameters are removed.
- [Adaptive Training Sample Selection](https://arxiv.org/abs/1912.02424) - Whether anchor-free and anchor-based detectors differ in anything but how positives are chosen.
- [End-to-End Object Detection with Transformers](https://arxiv.org/abs/2005.12872) - Where bipartite matching replaces both the anchor grid and the duplicate removal pass.
- [Deformable DETR](https://arxiv.org/abs/2010.04159) - Where attention to a few sampled points around each reference replaces dense attention in set prediction.

### Segmentation

- [U-Net](https://arxiv.org/abs/1505.04597) - Why skip connections between encoder and decoder decide how sharp a mask boundary is.
- [Mask R-CNN](https://arxiv.org/abs/1703.06870) - Why rounding a pooled region to the feature grid misaligns its mask, and what exact-coordinate sampling changes.
- [Segment Anything](https://arxiv.org/abs/2304.02643) - Why one click returns several candidate masks with no class attached, and how they are ranked.

### Postprocessing and what ships

- [NonMaxSuppression](https://github.com/onnx/onnx/blob/main/docs/Operators.md#NonMaxSuppression) - Where a runtime keeps a box exactly at the overlap threshold, and which box formats it accepts.
- [Soft-NMS](https://arxiv.org/abs/1704.04503) - Why a neighbouring object disappears at one overlap threshold and survives at another.
- [Detectron2](https://github.com/facebookresearch/detectron2) - Where the postprocessing defaults behind several published numbers can be read as code.
- [YOLOv10](https://arxiv.org/abs/2405.14458) - Where duplicate removal is trained into the network and not left to a separate postprocessing step.

Reproduce it: [misc/benchmarks/10-nms-threshold-operating-point](misc/benchmarks/10-nms-threshold-operating-point/README.md), the suppression threshold moving the operating point, and what suppression costs.

## 11. Video: temporal modelling and tracking

### Video datasets and their protocols

- [Temporal Segment Networks](https://arxiv.org/abs/1608.00859) - Why a video accuracy depends on how many snippets were sampled and averaged at test time.
- [The Kinetics Human Action Video Dataset](https://arxiv.org/abs/1705.06950) - Why two groups training on the same named benchmark may not hold the same videos.
- [Something-Something](https://arxiv.org/abs/1706.04261) - Where class labels are defined by motion templates, so a single frame cannot carry the class.
- [PySlowFast Model Zoo and Baselines](https://github.com/facebookresearch/SlowFast/blob/main/MODEL_ZOO.md) - Where the crop and clip count at test time sits beside every accuracy it produced.

### Temporal modelling

- [Quo Vadis, Action Recognition?](https://arxiv.org/abs/1705.07750) - Why a video backbone starts from image weights inflated along the time axis.
- [A Closer Look at Spatiotemporal Convolutions](https://arxiv.org/abs/1711.11248) - Whether a space-time filter has to be solid or can be split into space and then time.
- [TSM](https://arxiv.org/abs/1811.08383) - How shifting channels along time gives a two-dimensional network temporal reach with no extra convolution.
- [SlowFast Networks for Video Recognition](https://arxiv.org/abs/1812.03982) - Why the frame sampling rate is an architectural choice and not a property of the video.
- [TimeSformer](https://arxiv.org/abs/2102.05095) - How attention is factorised over space and time so that a video transformer fits in memory.

### Tracking metrics

- [MOT16](https://arxiv.org/abs/1603.00831) - Which public detections a tracker must consume before two tracking numbers can be compared.
- [Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking](https://arxiv.org/abs/1609.01775) - Where identity is scored over whole trajectories, in a paper whose dataset was later withdrawn.
- [HOTA](https://link.springer.com/article/10.1007/s11263-020-01375-2) - Where detection accuracy and association accuracy become two numbers that can disagree.
- [MOTChallenge Official Evaluation Kit](https://github.com/JonathonLuiten/TrackEval/blob/master/docs/MOTChallenge-Official/Readme.md) - Which implementation settles a disagreement about how a tracking metric was computed.

### Tracking

- [Simple Online and Realtime Tracking](https://arxiv.org/abs/1602.00763) - Where a tracker reduces to a motion model and one assignment problem per frame.
- [Deep SORT](https://arxiv.org/abs/1703.07402) - What an appearance embedding adds to association when box overlap alone is ambiguous.
- [Tracking without bells and whistles](https://arxiv.org/abs/1903.05625) - How much of a tracking score belongs to the detector and not the tracker.
- [ByteTrack](https://arxiv.org/abs/2110.06864) - Where low-scoring detections are kept for a second association pass and not discarded.

Reproduce it: [misc/benchmarks/11-per-frame-against-identity](misc/benchmarks/11-per-frame-against-identity/README.md), per-frame accuracy rising while identity consistency falls.

## 12. 3D: depth, stereo, SfM, SLAM, radiance fields and splatting

### Depth and stereo

- [Stereo Matching by Training a Convolutional Neural Network](https://arxiv.org/abs/1510.05970) - Where the matching cost is learned while the aggregation around it stays classical.
- [RAFT](https://arxiv.org/abs/2003.12039) - How dense flow is estimated by iterative updates over an all-pairs correlation volume.
- [RAFT-Stereo](https://arxiv.org/abs/2109.07547) - What the same iterative update becomes when correspondence is restricted to rectified rows.
- [Monodepth2](https://arxiv.org/abs/1806.01260) - What one camera can learn about depth from its own motion, and where the scale has to come from.
- [Towards Robust Monocular Depth Estimation](https://arxiv.org/abs/1907.01341) - Where the scale-and-shift-invariant protocol for comparing monocular depth across datasets is defined.

### Structure from motion

- [COLMAP](https://github.com/colmap/colmap) - Why an incremental reconstruction registers one image at a time, and where that order lets error drift.
- [Global Structure-from-Motion Revisited](https://arxiv.org/abs/2407.20219) - Whether solving rotations and translations globally can match incremental accuracy.
- [ETH3D Multi-View Evaluation Program](https://github.com/ETH3D/multi-view-evaluation) - Why a reconstruction score is unreadable without the tolerance it was computed at.

### Simultaneous localisation and mapping

- [A Photometrically Calibrated Benchmark For Monocular Visual Odometry](https://arxiv.org/abs/1607.02555) - Which response, vignetting and exposure calibration a capture needs before a trajectory error is trusted.
- [Direct Sparse Odometry](https://arxiv.org/abs/1607.02565) - Why photometric calibration becomes part of the algorithm when image intensities replace keypoints.
- [ORB-SLAM3](https://arxiv.org/abs/2007.11898) - Why a feature-based system keeps several maps and merges them when tracking is lost and regained.
- [DROID-SLAM](https://arxiv.org/abs/2108.10869) - Where a learned front end meets a dense bundle adjustment back end, and what that costs in memory.

### Radiance fields and splatting

- [NeRF](https://arxiv.org/abs/2003.08934) - Where view synthesis becomes a volume rendering problem fitted one scene at a time.
- [Instant Neural Graphics Primitives](https://github.com/NVlabs/instant-ngp) - How a multiresolution hash table moves an input encoding's work from network weights into lookups.
- [3D Gaussian Splatting](https://github.com/graphdeco-inria/gaussian-splatting) - What replaces marching along rays when a scene is a set of rasterised primitives and not a field.

Reproduce it: [misc/benchmarks/12-depth-error-against-distance](misc/benchmarks/12-depth-error-against-distance/README.md), depth error growing with distance under a fixed disparity error.

## 13. Generative vision: diffusion, editing, control

Distributional scores in this section depend on the feature network, the sample count and the resize, and a small gap between two of them is not a result.

### What the scores measure

- [GANs Trained by a Two Time-Scale Update Rule](https://arxiv.org/abs/1706.08500) - Where the Fréchet Inception Distance that generative results are quoted in is defined.
- [Rethinking FID](https://arxiv.org/abs/2401.09603) - What the feature network and the sample count contribute to the number before the images do.
- [GenEval](https://arxiv.org/abs/2310.11513) - How prompt adherence is scored object by object, which a distributional score cannot see.

### Diffusion and its samplers

- [Generative Modeling by Estimating Gradients of the Data Distribution](https://arxiv.org/abs/1907.05600) - Why sampling can follow the gradient of a log density that is never normalised.
- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) - Where the noise prediction objective is fixed as a reweighted form of the variational bound.
- [Score-Based Generative Modeling through Stochastic Differential Equations](https://arxiv.org/abs/2011.13456) - Why the discrete noise schedule and the score view are one continuous process.
- [Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) - Why the step count is a sampler choice and not a property of the trained network.
- [Elucidating the Design Space of Diffusion-Based Generative Models](https://arxiv.org/abs/2206.00364) - Which choices of noise level, preconditioning and solver separate a sampler from its training.
- [Consistency Models](https://arxiv.org/abs/2303.01469) - How a diffusion model is distilled to sample in one or a few steps.

### Latent and text-conditioned systems

- [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) - Why the process runs in an autoencoder latent, and what that autoencoder throws away.
- [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598) - Why the guidance scale in a text-conditioned interface exists and what it trades away.
- [Stable Diffusion v1 Model Card](https://github.com/CompVis/stable-diffusion/blob/main/Stable_Diffusion_v1_Model_Card.md) - What a released text-to-image checkpoint was trained on and what its own card says it fails at.
- [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748) - Whether the convolutional backbone was ever the part doing the work.
- [Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) - Where a straight-path objective meets separate weights for text and image tokens.

### Control and editing

- [SDEdit](https://arxiv.org/abs/2108.01073) - How far an image can be changed by adding noise and letting the reverse process finish.
- [Prompt-to-Prompt Image Editing with Cross Attention Control](https://arxiv.org/abs/2208.01626) - Why cross-attention maps are the handle for changing one object and keeping the rest.
- [ControlNet](https://arxiv.org/abs/2302.05543) - How a spatial condition attaches to a frozen checkpoint without retraining it.

Reproduce it: [misc/benchmarks/13-distributional-metric-sensitivity](misc/benchmarks/13-distributional-metric-sensitivity/README.md), a distributional distance moving under changes a viewer cannot see.

## 14. Vision-language models

### Contrastive image-text pretraining

- [CLIP](https://arxiv.org/abs/2103.00020) - Where classification by text prompt is defined, and what it needs from the caption corpus.
- [Sigmoid Loss for Language Image Pre-Training](https://arxiv.org/abs/2303.15343) - Why a pairwise sigmoid loss frees the batch size from carrying the whole negative set.
- [LAION-5B](https://arxiv.org/abs/2210.08402) - Which filtering steps decided what an openly released corpus kept, and what they let through.
- [DataComp](https://arxiv.org/abs/2304.14108) - What changes when the training recipe is frozen and only the data is allowed to move.

### Generative vision-language models

- [BLIP-2](https://arxiv.org/abs/2301.12597) - What a learned query bottleneck does when the image encoder and the language model both stay frozen.
- [LLaVA](https://arxiv.org/abs/2304.08485) - Where the instruction data for a conversational image model is synthesised by a text-only model.
- [Prismatic VLMs](https://arxiv.org/abs/2402.07865) - What happens when the connector, the encoder and the data are varied one at a time.

### Open weights and model cards

- [Model Card: CLIP](https://github.com/openai/CLIP/blob/main/model-card.md) - What the people who trained an image-text model say it was not built to do.
- [OpenCLIP](https://github.com/mlfoundations/open_clip) - Why an overlap audit between a benchmark and a corpus needs checkpoints whose corpus is named.
- [Molmo and PixMo](https://arxiv.org/abs/2409.17146) - Where training captions are collected from spoken descriptions and not distilled from a closed model.
- [Llama 3.2-Vision](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD_VISION.md) - Why a stated knowledge cutoff is the field an evaluation date has to be checked against.

### Benchmarks and contamination

- [MMBench](https://arxiv.org/abs/2307.06281) - Where answer options are rotated across repeated queries so a model scores only when it agrees with itself.
- [MMMU](https://arxiv.org/abs/2311.16502) - Why a multimodal exam score depends on an answer extraction rule that quoted numbers leave out.
- [POPE](https://arxiv.org/abs/2305.10355) - How object hallucination is measured with yes or no questions about objects that are absent.
- [MMStar](https://arxiv.org/abs/2403.20330) - How much of a multimodal score survives when the image is removed from the input.
- [VLMEvalKit](https://github.com/open-compass/VLMEvalKit) - Where the prompt template and answer extraction behind a reported score live.

Reproduce it: [misc/benchmarks/14-contamination-audit](misc/benchmarks/14-contamination-audit/README.md), a contamination audit that needs no access to the model.

## 15. Efficiency and deployment: quantisation, distillation, compilers, edge, NPU

Speedups in this section are tied to their own hardware, batch size and timer boundary, and a speedup from one setting says nothing about another.

### Quantisation

- [Quantization and Training of Neural Networks](https://arxiv.org/abs/1712.05877) - Where simulated quantisation in training and the integer-only inference pipeline are specified together.
- [TensorFlow Lite 8-bit quantization specification](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/g3doc/performance/quantization_spec.md) - Why a model quantised by another tool fails on a runtime unless its zero points and ranges match.
- [Up or Down? Adaptive Rounding for Post-Training Quantization](https://arxiv.org/abs/2004.10568) - Where rounding each weight up or down is learned from calibration data.
- [A White Paper on Neural Network Quantization](https://arxiv.org/abs/2106.08295) - Where post-training quantisation and its fine-tuning fallback are set out as one decision procedure.
- [SmoothQuant](https://arxiv.org/abs/2211.10438) - Why activation outliers in transformer layers break per-tensor eight-bit quantisation, and where they are moved.

### Distillation, pruning and sparsity

- [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) - Where softened outputs with a temperature become the training target for a smaller model.
- [Knowledge distillation: A good teacher is patient and consistent](https://arxiv.org/abs/2106.05237) - Which schedule length and augmentation consistency a distillation run needs before its result reproduces.
- [What is the State of Neural Network Pruning?](https://arxiv.org/abs/2003.03033) - Why two pruning results with the same headline cannot be compared without a shared baseline.
- [Accelerating Sparse Deep Neural Networks](https://arxiv.org/abs/2104.08378) - Why pruning speeds up a tensor core only when the zeros follow the pattern the hardware executes.

### Compilers and runtimes

- [Open Neural Network Exchange Intermediate Representation](https://github.com/onnx/onnx/blob/main/docs/IR.md) - Which side is wrong when one graph runs differently on two runtimes that both claim to follow it.
- [Quantize ONNX Models](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html) - How a shipping runtime's post-training pass picks calibration, formats and per-channel scales.
- [TVM](https://arxiv.org/abs/1802.04799) - Why a graph compiler searches schedules for each shape and does not call one vendor library.
- [ExecuTorch](https://github.com/pytorch/executorch) - Where ahead-of-time export and backend delegation replace a Python process as the deployment unit.

### Edge, accelerators and measurement

- [XNNPACK](https://github.com/google/XNNPACK) - Which operators and instruction sets a CPU inference library covers, the list a runtime's fallback depends on.
- [MLComputeUnits](https://developer.apple.com/documentation/coreml/mlcomputeunits) - Why a Core ML latency figure is unreadable until the compute units the model may use are named.
- [Apple Neural Engine Transformers](https://github.com/apple/ml-ane-transformers) - Which tensor layouts and operator choices a neural engine accepts before a transformer runs on it.
- [LoadGen](https://github.com/mlcommons/inference/blob/master/loadgen/README.md) - Where the timer boundary around each query is fixed in code.

Reproduce it: [misc/benchmarks/15-int8-quantisation-accuracy-and-latency](misc/benchmarks/15-int8-quantisation-accuracy-and-latency/README.md), integer quantisation accuracy and latency by layer shape.

## 16. Robustness and failure modes: distribution shift, adversarial, bias, safety

A score on a corruption suite measures the suite as much as the model, so no score in this section transfers to another suite.

### Distribution shift

- [Natural Adversarial Examples](https://arxiv.org/abs/1907.07174) - How a natural test set is built by keeping only images a fixed classifier gets wrong.
- [WILDS](https://arxiv.org/abs/2012.07421) - Where subpopulation shift and domain generalisation are separated into benchmarks with their own splits.
- [Measuring Robustness to Natural Distribution Shifts](https://arxiv.org/abs/2007.00644) - Whether robustness to synthetic perturbation predicts robustness to natural distribution shift.

### Corruptions and synthetic perturbation

- [Benchmarking Neural Network Robustness to Common Corruptions](https://arxiv.org/abs/1903.12261) - Where the corruption suite and its error metric are defined.
- [make_imagenet_c.py](https://github.com/hendrycks/robustness/blob/master/ImageNet-C/create_c/make_imagenet_c.py) - What each corruption name computes before a score is attributed to a model.
- [On Interaction Between Augmentations and Corruptions](https://github.com/facebookresearch/augmentation-corruption) - Where a corruption suite is built to be perceptually unlike the one augmentations were tuned near.
- [3D Common Corruptions](https://github.com/EPFL-VILAB/3DCommonCorruptions) - Which corruptions follow scene geometry, such as depth of field and fog, and so differ from per-pixel noise.

### Adversarial robustness

- [Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572) - Why a small perturbation flips a prediction and how cheaply one is found.
- [Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083) - Where the projected gradient attack and adversarial training are paired under a stated threat model.
- [Obfuscated Gradients Give a False Sense of Security](https://arxiv.org/abs/1802.00420) - Why a defence that only breaks the attacker's gradient fails when the attack is adapted to it.
- [Certified Adversarial Robustness via Randomized Smoothing](https://arxiv.org/abs/1902.02918) - What a guarantee looks like when the norm and the noise level are stated.
- [Adversarial Patch](https://arxiv.org/abs/1712.09665) - Why a printed patch placed in the scene falls outside any norm-bounded threat model.

### Bias, calibration and safety

- [FairFace](https://github.com/joojs/fairface) - What an audit set has to balance before a disparity between groups can be measured.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) - Why a confidence score is not a probability until it is fitted to be one.
- [Can You Trust Your Model's Uncertainty?](https://arxiv.org/abs/1906.02530) - What happens to calibration when the test data stops matching the training data.
- [A Baseline for Detecting Misclassified and Out-of-Distribution Examples](https://arxiv.org/abs/1610.02136) - Where the maximum softmax score becomes the baseline for rejecting inputs a model should not answer.

Reproduce it: [misc/benchmarks/16-corruption-tuning-transfer](misc/benchmarks/16-corruption-tuning-transfer/README.md), a pipeline tuned on one corruption, scored on corruptions held out from tuning.

## Watchlist

Everything below is real but unproven: no item yet has all three of a specification or paper, a shipped implementation, and a public measurement stating every field. Each line says what would promote it. Last checked **2026-10-21**.

### Images, geometry and convolutional designs

- [Deep Joint Demosaicking and Denoising](https://groups.csail.mit.edu/graphics/demosaicnet) - Demosaicing and denoising posed as one learned problem, with no maintained implementation. Enters the core when a maintained implementation is measured against a sequential pipeline.
- [LoFTR](https://arxiv.org/abs/2104.00680) - Detector-free matching whose pose result has been produced only by its authors. Enters the core when an outside group reruns the released configuration and checkpoint and publishes the pose result.
- [ShuffleNet V2](https://arxiv.org/abs/1807.11164) - Design rules derived from measured latency with the precision, warmup and timer boundary unstated. Enters the core when that latency is republished with precision, framework flags, warmup and the timer boundary.
- [Searching for MobileNetV3](https://arxiv.org/abs/1905.02244) - A searched mobile family whose on-device latency headline comes without a timer boundary. Enters the core when that latency is published with batch size, warmup and the timer boundary.

### Attention and self-supervision

- [Stand-Alone Self-Attention in Vision Models](https://arxiv.org/abs/1906.05909) - A backbone with no convolution left, measured only by its authors. Enters the core when released weights let another group reproduce the comparison at the stated budget.
- [Early Convolutions Help Transformers See Better](https://arxiv.org/abs/2106.14881) - A stability finding about the patch stem with no released weights behind it. Enters the core when weights for the compared stems are released with the hardware stated.
- [CoAtNet](https://arxiv.org/abs/2106.04803) - Convolution stacked under attention across growing corpora, with no official code or weights. Enters the core when the authors release weights for the models trained on public data.
- [Scalable Pre-training of Large Autoregressive Image Models](https://arxiv.org/abs/2401.08541) - Autoregressive pretraining on a corpus nobody else holds. Enters the core when it is compared with contrastive and masked baselines at equal data and compute.
- [DINOv3](https://arxiv.org/abs/2508.10104) - A finding that dense features decay over long schedules, measured only on the authors' largest private run. Enters the core when the decay is measured on a released checkpoint with the dense protocol stated.

### Tasks and generative systems

- [Mask2Former](https://arxiv.org/abs/2112.01527) - One mask classification design claimed to serve semantic, instance and panoptic tasks alike. Enters the core when every task's result is published with its checkpoint, protocol and hardware.
- [DreamBooth](https://arxiv.org/abs/2208.12242) - Subject-driven fine-tuning whose evaluation data is public and whose implementation is not. Enters the core when the authors release the training code behind the comparison.
- [FLUX](https://github.com/black-forest-labs/flux) - Open weights from a family with no paper, no specification and no public measurement. Enters the core when a paper or specification and a measurement stating every field are published.
- [Flamingo](https://arxiv.org/abs/2204.14198) - A frozen language model taught to read images, with no released weights or code. Enters the core when weights or an implementation are released with the evaluation protocol.
- [Improved Baselines with Visual Instruction Tuning](https://arxiv.org/abs/2310.03744) - Ablations that credit gains to the connector and the recipe, with checkpoints only for the final models. Enters the core when checkpoints for the ablation rows are released.

## What earns a place

An entry is admitted only when every one of these holds, and the burden of proof sits with the entry.

- It is a primary source: the original paper, the authors' own repository, an official model card or weight page, framework or compiler documentation, a dataset paper or official dataset page, or a standard.
- Its URL resolves to the live canonical copy, never a mirror, an aggregator or a rehost.
- Its line says why a reader would open it, in under one hundred and twenty characters, with no number, no author name and no praise.
- Any number it rests on carries every evidence field in the tables below. A missing field sends it to the watchlist or out, and it is not softened into a caveat.
- It sits in dependency order inside its subsection, and the subsection holds three to six entries. A seventh displaces one, and the pull request names which.
- It enters the core only when a specification or paper, a shipped implementation and a public measurement stating every field all exist at once. Otherwise it waits on the watchlist with the condition that would promote it.
- Each source appears once in the list.

An accuracy claim carries eight fields:

| | Accuracy claim |
|---|---|
| 1 | model and exact checkpoint |
| 2 | dataset, split and version |
| 3 | input resolution and preprocessing |
| 4 | metric with its full definition |
| 5 | protocol, single-scale or test-time augmentation, NMS settings |
| 6 | training data used |
| 7 | hardware |
| 8 | baseline compared against |

A speed claim carries seven:

| | Speed claim |
|---|---|
| 1 | hardware and count |
| 2 | precision |
| 3 | batch size |
| 4 | input resolution |
| 5 | framework and version, with compile flags |
| 6 | warmup and the statistic reported |
| 7 | whether preprocessing and postprocessing are inside the timer |

Every URL points at the live canonical copy, and `misc/scripts/check_links.py` and `misc/scripts/check_format.py` prove it on every push and again weekly.

[CONTRIBUTING.md](CONTRIBUTING.md) has the rules in full.

## License

MIT. Maintained by [@usamahz](https://github.com/usamahz).
