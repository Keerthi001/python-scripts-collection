import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_json_to_cvat_xml(json_path, output_xml_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    annotations = ET.Element('annotations')
    ET.SubElement(annotations, 'version').text = '1.1'
    
    # Meta
    meta = ET.SubElement(annotations, 'meta')
    job = ET.SubElement(meta, 'job')
    ET.SubElement(job, 'size').text = str(len(data.get('items', [])))
    ET.SubElement(job, 'mode').text = 'annotation'
    ET.SubElement(job, 'overlap').text = '0'
    ET.SubElement(job, 'bugtracker')
    
    # Labels
    labels_elem = ET.SubElement(job, 'labels')
    label_map = {}
    tag_labels = {'blur', 'bad_quality', 'front_door_not_concealed', 'parcel_in_bin'}
    
    for idx, label_info in enumerate(data['categories']['label']['labels']):
        label_name = label_info['name']
        label_map[idx] = label_name
        
        label_elem = ET.SubElement(labels_elem, 'label')
        ET.SubElement(label_elem, 'name').text = label_name
        ET.SubElement(label_elem, 'color').text = '#dd9d98'
        ET.SubElement(label_elem, 'type').text = 'tag' if label_name in tag_labels else 'rectangle'
        ET.SubElement(label_elem, 'attributes')
    
    # Process images
    for img_id, item in enumerate(data.get('items', [])):
        image_name = f"{item['id']}.jpg"
        
        # Get dimensions
        width = 720
        height = 1280
        for ann in item.get('annotations', []):
            if ann.get('type') == 'bbox':
                x, y, w, h = ann['bbox']
                width = max(width, int(x + w))
                height = max(height, int(y + h))
        
        image = ET.SubElement(annotations, 'image', {
            'id': str(img_id),
            'name': image_name,
            'width': str(width),
            'height': str(height)
        })
        
        for ann in item.get('annotations', []):
            label_id = ann.get('label_id')
            label_name = label_map.get(label_id, 'unknown')
            ann_attributes = ann.get('attributes', {})
            
            if ann.get('type') == 'bbox':
                # Bounding Box
                bbox = ann['bbox']
                xtl = round(bbox[0], 2)
                ytl = round(bbox[1], 2)
                xbr = round(xtl + bbox[2], 2)
                ybr = round(ytl + bbox[3], 2)
                
                box = ET.SubElement(image, 'box', {
                    'label': label_name,
                    'source': 'manual',
                    'occluded': '0',
                    'xtl': str(xtl),
                    'ytl': str(ytl),
                    'xbr': str(xbr),
                    'ybr': str(ybr),
                    'z_order': '0'
                })
                
                # Add attributes (like occluded, and any others)
                for attr_name, attr_value in ann_attributes.items():
                    if attr_name in ['occluded', 'rotation']:
                        continue  # CVAT handles occluded differently
                    attr_elem = ET.SubElement(box, 'attribute', {'name': attr_name})
                    attr_elem.text = str(attr_value).lower()
                
            elif ann.get('type') == 'label':
                # Tag annotation (e.g., blur, front_door_not_concealed)
                tag = ET.SubElement(image, 'tag', {
                    'label': label_name,
                    'source': 'manual'
                })
                
                for attr_name, attr_value in ann_attributes.items():
                    attr_elem = ET.SubElement(tag, 'attribute', {'name': attr_name})
                    attr_elem.text = str(attr_value).lower()
    
    # Pretty print
    rough_string = ET.tostring(annotations, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    with open(output_xml_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    convert_json_to_cvat_xml(
        '10th_Batch_merged_clean.json', 
        '10th_Batch_output_annotations.xml'
    )
    print("✅ Conversion completed with full attribute support!")