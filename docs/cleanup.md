# Repository preservation notes

The publication tree is described in the root [README](../README.md). Dataset documentation, the existing split manifest, and prior audit reports now live together in `detection_dataset/`. `data_paper.yaml` is the publication configuration; `data.yaml` preserves the original validation/test alias unchanged. Script defaults and documented commands use the publication configuration.

## Research history

Six original notebooks were restored byte-for-byte from commit `4790a55`, the last repository state before the earlier cleanup (`ff0d855`). Their code, metadata, execution counts, and saved outputs were preserved without execution. The root README describes each notebook and the two existing convenience notebooks. Earlier preparation scripts and experimental artifacts remain available in Git history.

The former ignored local `archive/development/` directory was moved intact to ignored `outputs/development/`. This preserves local-only code, notebook copies, intermediate images, reports, conflict-review records, run outputs, and checkpoints without putting an archive directory in the publication branch. No useful local research material was deleted. A fresh clone does not contain these ignored local files.

[local_preservation_manifest.csv](local_preservation_manifest.csv) retains the earlier file inventory, byte sizes, and SHA-256 values, with location prefixes updated to `outputs/development/`. Its `original_path` column describes historical locations, not the current publication layout. Local historical checkpoints are documented in [weights/README.md](../weights/README.md). Local source images, ZIPs, environments, and annotation backups remain untouched and ignored.

The observed dependency list moved to [requirements-observed.txt](requirements-observed.txt); it records the cleanup environment, not a verified final-experiment environment.

## Verification scope

This reorganization uses file-integrity, notebook-JSON, Python-syntax, configuration-path, Markdown-link, and Git-diff checks only. No training, evaluation, prediction, dataset-validation script, notebook, or figure-generation script was run. Dataset images, labels, class names, split membership, original YAML, paper figures, and reported results remain unchanged. No commit, push, or history rewrite was performed.

For scientific limitations and missing evidence, see [reproducibility.md](reproducibility.md).
