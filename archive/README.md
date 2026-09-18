# Local development archive

`development/` preserves earlier scripts, notebooks with original outputs, intermediate resized images, training/validation/prediction runs, checkpoints, old reports, conflict-review records, and the accidental Git-recovery filename. It is excluded from Git.

The complete portable inventory is [docs/archive_manifest.csv](../docs/archive_manifest.csv), containing original path, local archive path, byte size, and SHA-256. The archive exists in the cleanup workspace; a fresh clone does not receive it. Older committed files also remain available in existing Git history. No history was rewritten and nothing was pushed.

Historical artifacts are not evidence of the reported final 640-pixel experiment unless their provenance is independently confirmed. Keep the local archive or export it to a separate archival branch/storage before removing this workspace. Do not publish annotation backups.
