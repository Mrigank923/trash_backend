import os

for c in ["organic", "recyclable", "hazardous"]:
    print(c, len(os.listdir(f"dataset_3class-2/{c}")))
