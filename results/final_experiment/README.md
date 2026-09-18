# Final experiment: reported evidence

`metrics.csv` and `args.yaml` transcribe the author's final paper specification. Scores in the CSV are fractions, not percentages. These files are not the output of a new local experiment.

The final checkpoint, original training log, class-wise metrics, confusion matrices, curve arrays, and measurement environment have not been identified. No substitute artifacts are copied from the historical 1024-pixel run. Missing artifacts are intentionally absent rather than filled with invented values.

The reported F1 is preserved at 0.7767. Future `evaluate.py` outputs define overall F1 as the harmonic mean of mean precision and mean recall; class-wise F1 is calculated separately. The original aggregation convention still requires confirmation.

Author-reported efficiency: approximately 3.01 million parameters, 5.96 MB model size, and 6.54 ms/image on NVIDIA Tesla T4. Precision mode, timing warm-up, batch/measurement boundaries, and checkpoint identity are not established by these numbers.

New evaluations write to `outputs/evaluate/` and cannot overwrite this reference table by default. Once the original artifacts are supplied, record their hashes and provenance before adding them here.
