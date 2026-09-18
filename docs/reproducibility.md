# Reproducibility and scientific evidence

## Scope of this cleanup

The paper theme, two classes, YOLOv8n approach, reported results, image bytes, annotation bytes, and split membership are preserved. No model was trained, evaluated, or used for inference. No notebook or figure script was executed. A read-only dataset audit was run before the user narrowed the task to cleanup-only; its reports and manifest are retained as prior evidence. No validation script was executed after that instruction.

## Reported versus available evidence

The author supplied the final 640 × 640, batch-4, 50-epoch configuration and aggregate test results. `results/final_experiment/` explicitly records that source. The local historical run records 1024-pixel training and different validation metrics. This does not establish that the supplied final results are incorrect; it establishes a missing link between reported results and original artifacts.

Class-wise final metrics, final checkpoint, original curves/confusion matrices, and final training logs are unavailable. They are intentionally not populated using older runs. Original paper figures are preserved without regeneration. Missing workflow diagrams and final prediction illustrations are not fabricated.

The rounded paper metrics remain exactly: precision 81.36%, recall 74.30%, F1 77.67%, mAP50 87.04%, and mAP50–95 59.33%. Any future evaluation writes separately and is not a replacement for these records. The future evaluation script computes the harmonic mean of mean precision/recall for overall F1; original aggregation details require confirmation.

## Validation protocol

The original dataset YAML is preserved byte-for-byte and maps validation and testing to `images/test`. The publication YAML (`detection_dataset/data_paper.yaml`) resolves paths relative to its own location and sets validation to null. It is not an executable reconstruction of an unknown validation protocol.

`train.py` intentionally refuses to train without an explicit validation partition. It also rejects exact-byte overlap between train/validation/test. These are workflow checks, not changes to the stored dataset or a newly proposed split. Supplying a future independent split would define a different experiment unless original final membership can be recovered. There is no generated 80/10/10 or other invented partition.

A seed of zero is exposed as a workflow default based on the historical saved configuration. It is not a verified final-run seed. The figure seed of 42 is retained from the original annotation-figure notebook and has a different purpose.

## Dataset issues retained

Earlier auditing recorded 119 strict coordinate-boundary violations and 72 exact-duplicate groups crossing train/test. The snapshot manifest records membership as found; it does not eliminate leakage. Annotation counts include flagged boxes, and image counts include duplicate content. The final paper's independent held-out interpretation needs author confirmation in light of these findings.

The old conflict notes singled out `healthy_0717.txt` for semantic review. No active conflict markers remain, but the note does not document a final annotation adjudication. The original alternatives and backup files remain local; labels were not altered.

## Environment and hardware

The final experiment's package versions and Python/CUDA/PyTorch environment are unavailable. `requirements.txt` therefore lists dependencies without guessed historical pins. `docs/requirements-observed.txt` pins versions actually found in the local cleanup environment; these are not claimed as final-experiment versions or a portable GPU lock. `environment_observed.json` records that distinction and observed Python/PyTorch versions.

Author-reported efficiency is 6.54 ms/image on NVIDIA Tesla T4, approximately 3.01 million parameters, and 5.96 MB model size. Timing boundaries, warm-up, precision mode, batch size for timing, and checkpoint identity require confirmation. No local speed benchmark was run.

## API and output behavior

Evaluation calls `model.val(split='test', imgsz=640, plots=True)` with an explicit checkpoint and resolved dataset YAML. It writes aggregate and class-wise metrics plus run provenance to a new output folder. Ultralytics creates confusion matrices and PR/F1/P/R curves; filenames are framework-version dependent. See the [official validation API](https://docs.ultralytics.com/modes/val/).

Training uses a temporary resolved YAML and preserves the resolved contents in the resulting run if executed in the future. Prediction streams local image/video results and saves annotations. Figure generation only refactors the existing annotation-display notebook and writes to `outputs/paper_figures/`, leaving supplied figures untouched.

## Metadata needed from the authors

- Complete ordered paper author list, affiliations, conference, publication status/date, and DOI.
- Original final checkpoint, exact dataset/split manifest, validation/model-selection protocol, training log, class-wise results, and curves.
- Final Python/package/CUDA versions and the inference timing protocol.
- Dataset acquisition/annotation provenance and image redistribution rights.

The maintainer listed in `CITATION.cff` is inferred only from the existing LICENSE copyright. It is not asserted to be the complete paper author list. The citation version is explicitly an unreleased cleanup label.
