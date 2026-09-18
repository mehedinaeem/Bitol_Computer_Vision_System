"""Evaluate the final checkpoint on test and export metrics and plots."""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

if __package__:
    from .common import ROOT, DEFAULT_MODEL, f1_score, format_metrics, load_data, prepare_runtime, record_environment, sha256, write_csv
else:
    from common import ROOT, DEFAULT_MODEL, f1_score, format_metrics, load_data, prepare_runtime, record_environment, sha256, write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=DEFAULT_MODEL,
                        help='Checkpoint (default: weights/best.pt)')
    parser.add_argument('--data', type=Path, default=ROOT / 'detection_dataset/data_paper.yaml')
    parser.add_argument('--imgsz', type=int, default=640)
    parser.add_argument('--batch', type=int, default=4)
    parser.add_argument('--device', default=None)
    parser.add_argument('--project', type=Path, default=ROOT / 'outputs/evaluate')
    parser.add_argument('--name', default='test')
    parser.add_argument('--verbose', action='store_true', help='Show per-class framework logs')
    args = parser.parse_args()
    if not args.model.is_file():
        parser.error(f'Checkpoint does not exist: {args.model}')
    try:
        data = load_data(args.data)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    if not data.get('test'):
        parser.error('The dataset must explicitly define test.')

    prepare_runtime()
    import yaml
    from ultralytics import YOLO

    model = YOLO(str(args.model.resolve()))
    saved = {}
    model.add_callback('on_val_end', lambda validator: saved.update(output=Path(validator.save_dir)))
    with tempfile.TemporaryDirectory(prefix='bitol-eval-') as directory:
        config = Path(directory) / 'data.yaml'
        config.write_text(yaml.safe_dump(data))
        metrics = model.val(data=str(config), split='test', imgsz=args.imgsz,
                            batch=args.batch, device=args.device, plots=True,
                            project=str(args.project.resolve()), name=args.name,
                            verbose=args.verbose)
    output = saved['output']
    p, r = float(metrics.box.mp), float(metrics.box.mr)
    rows = [dict(split='test', precision=p, recall=r,
              f1=f1_score(p, r), map50=float(metrics.box.map50),
              map50_95=float(metrics.box.map), source='measured_by_evaluate.py')]
    write_csv(output / 'metrics.csv', rows)
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
    summary = format_metrics(rows + class_rows)
    (output / 'summary.txt').write_text(summary + '\n', encoding='utf-8')
    print(f'\n{summary}\n\nResults: {output}')


if __name__ == '__main__':
    main()
