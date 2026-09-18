# Bitol Banana Detection Dataset

A YOLO-format object-detection dataset containing images of bananas annotated as **healthy** or **unhealthy**. Each annotation identifies an individual object with a bounding box. Images may contain multiple objects and both classes.

This document describes the dataset files audited on **18 September 2026**. For software installation, training, inference, and historical experiments, see the [project README](../README.md).

## Dataset overview

| Property | Value |
|---|---|
| Task | Object detection |
| Classes | `0: healthy`, `1: unhealthy` |
| Stored images | 2,473 |
| Image dimensions | 1024 × 1024 pixels |
| Annotation files | 2,473 |
| Annotated objects | 5,827 |
| Format | JPG images and YOLO TXT labels |
| Current partitions | Train and test |

These are stored-file counts, including duplicate image content. Object totals include annotations flagged for coordinate issues. The dataset requires the quality corrections described below before supporting final research claims.

## Directory structure

```text
detection_dataset/
├── README.md
├── data.yaml
├── classes.txt
├── images/
│   ├── train/     # 1,982 images
│   └── test/      # 491 images
└── labels/
    ├── train/     # 1,982 annotation files
    └── test/      # 491 annotation files
```

An image and its label share the same filename stem:

```text
images/train/healthy_0091.jpg
labels/train/healthy_0091.txt
```

Files named `classes.txt` are class metadata and are excluded from annotation-file counts. Filename prefixes describe organizational categories; use the annotation rows to determine the actual object classes.

## Split and class statistics

| Split | Images | Share | Label files | Healthy objects | Unhealthy objects | Total objects |
|---|---:|---:|---:|---:|---:|---:|
| Train | 1,982 | 80.15% | 1,982 | 2,355 | 2,027 | 4,382 |
| Test | 491 | 19.85% | 491 | 878 | 567 | 1,445 |
| **Total** | **2,473** | **100%** | **2,473** | **3,233** | **2,594** | **5,827** |

Image-level class presence, calculated from the annotation files:

| Split | Healthy only | Unhealthy only | Both classes |
|---|---:|---:|---:|
| Train | 944 | 886 | 152 |
| Test | 252 | 192 | 47 |
| **Total** | **1,196** | **1,078** | **199** |

For comparison, filenames comprise 1,327 `healthy_*` and 1,146 `unhealthy_*` images. These counts differ from the annotation-based categories above.

## Annotation specification

| Class ID | Class name |
|---|---|
| `0` | `healthy` |
| `1` | `unhealthy` |

Each nonempty label row describes one object:

```text
class_id x_center y_center width height
```

Coordinates are normalized by image width and height. For example, the following illustrative row represents a healthy object centered in the image, with a box covering half its width and one quarter of its height:

```text
0 0.500000 0.500000 0.500000 0.250000
```

For image dimensions `W × H`, convert to pixel coordinates using:

```text
left   = (x_center - width / 2) × W
right  = (x_center + width / 2) × W
top    = (y_center - height / 2) × H
bottom = (y_center + height / 2) × H
```

Centers must lie within `[0, 1]`, widths and heights within `(0, 1]`, and all box edges within the image. A valid text structure does not establish that an object was correctly classified or localized.

## Dataset configuration

[data.yaml](data.yaml) currently contains:

```yaml
train: images/train
val: images/test
test: images/test
nc: 2
names:
  0: healthy
  1: unhealthy
```

**Validation and testing currently use the same images.** There is no separate validation partition. Create disjoint train, validation, and test sets before using validation for model selection and test performance for final reporting. Keep duplicate images and related acquisition groups within one partition.

## Quality audit and known limitations

The repository validator found:

| Check | Train | Test | Total |
|---|---:|---:|---:|
| Missing label files | 0 | 0 | 0 |
| Labels without matching images | 0 | 0 | 0 |
| Empty label files | 0 | 0 | 0 |
| Malformed annotation rows | 0 | 0 | 0 |
| Invalid class IDs | 0 | 0 | 0 |
| Duplicate annotation rows | 0 | 0 | 0 |
| Git conflict markers | 0 | 0 | 0 |
| Invalid box coordinates | 109 | 10 | **119** |

