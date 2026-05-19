from ultralytics import YOLO

model = YOLO(
    "runs/detect/models/trained/bitol_yolov8/weights/best.pt"
)

metrics = model.val(
    data="detection_dataset/data.yaml",
    split="test"
)

print("\n========== TEST RESULTS ==========\n")

print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)
print("Precision:", metrics.box.mp)
print("Recall:", metrics.box.mr)