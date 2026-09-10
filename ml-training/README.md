# ML Training

This folder is independent from the web app — do this work in Google Colab
(for free GPU) or locally if you have a GPU.

## Steps

1. Download the GhostVision dataset into `dataset/`:
   https://huggingface.co/datasets/PINGEcosystem/sss-crab-pot-detection-ds

2. Install ultralytics:
   pip install ultralytics

3. Fine-tune YOLOv8 on the dataset (see notebooks/train_yolo.ipynb for a
   starting template).

4. Once training is done, copy the resulting `best.pt` file into:
   backend/app/models/yolo_model.pt

5. Update backend/app/services/detection.py to load and use that model,
   then wire it into the /detect route in backend/app/main.py — replace
   the dummy response with real inference, but keep the same response
   shape so the frontend doesn't need any changes.
