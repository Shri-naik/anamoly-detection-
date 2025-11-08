# src/preprocess.py
import os
import shutil
from sklearn.model_selection import train_test_split
import random

random.seed(42)  # reproducibility


def split_dataset(src_dir, dest_dir, test_size=0.15, val_size=0.15):
    """
    Splits images in src_dir into train/val/test inside dest_dir.
    Assumes subfolders = class names.
    """
    for class_name in os.listdir(src_dir):
        class_path = os.path.join(src_dir, class_name)
        if not os.path.isdir(class_path):
            continue

        images = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
        if not images:
            continue

        # Split into train/test
        train_files, test_files = train_test_split(images, test_size=test_size)
        # Split train further into train/val
        train_files, val_files = train_test_split(
            train_files, test_size=val_size / (1 - test_size)
        )

        for split, files in zip(["train", "val", "test"], [train_files, val_files, test_files]):
            split_dir = os.path.join(dest_dir, split, class_name)
            os.makedirs(split_dir, exist_ok=True)
            for f in files:
                shutil.copy2(os.path.join(class_path, f), os.path.join(split_dir, f))

    print(f"✅ Dataset split saved inside: {dest_dir}")


def preprocess_air_data():
    """
    Air dataset: already in class folders. Just split into train/val/test.
    """
    src_dir = "data/air"
    dest_dir = "data/air_processed"
    split_dataset(src_dir, dest_dir)


def preprocess_water_data():
    """
    Water dataset: already in 3 class subfolders: clean, polluted, highly_polluted.
    Just split into train/val/test.
    """
    src_dir = "data/water"
    dest_dir = "data/water_processed"
    split_dataset(src_dir, dest_dir)


if __name__ == "__main__":
    print("🔹 Preprocessing Air dataset...")
    preprocess_air_data()

    print("\n🔹 Preprocessing Water dataset...")
    preprocess_water_data()
