# Final experiment reproducibility

The current release imports `Bitol_80_20_NoVal_Research-20260821T060258Z-1-001`, specifically `yolov8n_640_batch4_80_20_noval-2`. The other run in that export has `imgsz: 50` and no checkpoint; it is not used.

The selected checkpoint records Ultralytics **8.4.52**, 50 epochs, batch 4, input 640, seed 0, deterministic training, and `val: false`. Its embedded mAP@50 is 0.8704. Imported test tables report 0.8703663547764916. Original Colab paths in `results/final_experiment/training/args.yaml` are provenance, not runnable local paths.

Local verification uses `scripts/evaluate.py`, the installed packages, the existing 491-image test split, and the imported best checkpoint. Exact measured metrics and environment are recorded in `results/final_experiment/verification/`. Small differences from the original run can arise from package versions and device. Original efficiency timings describe the supplied experiment; local CPU timings are recorded separately.

The export's image-level table agrees with local filenames and split membership (1,982 train, 491 test). It has no raw dataset replacement or source image hashes, so original image-byte identity is not established by that table alone. Existing images, labels, and split membership remain unchanged.

Known local audit findings remain relevant: 72 exact duplicate image groups cross train/test and 119 annotation coordinate issues. A reproduced score does not establish an independent held-out test set. The export's empty annotation-issue table uses its own checks and does not override the stricter local audit.

`data_paper.yaml` leaves validation unset. Evaluation explicitly uses `split='test'`. New training requires a separate validation partition and rejects cross-split exact duplicates; it does not reproduce the historical no-validation procedure. The old `data.yaml` validation/test alias is retained only as historical evidence.

The full original training environment, acquisition-group identities, and annotation protocol are unavailable. Checkpoint hashes and imported file hashes are in `weights/README.md` and `results/final_experiment/import_manifest.json`.
