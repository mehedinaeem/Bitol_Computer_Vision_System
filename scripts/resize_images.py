import os
import sys
from pathlib import Path
from PIL import Image

TARGET_SIZE = (1024, 1024)
INPUT_DIR = Path(__file__).resolve().parent.parent / "raw_images"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "resized_images"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def resize_images():
    if not INPUT_DIR.exists():
        print(f"Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    total = 0
    skipped = 0

    for root, _, files in os.walk(INPUT_DIR):
        for filename in files:
            if Path(filename).suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            src_path = Path(root) / filename
            relative = src_path.relative_to(INPUT_DIR)
            dest_path = OUTPUT_DIR / relative

            dest_path.parent.mkdir(parents=True, exist_ok=True)

            if dest_path.exists():
                skipped += 1
                continue

            img = Image.open(src_path)
            img = img.resize(TARGET_SIZE, Image.LANCZOS)
            img.save(dest_path, quality=95)
            total += 1

    print(f"Resized: {total} images | Skipped (already exist): {skipped}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    resize_images()
