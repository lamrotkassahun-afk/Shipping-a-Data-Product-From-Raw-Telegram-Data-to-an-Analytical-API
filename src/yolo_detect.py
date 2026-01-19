import os
import pandas as pd
from ultralytics import YOLO

# 1. Load the YOLOv8 nano model
model = YOLO('yolov8n.pt')

def categorize_image(detections):
    """
    Categorization Logic:
    - promotional: Person + Product (bottle/cup/bowl/etc.)
    - product_display: Product, no Person
    - lifestyle: Person, no Product
    - other: Neither
    """
    labels = [d['name'] for d in detections]
    # Common YOLO classes for 'product' containers
    product_classes = {'bottle', 'cup', 'bowl', 'vase', 'wine glass'}
    
    has_person = 'person' in labels
    has_product = any(cls in labels for cls in product_classes)

    if has_person and has_product:
        return 'promotional'
    elif has_product:
        return 'product_display'
    elif has_person:
        return 'lifestyle'
    else:
        return 'other'

# 2. Scan image directory
image_dir = 'data/raw/images/'  # Adjust to your Task 1 path
results_data = []

for img_file in os.listdir(image_dir):
    if img_file.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(image_dir, img_file)
        
        # Run YOLO inference
        results = model(img_path)
        
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    'name': model.names[int(box.cls)],
                    'conf': float(box.conf)
                })
        
        # Categorize
        cat = categorize_image(detections)
        
        # Parse message_id from filename (assuming 'channel_msgid.jpg' format)
        msg_id = img_file.split('_')[-1].split('.')[0]
        
        results_data.append({
            'message_id': msg_id,
            'image_path': img_file,
            'detections': str(detections),
            'image_category': cat,
            'confidence_score': detections[0]['conf'] if detections else 0
        })

# 3. Save to CSV
pd.DataFrame(results_data).to_csv('data/raw/yolo_detections.csv', index=False)