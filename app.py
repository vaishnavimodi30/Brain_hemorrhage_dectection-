from flask import Flask, request, jsonify, render_template
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# Load the trained model
MODEL_PATH = 'my_model_weights.keras'  # Replace with your weights file
MODEL_STRUCTURE_PATH = 'my_model_weights.keras'  # Replace with your model structure file

try:
    Model = tf.keras.models.load_model(MODEL_STRUCTURE_PATH)
    Model.load_weights(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

def predict_and_check(img, threshold=0.6):
    """Predicts and checks if the image is within the model's domain."""
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

    print("🟢 Image Shape:", img_array.shape)  # Debugging

    prediction = Model.predict(img_array)
    confidence = np.max(prediction)
    
    print("🟢 Prediction Raw Output:", prediction)  # Debugging

    if confidence < threshold:
        return "Image not recognized. Provide a valid brain scan."
    return "Hemorrhage" if np.argmax(prediction) == 0 else "Normal"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        img = Image.open(io.BytesIO(file.read())).convert('L').resize((256, 256))  # Convert to grayscale
        prediction = predict_and_check(img)
        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
