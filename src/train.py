import os
import argparse
import numpy as np
import tensorflow as tf
from model import build_model
from utils.data_loader import get_datasets, get_num_classes


def compute_class_weights(train_ds, num_classes):
    """
    Compute class weights to handle imbalance.
    """
    counts = np.zeros(num_classes)
    for _, labels in train_ds.unbatch():
        counts[labels.numpy()] += 1

    total = np.sum(counts)
    class_weights = {i: total / (num_classes * counts[i]) for i in range(num_classes)}

    print("📊 Class distribution:", counts)
    print("⚖️ Computed class weights:", class_weights)
    return class_weights


def train_model(data_dir: str,
                num_classes: int,
                epochs: int = 10,
                batch_size: int = 32,
                img_size=(224, 224),
                save_path="best_model.h5"):
    """
    Train a CNN model on the dataset with class weights.
    """
    # Load datasets
    datasets = get_datasets(data_dir, img_size, batch_size)
    train_ds, val_ds, test_ds = datasets["train"], datasets["val"], datasets["test"]
    class_names = datasets["class_names"]

    print(f"✅ Classes: {class_names}")

    # Compute class weights
    class_weights = compute_class_weights(train_ds, num_classes)

    # Build model
    model = build_model(num_classes=num_classes, input_shape=img_size + (3,))
    model.summary()

    # Callbacks
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            save_path, monitor="val_accuracy", save_best_only=True, verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=5, restore_best_weights=True
        )
    ]

    # Train
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        class_weight=class_weights,
        callbacks=callbacks
    )

    # Evaluate
    print("✅ Training complete. Evaluating on test set...")
    loss, acc = model.evaluate(test_ds)
    print(f"Test Accuracy: {acc:.4f}")

    return model, history


# 🟦 Extra: Histogram-based RGB analysis (for water pollution)
def analyze_water_rgb(image):
    """
    Analyze water image using RGB histograms for pollution cues.
    """
    import numpy as np

    img = np.array(image)
    r_hist = np.histogram(img[:, :, 0], bins=256, range=(0, 256))[0]
    g_hist = np.histogram(img[:, :, 1], bins=256, range=(0, 256))[0]
    b_hist = np.histogram(img[:, :, 2], bins=256, range=(0, 256))[0]

    analysis = []
    if g_hist[150:].sum() > r_hist[150:].sum() and g_hist[150:].sum() > b_hist[150:].sum():
        analysis.append("🟢 Strong green dominance: Possible algae growth.")
    if r_hist[120:].sum() > g_hist[120:].sum() and r_hist[120:].sum() > b_hist[120:].sum():
        analysis.append("🔴 Brown/red tint: Possible industrial waste or sewage.")
    if b_hist[160:].sum() > r_hist[160:].sum() and b_hist[160:].sum() > g_hist[160:].sum():
        analysis.append("🔵 Strong blue presence: Likely clean water.")

    if not analysis:
        analysis.append("⚪ No major harmful constituents detected visually.")
    return analysis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CNN on Air or Water dataset")
    parser.add_argument("--dataset", type=str, required=True,
                        choices=["air", "water"],
                        help="Choose dataset: 'air' or 'water'")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    # Paths for datasets
    dataset_map = {
        "air": ("data/air_processed", "air_best_model.h5"),
        "water": ("data/water_processed", "water_best_model.h5")
    }

    data_dir, save_path = dataset_map[args.dataset]
    num_classes = get_num_classes(data_dir)

    train_model(
        data_dir=data_dir,
        num_classes=num_classes,
        epochs=args.epochs,
        batch_size=args.batch_size,
        save_path=save_path
    )
