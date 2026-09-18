# Publication cleanup inventory

## Scope and preservation

This is a working-tree reorganization. No commit, push, release, history rewrite, model training, evaluation, inference, or notebook execution was performed. No reported paper metrics were recalculated. Existing image bytes, label bytes, and split membership remain unchanged. The original dataset YAML is retained; the new publication YAML records unknown validation membership rather than inventing it.

Before the cleanup-only instruction, a read-only audit produced the current manifest/report. These files are preserved as prior audit evidence; no audit script was executed after that instruction. Static syntax, link, archive-integrity, and Git-diff checks are used for cleanup verification only.

## Final publication tree

```text
.
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── requirements-observed.txt
├── .gitignore
├── main.py                         # Existing prediction entry point
├── configs/data.yaml               # Publication config; validation unknown
├── dataset/
│   ├── README.md
│   ├── classes.txt
│   ├── split_manifest.csv
│   ├── validation_report.csv
│   └── audit_summary.json
├── detection_dataset/
│   ├── README.md                     # Link to dataset documentation
│   ├── data.yaml                     # Original historical YAML unchanged
│   ├── classes.txt
│   ├── images/{train,test}/
│   └── labels/{train,test}/
├── scripts/
│   ├── common.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── validate_dataset.py
│   └── generate_paper_figures.py
├── notebooks/
│   ├── 01_dataset_analysis.ipynb
│   └── 02_paper_figures.ipynb
├── results/final_experiment/
│   ├── README.md
│   ├── metrics.csv
│   └── args.yaml
├── paper_figures/                   # Eight existing PNG/PDF files
├── weights/README.md                # Final checkpoint placement/provenance
├── docs/
│   ├── cleanup.md
│   ├── reproducibility.md
│   ├── archive_manifest.csv
│   └── environment_observed.json
└── archive/
    ├── README.md
    └── development/                # Local only; excluded from Git
```

Local source images, annotation backups, virtual environments, ZIPs, and caches remain excluded from the publication tree. Empty auxiliary directories are not publication artifacts.

## Files moved or archived

[archive_manifest.csv](archive_manifest.csv) is the full file-by-file list, including original path, archived path, bytes, and SHA-256. Most original paths were moved under the same relative path in `archive/development/`. Originals retained or replaced in the public tree have archived copies of the pre-cleanup content.

| Original material | Disposition |
|---|---|
| `scripts/` | Original scripts preserved in archive; consolidated publication scripts replace them. |
| `notebooks/` including `notebooks/runs/` | Original notebooks, logs, outputs, and run images preserved in archive. |
| `runs/` | All historical training/evaluation/prediction outputs and both trained checkpoints preserved locally. |
| `resized_images/` | Intermediate image collection preserved locally; active detection images unchanged. |
| `yolov8n.pt` | Existing pretrained checkpoint preserved locally without replacement. |
| `conflict_annotation_files_before_cleanup.txt` | Archived conflict-recovery record. |
| `conflict_alternatives_manual_review.txt`, `manual_review_required.txt` | Archived originals; unresolved semantic-review issue remains documented. |
| `test_predictions_comparison.csv` | Archived historical 485-record analysis; not presented as final test results. |
| `dataset_validation_report.csv` | Archived earlier report; prior audit evidence is under `dataset/`. |
| `et --hard 61e6312` | Archived accidental Git-recovery file. |
| `README.md`, `requirements.txt` | Pre-cleanup copies preserved before replacement. |
| `detection_dataset/data.yaml` | Archived copy; original also restored unchanged in place. |
| `detection_dataset/README.md` | Archived long-form document; replaced with a pointer to `dataset/README.md`. |
| `paper_figures/*` | Archived copies and identical originals retained; no figures regenerated. |

Historical mismatch tools include `copy_mismatches.py`, `organize_mismatch_folders.py`, `rename_mismatch_files.py`, `rename_misnamed_dataset.py`, and `sync_resized_images.py`. Old preprocessing/splitting utilities and `rename_images.py` are archived. Placeholder `count_damage.py` and `webcam_detection.py`, the unrelated `family.pl`, old log parsers, and redundant `test_evaluate.py` are absent from the active workflow but preserved locally.

`annotation_backup/` remains local and ignored; it is not part of the archive to publish. No important research file was permanently deleted. Large archived binaries remain in existing Git history; reducing historical repository size would require a separately authorized history migration.

## Renamed/refactored roles

| Previous entry point | Publication entry point |
|---|---|
| `scripts/train_yolo.py` | `scripts/train.py` |
| `scripts/test_evaluate.py` and `scripts/evaluate.py` | `scripts/evaluate.py` |
| `scripts/predict.py` | `scripts/predict.py` |
| `scripts/validate_yolo_dataset.py` | `scripts/validate_dataset.py` |
| `notebooks/count_banana_annotations.ipynb` | `notebooks/01_dataset_analysis.ipynb` |
| `notebooks/paper_class_samples_with_annotations.ipynb` | `scripts/generate_paper_figures.py` and thin `notebooks/02_paper_figures.ipynb` |

Training, evaluation, and prediction expose arguments and use 640 pixels by default. Training retains 50 epochs, batch four, and pretrained YOLOv8n; unknown validation membership causes an explicit stop. Evaluation requires a checkpoint and selects test explicitly. The validator writes issues without modifying labels. Figures retain the existing class-sample/annotation-comparison logic; missing final-model plots were not invented. The scripts were not run under the cleanup-only instruction.

## Newly created documentation and artifacts

New paths include `CITATION.cff`, `configs/data.yaml`, `dataset/*`, `docs/*`, `results/final_experiment/*`, `archive/README.md`, `weights/README.md`, `requirements-observed.txt`, `scripts/common.py`, `scripts/train.py`, `scripts/validate_dataset.py`, `scripts/generate_paper_figures.py`, and the two numbered notebooks. The reported metrics/settings are transcriptions of author-provided values, not regenerated experimental outputs. No empty final class-metric tables or misleading substitute curves are added.

## Intentionally unchanged

- Original dataset images, labels, class definitions, counts, and split membership.
- Original dataset YAML contents, retained as historical evidence.
- Checkpoint bytes and historical scientific outputs, preserved locally.
- Eight original ground-truth figure PNG/PDF files.
- `LICENSE`, `main.py`, raw source images, and local annotation backups.
- Paper title, problem definition, YOLOv8n model family, two operational classes, and all reported paper results.

## Remaining author confirmation

The final checkpoint, final validation/model-selection protocol, complete author list, conference/DOI, original environment, dataset rights/provenance, class-wise results, and efficiency-measurement protocol remain unconfirmed. Existing data-integrity issues are documented rather than fixed. See [reproducibility.md](reproducibility.md).
