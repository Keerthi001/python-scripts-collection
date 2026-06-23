import os

def rename_default_to_validation(main_folder):
    renamed_count = 0
    
    for root, dirs, files in os.walk(main_folder):
        # Check if we're inside an "annotations" folder
        if os.path.basename(root) == "annotations":
            if "default.json" in files:
                old_path = os.path.join(root, "default.json")
                new_path = os.path.join(root, "Validation.json")
                
                # Check if Validation.json already exists
                if os.path.exists(new_path):
                    print(f"⚠️  Skipped (Validation.json already exists): {old_path}")
                else:
                    try:
                        os.rename(old_path, new_path)
                        print(f"✅ Renamed: {old_path} → Validation.json")
                        renamed_count += 1
                    except Exception as e:
                        print(f"❌ Error renaming {old_path}: {e}")
    
    print(f"\n🎉 Done! Total files renamed: {renamed_count}")

# ============== CHANGE THIS PATH ==============
main_folder = r"D:\python\Vara Prasad\Tippani Project\400_Rely_Script\Rework\UnZip_total_5k"   # Or use full path: r"C:\Users\YourName\Downloads\UnZip_total_5k"
# =============================================

if __name__ == "__main__":
    if os.path.exists(main_folder):
        rename_default_to_validation(main_folder)
    else:
        print(f"Folder not found: {main_folder}")