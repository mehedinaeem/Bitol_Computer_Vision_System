# BITOL: Banana Surface-Condition Detection

YOLOv8n detects **healthy (0)** and **unhealthy (1)** bananas. The final model comes from `Bitol_80_20_NoVal_Research-20260821T060258Z-1-001`, run `yolov8n_640_batch4_80_20_noval-2`.

**Test mAP@50: 87.04%.** The supplied checkpoint has also been evaluated locally on all **491 test images / 1,445 objects**. See [model accuracy](results/README.md) and [experiment details](results/final_experiment/README.md).

| Supplied test metric | Value |
|---|---:|
| Precision | 81.36% |
| Recall | 74.30% |
| F1 | 77.67% |
| mAP@50 | **87.04%** |
| mAP@50:95 | 59.33% |

## Run

Use Python 3.10+ and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

View the accuracy directly in **[results/README.md](results/README.md)** or [results/accuracy.csv](results/accuracy.csv).

Predict an image, folder, or local video with the included `weights/best.pt`:

```bash
python main.py detection_dataset/images/test/healthy_0099.jpg
python main.py path/to/image.jpg --conf 0.25 --device cpu
```

Predictions include annotated media, `detections.csv` (class, confidence, pixel coordinates), a short `summary.txt`, and checkpoint/environment provenance. Video counts count detections across frames, not unique tracked bananas. Use `--model` to select another checkpoint and `--save-dir` to choose an output directory.

Evaluate the complete test split:

```bash
python scripts/evaluate.py --device cpu
```

Evaluation prints a percentage table and saves aggregate/class-wise CSVs, confusion matrices, PR/F1 curves, `summary.txt`, and `provenance.json`. CSV metrics use fractions from 0 to 1; the console shows percentages. New runs get separate numbered directories under `outputs/`.

## Files

| Location | Contents |
|---|---|
| `weights/best.pt`, `weights/last.pt` | Imported final experiment checkpoints |
| `detection_dataset/` | Existing train/test images, YOLO labels, split manifest, and audits |
| `results/final_experiment/` | Imported metrics, training log/configuration, evaluation diagnostics, and import hashes |
| `results/final_experiment/verification/` | Independently measured local checkpoint results |
| `paper_figures/` | Updated dataset, loss, performance, qualitative, and evaluation figures |
| `scripts/` | Prediction, evaluation, reporting, auditing, training, and figure commands |
| `notebooks/` | Historical research notebooks; inspect paths before running |
| `outputs/` | Generated runs and ignored original/previous artifact backups |

![Final test confusion matrix](paper_figures/05_ultralytics_outputs/confusion_matrix.png)

![Class-wise test performance](paper_figures/03_test_metrics/classwise_test_performance.png)

## Dataset and experiment

| Split | Images | Healthy objects | Unhealthy objects |
|---|---:|---:|---:|
| Train | 1,982 | 2,355 | 2,027 |
| Test | 491 | 878 | 567 |

The export's image membership matches the local dataset by filename and split. The export does not contain replacement raw images/labels, so the existing dataset is retained. Model input is **640 × 640**, batch **4**, epochs **50**, seed **0**. The supplied run used `val: false`; its original arguments are preserved in [training/args.yaml](results/final_experiment/training/args.yaml).

The existing audit identifies **72 exact duplicate groups across train/test** and **119 bounding-box coordinate issues**. These affect interpretation of the test score; the data was not silently repaired or repartitioned. See [dataset details](detection_dataset/README.md) and [reproducibility](docs/reproducibility.md).

Audit or generate fresh annotation figures:

```bash
python scripts/validate_dataset.py --report outputs/dataset_validation_report.csv
python scripts/generate_paper_figures.py --output outputs/paper_figures
```

For **new training**, supply a separate, documented validation partition:

```bash
python scripts/train.py --data path/to/development.yaml
```

The training script checks split overlap and requires separate train/validation/test data. It is intended for new experiments; it does not recreate the imported no-validation run. Prediction and evaluation work directly with the included model.

## Paper and license

Research title: **“An Efficient Approach to Beetle Damage Detection of Banana Using Deep Learning.”** See [CITATION.cff](CITATION.cff). Complete author list, venue, and DOI remain unconfirmed. Labels describe visible surface condition, not a biological diagnosis or beetle species.

Code: [MIT](LICENSE). Dataset redistribution rights are not separately documented; third-party models and libraries retain their terms.
