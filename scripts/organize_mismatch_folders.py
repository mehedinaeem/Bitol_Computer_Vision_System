import shutil
from pathlib import Path

MISMATCH_DIR = Path("/home/mehedinaeem/Desktop/Code/Bitol_Computer_Vision_System/detection_dataset/mismatch")

for category in ["healthy", "unhealthy"]:
    cat_dir = MISMATCH_DIR / category
    if not cat_dir.exists():
        continue
    
    img_dir = cat_dir / "images"
    lbl_dir = cat_dir / "labels"
    
    img_dir.mkdir(parents=True, exist_ok=True)
    lbl_dir.mkdir(parents=True, exist_ok=True)
    
    # Move files sitting directly in category directory into images/ or labels/
    for file_path in list(cat_dir.glob("*")):
        if file_path.is_file():
            if file_path.suffix.lower() in [".jpg", ".png", ".jpeg"]:
                shutil.move(file_path, img_dir / file_path.name)
            elif file_path.suffix.lower() == ".txt":
                shutil.move(file_path, lbl_dir / file_path.name)

print("Reorganization complete!")
