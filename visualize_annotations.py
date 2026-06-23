import json
import cv2
import os
from pathlib import Path
import shutil

# ========================= CONFIG =========================
JSON_FILE = "new_all_batches_merged_clean.json"   # Your JSON file
INPUT_FOLDER = "input"                            # Folder containing all images
OUTPUT_FOLDER = "output"                          # Where visualized images will be saved

# Colors for different labels (BGR format)
COLORS = {
    "Parcel": (0, 255, 0),          # Green
    "Bin": (255, 0, 0),             # Blue
    "Front door": (0, 165, 255),    # Orange
    "Front door handle": (255, 255, 0),  # Cyan
    "Doorbell/Knocker": (147, 20, 255),  # Purple
    "Letterbox": (0, 255, 255),     # Yellow
    "Property Identifier": (255, 0, 255), # Magenta
    "Building Identifier": (255, 100, 0),
    "Hand": (0, 0, 255),            # Red
    "Person": (180, 105, 255),
    "in_the_bin": (0, 0, 128),      # Dark Red
    "External Doors": (50, 205, 50),
    "Buzzers": (255, 215, 0)
}

# Label names mapping from label_id
LABEL_NAMES = {
    0: "Parcel",
    1: "Bin",
    2: "Front door",
    3: "Front door handle",
    4: "Doorbell/Knocker",
    5: "Letterbox",
    6: "Property Identifier",
    7: "Building Identifier",
    8: "Hand",
    9: "Person",
    10: "in_the_bin",
    11: "External Doors",
    12: "Buzzers"
}

# ========================================================

def main():
    # Create output folder
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)

    # Load JSON
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded JSON with {len(data['items'])} items")

    processed = 0
    not_found = 0

    for item in data['items']:
        item_id = item['id']
        annotations = item.get('annotations', [])

        # Find matching image in input folder
        # Since JSON has no extension, we try common image extensions
        image_path = None
        for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
            potential_path = os.path.join(INPUT_FOLDER, item_id + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break

        if not image_path:
            print(f"⚠️  Image not found for ID: {item_id}")
            not_found += 1
            continue

        # Read image
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Failed to read image: {image_path}")
            continue

        height, width = img.shape[:2]

        # Draw all annotations
        for ann in annotations:
            if ann['type'] == 'bbox':
                label_id = ann['label_id']
                bbox = ann['bbox']  # [x, y, w, h]
                occluded = ann['attributes'].get('occluded', False)

                x, y, w, h = map(int, bbox)
                color = COLORS.get(LABEL_NAMES.get(label_id, "Unknown"), (0, 255, 255))

                # Draw rectangle
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)

                # Label text
                label_name = LABEL_NAMES.get(label_id, f"Label_{label_id}")
                text = label_name
                if occluded:
                    text += " (occluded)"

                # Put label
                cv2.putText(img, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            elif ann['type'] == 'label' and 'in_the_bin' in ann['attributes']:
                # Special case for "in_the_bin" label
                cv2.putText(img, "IN THE BIN", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        # Save visualized image
        output_path = os.path.join(OUTPUT_FOLDER, f"{item_id}.jpg")
        cv2.imwrite(output_path, img)
        processed += 1

        if processed % 500 == 0:
            print(f"Processed: {processed} images...")

    print("\n" + "="*60)
    print(f"✅ Visualization completed!")
    print(f"   Total items in JSON : {len(data['items'])}")
    print(f"   Successfully processed: {processed}")
    print(f"   Images not found     : {not_found}")
    print(f"   Output saved to      : ./{OUTPUT_FOLDER}/")
    print("="*60)


if __name__ == "__main__":
    main()