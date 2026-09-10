"""
Sonar image preprocessing utilities.

Fill this in during Phase 4:
- CLAHE contrast enhancement
- Speckle noise reduction
- Slant-range correction (if working with raw sonar formats)

Example starting point:

import cv2

def preprocess_sonar_image(image_path: str) -> "cv2.Mat":
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(img)
    denoised = cv2.medianBlur(enhanced, 3)
    return denoised
"""
