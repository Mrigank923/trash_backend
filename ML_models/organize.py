import os
import shutil

SRC_DIR = "dataset/new-dataset-trash-type-v2"
DST_DIR = "dataset_3class-2"

CATEGORY_MAP = {
    # Organic
    "organic": "organic",

    # Recyclable
    "cardboard": "recyclable",
    "glass": "recyclable",
    "metal": "recyclable",
    "plastic": "recyclable",
    "paper": "recyclable",

    # hazardous
    "trash": "hazardous",
    "e-waste": "hazardous",
}

os.makedirs(DST_DIR, exist_ok=True)

for src_class, dst_class in CATEGORY_MAP.items():
    src_path = os.path.join(SRC_DIR, src_class)
    dst_path = os.path.join(DST_DIR, dst_class)
    os.makedirs(dst_path, exist_ok=True)

    if not os.path.exists(src_path):
        print(f"⚠️ Skipping {src_class}, not found.")
        continue

    for file in os.listdir(src_path):
        src_file = os.path.join(src_path, file)
        dst_file = os.path.join(dst_path, file)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)

print("✅ Garbage Classification V2 reorganized into 3 categories!")
