import json
import cv2
import os
from pathlib import Path

# ================== CONFIGURATION ==================
JSON_FILE = 'filtered_at_least_one_label_2.json'
IMAGES_FOLDER = 'batch_1'
OUTPUT_FOLDER = 'visualizations_label_2_only'   # Updated folder name

# Colors (BGR)
COLOR_LABEL_2 = (0, 255, 0)      # Green - Front Door

BOX_THICKNESS = 3
TEXT_THICKNESS = 2
FONT_SCALE = 0.6
# ===================================================

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    items = data.get('items', [])
    print(f"Loaded {len(items)} items from JSON.\n")
    
    # Get all image files in the folder
    image_folder = Path(IMAGES_FOLDER)
    if not image_folder.exists():
        print(f"❌ Folder not found: {IMAGES_FOLDER}")
        return
    
    # Create a map from possible identifiers to actual image path
    image_map = {}
    for img_path in image_folder.glob('*.*'):
        if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            stem = img_path.stem
            image_map[stem] = img_path
            if stem.startswith('frame_'):
                frame_num = stem.replace('frame_', '')
                image_map[frame_num] = img_path
            image_map[str(int(stem) if stem.isdigit() else stem)] = img_path
    
    print(f"Found {len(image_map)} images in folder.\n")
    
    processed = 0
    not_found = 0
    skipped_annotations = 0
    
    for item in items:
        item_id = item.get('id')
        frame = item.get('attr', {}).get('frame')
        
        if frame is None:
            continue
        
        frame_str = str(frame)
        
        # Try multiple ways to find the image
        image_path = None
        candidates = [
            frame_str,
            f"frame_{frame}",
            item_id,
            str(item_id).split('_')[0] if '_' in str(item_id) else None
        ]
        
        for cand in candidates:
            if cand and cand in image_map:
                image_path = image_map[cand]
                break
        
        if not image_path:
            not_found += 1
            print(f"⚠️  Image not found for frame {frame} (item: {item_id[:30]}...)")
            continue
        
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"❌ Could not read: {image_path.name}")
            continue
        
        # Draw ONLY label_id = 2
        drawn = False
        for ann in item.get('annotations', []):
            if ann.get('type') != 'bbox':
                continue
            label_id = ann.get('label_id')
            if label_id != 2:          # <--- Changed to only label 2
                skipped_annotations += 1
                continue
                
            bbox = ann.get('bbox')
            if not bbox or len(bbox) != 4:
                continue
                
            x, y, w, h = map(int, bbox)
            label_name = "Front Door"
            
            cv2.rectangle(img, (x, y), (x + w, y + h), COLOR_LABEL_2, BOX_THICKNESS)
            cv2.putText(img, label_name, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, COLOR_LABEL_2, TEXT_THICKNESS)
            drawn = True
        
        # Save image
        output_path = Path(OUTPUT_FOLDER) / image_path.name
        cv2.imwrite(str(output_path), img)
        processed += 1
        
        if processed % 200 == 0:
            print(f"✅ Processed: {processed} images...")
    
    print("\n" + "="*80)
    print("🎉 VISUALIZATION COMPLETED! (Only Label 2)")
    print("="*80)
    print(f"Successfully processed : {processed}")
    print(f"Images not found       : {not_found}")
    print(f"Annotations skipped    : {skipped_annotations}")
    print(f"Output folder          : {Path(OUTPUT_FOLDER).resolve()}")
    print("="*80)

if __name__ == "__main__":
    main()