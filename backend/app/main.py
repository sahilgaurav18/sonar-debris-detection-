from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

app = FastAPI(title="Sonar Debris Detection API")

# Allow frontend (React) to call this backend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later to your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    """Quick check to confirm the server is running."""
    return {"status": "ok", "message": "Backend is running"}


@app.post("/upload")
async def upload_sonar_image(file: UploadFile = File(...)):
    """
    Accepts a sonar image, saves it locally, and returns its path.
    No AI processing yet — this just confirms upload works end to end.
    """
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{file_id}{file_ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "original_filename": file.filename,
        "saved_as": saved_filename,
        "file_id": file_id,
        "message": "Image uploaded successfully. Detection not yet connected."
    }


@app.get("/detect/{file_id}")
def detect_placeholder(file_id: str):
    """
    Placeholder for the future YOLO detection route.
    Returns dummy data so the frontend can be built against this shape now.
    Replace the body of this function with real YOLO inference later —
    keep the response shape the same so the frontend doesn't need changes.
    """
    return {
        "file_id": file_id,
        "detections": [
            {
                "object_id": 1,
                "type": "ghost_net",
                "confidence": 0.92,
                "bbox": [120, 80, 260, 190],
                "lat": 19.0760,
                "long": 72.8777,
                "estimated_size_m": "12.4 x 4.1"
            },
            {
                "object_id": 2,
                "type": "shipwreck",
                "confidence": 0.87,
                "bbox": [300, 150, 480, 320],
                "lat": 19.0800,
                "long": 72.8801,
                "estimated_size_m": "20.0 x 8.2"
            }
        ]
    }
