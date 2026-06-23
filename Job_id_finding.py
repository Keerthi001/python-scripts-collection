import json
from pathlib import Path

def merge_datumaro_jsons(main_folder: str, output_file: str = "merged_annotations.json") -> None:
    """
    Merges multiple Datumaro default.json files into one combined file.
    Adds 'subfolder' name to each item.
    """
    main_path = Path(main_folder).resolve()
    if not main_path.is_dir():
        print(f"Error: {main_path} is not a directory")
        return

    # Find all default.json files recursively
    json_files = list(main_path.rglob("default.json"))
    
    if not json_files:
        print("No default.json files found in the folder structure.")
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
                merged_data["info"] = data.get("info", {})
                merged_data["categories"] = data.get("categories", {})
                first_file = False
                print(f"Using categories & info from: {json_path.parent.parent.name}")

            subfolder_name = json_path.parent.parent.name

            # Merge items and add subfolder info
            items = data.get("items", [])
            if items:
                for item in items:
                    item["subfolder"] = subfolder_name

                merged_data["items"].extend(items)
                print(f"  + {len(items):5,d} items from subfolder: {subfolder_name}")

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
        
        print("\n" + "=" * 80)
        print(f"Successfully merged {len(merged_data['items']):,} items")
        print(f"Saved to: {output_path}")
        print(f"Total frames/images: {len(merged_data['items']):,}")
        print("Each item now contains 'subfolder' field.")
        print("=" * 80)
    
    except Exception as e:
        print(f"Error saving merged file: {e}")


# ────────────────────────────────────────────────
#  Usage
# ────────────────────────────────────────────────

if __name__ == "__main__":
    MAIN_FOLDER = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Corn_Images_or_Becks_Visualizations_and_XML_Generation_Script\UnZip_Becks_5k_Images_18_05_2026"

    merge_datumaro_jsons(
        main_folder=MAIN_FOLDER,
        output_file="Batch_5k_18_05_2026_merged_with_subfolders.json"
    )