"""
YOLO detection service.

Fill this in during Phase 5, once you have a trained model (.pt file)
from ml-training/. Load the model ONCE at startup, not per-request.

Example starting point:

from ultralytics import YOLO

model = YOLO("app/models/yolo_model.pt")

def run_detection(image_path: str):
    results = model(image_path)
    detections = []
    for box in results[0].boxes:
        detections.append({
            "type": model.names[int(box.cls)],
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist()[0],
        })
    return detections
"""