The 119 coordinate issues affect 113 label files: 59 right edges and 60 bottom edges exceed the normalized boundary under strict comparisons. Review each case against the image before correcting it; assess whether the excess is rounding or a substantive annotation error.

A SHA-256 audit found **218 groups of byte-identical images**, including **72 groups spanning train and test**. These are hash-group counts, not duplicate-pair counts. Recompressed duplicates and visually similar images require additional review.

A historical review note identifies `healthy_0717.txt` as requiring a semantic annotation decision. Current active labels contain no conflict markers, but the notes do not establish whether the underlying disagreement was resolved. See the [manual-review list](../manual_review_required.txt) and [recorded alternatives](../conflict_alternatives_manual_review.txt).

### Reproduce annotation validation

From the repository root:

```bash
python3 scripts/validate_yolo_dataset.py \
  --dataset detection_dataset \
  --report outputs/dataset_validation_report.csv
```

The validator uses the Python standard library and requires Python 3.10 or newer. It writes `split`, `category`, `path`, `line`, and `details` columns. The current dataset produces exit status **1** because coordinate issues remain. It checks train/test pairing and annotation structure, but does not audit duplicate image content or semantic label correctness.

The [existing validation report](../dataset_validation_report.csv) provides per-row details. The [project README](../README.md#v-reproducing-the-workflow) includes the exact-byte duplicate audit command.

## Image preparation and split history

The preprocessing scripts resize images directly to 1024 × 1024 using Lanczos resampling. Direct resizing can change the aspect ratio of nonsquare source images.

Two historical split utilities exist:

- `scripts/split_dataset.py` uses sorted, unshuffled 80/20 splits within resized-image folders and copies images only.
- `scripts/split_dataset01.py` shuffles the `healthy03` and `unhealthy03` folders with seed 42, creates an 80/20 split, and copies matching existing labels when available.

Both retain existing destination files. Neither is a verified reconstruction procedure for this complete snapshot. Do not infer that the current dataset was produced by a single clean seed-42 split.

Local archives contain different dataset snapshots:

| Archive | Train | Validation | Test | Total images |
|---|---:|---:|---:|---:|
| `detection_dataset.zip` | 1,698 | 486 | 248 | 2,432 |
| `detection_dataset_80.zip` | 1,982 | — | 491 | 2,473 |

These counts come from archive member listings. Equal counts do not guarantee identical image or label contents. ZIP archives and raw images are excluded from Git; the active detection images and labels are tracked. The local `annotation_backup/` folder is excluded from tracking and is not part of the dataset distribution.

## Visual examples

![Healthy and unhealthy banana ground-truth annotations](../paper_figures/all_classes_annotated_train.png)

These boxes illustrate ground-truth labels, not model predictions. The [figure notebook](../notebooks/paper_class_samples_with_annotations.ipynb) exports PNG and PDF examples. Verify selected image paths and regenerate figures after annotation or split changes.

## Provenance and permitted use

The repository does not document collection locations and dates, camera details, cultivars, acquisition-session identifiers, sampling criteria, annotation tool, annotator count, agreement measurements, or a formal healthy/unhealthy grading rubric. Add these from original records before presenting the dataset as a reproducible research release.

The project's [MIT License](../LICENSE) covers the repository's software. Separate dataset ownership and redistribution terms are not documented; do not infer image permissions solely from the code license. There is no supplied dataset DOI, formal dataset citation, or independently versioned public download.

Before publishing a dataset release, resolve the audit issues, establish independent partitions, document provenance and usage rights, and preserve image/label checksums and split manifests. Cite the exact release or source commit together with the repository title and author; add a formal dataset citation when its bibliographic details are available.
