# predict.py
# Placeholder for prediction script.

from ultralytics import YOLO

# Load trained model
model = YOLO(
    "runs/detect/models/trained/bitol_yolov8/weights/best.pt"
)

# Run prediction
results = model.predict(
    source="detection_dataset/images/test",
    save=True,
    conf=0.25
)

print("Prediction completed!")
