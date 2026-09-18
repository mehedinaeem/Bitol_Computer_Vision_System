# BITOL banana detection dataset

The preserved dataset supports instance-level detection of visible banana surface condition with **0: healthy** and **1: unhealthy**. These are appearance-based labels, not biological diagnosis or beetle species identification.

## Files and format

Images and labels remain in `../detection_dataset/`; they were not moved, relabeled, resized, or repartitioned during publication cleanup.

```text
detection_dataset/
├── images/{train,test}/*.jpg
├── labels/{train,test}/*.txt
├── classes.txt
└── data.yaml                 # Original historical configuration
```

Each image and text label share a stem. Each nonempty row is:

```text
class_id x_center y_center width height
```

Coordinates are normalized by image dimensions; widths/heights must be positive and boxes must lie within image boundaries. Multiple rows describe multiple objects. Filename prefixes are organizational metadata and need not match every annotated object in an image. Class metadata files are excluded from label counts.

## Preserved snapshot

| Partition | Images | Labels | Healthy instances | Unhealthy instances | Instances |
|---|---:|---:|---:|---:|---:|
| Development/training | 1,982 | 1,982 | 2,355 | 2,027 | 4,382 |
| Reported held-out test | 491 | 491 | 878 | 567 | 1,445 |
| **Total** | **2,473** | **2,473** | **3,233** | **2,594** | **5,827** |

Stored image dimensions are 1024 × 1024. The publication model input is 640 × 640; storage files were not converted. Counts include duplicate image bytes and coordinate-flagged annotation rows.

| Partition | Healthy-only images | Unhealthy-only images | Both classes |
|---|---:|---:|---:|
| Train | 944 | 886 | 152 |
| Test | 252 | 192 | 47 |

## Existing audit evidence

The audit created before the cleanup-only instruction is preserved in [audit_summary.json](audit_summary.json) and [validation_report.csv](validation_report.csv). It found:

- Complete image/label pairing, with no missing, orphan, empty, malformed, or invalid-class labels and no active Git conflict markers.
- **119 coordinate issues** in 113 label files: 109 rows in train and 10 in test. In total, 59 right edges and 60 bottom edges exceed normalized bounds under strict comparisons. No coordinates were corrected.
- **218 exact-duplicate image groups**, including **72 spanning train/test**. Duplicate groups count shared hashes, not image pairs. Near duplicates were not assessed.
- A historical semantic-review note for `healthy_0717.txt`; absence of conflict markers does not verify the labeling decision.

[split_manifest.csv](split_manifest.csv) records current membership and SHA-256 image/label hashes. It is an inventory of the supplied split, not a new split or proof of the original experiment's membership. Paths are relative to `detection_dataset/`.

The original `detection_dataset/data.yaml` aliases `val` to `images/test`; it is retained unchanged as historical evidence. The [publication config](../configs/data.yaml) leaves `val: null` because final-experiment validation membership is unknown. The reported held-out test designation is preserved, but statistical independence is not established by the current files.

For future read-only auditing, from the repository root:

```bash
python scripts/validate_dataset.py --report outputs/dataset_validation_report.csv
```

This script does not repair labels or move images. Its expected nonzero status reflects unresolved issues. It was not executed after the cleanup-only instruction.

## Provenance and rights

Collection location/dates, cultivar, device settings, acquisition groups, sampling criteria, annotation rubric/tool, annotator count, and agreement measurements are not documented. No new provenance is inferred. Dataset-specific redistribution rights and a DOI remain unconfirmed; the repository's MIT code license does not establish ownership of images.

Original annotation figures remain in [paper_figures/](../paper_figures/). Historical preparation scripts, logs, notebooks, and intermediate images are preserved in a local archive; see [the archive inventory](../docs/archive_manifest.csv). `annotation_backup/` stays local and excluded from Git.
