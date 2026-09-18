# Model accuracy

**Test mAP@50: 87.04%**

Verified using `weights/best.pt` on **491 test images** containing **1,445 annotated objects**.
For this object-detection model, the main accuracy metric is mAP@50.

| Test metric | Result |
|---|---:|
| mAP@50 | 87.04% |
| mAP@50:95 | 59.33% |
| Precision | 81.36% |
| Recall | 74.30% |
| F1-score | 77.67% |

Model: YOLOv8n · Input: 640 × 640 · Batch: 4 · Training: 50 epochs.

[Accuracy CSV](accuracy.csv) · [Full verification metrics](final_experiment/verification/metrics.csv) · [Checkpoint and environment](final_experiment/verification/provenance.json)

The existing train/test duplicate-image overlap remains a limitation of this score; see [dataset audit](../detection_dataset/README.md).
