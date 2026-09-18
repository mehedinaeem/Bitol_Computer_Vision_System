from pathlib import Path

MISMATCH_DIR = Path("/home/mehedinaeem/Desktop/Code/Bitol_Computer_Vision_System/detection_dataset/mismatch")

def rename_category(category, start_num):
    img_dir = MISMATCH_DIR / category / "images"
    lbl_dir = MISMATCH_DIR / category / "labels"
    
    # Collect all image files sorted by filename
    img_files = sorted(list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg")))
    
    current_num = start_num
    print(f"\n=== Renaming {category.upper()} files starting from {start_num} ===")
    
    for img_file in img_files:
        stem = img_file.stem
        ext = img_file.suffix
        lbl_file = lbl_dir / f"{stem}.txt"
        
        new_stem = f"{category}_{current_num:04d}"
        new_img_path = img_dir / f"{new_stem}{ext}"
        new_lbl_path = lbl_dir / f"{new_stem}.txt"
        
        print(f"Renaming {stem} -> {new_stem}")
        
        # Rename image
        img_file.rename(new_img_path)
        
        # Rename label if exists
        if lbl_file.exists():
            lbl_file.rename(new_lbl_path)
        else:
            print(f"  Warning: label file {lbl_file} not found!")
            
        current_num += 1

rename_category("healthy", 1442)
rename_category("unhealthy", 1410)

print("\nRenaming complete!")
