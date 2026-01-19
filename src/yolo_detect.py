import os
import pandas as pd
from ultralytics import YOLO

# 1. Initialize YOLOv8
model = YOLO('yolov8n.pt')

def categorize_image(detections):
    """
    Categorizes the image based on detected objects.
    - promotional: Person + Product
    - product_display: Product, no Person
    - lifestyle: Person, no Product
    - other: Neither detected
    """
    labels = [d['name'] for d in detections]
    product_classes = {'bottle', 'cup', 'bowl', 'vase', 'wine glass', 'box'}
    
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

# 2. Path Configuration
# Points to your Task 1 images folder
base_image_dir = 'data/raw/images' 
results_data = []

print("Starting object detection...")

# 3. Process Images
# os.walk ensures we find images inside subfolders like 'cheMed123'
for root, dirs, files in os.walk(base_image_dir):
    for img_file in files:
        if img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
            img_path = os.path.join(root, img_file)
            
            # Run Inference
            results = model(img_path)
            
            detections = []
            for r in results:
                for box in r.boxes:
                    detections.append({
                        'name': model.names[int(box.cls)],
                        'conf': float(box.conf)
                    })
            
            # Determine Category (Always defined now)
            cat = categorize_image(detections)
            
            # Extract Message ID (Assumes format: channel_id.jpg or similar)
            # Use split to get the numeric ID before the extension
            msg_id = img_file.split('_')[-1].split('.')[0]
            
            results_data.append({
                'message_id': msg_id,
                'image_path': img_file,
                'image_category': cat,
                'confidence_score': detections[0]['conf'] if detections else 0
            })

# 4. Save Results
df = pd.DataFrame(results_data)

if not df.empty:
    # Save directly to dbt seeds folder
    output_path = 'medical_warehouse/seeds/yolo_detections.csv'
    df.to_csv(output_path, index=False)
    print(f"Success! {len(df)} detections saved to {output_path}")
else:
    print("Zero detections found. Check if your images are in the correct folder.")