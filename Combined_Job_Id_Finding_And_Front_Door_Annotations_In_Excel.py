import json
from pathlib import Path
import pandas as pd
from collections import defaultdict

def merge_filter_and_export_to_excel(main_folder: str, output_excel: str = "job_id_with_subfolder.xlsx"):
    """
    1. Merges all Validation.json files from subfolders
    2. Filters items that have at least one bbox with label_id == 2
    3. Exports 'id' and 'subfolder' (Job ID) to Excel
    """
    main_path = Path(main_folder).resolve()
    if not main_path.is_dir():
        print(f"Error: {main_path} is not a directory")
        return

    # Find all Validation.json files
    json_files = list(main_path.rglob("Validation.json"))
    
    if not json_files:
        print("No Validation.json files found!")
        return

    print(f"Found {len(json_files)} Validation.json files\n")

    records = []  # To store final data for Excel

    for json_path in json_files:
        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            relative_folder = json_path.parent.relative_to(main_path).as_posix()
            # Clean subfolder name (optional: remove /Annotations if present)
            subfolder_name = relative_folder.replace("/Annotations", "").replace("/annotations", "")

            print(f"Processing: {subfolder_name} ({len(data.get('items', [])):,} items)")

            # Filter items with label_id == 2
            for item in data.get("items", []):
                annotations = item.get("annotations", [])
                has_label_2 = any(
                    ann.get("type") == "bbox" and ann.get("label_id") == 2 
                    for ann in annotations
                )

                if has_label_2:
                    records.append({
                        "id": item.get("id"),
                        "subfolder": subfolder_name,           # This is your Job ID / Subfolder
                        "full_relative_path": relative_folder,
                        "image_name": item.get("image", {}).get("path") or item.get("id")
                    })

        except Exception as e:
            print(f"Error reading {json_path}: {e}")

    if not records:
        print("No items with label_id=2 found.")
        return

    # Create DataFrame and save to Excel
    df = pd.DataFrame(records)
    
    # Optional: Sort and remove duplicates if any
    df = df.drop_duplicates(subset=["id"]).sort_values(by=["subfolder", "id"])

    # Save to Excel
    output_path = main_path / output_excel
    df.to_excel(output_path, index=False)

    print("\n" + "═" * 90)
    print(f"✅ SUCCESS!")
    print(f"Total items with label_id=2: {len(df):,}")
    print(f"Unique subfolders (Job IDs): {df['subfolder'].nunique()}")
    print(f"File saved: {output_path}")
    print("═" * 90)

    # Show summary by subfolder
    summary = df['subfolder'].value_counts().head(10)
    print("\nTop 10 subfolders by count:")
    print(summary)


# ────────────────────────────────────────────────
#  Usage
# ────────────────────────────────────────────────

if __name__ == "__main__":
    MAIN_FOLDER = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Rework\UnZip_total_5k"
    
    merge_filter_and_export_to_excel(
        main_folder=MAIN_FOLDER,
        output_excel="job_id_with_subfolder.xlsx"
    )