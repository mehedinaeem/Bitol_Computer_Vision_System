"""Train the YOLOv8n baseline after the validation protocol is supplied."""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from common import ROOT, check_training_splits, load_data, record_environment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT / 'configs/data.yaml')
    parser.add_argument('--model', default='yolov8n.pt')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--batch', type=int, default=4)
    parser.add_argument('--device', default=None, help='cpu, 0, or a device list')
    parser.add_argument('--seed', type=int, default=0,
                        help='Reproduction default; final experiment seed is unverified')
    parser.add_argument('--project', type=Path, default=ROOT / 'outputs/train')
    parser.add_argument('--name', default='bitol_yolov8n')
    args = parser.parse_args()
    try:
        data = load_data(args.data)
        check_training_splits(data)
    except (ValueError, OSError) as error:
        parser.error(str(error))

    import yaml
    from ultralytics import YOLO

    model = YOLO(args.model)
    with tempfile.TemporaryDirectory(prefix='bitol-train-') as directory:
        resolved = Path(directory) / 'data.yaml'
        resolved.write_text(yaml.safe_dump(data))
        model.train(data=str(resolved), epochs=args.epochs, imgsz=args.imgsz,
                    batch=args.batch, device=args.device, seed=args.seed,
                    deterministic=True, pretrained=True,
                    project=str(args.project.resolve()), name=args.name)
        output = Path(model.trainer.save_dir)
        (output / 'data.resolved.yaml').write_text(yaml.safe_dump(data))
        record_environment(output / 'provenance.json',
                           arguments={k: str(v) if isinstance(v, Path) else v
                                      for k, v in vars(args).items()},
                           validation_protocol='User-supplied; see data.resolved.yaml')
    print(f'Run saved to {output}')


if __name__ == '__main__':
    main()
