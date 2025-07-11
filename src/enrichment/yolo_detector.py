# src/enrichment/yolo_detector.py

from ultralytics import YOLO
from pathlib import Path
import os
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()

model = YOLO('yolov8n.pt')  # You can use yolov8m.pt or yolov8l.pt for better accuracy

IMAGE_DIR = Path("data/raw/images")
OUTPUT_FILE = Path("data/processed/image_detections.csv")
results = []

# Scan images
for channel_dir in IMAGE_DIR.iterdir():
    for image_file in channel_dir.glob("*.jpg"):
        message_id = int(image_file.stem)
        detections = model(image_file)[0]  # Single image inference

        for box in detections.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            conf = float(box.conf[0])
            results.append({
                "message_id": message_id,
                "channel_name": channel_dir.name,
                "detected_object_class": class_name,
                "confidence_score": round(conf, 4)
            })

# Save to CSV
df = pd.DataFrame(results)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"[✓] Saved {len(df)} detection results to {OUTPUT_FILE}")
