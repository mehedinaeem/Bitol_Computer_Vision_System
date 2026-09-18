import shutil
from pathlib import Path

# Project root and dataset paths
DATASET_ROOT = Path("/home/mehedinaeem/Desktop/Code/Bitol_Computer_Vision_System/detection_dataset")
MISMATCH_DIR = DATASET_ROOT / "mismatch"

HEALTHY_MISMATCHES = [
    "healthy_0707", "healthy_0716", "healthy_0745", "healthy_0796",
    "healthy_0867", "healthy_0876", "healthy_0878", "healthy_0897",
    "healthy_0899", "healthy_0905", "healthy_0972", "healthy_1206",
    "healthy_1209", "healthy_1228", "healthy_1230"
]

UNHEALTHY_MISMATCHES = [
    "unhealthy_0370", "unhealthy_0371", "unhealthy_0372", "unhealthy_0373",
    "unhealthy_0378", "unhealthy_0379", "unhealthy_0383", "unhealthy_0384",
    "unhealthy_0391", "unhealthy_0392", "unhealthy_0395", "unhealthy_0396",
    "unhealthy_0403", "unhealthy_0404", "unhealthy_0405", "unhealthy_0406",
    "unhealthy_0407", "unhealthy_0408", "unhealthy_0411", "unhealthy_0438",
    "unhealthy_1405"
]

target_healthy_dir = MISMATCH_DIR / "healthy"
target_unhealthy_dir = MISMATCH_DIR / "unhealthy"

target_healthy_dir.mkdir(parents=True, exist_ok=True)
target_unhealthy_dir.mkdir(parents=True, exist_ok=True)

def find_and_copy(stem, target_dir):
    copied_img = False
    copied_lbl = False
    
    # Search across all splits (test, train)
    for split in ["test", "train"]:
        img_dir = DATASET_ROOT / "images" / split
        lbl_dir = DATASET_ROOT / "labels" / split
        
        # Check image candidates
        for ext in [".jpg", ".png", ".jpeg"]:
            img_path = img_dir / f"{stem}{ext}"
            if img_path.exists():
                shutil.copy2(img_path, target_dir / img_path.name)
                copied_img = True
                break
        
        # Check label candidate
        lbl_path = lbl_dir / f"{stem}.txt"
        if lbl_path.exists():
            shutil.copy2(lbl_path, target_dir / lbl_path.name)
            copied_lbl = True
            
        if copied_img and copied_lbl:
            break
            
    print(f"[{stem}] Image copied: {copied_img}, Label copied: {copied_lbl}")

print("=== Copying Healthy Mismatches ===")
for stem in HEALTHY_MISMATCHES:
    find_and_copy(stem, target_healthy_dir)

print("\n=== Copying Unhealthy Mismatches ===")
for stem in UNHEALTHY_MISMATCHES:
    find_and_copy(stem, target_unhealthy_dir)

print(f"\nDone! Files organized in {MISMATCH_DIR}")
