import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

BASE_DIR = Path(__file__).resolve().parent.parent

# Source images
SOURCE_DIR = BASE_DIR / "resized_images"

# Existing YOLO labels
LABELS_DIR = BASE_DIR / "detection_dataset" / "labels"

# Output dataset
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


def copy_if_not_exists(src: Path, dest: Path):

    dest.parent.mkdir(parents=True, exist_ok=True)

    # IMPORTANT:
    # skip existing files
    # do NOT overwrite old dataset
    if dest.exists():
        return False

    shutil.copy2(src, dest)
    return True


def split_dataset():

    if not SOURCE_DIR.exists():
        print(f"Source directory not found: {SOURCE_DIR}")
        return

    images = find_images(SOURCE_DIR)

    if not images:
        print(f"No images found in {SOURCE_DIR}")
        return

    # Create dataset folders
    for split in ("train", "val", "test"):

        (TARGET_DIR / "images" / split).mkdir(
            parents=True,
            exist_ok=True
        )

        (TARGET_DIR / "labels" / split).mkdir(
            parents=True,
            exist_ok=True
        )

    counts = {
        "train": 0,
        "val": 0,
        "test": 0
    }

    grouped_images = group_by_class(images)

    for class_name, class_images in grouped_images.items():

        total_images = len(class_images)

        train_end = int(total_images * TRAIN_RATIO)
        val_end = int(total_images * (TRAIN_RATIO + VAL_RATIO))

        splits = {
            "train": class_images[:train_end],
            "val": class_images[train_end:val_end],
            "test": class_images[val_end:]
        }

        for split, split_images in splits.items():

            added = 0

            for img_path in split_images:

                # Image destination
                img_dest = (
                    TARGET_DIR
                    / "images"
                    / split
                    / img_path.name
                )

                # Copy image only if not exists
                image_added = copy_if_not_exists(
                    img_path,
                    img_dest
                )

                # Matching label
                label_name = img_path.stem + ".txt"

                label_src = LABELS_DIR / label_name

                if label_src.exists():

                    label_dest = (
                        TARGET_DIR
                        / "labels"
                        / split
                        / label_name
                    )

                    copy_if_not_exists(
                        label_src,
                        label_dest
                    )

                if image_added:
                    added += 1
                    counts[split] += 1

            print(
                f"{class_name} -> {split}: added {added}"
            )

    total = sum(counts.values())

    print(f"\nNew images added: {total}")

    for split, count in counts.items():
        print(f"{split}: {count}")

    print(f"\nDataset updated successfully!")
    print(f"Output: {TARGET_DIR}")


if __name__ == "__main__":
    split_dataset()