import re
from pathlib import Path
from collections import Counter, defaultdict

log_file = Path("scripts/test_predictions_log.txt")
if not log_file.exists():
    print("Log file not found at scripts/test_predictions_log.txt")
    exit(1)

with open(log_file, "r") as f:
    log_text = f.read()

lines = [line.strip() for line in log_text.strip().splitlines() if line.startswith("image ")]

records = []
for line in lines:
    m = re.search(r'images/test/([^:]+): 640x640 (.*?), \d+\.\d+ms', line)
    if not m:
        continue
    img_name = m.group(1)
    det_str = m.group(2)
    
    gt_prefix = "healthy" if img_name.startswith("healthy") else "unhealthy"
    
    if "(no detections)" in det_str:
        num_healthy = 0
        num_unhealthy = 0
        status = "no_detections"
    else:
        healthy_match = re.search(r'(\d+)\s+healthy', det_str)
        unhealthy_match = re.search(r'(\d+)\s+unhealthy', det_str)
        num_healthy = int(healthy_match.group(1)) if healthy_match else 0
        num_unhealthy = int(unhealthy_match.group(1)) if unhealthy_match else 0
        
        if num_healthy > 0 and num_unhealthy > 0:
            status = "mixed_detections"
        elif gt_prefix == "healthy" and num_healthy > 0 and num_unhealthy == 0:
            status = "pure_correct"
        elif gt_prefix == "unhealthy" and num_unhealthy > 0 and num_healthy == 0:
            status = "pure_correct"
        elif gt_prefix == "healthy" and num_healthy == 0 and num_unhealthy > 0:
            status = "full_mismatch"
        elif gt_prefix == "unhealthy" and num_unhealthy == 0 and num_healthy > 0:
            status = "full_mismatch"
        else:
            status = "other"

    records.append({
        "image": img_name,
        "gt_prefix": gt_prefix,
        "det_summary": det_str,
        "num_healthy": num_healthy,
        "num_unhealthy": num_unhealthy,
        "status": status
    })

print(f"=== PREDICTION SUMMARY FOR {len(records)} TEST IMAGES ===")
status_counts = Counter(r["status"] for r in records)
for status, count in status_counts.most_common():
    print(f"  {status}: {count} ({count/len(records)*100:.2f}%)")

print("\n=== DETAILED BREAKDOWN BY GROUND TRUTH PREFIX ===")
gt_breakdown = defaultdict(Counter)
for r in records:
    gt_breakdown[r["gt_prefix"]][r["status"]] += 1

for gt, counts in gt_breakdown.items():
    print(f"\nGround Truth Prefix: {gt.upper()}")
    for st, cnt in counts.most_common():
        print(f"  - {st}: {cnt}")

print("\n=== NO DETECTIONS (0 DETECTIONS) ===")
no_det = [r for r in records if r["status"] == "no_detections"]
print(f"Total: {len(no_det)}")
for r in no_det:
    print(f" - {r['image']}: {r['det_summary']}")

print("\n=== FULL MISMATCH (E.G. HEALTHY IMAGE -> ONLY UNHEALTHY DETECTED, OR UNHEALTHY IMAGE -> ONLY HEALTHY DETECTED) ===")
mismatch = [r for r in records if r["status"] == "full_mismatch"]
print(f"Total: {len(mismatch)}")
for r in mismatch:
    print(f" - {r['image']} (GT: {r['gt_prefix']}): {r['det_summary']}")

print("\n=== MIXED DETECTIONS (E.G. IMAGE HAS BOTH HEALTHY AND UNHEALTHY DETECTIONS) ===")
mixed = [r for r in records if r["status"] == "mixed_detections"]
print(f"Total: {len(mixed)}")
for r in mixed:
    print(f" - {r['image']} (GT: {r['gt_prefix']}): {r['det_summary']}")

