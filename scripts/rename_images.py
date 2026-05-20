import os

# Base dataset path
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "raw_images")
)

# Folder configuration
folders = {
    "healthy01": {
        "prefix": "healthy",
        "start": 139
    },
    "unhealthy01": {
        "prefix": "unhealthy",
        "start": 361
    }
}

for folder, config in folders.items():

    folder_path = os.path.join(BASE_DIR, folder)

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue

    # Get all image files
    files = sorted(os.listdir(folder_path))

    # Starting counter
    count = config["start"]

    for file in files:

        # Skip non-image files
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Preserve original extension
        extension = os.path.splitext(file)[1].lower()

        # New filename
        new_name = f"{config['prefix']}_{count:04}{extension}"

        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)

        # Rename file
        os.rename(old_path, new_path)

        print(f"Renamed: {file} -> {new_name}")

        count += 1

print("\nRenaming completed successfully!")