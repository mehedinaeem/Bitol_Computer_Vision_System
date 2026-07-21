import os
import sys
from pathlib import Path
from PIL import Image

TARGET_SIZE = (1024, 1024)

# Input and output base folders
INPUT_DIR = Path(__file__).resolve().parent.parent / "raw_images"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "resized_images"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Specific folders to resize
FOLDERS = ["healthy02", "unhealthy02"]


def resize_images():

    if not INPUT_DIR.exists():
        print(f"Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    total = 0
    skipped = 0

    for folder_name in FOLDERS:

        input_folder = INPUT_DIR / folder_name
        output_folder = OUTPUT_DIR / folder_name

        # Check folder exists
        if not input_folder.exists():
            print(f"Folder not found: {input_folder}")
            continue

        # Create output folder
        output_folder.mkdir(parents=True, exist_ok=True)

        # Loop through images
        for filename in os.listdir(input_folder):

            file_path = input_folder / filename

            # Skip non-image files
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            output_path = output_folder / filename

            # Skip already resized images
            if output_path.exists():
                skipped += 1
                continue

            try:
                # Open image
                img = Image.open(file_path)

                # Resize image
                img = img.resize(TARGET_SIZE, Image.LANCZOS)

                # Save resized image
                img.save(output_path, quality=95)

                print(f"Resized: {filename}")

                total += 1

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nResized: {total} images")
    print(f"Skipped (already exist): {skipped}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    resize_images()