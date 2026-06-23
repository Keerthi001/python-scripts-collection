import json

# Input and output file paths
input_file = 'Batch1_merged_clean.json'
output_file = 'filtered_labels_8_or_9.json'

# Load the JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter items
filtered_items = []

for item in data.get('items', []):
    annotations = item.get('annotations', [])
    
    has_label_8_or_9 = False
    
    for ann in annotations:
        if ann.get('type') == 'bbox':  # Only consider bbox annotations
            label_id = ann.get('label_id')
            if label_id in [8, 9]:
                has_label_8_or_9 = True
                break  # No need to check further
    
    # Keep item if it has at least one label 8 or 9
    if has_label_8_or_9:
        filtered_items.append(item)

# Create the new data structure
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
print(f"Filtered items (with at least one label 8 or 9): {len(filtered_items)}")