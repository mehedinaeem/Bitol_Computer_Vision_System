import hashlib
from pathlib import Path

def file_hash(p):
    return hashlib.md5(p.read_bytes()).hexdigest()

def sync_resized_images(dry_run=True):
    ds_dir = Path("detection_dataset/images")
    resized_dir = Path("resized_images")
    
    if not ds_dir.exists() or not resized_dir.exists():
        print("Required directories missing.")
        return
        
    # Map MD5 hash -> (split, new_filename) in detection_dataset
    ds_map = {}
    for p in ds_dir.rglob("*.jpg"):
        ds_map[file_hash(p)] = (p.parent.name, p.name)
        
    moves = []
    renames_in_place = []
    
    for p in sorted(resized_dir.rglob("*.jpg")):
        h = file_hash(p)
        if h in ds_map:
            split, new_name = ds_map[h]
            current_folder = p.parent.name
            
            # Determine target folder base
            is_new_unhealthy = new_name.startswith("unhealthy")
            is_new_healthy = new_name.startswith("healthy")
            
            target_parent = p.parent
            
            # If cross-class move (e.g. from healthy* folder to unhealthy folder)
            if is_new_unhealthy and "healthy" in current_folder and "unhealthy" not in current_folder:
                # Move to main unhealthy directory
                target_parent = resized_dir / "unhealthy"
            elif is_new_healthy and "unhealthy" in current_folder:
                # Move to main healthy directory
                target_parent = resized_dir / "healthy"
                
            target_path = target_parent / new_name
            
            if p != target_path:
                moves.append((p, target_path))

    print(f"\n--- Syncing Resized Images ({'DRY RUN' if dry_run else 'EXECUTING'}) ---")
    print(f"Total files to rename/move in resized_images: {len(moves)}")
    
    if not dry_run:
        for old_p, new_p in moves:
            new_p.parent.mkdir(parents=True, exist_ok=True)
            old_p.rename(new_p)
        print("Successfully synchronized resized_images directory!")

if __name__ == "__main__":
    import sys
    execute = "--execute" in sys.argv
    sync_resized_images(dry_run=not execute)
