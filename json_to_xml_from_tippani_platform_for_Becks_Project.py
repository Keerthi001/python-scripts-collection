import os
import json
import xml.etree.ElementTree as ET

# Input JSON
json_path = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Corn_Images_or_Becks_Visualizations_and_XML_Generation_Script/Batch_5k_18_05_2026_merged_clean.json"

# Output folder
output_folder = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Corn_Images_or_Becks_Visualizations_and_XML_Generation_Script/unzipped_Batch_5k_18_05_2026_xml_output"
os.makedirs(output_folder, exist_ok=True)

# Label mapping
label_map = {
    0: "u",
    1: "d"
}

# Default image size (update if needed)
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 400

with open(json_path, "r") as f:
    data = json.load(f)

items = data.get("items", [])

for item in items:
    image_id = item.get("id")
    annotations = item.get("annotations", [])

    if not annotations:
        continue

    # Create XML root
    annotation_xml = ET.Element("annotation")

    filename = image_id + ".jpeg"
    ET.SubElement(annotation_xml, "filename").text = filename

    # Size block
    size = ET.SubElement(annotation_xml, "size")
    ET.SubElement(size, "width").text = str(IMAGE_WIDTH)
    ET.SubElement(size, "height").text = str(IMAGE_HEIGHT)

    for ann in annotations:
        bbox = ann.get("bbox", [])
        label_id = ann.get("label_id")

        if len(bbox) != 4:
            continue

        x, y, w, h = bbox

        xmin = int(x)
        ymin = int(y)
        xmax = int(x + w)
        ymax = int(y + h)

        obj = ET.SubElement(annotation_xml, "object")
        ET.SubElement(obj, "name").text = label_map.get(label_id, "unknown")

        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(xmin)
        ET.SubElement(bndbox, "ymin").text = str(ymin)
        ET.SubElement(bndbox, "xmax").text = str(xmax)
        ET.SubElement(bndbox, "ymax").text = str(ymax)

    # Save XML
    xml_path = os.path.join(output_folder, image_id + ".xml")
    tree = ET.ElementTree(annotation_xml)
    tree.write(xml_path)

    print(f"Converted: {filename}")

print("✅ All JSON items converted to XML successfully!")