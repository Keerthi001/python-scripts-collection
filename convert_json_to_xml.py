import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_json_to_cvat_xml(json_path, output_xml_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Root element
    annotations = ET.Element('annotations')
    
    # Version
    ET.SubElement(annotations, 'version').text = '1.1'
    
    # Meta section
    meta = ET.SubElement(annotations, 'meta')
    job = ET.SubElement(meta, 'job')
    ET.SubElement(job, 'size').text = str(len(data.get('items', [])))
    ET.SubElement(job, 'mode').text = 'annotation'
    ET.SubElement(job, 'overlap').text = '0'
    ET.SubElement(job, 'bugtracker')
    
    # Labels (using actual label names from JSON)
    labels_elem = ET.SubElement(job, 'labels')
    label_map = {}
    for idx, label_info in enumerate(data['categories']['label']['labels']):
        label_name = label_info['name']
        label_map[idx] = label_name
        
        label_elem = ET.SubElement(labels_elem, 'label')
        ET.SubElement(label_elem, 'name').text = label_name
        ET.SubElement(label_elem, 'color').text = '#dd9d98'  # default color like sample
        ET.SubElement(label_elem, 'type').text = 'rectangle'
        ET.SubElement(label_elem, 'attributes')
    
    # Process each item as an <image>
    for img_id, item in enumerate(data.get('items', [])):
        image_name = f"{item['id']}.jpeg"  # As per your requirement
        
        # Determine image dimensions from bboxes (fallback to common values)
        width = 1280
        height = 720
        max_x, max_y = 0, 0
        for ann in item.get('annotations', []):
            if ann.get('type') == 'bbox':
                x, y, w, h = ann['bbox']
                max_x = max(max_x, x + w)
                max_y = max(max_y, y + h)
        if max_x > 0:
            width = int(max_x)
        if max_y > 0:
            height = int(max_y)
        
        image = ET.SubElement(annotations, 'image', {
            'id': str(img_id),
            'name': image_name,
            'width': str(width),
            'height': str(height)
        })
        
        # Add bounding boxes
        for ann in item.get('annotations', []):
            if ann.get('type') == 'bbox':
                label_id = ann.get('label_id')
                label_name = label_map.get(label_id, 'unknown')
                bbox = ann['bbox']  # [x, y, width, height]
                
                xtl = round(bbox[0], 2)
                ytl = round(bbox[1], 2)
                xbr = round(xtl + bbox[2], 2)
                ybr = round(ytl + bbox[3], 2)
                
                ET.SubElement(image, 'box', {
                    'label': label_name,
                    'source': 'manual',
                    'occluded': '0',
                    'xtl': str(xtl),
                    'ytl': str(ytl),
                    'xbr': str(xbr),
                    'ybr': str(ybr),
                    'z_order': '0'
                })
    
    # Pretty XML output
    rough_string = ET.tostring(annotations, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    with open(output_xml_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

# Run the conversion
if __name__ == "__main__":
    convert_json_to_cvat_xml(
        'Batch-1_label_2k_Images_merged_clean.json', 
        'Batch-1_label_2k_Images_output_annotations.xml'
    )
    print("✅ Conversion completed! Output saved to: output_annotations.xml")