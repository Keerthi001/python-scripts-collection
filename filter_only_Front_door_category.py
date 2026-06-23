import json
# Input and output file paths
input_file = 'Batch1_merged_clean.json'
output_file = 'filtered_at_least_one_label_2.json'

# Load the JSON data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter items
filtered_items = []

for item in data.get('items', []):
    annotations = item.get('annotations', [])
    
    has_label_2 = False
    
    for ann in annotations:
        if ann.get('type') == 'bbox':  # Only consider bbox annotations
            if ann.get('label_id') == 2:
                has_label_2 = True
                break  # No need to check further once we find one
    
    # Keep item if at least one label_id == 2 is present
    if has_label_2:
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
print(f"Filtered items (with at least one label_2): {len(filtered_items)}")