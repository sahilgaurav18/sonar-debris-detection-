from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import shutil
import os
import uuid

from PIL import Image

from app.services.detection import run_detection


app = FastAPI(title="Sonar Debris Detection API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024

os.makedirs(UPLOAD_DIR, exist_ok=True)


app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "message": "Backend is running"
    }


@app.post("/upload")
async def upload_sonar_image(
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    file_ext = os.path.splitext(file.filename)[1].lower()

    # Read file to check its size
    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum allowed size is 10 MB."
        )

    await file.seek(0)

    # Check whether the uploaded file is a real, readable image
    try:
        image = Image.open(file.file)
        image.verify()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file. Please upload a valid JPG, JPEG, PNG, or WEBP image."
        )

    await file.seek(0)

    # Check allowed file extension
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload JPG, JPEG, PNG, or WEBP."
        )

    file_id = str(uuid.uuid4())

    saved_filename = f"{file_id}{file_ext}"

    saved_path = os.path.join(
        UPLOAD_DIR,
        saved_filename
    )

    with open(saved_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "status": "success",
        "original_filename": file.filename,
        "saved_as": saved_filename,
        "file_id": file_id,
        "message": "Image uploaded successfully."
    }


@app.get("/detect/{file_id}")
def detect_file(file_id: str):

    matching_files = [
        os.path.join(
            UPLOAD_DIR,
            filename
        )
        for filename in os.listdir(UPLOAD_DIR)
        if filename.startswith(file_id + ".")
    ]

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Uploaded file not found."
        )

    file_path = matching_files[0]

    try:

        detection_result = run_detection(
            file_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Detection failed: {str(e)}"
        )

    annotated_path = detection_result[
        "annotated_image"
    ]

    annotated_filename = os.path.basename(
        annotated_path
    )

    annotated_url = (
        f"/uploads/{annotated_filename}"
    )

    return {
        "status": "success",
        "file_id": file_id,
        "image_width": detection_result["image_width"],
        "image_height": detection_result["image_height"],
        "detection_count": len(detection_result["detections"]),
        "detections": detection_result["detections"],
        "annotated_image": annotated_url
    }