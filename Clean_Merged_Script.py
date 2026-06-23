import json
from pathlib import Path

def merge_datumaro_jsons(main_folder: str, output_file: str = "merged_annotations.json") -> None:
    """
    Merges multiple Datumaro default.json files into one combined file.
    
    - Keeps 'info' and 'categories' from the first file found
    - Concatenates all 'items' lists
    - No extra tracing fields (_source, source_file, etc.) are added
    """
    main_path = Path(main_folder).resolve()
    if not main_path.is_dir():
        print(f"Error: {main_path} is not a directory")
        return

    # Find all default.json files recursively
    json_files = list(main_path.rglob("default.json"))
    
    if not json_files:
        print("default.json files found in the folder structure.")
        return

    print(f"Found {len(json_files)} default.json files")

    merged_data = {
        "info": {},
        "categories": {},
        "items": []
    }

    first_file = True

    for json_path in json_files:
        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            # Take structure from the first valid file
            if first_file:
                merged_data["info"]      = data.get("info", {})
                merged_data["categories"] = data.get("categories", {})
                first_file = False
                print(f"Using categories & info from: {json_path.parent.parent.name}")

            # Merge items — no modifications, no extra fields
            items = data.get("items", [])
            if items:
                merged_data["items"].extend(items)
                print(f"  + {len(items):5,d} items from {json_path.parent.parent.name}")

        except Exception as e:
            print(f"Error reading {json_path}: {e}")
            continue

    if not merged_data["items"]:
        print("No items/annotations were merged.")
        return

    # Save merged result
    output_path = main_path / output_file
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "═" * 70)
        print(f"Successfully merged {len(merged_data['items']):,} items")
        print(f"Saved to: {output_path}")
        print(f"Total frames/images: {len(merged_data['items']):,}")
        print("═" * 70)
    
    except Exception as e:
        print(f"Error saving merged file: {e}")


# ────────────────────────────────────────────────
#  Usage
# ────────────────────────────────────────────────

if __name__ == "__main__":
    # Change this path to your actual main folder
    MAIN_FOLDER = r"D:\python\Peddaiah\Beck's_Rework_All_Images\UnZip_Batch-1_label_2k_Images"

    # You can also ask for the path interactively:
    # MAIN_FOLDER = input("Enter main folder path: ").strip()

    merge_datumaro_jsons(
        main_folder = MAIN_FOLDER,
        output_file = "Batch-1_label_2k_Images_merged_clean.json"   # ← feel free to change name
    )