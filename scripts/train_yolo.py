from ultralytics import YOLO

# Automatically download pretrained model
model = YOLO("yolov8n.pt")

# Train model
model.train(
    data="detection_dataset/data.yaml",
    epochs=50,
    imgsz=1024,
    batch=4,
    project="models/trained",
    name="bitol_yolov8"
)

print("Training completed!")