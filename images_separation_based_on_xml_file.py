import os
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

# ========================= CONFIGURATION =========================
XML_FILE = "merged_annotations.xml"          # Your annotation file
SOURCE_FOLDER = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\5k_Output\5kimages"                  # Folder containing all images
DEST_FOLDER = "matched_normal_images"        # Output folder for copied images

# Create destination folder if it doesn't exist
os.makedirs(DEST_FOLDER, exist_ok=True)

# ========================= PARSE XML =========================
print("Parsing XML file...")
tree = ET.parse(XML_FILE)
root = tree.getroot()

# Get all image names that have annotations
annotated_images = set()

for image_elem in root.findall('image'):
    img_name = image_elem.get('name')
    if img_name:
        annotated_images.add(img_name)

print(f"Found {len(annotated_images)} annotated images in XML.")

# ========================= COPY MATCHED IMAGES =========================
print(f"Scanning source folder: {SOURCE_FOLDER}")

copied_count = 0
missing_count = 0

for img_name in annotated_images:
    src_path = os.path.join(SOURCE_FOLDER, img_name)
    
    if os.path.exists(src_path):
        dest_path = os.path.join(DEST_FOLDER, img_name)
        shutil.copy2(src_path, dest_path)
        copied_count += 1
        
        if copied_count % 500 == 0:
            print(f"Copied {copied_count} images...")
    else:
        missing_count += 1
        print(f"⚠️  Missing: {img_name}")

print("\n" + "="*60)
print("✅ DONE!")
print(f"Total annotated in XML : {len(annotated_images)}")
print(f"Successfully copied    : {copied_count}")
print(f"Missing images         : {missing_count}")
print(f"Output folder          : ./{DEST_FOLDER}/")
print("="*60)