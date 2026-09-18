# BITOL: Banana Surface-Condition Detection

Research code accompanying **“An Efficient Approach to Beetle Damage Detection of Banana Using Deep Learning.”** BITOL uses pretrained YOLOv8n for instance-level detection of visible banana surface condition. This repository preserves the supplied dataset and reported paper results; cleanup did not train or evaluate a model.

## Paper

**Title:** An Efficient Approach to Beetle Damage Detection of Banana Using Deep Learning

**Conference / DOI / complete author list:** pending author confirmation.

**Repository:** [Bitol_Computer_Vision_System](https://github.com/mehedinaeem/Bitol_Computer_Vision_System)

## Task and classes

Detect individual bananas with two operational labels: **healthy (0)** and **unhealthy (1)**. Predictions describe visible surface appearance; they do not establish biological diagnosis, causal beetle attribution, or beetle species identity.

## Dataset

| Partition | Images | Healthy instances | Unhealthy instances | Total instances |
|---|---:|---:|---:|---:|
| Development/training | 1,982 | 2,355 | 2,027 | 4,382 |
| Reported held-out test | 491 | 878 | 567 | 1,445 |
| **Total** | **2,473** | **3,233** | **2,594** | **5,827** |

Images and YOLO labels remain in `detection_dataset/`. Stored images are 1024 × 1024; model input is 640 × 640. See the [dataset documentation](dataset/README.md) for format, provenance gaps, and known split-integrity issues.

## Final model configuration

| Setting | Paper specification |
|---|---|
| Model | YOLOv8n, pretrained |
| Input | 640 × 640 |
| Epochs / batch | 50 / 4 |
| Classes | healthy, unhealthy |

## Reported paper results

| Test metric | Reported value |
|---|---:|
| Precision | 81.36% |
| Recall | 74.30% |
| F1-score | 77.67% |
| mAP@0.50 | 87.04% |
| mAP@0.50:0.95 | 59.33% |

Reported efficiency: approximately **3.01 million parameters**, **5.96 MB**, and **6.54 ms/image on NVIDIA Tesla T4**. These values are preserved from the author's specification, not newly measured. [Results provenance](results/final_experiment/README.md) distinguishes reported results from available local evidence.

## Repository structure

| Location | Purpose |
|---|---|
| `configs/` | Publication-facing dataset configuration; unknown validation membership remains explicit. |
| `dataset/` | Dataset documentation, class names, snapshot manifest, and previously generated audit records. |
| `detection_dataset/` | Original image/label files and original dataset configuration, retained unchanged. |
| `scripts/` | One CLI per task: training, evaluation, prediction, validation, and annotation figures. |
| `notebooks/` | Two research notebooks with saved outputs cleared. |
| `results/final_experiment/` | Author-reported metrics and settings with evidence limitations. |
| `paper_figures/` | Existing annotation figures, preserved without regeneration. |
| `docs/` | Reproducibility notes, observed environment, and detailed cleanup inventory. |
| `archive/development/` | Local historical files preserved outside Git tracking. |

## Installation

Use Python **3.10+**; the original final-experiment Python/PyTorch/CUDA versions are unknown.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Use `.venv\Scripts\activate` on Windows. Dependencies are not falsely pinned to a final experiment environment. [Observed local versions](docs/environment_observed.json) and an optional [local version list](requirements-observed.txt) are provided separately.

## Commands

These commands are documented for future use; the cleaned scripts and notebooks were **not executed**. Training requires the original validation protocol, and evaluation/prediction require a supplied checkpoint.

**Training** — defaults: YOLOv8n, 640 pixels, 50 epochs, batch 4:

```bash
python scripts/train.py --data configs/data.yaml
```

The supplied config deliberately has `val: null`. Training stops until a documented, separate validation partition is supplied; it never silently uses test for validation. Seed `0` is a documented workflow default, not a verified final-experiment seed.

**Evaluation** — explicit test split, aggregate/class-wise CSV metrics and standard Ultralytics plots:

```bash
python scripts/evaluate.py --model weights/best.pt --data configs/data.yaml
```

**Prediction** — image, directory, or local video:

```bash
python scripts/predict.py path/to/image.jpg --model weights/best.pt --conf 0.25
```

`weights/best.pt` is a placement example; a verified final checkpoint is not bundled. Historical weights are preserved locally, with locations listed in [weights/README.md](weights/README.md).

**Dataset validation** — read-only checks, CSV report:

```bash
python scripts/validate_dataset.py --report outputs/dataset_validation_report.csv
```

**Paper figures** — refactored existing ground-truth illustration logic, without inference:

```bash
python scripts/generate_paper_figures.py --output outputs/paper_figures
```

Outputs use `outputs/` by default, preserving recorded results and existing figures. Evaluation uses the framework's [explicit test-split API](https://docs.ultralytics.com/modes/val/).

## Reproducibility notes and limitations

- The final 640-pixel checkpoint, original validation membership, environment, seed, and class-wise results have not been verified. Historical 1024-pixel artifacts are archived, not relabeled as final evidence.
- Prior audits found **119 coordinate issues** and **72 exact-duplicate groups spanning train/test**. The reported test partition is therefore not established as independent by the current files. Images, labels, and split membership were not corrected or changed.
- The original `detection_dataset/data.yaml` is retained as evidence and still aliases validation to test. Use `configs/data.yaml` for the publication workflow; it explicitly leaves validation unknown.
- Tesla T4 efficiency values are author-reported. CUDA/PyTorch versions, timing protocol, and checkpoint identity require confirmation.

See [detailed reproducibility notes](docs/reproducibility.md) and the [cleanup inventory](docs/cleanup.md).

## Citation

[CITATION.cff](CITATION.cff) identifies this repository using the paper title. It records the known repository maintainer; the complete paper author list, conference, DOI, and publication date remain pending. The version identifies an unreleased documentation cleanup, not a published experiment release.

## License

Code: [MIT](LICENSE). Dataset ownership and redistribution rights are not separately documented. Third-party software and pretrained weights retain their own terms; the code license does not establish image permissions.
