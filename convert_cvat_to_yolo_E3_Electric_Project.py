import json
from pathlib import Path
import cv2
import numpy as np

# ====================== CLASS MAPPING ======================
CLASS_MAP = {
    "Go_1": 1,
    "Bump_0": 0,
    "Pothole_2": 2,
    "Stop_3": 3,
    "Wait_4": 4,
}
# ========================================================

def safe_imread(image_path):
    path_str = str(image_path)
    img = cv2.imread(path_str)
    if img is not None:
        return img
    try:
        with open(path_str, 'rb') as f:
            data = f.read()
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            return img
    except:
        pass
    raise ValueError(f"Could not load image: {path_str}")


def parse_annotations(json_path, img):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    height, width = img.shape[:2]
    annotations = []
    
    for item in data.get("items", []):
        for ann in item.get("annotations", []):
            if ann.get("type") != "bbox":
                continue
            label_id = ann.get("label_id")
            labels = data["categories"]["label"]["labels"]
            if label_id >= len(labels):
                continue
            label_name = labels[label_id]["name"]
            class_id = CLASS_MAP.get(label_name)
            if class_id is None:
                continue
            x, y, w, h = ann["bbox"]
            xc = (x + w / 2) / width
            yc = (y + h / 2) / height
            nw = w / width
            nh = h / height
            annotations.append(f"{class_id} {xc:.8f} {yc:.8f} {nw:.8f} {nh:.8f}")
    
    return annotations


def visualize_annotations(image, annotations, output_path):
    h, w = image.shape[:2]
    for ann in annotations:
        parts = ann.strip().split()
        class_id = int(parts[0])
        xc, yc, nw, nh = map(float, parts[1:])
        x1 = int((xc - nw/2) * w)
        y1 = int((yc - nh/2) * h)
        x2 = int((xc + nw/2) * w)
        y2 = int((yc + nh/2) * h)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(image, str(class_id), (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.imwrite(output_path, image)


def get_category_from_image_id(image_id: str):
    image_id_lower = image_id.lower()
    if "pothole" in image_id_lower:
        return "Pothole"
    elif "bump" in image_id_lower:
        return "Speed_Bump"
    elif "go (green)" in image_id_lower or "go_1" in image_id_lower:
        return "Traffic_Light_Go_Green"
    elif "stop (red)" in image_id_lower or "stop_3" in image_id_lower:
        return "Traffic_Light_Stop_Red"
    elif "wait (yellow)" in image_id_lower or "wait_4" in image_id_lower:
        return "Traffic_Light_Wait_Yellow"
    else:
        return "Other"


def process_all(json_base, image_base, output_base="Organized_Dataset"):
    json_path = Path(json_base)
    image_base_path = Path(image_base)
    output_path = Path(output_base)
    
    # Clear previous output if exists
    if output_path.exists():
        import shutil
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)
    
    subfolders = [d for d in json_path.iterdir() if d.is_dir()]
    print(f"Total job folders: {len(subfolders)}\n")
    
    processed = 0
    for job_folder in subfolders:
        json_file = job_folder / "annotations" / "default.json"
        if not json_file.exists():
            continue
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            image_id = None
            for item in data.get("items", []):
                if item.get("id"):
                    image_id = item["id"]
                    break
        except:
            continue
        
        # Find image
        found_image = None
        for cat_folder in image_base_path.iterdir():
            if not cat_folder.is_dir():
                continue
            for img_file in cat_folder.glob("*.*"):
                if img_file.suffix.lower() not in ['.jpg','.jpeg','.png','.JPG','.JPEG','.PNG']:
                    continue
                stem = img_file.stem
                if image_id == stem or image_id in stem:
                    found_image = img_file
                    break
            if found_image:
                break
        
        if not found_image:
            continue
        
        category = get_category_from_image_id(image_id)
        cat_base = output_path / category
        labels_dir = cat_base / "labels"
        vis_dir = cat_base / "visualizations"
        
        labels_dir.mkdir(parents=True, exist_ok=True)
        vis_dir.mkdir(parents=True, exist_ok=True)
        
        txt_path = labels_dir / f"{found_image.stem}.txt"
        vis_path = vis_dir / f"{found_image.stem}_vis.jpg"
        
        try:
            img = safe_imread(found_image)
            anns = parse_annotations(str(json_file), img)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(anns) + "\n" if anns else "")
            
            vis_img = img.copy()
            visualize_annotations(vis_img, anns, str(vis_path))
            
            print(f"✅ {category} | {found_image.stem} → {len(anns)} annotations")
            processed += 1
        except Exception as e:
            print(f"❌ Error {found_image.stem}: {e}")
    
    print(f"\n🎉 FINISHED! All files organized in '{output_base}' folder.")
    print("Structure: Category → labels/ and visualizations/")


if __name__ == "__main__":
    json_base = r"D:\python\Vara Prasad\Tippani Project\E3_Electric_Sample_images_50_Project\UnZip_Pothole2"
    image_base = r"D:\python\Vara Prasad\Tippani Project\E3_Electric_Sample_images_50_Project\images_folder"
    
    process_all(json_base, image_base)