"""Small shared helpers for paths, result tables, and experiment provenance."""
from __future__ import annotations

import csv
import hashlib
import json
import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tif', '.tiff'}


def sha256(path: Path) -> str:
    """Hash file contents without loading a complete dataset into memory."""
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def load_data(path: Path) -> dict:
    """Resolve dataset roots relative to the YAML rather than the shell directory."""
    import yaml

    path = path.expanduser().resolve()
    data = yaml.safe_load(path.read_text())
    root = (path.parent / data.get('path', '.')).resolve()
    data['path'] = str(root)
    names = data.get('names')
    if names not in ({0: 'healthy', 1: 'unhealthy'}, ['healthy', 'unhealthy']):
        raise ValueError('Expected classes 0: healthy and 1: unhealthy.')
    for split in ('train', 'val', 'test'):
        value = data.get(split)
        if value:
            values = value if isinstance(value, list) else [value]
            resolved = [str((root / item).resolve()) for item in values]
            data[split] = resolved if isinstance(value, list) else resolved[0]
    return data


def split_images(value: str | list[str] | None) -> list[Path]:
    """Read image directories or YOLO image-list files."""
    if not value:
        return []
    paths = value if isinstance(value, list) else [value]
    images = []
    for item in paths:
        path = Path(item)
        if path.is_dir():
            images.extend(p.resolve() for p in sorted(path.rglob('*'))
                          if p.suffix.lower() in IMAGE_EXTENSIONS)
        elif path.is_file() and path.suffix.lower() == '.txt':
            images.extend((path.parent / line.strip()).resolve()
                          for line in path.read_text().splitlines() if line.strip())
        else:
            raise ValueError(f'Expected an image directory or image-list file: {path}')
    if any(not p.is_file() for p in images):
        raise ValueError('An image-list entry does not exist.')
    return images


def check_training_splits(data: dict) -> None:
    """Refuse unknown validation membership and exact-byte split leakage."""
    if not data.get('val'):
        raise ValueError('Validation membership is unknown. Supply --data with the '
                         'documented development train/validation protocol; test must '
                         'remain separate. See docs/reproducibility.md.')
    sets = {}
    for split in ('train', 'val', 'test'):
        images = split_images(data.get(split))
        if not images:
            raise ValueError(f'No images in {split}.')
        sets[split] = {sha256(p) for p in images}
    for left, right in (('train', 'val'), ('train', 'test'), ('val', 'test')):
        overlap = sets[left] & sets[right]
        if overlap:
            raise ValueError(f'{len(overlap)} exact-image hash groups overlap '
                             f'{left}/{right}; resolve leakage before training.')


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    """Write a portable result table, retaining headers for an empty table."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def record_environment(path: Path, **details) -> None:
    """Record observed packages and explicit run arguments, not assumed history."""
    packages = {}
    for name in ('ultralytics', 'torch', 'numpy', 'pandas', 'matplotlib', 'Pillow', 'PyYAML'):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = None
    path.write_text(json.dumps({'python': platform.python_version(),
                                'packages': packages, **details}, indent=2) + '\n')


def f1_score(precision: float, recall: float) -> float:
    """Harmonic mean; return zero when both inputs are zero."""
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0
