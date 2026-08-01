import random
import shutil
from pathlib import Path
from typing import Dict, List, Optional

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "resized_images"
TARGET_DIR = BASE_DIR / "detection_dataset"
LABELS_DIR = TARGET_DIR / "labels"

# Only add the two new batches. Every image in each class is independently
# split into train/validation/test using the same 70/20/10 proportions.
SOURCE_CLASSES = {
    "healthy": SOURCE_DIR / "healthy03",
    "unhealthy": SOURCE_DIR / "unhealthy03",
}

SPLIT_RATIOS = {"train": 0.70, "val": 0.20, "test": 0.10}
RANDOM_SEED = 42


def find_images(src_dir: Path) -> List[Path]:
    return sorted(
        path
        for path in src_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def build_label_index(labels_dir: Path) -> Dict[str, Path]:
    """Index labels whether they are in labels/ or labels/train|val|test/."""
    index: Dict[str, Path] = {}
    if not labels_dir.exists():
        return index

    for label_path in sorted(labels_dir.rglob("*.txt")):
        if label_path.name != "classes.txt":
            index.setdefault(label_path.name, label_path)
    return index


def split_counts(total: int) -> Dict[str, int]:
    """Allocate all samples while keeping the requested 70/20/10 ratio."""
    train = int(total * SPLIT_RATIOS["train"])
    val = int(total * SPLIT_RATIOS["val"])
    return {"train": train, "val": val, "test": total - train - val}


def copy_if_not_exists(src: Path, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return False
    shutil.copy2(src, dest)
    return True


def matching_label(image: Path, label_index: Dict[str, Path]) -> Optional[Path]:
    return label_index.get(f"{image.stem}.txt")


def split_dataset() -> None:
    missing_dirs = [path for path in SOURCE_CLASSES.values() if not path.exists()]
    if missing_dirs:
        for path in missing_dirs:
            print(f"Source directory not found: {path}")
        return

    class_images = {
        class_name: find_images(source_path)
        for class_name, source_path in SOURCE_CLASSES.items()
    }
    if any(not images for images in class_images.values()):
        for class_name, images in class_images.items():
            print(f"{class_name}: found {len(images)} images")
        return

    for split in SPLIT_RATIOS:
        (TARGET_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (TARGET_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

    label_index = build_label_index(LABELS_DIR)
    print("Source images:")
    for class_name, images in class_images.items():
        label_count = sum(
            matching_label(image, label_index) is not None for image in images
        )
        print(f"  {class_name}: {len(images)} images, {label_count} existing labels")

    rng = random.Random(RANDOM_SEED)

    added = {split: {class_name: 0 for class_name in SOURCE_CLASSES} for split in SPLIT_RATIOS}
    existing = {split: {class_name: 0 for class_name in SOURCE_CLASSES} for split in SPLIT_RATIOS}
    expected_counts: Dict[str, Dict[str, int]] = {}

    copied_labels = 0
    missing_labels = 0

    for class_name, images in class_images.items():
        rng.shuffle(images)
        class_counts = split_counts(len(images))
        expected_counts[class_name] = class_counts

        train_end = class_counts["train"]
        val_end = train_end + class_counts["val"]
        splits = {
            "train": images[:train_end],
            "val": images[train_end:val_end],
            "test": images[val_end:],
        }

        for split, split_images in splits.items():
            for image_path in split_images:
                image_dest = TARGET_DIR / "images" / split / image_path.name
                if copy_if_not_exists(image_path, image_dest):
                    added[split][class_name] += 1
                else:
                    existing[split][class_name] += 1

                label_path = matching_label(image_path, label_index)
                if label_path is None:
                    missing_labels += 1
                else:
                    label_dest = TARGET_DIR / "labels" / split / label_path.name
                    if copy_if_not_exists(label_path, label_dest):
                        copied_labels += 1

    print("\n70/20/10 split per class:")
    for split in SPLIT_RATIOS:
        healthy = expected_counts["healthy"][split]
        unhealthy = expected_counts["unhealthy"][split]
        print(
            f"  {split}: {healthy} healthy + {unhealthy} unhealthy "
            f"({healthy + unhealthy} total)"
        )

    print("\nNew images copied:")
    for split in SPLIT_RATIOS:
        print(
            f"  {split}: healthy={added[split]['healthy']}, "
            f"unhealthy={added[split]['unhealthy']}"
        )

    already_present = sum(sum(counts.values()) for counts in existing.values())
    if already_present:
        print(f"Already present and not overwritten: {already_present}")

    print(f"Existing labels copied: {copied_labels}")
    print(
        f"Images waiting for annotation: {missing_labels} "
        "(no empty label files were created)"
    )

    print(f"\nDataset updated: {TARGET_DIR}")


if __name__ == "__main__":
    split_dataset()
