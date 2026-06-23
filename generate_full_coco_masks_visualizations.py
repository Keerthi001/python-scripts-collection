import os
import json
import cv2
import numpy as np
from pathlib import Path

# ====================== CONFIG ======================
ROOT_FOLDER = Path(r"D:\python\Vara Prasad\Agri Pass - Tippani Platform\UnZip_Harvested_Robotics")

MASK_OUTPUT_DIR = "masks"
VIS_OUTPUT_DIR = "visualizations"
COCO_OUTPUT_DIR = "coco_annotations"

# Colors for visualization
COLOR_MAP = {
    0: (255, 105, 180),   # Crop
    1: (255, 182, 193),   # Broad Leaf
    2: (0, 255, 255),     # Grass
    3: (0, 255, 0),       # Growth Point
}

ALPHA = 0.65
# ===================================================

def load_json(json_path: Path) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_mask_and_vis(image_path: Path, json_data: dict, mask_path: Path, vis_path: Path):
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"⚠️ Could not load: {image_path.name}")
        return
    h, w = img.shape[:2]
    mask = np.zeros((h, w, 3), dtype=np.uint8)
    vis = img.copy()

    for item in json_data.get("items", []):
        for ann in item.get("annotations", []):
            label_id = ann.get("label_id", 0)
            color = COLOR_MAP.get(label_id, (255, 0, 255))

            if ann.get("type") == "polygon":
                pts = np.array(ann["points"], dtype=np.int32).reshape((-1, 2))
                cv2.fillPoly(mask, [pts], color)
                cv2.polylines(vis, [pts], isClosed=True, color=color, thickness=3)
                cv2.fillPoly(vis, [pts], color)

            elif ann.get("type") == "points":
                pts = ann.get("points", [])
                for i in range(0, len(pts), 2):
                    if i + 1 < len(pts):
                        x, y = int(pts[i]), int(pts[i+1])
                        cv2.circle(vis, (x, y), 10, color, -1)
                        cv2.circle(vis, (x, y), 14, (255,255,255), 2)

    cv2.imwrite(str(mask_path), mask)
    overlay = cv2.addWeighted(vis, ALPHA, mask, 1-ALPHA, 0)
    cv2.imwrite(str(vis_path), overlay)


def main():
    os.makedirs(MASK_OUTPUT_DIR, exist_ok=True)
    os.makedirs(VIS_OUTPUT_DIR, exist_ok=True)
    os.makedirs(COCO_OUTPUT_DIR, exist_ok=True)

    coco = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 0, "name": "Crop", "supercategory": "plant"},
            {"id": 1, "name": "Broad Leaf", "supercategory": "plant", "keypoints": ["growth_point"]},
            {"id": 2, "name": "Grass", "supercategory": "plant", "keypoints": ["growth_point"]}
        ]
    }

    image_id_counter = 1
    ann_id_counter = 1
    processed = 0

    for subdir in sorted(ROOT_FOLDER.iterdir()):
        if not subdir.is_dir():
            continue

        json_path = subdir / "annotations" / "default.json"
        image_dir = subdir / "images" / "default"

        if not json_path.exists():
            continue

        image_files = list(image_dir.glob("*.webp")) + list(image_dir.glob("*.png")) + \
                      list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.jpeg"))
        if not image_files:
            continue

        image_path = image_files[0]
        try:
            data = load_json(json_path)
            image_name = data["items"][0]["id"] if data.get("items") else subdir.name

            # === Mask & Visualization ===
            mask_path = Path(MASK_OUTPUT_DIR) / f"{image_name}_mask.png"
            vis_path = Path(VIS_OUTPUT_DIR) / f"{image_name}_vis.png"
            create_mask_and_vis(image_path, data, mask_path, vis_path)

            # === Add to COCO ===
            img = cv2.imread(str(image_path))
            h, w = img.shape[:2] if img is not None else (1080, 1920)

            coco["images"].append({
                "id": image_id_counter,
                "file_name": image_path.name,
                "height": h,
                "width": w
            })

            items = data.get("items", [])
            for item in items:
                for ann in item.get("annotations", []):
                    if ann.get("type") != "polygon":
                        continue

                    label_id = ann.get("label_id")
                    points = ann.get("points", [])
                    if len(points) < 6:
                        continue

                    pts_array = np.array(points).reshape(-1, 2)
                    x_min, y_min = pts_array.min(axis=0)
                    x_max, y_max = pts_array.max(axis=0)

                    bbox = [float(x_min), float(y_min), float(x_max-x_min), float(y_max-y_min)]
                    area = float(cv2.contourArea(pts_array.reshape(1, -1, 2).astype(np.int32)))

                    coco_ann = {
                        "id": ann_id_counter,
                        "image_id": image_id_counter,
                        "category_id": label_id,
                        "segmentation": [points],
                        "area": area,
                        "bbox": bbox,
                        "iscrowd": 0
                    }

                    # Add keypoints for weeds
                    if label_id in [1, 2]:
                        for p_ann in item.get("annotations", []):
                            if p_ann.get("type") == "points" and p_ann.get("label_id") == 3:
                                pts = p_ann.get("points", [])
                                if len(pts) >= 2:
                                    coco_ann["keypoints"] = [float(pts[0]), float(pts[1]), 2]
                                    coco_ann["num_keypoints"] = 1
                                break

                    coco["annotations"].append(coco_ann)
                    ann_id_counter += 1

            processed += 1
            image_id_counter += 1
            print(f"✅ Added: {image_name}")

        except Exception as e:
            print(f"❌ Error in {subdir.name}: {e}")

    # Save the single combined COCO JSON
    coco_path = Path(COCO_OUTPUT_DIR) / "coco_dataset.json"
    with open(coco_path, 'w', encoding='utf-8') as f:
        json.dump(coco, f, indent=2)

    print(f"\n🎉 Processing Completed!")
    print(f"   Total images processed: {processed}")
    print(f"   Single COCO file saved: {coco_path}")
    print(f"   Masks → {MASK_OUTPUT_DIR}/")
    print(f"   Visualizations → {VIS_OUTPUT_DIR}/")


if __name__ == "__main__":
    main()