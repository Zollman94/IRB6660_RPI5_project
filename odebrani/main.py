import sys
from pathlib import Path
import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.data.loaders import LoadImages
from yolov5.utils.general import non_max_suppression
from yolov5.utils.torch_utils import select_device

# Nastavení cest
MODEL_PATH = 'models/best.pt'
IMAGE_PATH = 'images/input.jpg'
IMG_SIZE = 640

# Výběr zařízení (CPU nebo GPU)
device = select_device('')  # automaticky

# Načtení modelu
model = DetectMultiBackend(MODEL_PATH, device=device)
names = model.names if hasattr(model, 'names') else [str(i) for i in range(1000)]  # název tříd

# Načtení obrázku
dataset = LoadImages(IMAGE_PATH, img_size=IMG_SIZE)

for path, img, im0s, vid_cap, s in dataset:
    img = torch.from_numpy(img).to(device)
    img = img.float() / 255.0  # normalizace 0-1
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model(img, augment=False)

    # Non-Maximum Suppression (NMS)
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)

    # Výpis výsledků
    for det in pred:
        if len(det):
            # Seřadit podle konfidence a vzít TOP 5
            det = det[det[:, 4].argsort(descending=True)][:5]
            print("\nTop 5 detekcí:")
            for *xyxy, conf, cls in det:
                label = names[int(cls)]
                print(f"{label} - Confidence: {conf:.2f}")