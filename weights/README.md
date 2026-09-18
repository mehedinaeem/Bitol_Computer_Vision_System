# Model checkpoint placement

A verified checkpoint for the reported final 640-pixel experiment has not been identified. Place an author-confirmed checkpoint at `weights/best.pt`, or pass its actual path with `--model`.

Existing weights are preserved unchanged in the local ignored archive:

- `archive/development/yolov8n.pt`
- `archive/development/runs/detect/models/trained/bitol_yolov8/weights/best.pt`
- `archive/development/runs/detect/models/trained/bitol_yolov8/weights/last.pt`

The saved run configuration uses 1024 pixels. Its weights must not be presented as the verified final paper checkpoint without confirmation. No checkpoint was replaced or generated.

For eventual distribution, attach the confirmed final checkpoint to a GitHub Release with its SHA-256, source run, dataset version, software environment, and usage terms. No release or external download URL has been created. Moving files out of the current tree does not remove their bytes from existing Git history.
