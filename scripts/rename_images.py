import os

# Base dataset path (resolved relative to this script)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "raw_images"))

# Folders
folders = ["healthy", "unhealthy"]

for folder in folders:

    folder_path = os.path.join(BASE_DIR, folder)

    # Get all image files
    files = sorted(os.listdir(folder_path))

    # Counter
    count = 1

    for file in files:

        # Skip non-image files
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # New filename
        new_name = f"{folder}_{count:04}.jpg"

        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)

        # Rename
        os.rename(old_path, new_path)

        print(f"Renamed: {file} -> {new_name}")

        count += 1

print("\nRenaming completed successfully!")