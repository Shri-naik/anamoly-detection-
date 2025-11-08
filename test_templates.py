from flask import Flask, render_template, request, redirect, url_for
import os

# ---------------------------
# Config
# ---------------------------
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Mock data for testing templates
CLASS_NAMES = ["Clean", "Little Polluted", "Highly Polluted"]

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
        # Mock successful upload
        return redirect(url_for('result', type=pollution_type))
    
    return render_template("predict.html")

@app.route("/result")
def result():
    # Mock data for template testing
    pollution_type = request.args.get("type", "water").lower()
    mock_data = {
        "filename": "mock_image.jpg",
        "prediction": "Medium Pollution Level",
        "class_name": "Medium",
        "probs": {
            "Clean": 20,
            "Little Polluted": 65,
            "Highly Polluted": 15
        },
        "analysis": [
            "🟢 Sample analysis point 1",
            "🔴 Sample analysis point 2",
            "⚫ Sample analysis point 3"
        ]
    }
    
    return render_template("result.html", **mock_data)

if __name__ == "__main__":
    app.run(debug=True)