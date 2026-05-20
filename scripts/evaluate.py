# evaluate.py
# Placeholder for evaluation script.
from ultralytics import YOLO

# Load best model
model = YOLO(
    "runs/detect/models/trained/bitol_yolov8/weights/best.pt"
)

# Evaluate model
metrics = model.val()

# Print metrics
print("\n========== EVALUATION RESULTS ==========\n")

print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)
print("Precision:", metrics.box.mp)
print("Recall:", metrics.box.mr)