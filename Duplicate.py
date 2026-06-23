import os
from PIL import Image
import imagehash

# ===== CHANGE THIS =====
main_folder = r"D:\python\Vara Prasad\Tippani Project\convert_voc_to_cvat\5kimages"
similarity_threshold = 5   # lower = stricter, higher = more loose
# =======================

image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')

hash_dict = {}
similar_images = []

for root, dirs, files in os.walk(main_folder):
    for file in files:
        if file.lower().endswith(image_extensions):
            file_path = os.path.join(root, file)
            try:
                img = Image.open(file_path)
                img_hash = imagehash.phash(img)

                for existing_hash in hash_dict:
                    difference = img_hash - existing_hash
                    if difference <= similarity_threshold:
                        similar_images.append((file_path, hash_dict[existing_hash]))
                        break
                else:
                    hash_dict[img_hash] = file_path

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

print("\nSimilar Images Found:\n")

if similar_images:
    for sim in similar_images:
        print("Similar :", sim[0])
        print("Matched :", sim[1])
        print("-" * 60)
else:
    print("No similar images found.")

print("\nDone.")