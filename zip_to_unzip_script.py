import os
import zipfile

input_folder = r"D:\python\Peddaiah\Beck's_Rework_All_Images\Batch-1_label_2k_Images"
output_folder = r"UnZip_Batch-1_label_2k_Images"

os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(".zip"):
        zip_path = os.path.join(input_folder, file_name)
        
        # Create subfolder with zip name
        extract_folder = os.path.join(output_folder, file_name.replace(".zip", ""))
        os.makedirs(extract_folder, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        
        print(f"Extracted: {file_name} → {extract_folder}")