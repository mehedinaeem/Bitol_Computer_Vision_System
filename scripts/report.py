"""Print the imported research metrics and the independent local verification."""
from __future__ import annotations

import csv
if __package__:
    from .common import ROOT, format_metrics
else:
    from common import ROOT, format_metrics


def main() -> None:
    base = ROOT / 'results/final_experiment'
    for title, path in (
        ('Supplied research results', base / 'metrics.csv'),
        ('Local checkpoint verification', base / 'verification/metrics.csv'),
    ):
        print(f'\n{title}')
        if path.is_file():
            with path.open(newline='', encoding='utf-8') as handle:
                print(format_metrics(list(csv.DictReader(handle))))
        else:
            print(f'Not available: {path}')
    print(f'\nDefault model: {ROOT / "weights/best.pt"}')
    print(f'Figures: {ROOT / "paper_figures"}')


if __name__ == '__main__':
    main()
