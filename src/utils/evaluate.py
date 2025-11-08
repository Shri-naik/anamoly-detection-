# src/utils/evaluate.py
import os
import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_loader import get_datasets


def evaluate_model(model_path: str, data_dir: str, img_size=(224, 224), batch_size=32):
    """
    Evaluate a trained model with precision, recall, F1, and confusion matrix.
    """
    datasets = get_datasets(data_dir, img_size, batch_size)
    test_ds = datasets["test"]

    # Load model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found at {model_path}")
    model = tf.keras.models.load_model(model_path)

    # Get predictions
    y_true, y_pred = [], []
    for x, y in test_ds:
        preds = model.predict(x, verbose=0)
        y_true.extend(y.numpy())
        y_pred.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # Classification report
    print("\n📊 Classification Report:")
    print(classification_report(y_true, y_pred, digits=4))

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.show()


def predict_image(model_path: str, image_path: str, img_size=(224, 224)):
    """
    Predict the class of a single image using a trained model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found at {model_path}")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found at {image_path}")

    model = tf.keras.models.load_model(model_path)

    # Load and preprocess image
    img = tf.keras.utils.load_img(image_path, target_size=img_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = tf.expand_dims(img_array, 0)  # batch dimension

    preds = model.predict(img_array)
    pred_class = preds.argmax(axis=-1)[0]
    confidence = preds.max()

    print(f"🔮 Prediction: Class {pred_class} (Confidence: {confidence:.2f})")
    return pred_class, confidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate or predict with trained model")
    parser.add_argument("--dataset", type=str, choices=["air", "water"], help="Dataset to evaluate")
    parser.add_argument("--model", type=str, help="Path to trained model (.h5)")
    parser.add_argument("--image", type=str, help="Optional: path to a single image for prediction")
    args = parser.parse_args()

    dataset_map = {
        "air": "data/air_processed",
        "water": "data/water_processed"
    }

    if args.image:
        predict_image(args.model, args.image)
    else:
        data_dir = dataset_map[args.dataset]
        evaluate_model(args.model, data_dir)
