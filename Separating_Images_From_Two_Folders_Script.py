import os
import shutil

# ====== FOLDER PATHS ======
folder_5k = r"D:\python\Vara Prasad\Tippani Project\Separating_Images_From_Two_Folders\5kimages"
folder_2k = r"D:\python\Vara Prasad\Tippani Project\Separating_Images_From_Two_Folders\2kImages"
output_folder = r"D:\New_Unique_Images"

# ==========================

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')

# Get image names from 2k folder
folder2k_images = set()

for file in os.listdir(folder_2k):
    if file.lower().endswith(image_extensions):
        # Store only filename without extension
        name_without_ext = os.path.splitext(file)[0].lower()
        folder2k_images.add(name_without_ext)

# Compare with 5k folder
copied_count = 0

for file in os.listdir(folder_5k):
    if file.lower().endswith(image_extensions):

        name_without_ext = os.path.splitext(file)[0].lower()

        # If image name NOT present in 2k folder
        if name_without_ext not in folder2k_images:

            source_path = os.path.join(folder_5k, file)
            destination_path = os.path.join(output_folder, file)

            shutil.copy2(source_path, destination_path)
            copied_count += 1

            print(f"Copied: {file}")

print("\n=================================")
print(f"Total unique images copied: {copied_count}")
print("Process Completed Successfully")
print("=================================")