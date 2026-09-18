"""Evaluate an explicitly supplied checkpoint on test at 640 pixels."""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from common import ROOT, f1_score, load_data, record_environment, sha256, write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, required=True,
                        help='Verified final checkpoint; not bundled with this release')
    parser.add_argument('--data', type=Path, default=ROOT / 'detection_dataset/data_paper.yaml')
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--batch', type=int, default=4)
    parser.add_argument('--device', default=None)
    parser.add_argument('--project', type=Path, default=ROOT / 'outputs/evaluate')
    parser.add_argument('--name', default='test')
    args = parser.parse_args()
    if not args.model.is_file():
        parser.error(f'Checkpoint does not exist: {args.model}')
    data = load_data(args.data)
    if not data.get('test'):
        parser.error('The dataset must explicitly define test.')

    import yaml
    from ultralytics import YOLO

    model = YOLO(str(args.model.resolve()))
    with tempfile.TemporaryDirectory(prefix='bitol-eval-') as directory:
        config = Path(directory) / 'data.yaml'
        config.write_text(yaml.safe_dump(data))
        metrics = model.val(data=str(config), split='test', imgsz=args.imgsz,
                            batch=args.batch, device=args.device, plots=True,
                            project=str(args.project.resolve()), name=args.name)
    output = Path(model.validator.save_dir)
    p, r = float(metrics.box.mp), float(metrics.box.mr)
    write_csv(output / 'metrics.csv', [dict(split='test', precision=p, recall=r,
              f1=f1_score(p, r), map50=float(metrics.box.map50),
              map50_95=float(metrics.box.map), source='measured_by_evaluate.py')])
    class_rows = []
    for index, class_id in enumerate(metrics.box.ap_class_index):
        cp, cr = float(metrics.box.p[index]), float(metrics.box.r[index])
        class_rows.append(dict(class_id=int(class_id),
                               class_name=model.names[int(class_id)], precision=cp,
                               recall=cr, f1=f1_score(cp, cr),
                               map50=float(metrics.box.ap50[index]),
                               map50_95=float(metrics.box.ap[index])))
    write_csv(output / 'class_metrics.csv', class_rows,
              ['class_id', 'class_name', 'precision', 'recall', 'f1', 'map50', 'map50_95'])
    record_environment(output / 'provenance.json', checkpoint=str(args.model.resolve()),
                       checkpoint_sha256=sha256(args.model), split='test',
                       imgsz=args.imgsz, batch=args.batch, device=args.device,
                       dataset=data, speed_ms_per_image=metrics.speed,
                       f1_definition='Harmonic mean of mean precision and mean recall')
    print(f'Metrics and Ultralytics confusion matrices/PR/F1/P/R curves: {output}')


if __name__ == '__main__':
    main()
