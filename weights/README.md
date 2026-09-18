# Final model checkpoints

Imported from `Bitol_80_20_NoVal_Research-20260821T060258Z-1-001`, run `yolov8n_640_batch4_80_20_noval-2`.

- `best.pt`: default for prediction and evaluation; locally verified on 491 test images at **87.04% mAP@50**.
- `last.pt`: retained final-epoch checkpoint from the same run; not separately evaluated.

YOLOv8n, 640 pixels, batch 4, 50 epochs, seed 0, `val: false`. Checkpoint metadata reports Ultralytics 8.4.52. Full training arguments and evaluation evidence are in `results/final_experiment/`.

## SHA-256

```text
bd1b1c4461fc6fb77f95f26e0c7bfce29e1596b96d519cca7077a72acc6fc4d6  best.pt
188abd109fcd717c0d8c8ac6892c46c7b8798a357ec674706b21ce0bff25dcf9  last.pt
```

Historical checkpoints remain only in ignored `outputs/archive/development/`. Unique files from the supplied export are archived under `outputs/archive/research_export/`. The two active checkpoints are included by `.gitignore` exceptions.
