"""Export the existing ground-truth sample figures; no inference or evaluation."""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASS_NAMES = {0: 'healthy', 1: 'unhealthy'}
SAMPLE_FILES = {
    0: ['healthy_0091.jpg', 'healthy_0095.jpg', 'healthy_0096.jpg'],
    1: ['unhealthy_0139.jpg', 'unhealthy_0166.jpg', 'unhealthy_0406.jpg'],
}


def read_annotations(path: Path) -> list[tuple]:
    """Read existing YOLO annotations without modifying them."""
    if not path.exists():
        return []
    return [tuple(map(float, line.split())) for line in path.read_text().splitlines()
            if line.strip()]


def select_samples(dataset: Path, split: str, count: int, seed: int,
                   automatic: bool = False) -> dict:
    """Retain the original notebook's ranking, seeded selection, and manual samples."""
    candidates = {class_id: [] for class_id in CLASS_NAMES}
    for label in sorted((dataset / 'labels' / split).glob('*.txt')):
        if label.name == 'classes.txt':
            continue
        image = next((dataset / 'images' / split / f'{label.stem}{ext}'
                      for ext in ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp')
                      if (dataset / 'images' / split / f'{label.stem}{ext}').is_file()), None)
        if image is None:
            continue
        annotations = read_annotations(label)
        for class_id in CLASS_NAMES:
            boxes = [a for a in annotations if a[0] == class_id and a[3] * a[4] >= 0.01]
            if boxes:
                score = sum(a[3] * a[4] for a in boxes) + 0.02 * min(len(boxes), 5)
                candidates[class_id].append((score, image, annotations))
    rng = random.Random(seed)
    selected = {}
    for class_id, items in candidates.items():
        items.sort(key=lambda item: item[0], reverse=True)
        pool = items[:max(count, math.ceil(len(items) / 3))]
        selected[class_id] = rng.sample(pool, min(count, len(pool)))
        if automatic:
            continue
        manual = []
        for filename in SAMPLE_FILES[class_id][:count]:
            paths = [dataset / 'images' / split / filename]
            paths += sorted((dataset / 'images').glob(f'*/{filename}'))
            image = next((p for p in paths if p.exists()), None)
            if image is None:
                raise FileNotFoundError(filename)
            annotations = read_annotations(dataset / 'labels' / image.parent.name /
                                           f'{image.stem}.txt')
            if any(a[0] == class_id for a in annotations):
                manual.append((0, image, annotations))
        used = {item[1].name for item in manual}
        selected[class_id] = (manual + [item for item in selected[class_id]
                                       if item[1].name not in used])[:count]
    return selected


def generate_figures(dataset: Path, output: Path, split: str = 'train',
                     samples: int = 3, seed: int = 42, dpi: int = 300,
                     automatic: bool = False) -> None:
    """Draw class-focused annotations and original/annotation comparisons."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image

    plt.rcParams.update({'font.size': 9, 'axes.titlesize': 10, 'figure.facecolor': 'white'})
    selected = select_samples(dataset, split, samples, seed, automatic)
    output.mkdir(parents=True, exist_ok=True)
    colors = {0: '#20A387', 1: '#D1495B'}

    def draw(ax, item, class_id, annotated=True):
        _, path, annotations = item
        with Image.open(path) as source:
            image = source.convert('RGB')
        ax.imshow(image)
        width, height = image.size
        if annotated:
            for label, xc, yc, bw, bh in annotations:
                if label != class_id:
                    continue
                x, y = (xc - bw / 2) * width, (yc - bh / 2) * height
                ax.add_patch(Rectangle((x, y), bw * width, bh * height,
                                       fill=False, edgecolor=colors[class_id], linewidth=1.5))
                ax.text(x, max(0, y - 3), CLASS_NAMES[class_id], fontsize=8,
                        color=colors[class_id], va='bottom')
        ax.axis('off')
        ax.set_title(f'{CLASS_NAMES[class_id]} ({path.parent.name})')

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(output / f'{name}.png', dpi=dpi, bbox_inches='tight')
        fig.savefig(output / f'{name}.pdf', bbox_inches='tight')
        plt.close(fig)

    fig, axes = plt.subplots(2, samples, figsize=(3.2 * samples, 6), squeeze=False)
    for class_id in CLASS_NAMES:
        for col in range(samples):
            axes[class_id, col].axis('off')
            if col < len(selected[class_id]):
                draw(axes[class_id, col], selected[class_id][col], class_id)
    save(fig, f'all_classes_annotated_{split}')
    fig, axes = plt.subplots(2, 2, figsize=(6.4, 6), squeeze=False)
    for class_id in CLASS_NAMES:
        for col in range(2):
            axes[class_id, col].axis('off')
            if selected[class_id]:
                draw(axes[class_id, col], selected[class_id][0], class_id, bool(col))
    save(fig, f'original_vs_annotation_{split}')
    print(f'Ground-truth figures saved to {output}; no model was run.')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, default=ROOT / 'detection_dataset')
    parser.add_argument('--output', type=Path, default=ROOT / 'outputs/paper_figures')
    parser.add_argument('--split', choices=('train', 'test'), default='train')
    parser.add_argument('--samples', type=int, default=3)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--dpi', type=int, default=300)
    parser.add_argument('--automatic', action='store_true',
                        help='Use only samples from --split instead of original manual examples')
    args = parser.parse_args()
    if args.samples < 1 or args.dpi < 1:
        parser.error('--samples and --dpi must be positive.')
    generate_figures(args.dataset.resolve(), args.output.resolve(), args.split,
                     args.samples, args.seed, args.dpi, args.automatic)


if __name__ == '__main__':
    main()
