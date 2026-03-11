from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
import os

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = "model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Load class names
with open("class_names.txt") as f:
    CLASS_NAMES = [c.strip() for c in f.readlines()]

print("Model loaded successfully")
print("Classes:", CLASS_NAMES)

# -----------------------------
# Disease → Treatment Mapping
# -----------------------------
TREATMENTS = {
    "Pepper__bell___Bacterial_spot": "Use copper fungicide. Remove infected leaves.",
    "Pepper__bell___healthy": "Healthy plant.",
    "Potato___Early_blight": "Apply chlorothalonil fungicide.",
    "Potato___Late_blight": "Use mancozeb fungicide.",
    "Potato___healthy": "Healthy plant.",
    "Tomato_Bacterial_spot": "Copper spray recommended.",
    "Tomato_Early_blight": "Apply fungicide.",
    "Tomato_Late_blight": "Immediate fungicide spray.",
    "Tomato_Leaf_Mold": "Improve ventilation + fungicide.",
    "Tomato_Septoria_leaf_spot": "Remove infected leaves.",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Use neem oil.",
    "Tomato__Target_Spot": "Weekly fungicide.",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Control whiteflies.",
    "Tomato__Tomato_mosaic_virus": "Remove infected plant.",
    "Tomato_healthy": "Healthy plant."
}

# -----------------------------
# Preprocess Image
# -----------------------------
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]
    filename = "temp.jpg"
    file.save(filename)

    img = preprocess_image(filename)
    preds = model.predict(img)[0]

    index = np.argmax(preds)
    disease = CLASS_NAMES[index]
    accuracy = float(preds[index]) * 100
    treatment = TREATMENTS.get(disease, "Consult agriculture expert")

    os.remove(filename)

    return jsonify({
        "disease": disease,
        "accuracy": round(accuracy, 2),
        "treatment": treatment
    })

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)