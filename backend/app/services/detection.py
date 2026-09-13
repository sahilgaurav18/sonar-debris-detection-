from ultralytics import YOLO
import os
import cv2

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "best.pt"
)

model = YOLO(MODEL_PATH)


def run_detection(image_path: str):

    results = model.predict(
        source=image_path,
        conf=0.15
    )

    detections = []

    for result in results:

        image_height, image_width = result.orig_shape

        annotated_image = result.plot()

        base_name = os.path.splitext(image_path)[0]
        annotated_path = base_name + "_annotated.jpg"

        cv2.imwrite(annotated_path, annotated_image)

        for box in result.boxes:

            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(float, box.xyxy[0])

            detections.append({
                "object_type": model.names[cls_id],
                "confidence": confidence,
                "bbox": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                }
            })

    return {
        "image_width": image_width,
        "image_height": image_height,
        "detections": detections,
        "annotated_image": annotated_path
    }
