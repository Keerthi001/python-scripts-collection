import json
from collections import defaultdict

# Input and output file paths
input_file = '30thousand_files_merged_clean.json'
output_file = 'filtered_two_or_more_label_2_or_6.json'

# Load the JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter items
filtered_items = []

for item in data.get('items', []):
    annotations = item.get('annotations', [])
    
    # Count label_id 2 and 6
    count_label_2 = 0
    count_label_6 = 0
    
    for ann in annotations:
        if ann.get('type') == 'bbox':  # Only consider bbox annotations
            label_id = ann.get('label_id')
            if label_id == 2:
                count_label_2 += 1
            elif label_id == 6:
                count_label_6 += 1
    
    # Condition: 2 or more label_id 2 OR 2 or more label_id 6
    if count_label_2 >= 2 or count_label_6 >= 2:
        filtered_items.append(item)

# Create the new data structure (same format)
filtered_data = {
    "info": data.get("info", {}),
    "categories": data.get("categories", {}),
    "items": filtered_items
}

# Save to new JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, indent=2, ensure_ascii=False)

print(f"Filtered JSON saved to: {output_file}")
print(f"Total original items: {len(data.get('items', []))}")
print(f"Filtered items (with >=2 label_2 or >=2 label_6): {len(filtered_items)}")