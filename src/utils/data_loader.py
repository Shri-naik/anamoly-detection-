import os
import tensorflow as tf
from PIL import Image

def clean_dataset(folder):
    valid_exts = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    removed = []
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            ext = os.path.splitext(f)[1].lower()
            if ext not in valid_exts:
                removed.append(path)
                continue
            try:
                img = Image.open(path)
                img.verify()
            except Exception:
                removed.append(path)
                try:
                    os.remove(path)
                except:
                    pass
    return removed

def get_datasets(data_dir: str, img_size=(224, 224), batch_size=32):
    datasets = {}
    preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
    class_names = None

    for split in ["train", "val", "test"]:
        split_dir = os.path.join(data_dir, split)
        if not os.path.exists(split_dir):
            raise FileNotFoundError(f"Directory not found: {split_dir}")

        clean_dataset(split_dir)

        ds = tf.keras.utils.image_dataset_from_directory(
            split_dir,
            image_size=img_size,
            batch_size=batch_size,
            shuffle=(split=="train")
        )

        if split == "train":
            class_names = ds.class_names  # ✅ capture class names here

        ds = ds.map(lambda x, y: (preprocess_input(x), y))
        ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE)
        datasets[split] = ds

    datasets["class_names"] = class_names  # ✅ add class_names to dict
    return datasets

def get_num_classes(data_dir: str) -> int:
    train_dir = os.path.join(data_dir, "train")
    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"Train folder not found: {train_dir}")
    return len(os.listdir(train_dir))
