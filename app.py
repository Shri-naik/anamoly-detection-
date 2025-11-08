from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import uuid

# ---------------------------
# Config
# ---------------------------
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

MODEL_PATHS = {
    "water": "water_best_model.h5",
    "air": "air_best_model.h5"
}

CLASS_NAMES = ["Clean", "Little Polluted", "Highly Polluted"]

# ---------------------------
# Helper functions
# ---------------------------
def load_model(model_path):
    if not os.path.exists(model_path):
        return None
    return tf.keras.models.load_model(model_path)

def preprocess_image(image, img_size=(224, 224)):
    img = image.resize(img_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

def analyze_water_rgb(image):
    img = np.array(image)
    avg_rgb = np.mean(img, axis=(0, 1))  
    r, g, b = avg_rgb
    analysis = []

    if g > r and g > b and g > 100:
        analysis.append("🟢 High green: Possible algae growth. If harmful algae → remove with UV/chemical treatment. If harmless → can be used as biofertilizer or biofuel.")
    if r > g and r > b and r > 100:
        analysis.append("🔴 High red/brown: Possible iron or suspended solids. Treat with filtration/sedimentation.")
    if b > r and b > g and b > 120:
        analysis.append("🔵 Strong blue: Likely clean water, suitable for use.")
    if np.mean(avg_rgb) < 60:
        analysis.append("⚫ Very dark: Possible industrial waste / oil contamination. Requires chemical treatment before safe use.")
    if not analysis:
        analysis.append("No major harmful constituents detected visually.")
    return avg_rgb, analysis

def analyze_air_rgb(image):
    img = np.array(image)
    avg_rgb = np.mean(img, axis=(0, 1))  
    r, g, b = avg_rgb
    analysis = []

    if np.mean(avg_rgb) < 80:
        analysis.append("🌫️ Dark/gray tones: Possible smog or soot. Avoid exposure, use masks/air filters.")
    if r > 120 and r > g and r > b:
        analysis.append("🟤 Brown haze: Possible dust or industrial emissions. Reduce outdoor activity.")
    if g > 120 and g > r and g > b:
        analysis.append("🟢 Greenish tint: Could indicate chemical pollutants. Ventilation and monitoring advised.")
    if b > 130 and b > r and b > g:
        analysis.append("🔵 Clear sky with strong blue: Clean air likely.")
    if not analysis:
        analysis.append("No major harmful air constituents detected visually.")
    return avg_rgb, analysis

# ---------------------------
# Flask Routes
# ---------------------------
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/select")
def select():
    return render_template("select.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    pollution_type = request.args.get("type", "water").lower()

    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        # Save uploaded file
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(filepath)

        # Open image
        image = Image.open(filepath).convert("RGB")

        # Load model
        model = load_model(MODEL_PATHS[pollution_type])
        if not model:
            return "Model not found", 500

        # Predict
        img_array = preprocess_image(image)
        pred = model.predict(img_array)
        confidence = np.max(pred)
        label_index = np.argmax(pred)
        prediction = CLASS_NAMES[label_index]

        # All class probabilities (for frontend display)
        probs = {CLASS_NAMES[i]: float(pred[0][i] * 100) for i in range(len(CLASS_NAMES))}

        # Decide severity class (for CSS color)
        if label_index == 0:
            class_name = "Low"
        elif label_index == 1:
            class_name = "Medium"
        else:
            class_name = "High"

        # Extra RGB analysis
        if pollution_type == "water":
            avg_rgb, analysis = analyze_water_rgb(image)
        else:
            avg_rgb, analysis = analyze_air_rgb(image)

        return render_template(
            "result.html",
            filename=filename,
            prediction=f"{prediction} ({confidence*100:.2f}% confidence)",
            class_name=class_name,
            probs=probs,
            analysis=analysis,
            avg_rgb=avg_rgb
        )

    return render_template("predict.html", type=pollution_type)

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
