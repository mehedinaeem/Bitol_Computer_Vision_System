# Final experiment: YOLOv8n, batch 4, 80/20, no validation

Source: `Bitol_80_20_NoVal_Research-20260821T060258Z-1-001`, run `yolov8n_640_batch4_80_20_noval-2`.

**Imported test mAP@50: 87.0366%. Local verification: 87.0366%.** The local run used the included `weights/best.pt` at 640 pixels, batch 4, CPU, on all 491 test images (1,445 instances).

| File/directory | Meaning |
|---|---|
| `metrics.csv` | Imported train/test metrics as fractions, not newly measured training metrics |
| `train_test_metrics_80_20_noval.csv` | Original export table, percentages |
| `training/` | Original 50-epoch log, configuration, and training plots |
| `evaluation/` | Imported train/test and diagnostic plots/predicted labels |
| `verification/` | Locally measured aggregate/class metrics, summary, and environment/checkpoint provenance |
| `dataset_audit_80_20.csv` | Original export audit; does not replace the stricter local dataset audit |
| `import_manifest.json` | Original source-to-destination mapping with SHA-256 hashes |

Class-wise source metrics and figures are in `paper_figures/03_test_metrics/`. Unique files from the original export are archived under ignored `outputs/archive/research_export/`; previous release artifacts are under `outputs/archive/previous_release/`.

Local verification command:

```bash
python scripts/evaluate.py --device cpu --name verified_final
```

Print both result sets with `python scripts/report.py`. CSV values use 0–1 fractions unless the column explicitly says `(%)`. Console summaries use percentages. F1 is the harmonic mean of the displayed precision and recall; aggregate F1 is not the mean of class-wise F1.

Known split overlap and annotation issues remain documented in `detection_dataset/README.md`. Reproducing the score does not resolve those limitations. No model was retrained during integration.
