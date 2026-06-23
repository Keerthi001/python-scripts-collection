import os
import shutil

# Folder paths
folder_5000 = r"D:\python\Vara Prasad\Tippani Project\.xml and visualizations\Becks’ Hybrids Output\visualizations"
folder_95 = r"C:\Users\KEERTHI K\Downloads\visualizations-20260617T073613Z-3-001\visualizations"
output_folder = r"Matched_Images_2"

os.makedirs(output_folder, exist_ok=True)

# Get base names from the 95-file folder
target_names = {
    os.path.splitext(file)[0]
    for file in os.listdir(folder_95)
}

# Find matching files in the 5000-image folder
copied_count = 0

for file in os.listdir(folder_5000):
    base_name = os.path.splitext(file)[0]

    if base_name in target_names:
        source_path = os.path.join(folder_5000, file)
        destination_path = os.path.join(output_folder, file)

        shutil.copy2(source_path, destination_path)
        copied_count += 1
        print(f"Copied: {file}")

print(f"\nTotal files copied: {copied_count}")