import os
import shutil
from pathlib import Path
from collections import defaultdict

# ================== CONFIGURATION ==================
# Change this to your main source folder
SOURCE_ROOT = r"D:\python\Vara Prasad\Tippani Project\Front_Door_Property_Identifier_images_visualization_script\UnZip_30KZIP"   # ←←← CHANGE THIS

# Destination folder
DEST_FOLDER = "30000_images"

# Image extensions (add more if needed)
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}

# Choose action: 'copy' (safer) or 'move'
ACTION = 'copy'   # Change to 'move' if you want to move instead of copy
# ===================================================

def is_image_file(filename):
    return Path(filename).suffix.lower() in IMAGE_EXTENSIONS

def main():
    source_path = Path(SOURCE_ROOT)
    dest_path = Path(DEST_FOLDER)
    
    if not source_path.exists():
        print(f"❌ Source folder not found: {source_path}")
        return
    
    # Create destination folder
    dest_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Scanning images from: {source_path}")
    print(f"Destination: {dest_path.resolve()}\n")
    
    copied_count = 0
    skipped_count = 0
    conflict_count = 0
    
    # Track filename conflicts
    filename_count = defaultdict(int)
    
    for file_path in source_path.rglob("*"):
        if file_path.is_file() and is_image_file(file_path.name):
            # Generate unique filename if conflict exists
            original_name = file_path.name
            filename_count[original_name] += 1
            
            if filename_count[original_name] > 1:
                # Add counter to filename (e.g., image.jpg → image_2.jpg)
                stem = file_path.stem
                suffix = file_path.suffix
                new_name = f"{stem}_{filename_count[original_name]}{suffix}"
                dest_file = dest_path / new_name
                conflict_count += 1
            else:
                dest_file = dest_path / original_name
            
            try:
                if ACTION == 'move':
                    shutil.move(str(file_path), str(dest_file))
                else:
                    shutil.copy2(str(file_path), str(dest_file))  # copy2 preserves metadata
                
                copied_count += 1
                if copied_count % 1000 == 0:
                    print(f"Processed: {copied_count:,} images...")
                    
            except Exception as e:
                print(f"Error with {file_path}: {e}")
                skipped_count += 1
    
    print("\n" + "="*60)
    print("✅ TASK COMPLETED!")
    print("="*60)
    print(f"Total images {ACTION}ed : {copied_count:,}")
    print(f"Filename conflicts resolved : {conflict_count}")
    print(f"Skipped (errors)         : {skipped_count}")
    print(f"Destination folder       : {dest_path.resolve()}")
    print("="*60)

if __name__ == "__main__":
    main()