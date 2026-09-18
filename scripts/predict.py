"""Predict visible banana surface condition in a local image, directory, or video."""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

if __package__:
    from .common import DEFAULT_MODEL, ROOT, prepare_runtime, record_environment, sha256
else:
    from common import DEFAULT_MODEL, ROOT, prepare_runtime, record_environment, sha256


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--model', type=Path, default=DEFAULT_MODEL)
    parser.add_argument('--conf', type=float, default=0.25)
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--save-dir', type=Path, default=ROOT / 'outputs/predict')
    parser.add_argument('--device', default=None)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    if not args.source.exists() or not args.model.is_file():
        parser.error('Source and checkpoint must exist locally.')
    if not 0 <= args.conf <= 1:
        parser.error('--conf must be between 0 and 1.')

    prepare_runtime()
    from ultralytics import YOLO

    model = YOLO(str(args.model.resolve()))
    output = args.save_dir.resolve()
    # Streaming avoids retaining every video frame in memory.
    counts = Counter()
    processed = empty = 0
    handle = None
    saved = None
    try:
        for result in model.predict(source=str(args.source.resolve()), conf=args.conf,
                                    imgsz=args.imgsz, device=args.device, save=True,
                                    stream=True, project=str(output.parent),
                                    name=output.name, verbose=args.verbose):
            if handle is None:
                saved = Path(result.save_dir)
                handle = (saved / 'detections.csv').open('w', newline='', encoding='utf-8')
                writer = csv.writer(handle, lineterminator='\n')
                writer.writerow(['source', 'item_index', 'class_id', 'class_name', 'confidence',
                                 'x1', 'y1', 'x2', 'y2'])
            processed += 1
            boxes = result.boxes.cpu()
            empty += int(len(boxes) == 0)
            for cls, conf, xyxy in zip(boxes.cls.tolist(), boxes.conf.tolist(), boxes.xyxy.tolist()):
                name = result.names[int(cls)]
                counts[name] += 1
                writer.writerow([result.path, processed, int(cls), name, f'{conf:.6f}',
                                 *[round(value, 2) for value in xyxy]])
    finally:
        if handle is not None:
            handle.close()
    if saved is None:
        parser.error('No images or video frames were processed.')
    summary = (f'Processed: {processed} images/frames\n'
               f'Detections: {sum(counts.values())} '
               f'(healthy: {counts["healthy"]}, unhealthy: {counts["unhealthy"]})\n'
               f'Images/frames with no detections: {empty}\n')
    (saved / 'summary.txt').write_text(summary, encoding='utf-8')
    record_environment(saved / 'provenance.json', checkpoint=str(args.model.resolve()),
                       checkpoint_sha256=sha256(args.model), source=str(args.source.resolve()),
                       conf=args.conf, imgsz=args.imgsz, device=args.device)
    print(f'\n{summary}\nAnnotated media and detections.csv: {saved}')


if __name__ == '__main__':
    main()
