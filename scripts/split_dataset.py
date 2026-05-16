import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "resized_images"
TARGET_DIR = BASE_DIR / "detection_dataset"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2


def find_images(src_dir: Path) -> List[Path]:
    return sorted(
        p for p in src_dir.rglob("*")
        if p.suffix.lower() in IMAGE_EXTENSIONS
    )


def group_by_class(images: List[Path]) -> Dict[str, List[Path]]:
    groups = defaultdict(list)
    for img in images:
        groups[img.parent.name].append(img)
    return dict(groups)


def split_dataset():
    if not SOURCE_DIR.exists():
        print(f"Source directory not found: {SOURCE_DIR}")
        print("Run resize_images.py first.")
        return

    images = find_images(SOURCE_DIR)
    if not images:
        print(f"No images found in {SOURCE_DIR}")
        return

    for split in ("train", "val", "test"):
        (TARGET_DIR / "images" / split).mkdir(parents=True, exist_ok=True)

    counts = {"train": 0, "val": 0, "test": 0}

    for class_name, class_images in group_by_class(images).items():
        train_end = int(len(class_images) * TRAIN_RATIO)
        val_end = int(len(class_images) * (TRAIN_RATIO + VAL_RATIO))

        splits = {
            "train": class_images[:train_end],
            "val": class_images[train_end:val_end],
            "test": class_images[val_end:],
        }

        for split, split_images in splits.items():
            for img_path in split_images:
                dest = TARGET_DIR / "images" / split / img_path.name
                if not dest.exists():
                    shutil.copy2(img_path, dest)
                counts[split] += 1

        for split, split_images in splits.items():
            print(f"  {class_name} -> {split}: {len(split_images)}")

    total = sum(counts.values())
    print(f"\nTotal {total} images split into:")
    for split, count in counts.items():
        print(f"  {split}: {count}")
    print(f"Output: {TARGET_DIR}")


if __name__ == "__main__":
    split_dataset()
