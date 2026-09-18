"""Predict visible banana surface condition in a local image, directory, or video."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--model', type=Path, required=True)
    parser.add_argument('--conf', type=float, default=0.25)
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--save-dir', type=Path, default=Path('outputs/predict'))
    parser.add_argument('--device', default=None)
    args = parser.parse_args()
    if not args.source.exists() or not args.model.is_file():
        parser.error('Source and checkpoint must exist locally.')
    if not 0 <= args.conf <= 1:
        parser.error('--conf must be between 0 and 1.')

    from ultralytics import YOLO

    model = YOLO(str(args.model.resolve()))
    output = args.save_dir.resolve()
    # Streaming avoids retaining every video frame in memory.
    saved = output
    for result in model.predict(source=str(args.source.resolve()), conf=args.conf,
                                imgsz=args.imgsz, device=args.device, save=True,
                                stream=True, project=str(output.parent),
                                name=output.name):
        saved = result.save_dir
    print(f'Predictions saved to {saved}')


if __name__ == '__main__':
    main()
