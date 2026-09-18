# Research import and cleanup

The active model, metrics, training evidence, evaluation diagnostics, and paper figures now come from `Bitol_80_20_NoVal_Research-20260821T060258Z-1-001`. Every imported file was checked by SHA-256; the mapping is in `results/final_experiment/import_manifest.json`.

Superseded `results/final_experiment/` and `paper_figures/` were removed from the active tree and moved to ignored `outputs/archive/previous_release/`. Unique files from the original export are preserved under ignored `outputs/archive/research_export/`. Active files use short, stable paths. Older local development assets remain under `outputs/archive/development/`; their inventory is `local_preservation_manifest.csv`.

Dataset images/labels, raw sources, ZIP backups, and existing environments were retained. Historical notebooks were preserved, including the user's pre-existing change to `paper_class_samples_with_annotations.ipynb`. No retraining, commit, push, or publication was performed.

The best checkpoint was evaluated on the complete local test split before adoption. The evaluation export-path bug was fixed, prediction now writes a detection table and readable counts, and both default to `weights/best.pt`. Local verification evidence is stored separately from imported results.

## Output deduplication

Removed 6,816 byte-identical files from `outputs/`, reclaiming 1.82 GB. SHA-256 grouping and full byte comparisons verified each removal against a retained copy. Unique historical files now live under `outputs/archive/`; active data, models, figures, and notebooks were not modified. `outputs/deduplication.csv` maps removed paths to retained files. The earlier `local_preservation_manifest.csv` remains a historical inventory of pre-deduplication locations, not the current layout.
