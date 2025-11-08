# src/model.py
import tensorflow as tf
from tensorflow.keras import layers, models


def build_model(num_classes: int, input_shape=(224, 224, 3)):
    """
    Build a CNN model using transfer learning (MobileNetV2).
    Args:
        num_classes: number of output classes
        input_shape: input image shape (H, W, C)
    """
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # freeze feature extractor

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    m = build_model(num_classes=3)
    m.summary()
