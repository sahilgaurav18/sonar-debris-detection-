---
task_categories:
- object-detection
dataset_info:
  features:
  - name: image
    dtype: image
  - name: objects
    sequence:
    - name: bbox
      sequence: float32
      length: 4
    - name: category
      dtype: string
    - name: area
      dtype: float64
license: cc-by-sa-4.0
models:
- PINGEcosystem/gv-rf-detr
- PINGEcosystem/gv-yolo12
- PINGEcosystem/gv-yolo26
language:
- en
tags:
- sonar
- side-scan-sonar
- crab-pot
- derelict-fishing-gear
pretty_name: Ghost Pot Side-Scan Sonar Detection Dataset
size_categories:
- 1K<n<10K
---

# 🦀 Ghost Pot Side‑Scan Sonar Detection Dataset
**Side‑Scan Sonar Imagery & Annotations for Derelict Crab Pot Detection**

[![Dataset on Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-orange)](https://huggingface.co/datasets/PINGEcosystem/sss-crab-pot-detection-ds)
[![RF-DETR Model](https://img.shields.io/badge/Hugging%20Face-RF--DETR%20Model-yellow)](https://huggingface.co/PINGEcosystem/gv-rf-detr)
[![YOLO12 Model](https://img.shields.io/badge/Hugging%20Face-YOLO12%20Model-yellow)](https://huggingface.co/PINGEcosystem/gv-yolo12)
[![YOLO26 Model](https://img.shields.io/badge/Hugging%20Face-YOLO26%20Model-yellow)](https://huggingface.co/PINGEcosystem/gv-yolo26)

This dataset contains manually annotated side‑scan sonar (SSS) imagery collected across Delaware’s Inland Bays and Delaware Bay to support research on automated detection of derelict crab pots (“ghost pots”). It is designed for training and evaluating object‑detection models in turbid, shallow‑water environments where visual surveys are limited and acoustic mapping is essential.

The dataset accompanies the [GhostVision](https://github.com/PINGEcosystem/GhostVision) project, an open‑source pipeline for near–real‑time detection and mapping of derelict fishing gear.

## 🤖 Related Models
The corresponding trained models are available at [PINGEcosystem/gv-rf-detr](https://huggingface.co/PINGEcosystem/gv-rf-detr), [PINGEcosystem/gv-yolo12](https://huggingface.co/PINGEcosystem/gv-yolo12), and [PINGEcosystem/gv-yolo26](https://huggingface.co/PINGEcosystem/gv-yolo26).

## 📜 Publication
Bodine, C. S., Baxevani, K., Abbasi, N., Wierzbicki, J., Christoph, O., Hughes, C., Bagoren, O., Hines, O., Greco, J., & Trembanis, A. (2026). GhostVision: Democratizing Derelict Gear Detection Using Low-Cost Sonar and Artificial Intelligence. Journal of Marine Science and Engineering, 14(10), 951. https://doi.org/10.3390/jmse14100951

## 📦 Dataset Overview
- Total images: 6,674

- Sensor type: Consumer‑grade Humminbird side‑scan sonar

- Spatial coverage:

  - northern Rehoboth Bay near Dewey Beach
  - western Indian River Bay
  - southern Indian River Bay near White Creek

- Annotation format: JSON Lines (JSONL)

- Annotation type: Axis‑aligned bounding boxes

- Classes:
  - Crab-Pot — high confidence
  - Maybe-Crab-Pot — ambiguous or low‑confidence pot‑like target

- Coordinate system: Pixel coordinates in image space

File structure:

```Code
sss-crab-pot-detection
├── train/
│   ├── <image>.jpg
│   └── metadata.jsonl
├── valid/
│   ├── <image>.jpg
│   └── metadata.jsonl
├── train/
│   ├── <image>.jpg
│   └── metadata.jsonl
```

All annotations were created manually by trained analysts using high‑resolution sonar mosaics and cross‑validated with field notes and independent review.

## 🎯 Motivation
Derelict crab pots are a major source of ghost‑fishing mortality and benthic habitat damage. Existing removal programs rely on opportunistic sonar use during retrieval operations, meaning no formal mapping or archiving of pot locations exists. As a result, managers lack:

- basin‑wide estimates of derelict pot abundance
- spatial patterns of accumulation
- quantitative evaluation of removal efforts

This dataset enables reproducible, scalable research on automated detection, mapping, and monitoring of derelict fishing gear.

## 🗂️ Data Structure
This dataset uses JSON Lines (JSONL) format, where each line corresponds to a single image and all annotations associated with that image. This structure is natively supported by the Hugging Face Datasets library and enables efficient streaming and inspection.

### 🧾 JSONL Schema
Each row has the following structure:

```json
{
  "file_name": "<image filename>",
  "objects": {
    "bbox": [ [x, y, width, height], ... ],
    "category": [ "<class>", ... ],
    "area": [ <area>, ... ]
  }
}
```

### 🏷️ Field Definitions
- file_name — relative path to the image file
- objects.bbox — list of bounding boxes in [x, y, width, height] format
- objects.category — list of class labels ("Crab-Pot" or "Maybe-Crab-Pot")
- objects.area — list of pixel areas for each bounding box

### 📭 Example: Image With No Detections
```json
{
  "file_name": "Contact_334_sslo_png_jpg.rf.9c8a769f3c36deba4278527e714e09b7.jpg",
  "objects": {
    "bbox": [],
    "category": [],
    "area": []
  }
}
```

### 🖼️ Example: Image With Annotations
```json
{
  "file_name": "Contact_203_sslo_png_jpg.rf.d9b44748a1bf7d9a30126e649741d745.jpg",
  "objects": {
    "bbox": [
      [309, 307, 26, 21],
      [196, 198, 29.5, 19]
    ],
    "category": ["Crab-Pot", "Crab-Pot"],
    "area": [546, 560.5]
  }
}
```

### 🏷️ Class Labels
- Crab-Pot — high-confidence derelict pot
- Maybe-Crab-Pot — ambiguous or low‑confidence pot‑like target

These are stored as strings for readability and compatibility with the Hugging Face viewer.

## 🚀 Loading the Dataset

```python
from datasets import load_dataset

ds = load_dataset(PINGEcosystem/sss-crab-pot-detection)

# Get test dataset
ds = ds['test']

# Access bounding boxes for the first image
ds[0]["objects"]["bbox"]
```

## 🧪 Recommended Uses
This dataset is suitable for:
- Object detection (YOLO, DETR, RT‑DETR, RF‑DETR, etc.)
- Acoustic target classification
- Weakly supervised or semi‑supervised learning
- Spatiotemporal persistence modeling
- Benchmarking confidence/persistence fusion methods
- Research on ghost‑gear mapping and marine debris monitoring

## ⚠️ Limitations
- Sonar appearance varies with substrate, tow speed, and turbidity.
- Ambiguous targets are labeled as Maybe-Crab-Pot to avoid forcing false certainty.
- Not all pots are visible in every pass; some are buried or obscured.
- Dataset is region‑specific (Delaware), though methods generalize broadly.
- Users should consider domain adaptation when applying models to other regions or sonar systems.

## 🔗 Related Resources
- GhostVision project: [PINGEcosystem/GhostVision](https://github.com/PINGEcosystem/GhostVision)
- RF-DETR model: [PINGEcosystem/gv-rf-detr](https://huggingface.co/PINGEcosystem/gv-rf-detr)
- YOLO12 model: [PINGEcosystem/gv-yolo12](https://huggingface.co/PINGEcosystem/gv-yolo12)
- YOLO26 model: [PINGEcosystem/gv-yolo26](https://huggingface.co/PINGEcosystem/gv-yolo26)

## 📜 License
This dataset is released under the GPL license.

## 🙌 Acknowledgments
This dataset was developed with support from:
- University of Delaware -- Center for Coastal Sediments Hydrodynamics and Engineering Lab (CSHEL)
- Delaware Sea Grant
- 2024 Autonomous Systems Bootcamp
- NOAA's Project ABLE
- NOAA Marine Debris Program
- Delaware Department of Natural Resources and Environmental Control (DNREC)
- Community volunteers participating in ghost‑gear surveys