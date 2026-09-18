import os
import re
from pathlib import Path
from collections import Counter

def rename_misnamed_dataset(dataset_dir="detection_dataset", dry_run=True):
    ds = Path(dataset_dir)
    
    summary = {
        "train": {"h_to_u": [], "u_to_h": []},
        "test": {"h_to_u": [], "u_to_h": []}
    }

    for split in ["train", "test"]:
        img_dir = ds / "images" / split
        lbl_dir = ds / "labels" / split
        
        if not img_dir.exists() or not lbl_dir.exists():
            print(f"Warning: Split {split} directory missing. Skipping.")
            continue
            
        current_stems = {f.stem for f in img_dir.glob("*.jpg")}
        
        max_h = max([int(m.group(1)) for s in current_stems if (m := re.match(r"^healthy_(\d+)$", s))] or [0])
        max_u = max([int(m.group(1)) for s in current_stems if (m := re.match(r"^unhealthy_(\d+)$", s))] or [0])
        
        next_free_h = max_h + 1
        next_free_u = max_u + 1
        
        # Track reserved names to avoid collisions during batch rename
        reserved_stems = set(current_stems)
        
        rename_pairs = [] # (old_stem, new_stem, type)
        
        for lbl_path in sorted(lbl_dir.glob("*.txt")):
            if lbl_path.name == "classes.txt":
                continue
            lines = [l.strip() for l in lbl_path.read_text(encoding="utf-8").splitlines() if l.strip()]
            if not lines:
                continue
                
            classes = [int(l.split()[0]) for l in lines if l.split()]
            counts = Counter(classes)
            stem = lbl_path.stem
            
            # Check image file existence
            img_path = img_dir / f"{stem}.jpg"
            if not img_path.exists():
                print(f"Warning: Label {lbl_path.name} exists but image {img_path.name} is missing!")
                continue
                
            target_stem = None
            rename_type = None
            
            # Case 1: File named healthy, but labels are mostly/all class 1 (unhealthy)
            if stem.startswith("healthy") and counts[1] > counts[0]:
                rename_type = "healthy_to_unhealthy"
                ideal = stem.replace("healthy", "unhealthy", 1)
                if ideal not in reserved_stems:
                    target_stem = ideal
                else:
                    while f"unhealthy_{next_free_u:04d}" in reserved_stems:
                        next_free_u += 1
                    target_stem = f"unhealthy_{next_free_u:04d}"
                    next_free_u += 1
                    
            # Case 2: File named unhealthy, but labels are mostly/all class 0 (healthy)
            elif stem.startswith("unhealthy") and counts[0] > counts[1]:
                rename_type = "unhealthy_to_healthy"
                ideal = stem.replace("unhealthy", "healthy", 1)
                if ideal not in reserved_stems:
                    target_stem = ideal
                else:
                    while f"healthy_{next_free_h:04d}" in reserved_stems:
                        next_free_h += 1
                    target_stem = f"healthy_{next_free_h:04d}"
                    next_free_h += 1

            if target_stem and target_stem != stem:
                # Remove old stem from reserved, add new stem to reserved
                reserved_stems.discard(stem)
                reserved_stems.add(target_stem)
                rename_pairs.append((stem, target_stem, rename_type, counts))
                
                if rename_type == "healthy_to_unhealthy":
                    summary[split]["h_to_u"].append((stem, target_stem, dict(counts)))
                else:
                    summary[split]["u_to_h"].append((stem, target_stem, dict(counts)))

        print(f"\n--- Split [{split.upper()}] ({'DRY RUN' if dry_run else 'EXECUTING'}) ---")
        print(f"  Healthy -> Unhealthy renames: {len(summary[split]['h_to_u'])}")
        print(f"  Unhealthy -> Healthy renames: {len(summary[split]['u_to_h'])}")
        print(f"  Total Renamed Files in {split}: {len(rename_pairs)}")

        if not dry_run:
            # Perform atomic/safe rename
            # Step A: Rename to temporary names first to avoid collision loops
            temp_map = []
            for old_s, new_s, _, _ in rename_pairs:
                tmp_s = f"__TMP_RENAME_{old_s}"
                
                old_img = img_dir / f"{old_s}.jpg"
                old_lbl = lbl_dir / f"{old_s}.txt"
                tmp_img = img_dir / f"{tmp_s}.jpg"
                tmp_lbl = lbl_dir / f"{tmp_s}.txt"
                
                old_img.rename(tmp_img)
                old_lbl.rename(tmp_lbl)
                temp_map.append((tmp_s, new_s))
                
            # Step B: Rename temporary files to final names
            for tmp_s, new_s in temp_map:
                tmp_img = img_dir / f"{tmp_s}.jpg"
                tmp_lbl = lbl_dir / f"{tmp_s}.txt"
                final_img = img_dir / f"{new_s}.jpg"
                final_lbl = lbl_dir / f"{new_s}.txt"
                
                tmp_img.rename(final_img)
                tmp_lbl.rename(final_lbl)
                
            print(f"Successfully executed rename operations for split [{split}].")

    return summary

if __name__ == "__main__":
    import sys
    execute = "--execute" in sys.argv
    rename_misnamed_dataset(dry_run=not execute)
