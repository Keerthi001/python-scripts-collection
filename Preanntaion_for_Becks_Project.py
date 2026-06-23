import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

# 🔹 Folder path
folder_path = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Corn_Images_or_Becks_Visualizations_and_XML_Generation_Script\images_and_xmls"

# 🔹 Output folder
output_folder = os.path.join(folder_path, "output")
os.makedirs(output_folder, exist_ok=True)

# 🔹 Loop through all jpeg files
for file in os.listdir(folder_path):
    
    if file.endswith(".jpeg"):
        
        image_path = os.path.join(folder_path, file)
        xml_name = file.replace(".jpeg", ".xml")
        xml_path = os.path.join(folder_path, xml_name)
        
        # Skip if XML not found
        if not os.path.exists(xml_path):
            print(f"XML not found for {file}")
            continue
        
        # Open image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        # Parse XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for obj in root.findall("object"):
            label = obj.find("name").text
            bbox = obj.find("bndbox")
            
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)
            
            draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)
            draw.text((xmin, ymin - 10), label, fill="red")
        
        # Save output
        output_path = os.path.join(output_folder, file)
        image.save(output_path)
        
        print(f"Processed: {file}")

print("All files processed successfully.")