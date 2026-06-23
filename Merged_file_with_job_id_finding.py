import json
from pathlib import Path

def merge_datumaro_jsons(main_folder: str, output_file: str = "merged_annotations.json") -> None:
    """
    Merges multiple Datumaro Validation.json files into one combined file.
    
    - Keeps 'info' and 'categories' from the first file found
    - Concatenates all 'items' lists
    - Adds 'source_folder' field to each item showing the relative subfolder path
    """
    main_path = Path(main_folder).resolve()
    if not main_path.is_dir():
        print(f"Error: {main_path} is not a directory")
        return

    # Find all Validation.json files recursively
    json_files = list(main_path.rglob("Validation.json"))
    
    if not json_files:
        print("No Validation.json files found in the folder structure.")
        return

    print(f"Found {len(json_files)} Validation.json files")

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

            # Get relative subfolder path (from main folder)
            # This gives you the full relative path like "Subfolder1/Annotations" or just "Subfolder1"
            relative_folder = json_path.parent.relative_to(main_path).as_posix()

            # Merge items with source_folder added
            items = data.get("items", [])
            for item in items:
                # Add source tracking field
                item["source_folder"] = relative_folder
                # Optional: also save full path if needed
                # item["source_file"] = str(json_path.relative_to(main_path))

            if items:
                merged_data["items"].extend(items)
                print(f"  + {len(items):5,d} items from {relative_folder}")

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
        
        print("\n" + "═" * 80)
        print(f"Successfully merged {len(merged_data['items']):,} items")
        print(f"Saved to: {output_path}")
        print(f"Total frames/images: {len(merged_data['items']):,}")
        print("═" * 80)
    
    except Exception as e:
        print(f"Error saving merged file: {e}")


# ────────────────────────────────────────────────
#  Usage
# ────────────────────────────────────────────────

if __name__ == "__main__":
    MAIN_FOLDER = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Rework\UnZip_total_5k"

    merge_datumaro_jsons(
        main_folder=MAIN_FOLDER,
        output_file="including_job_ids_total_5k_merged_clean.json"
    )