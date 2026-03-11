import tensorflow as tf
import numpy as np
from PIL import Image
import os

IMG_SIZE = 224

# Load model
model = tf.keras.models.load_model("model.h5")

# Load class names
with open("class_names.txt") as f:
    class_names = [line.strip() for line in f]

# Optional: Disease → Treatment mapping
TREATMENTS = {
    "Pepper__bell___Bacterial_spot": "Apply copper-based bactericide. Avoid overhead watering.",
    "Pepper__bell___healthy": "Plant is healthy. No treatment required.",

    "Potato___Early_blight": "Use fungicides like chlorothalonil. Remove infected leaves.",
    "Potato___Late_blight": "Apply metalaxyl-based fungicide. Destroy infected plants.",
    "Potato___healthy": "Plant is healthy. Maintain good irrigation and nutrition.",

    "Tomato_Bacterial_spot": "Use copper fungicide. Avoid splashing water on leaves.",
    "Tomato_Early_blight": "Apply fungicide. Practice crop rotation.",
    "Tomato_Late_blight": "Use systemic fungicide immediately. Remove infected plants.",
    "Tomato_Leaf_Mold": "Improve air circulation. Apply fungicide.",
    "Tomato_Septoria_leaf_spot": "Remove infected leaves. Apply fungicide.",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Use neem oil or insecticidal soap.",
    "Tomato__Target_Spot": "Apply appropriate fungicide. Remove infected leaves.",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Control whiteflies. Remove infected plants.",
    "Tomato__Tomato_mosaic_virus": "Remove infected plants. Disinfect tools.",
    "Tomato_healthy": "Plant is healthy. No treatment needed."
}

# -----------------------------
# Image preprocessing
# -----------------------------
def preprocess_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    return np.expand_dims(img, axis=0)

# -----------------------------
# Prediction
# -----------------------------
IMAGE_PATH = "image.png"

if not os.path.exists(IMAGE_PATH):
    print("Image not found:", IMAGE_PATH)
    exit()

img = preprocess_image(IMAGE_PATH)

pred = model.predict(img)[0]
index = int(np.argmax(pred))
confidence = float(pred[index]) * 100

disease = class_names[index]
treatment = TREATMENTS.get(disease, "Consult agriculture expert.")

print("\n--- Prediction Result ---")
print("Predicted Disease:", disease)
print("Confidence:", round(confidence, 2), "%")
print("Treatment:", treatment)
