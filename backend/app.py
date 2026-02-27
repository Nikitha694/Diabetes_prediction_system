from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import os
import joblib

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "encoder.pkl")
TARGET_ENCODER_PATH = os.path.join(BASE_DIR, "target_encoder.pkl")

# ⭐ Lazy load variables
model = None
encoders = None
target_encoder = None

def load_model_files():
    global model, encoders, target_encoder
    if model is None:
        print("🔄 Loading model...")
        model = joblib.load(MODEL_PATH)
        with open(ENCODER_PATH, "rb") as f:
            encoders = pickle.load(f)
        with open(TARGET_ENCODER_PATH, "rb") as f:
            target_encoder = pickle.load(f)
        print("✅ Model loaded")


@app.route('/')
def home():
    return "✅ Diabetes Prediction API is running!"


@app.route('/predict', methods=['POST'])
def predict():
    try:
        load_model_files()  # ⭐ lazy load happens here

        data = request.get_json()

        feature_map = {
            'polyuria': 'Polyuria',
            'gender': 'Gender',
            'polydipsia': 'Polydipsia',
            'suddenWeightLoss': 'sudden weight loss',
            'partialParesis': 'partial paresis',
            'visualBlurring': 'visual blurring',
            'alopecia': 'Alopecia',
            'irritability': 'Irritability'
        }

        bool_map = {True: 'Yes', False: 'No'}

        row = {}
        for key, col in feature_map.items():
            value = data.get(key)

            if isinstance(value, bool):
                value = bool_map[value]
            elif key == 'gender':
                value = str(value).capitalize()

            row[col] = [value]

        df = pd.DataFrame(row)

        for col in df.columns:
            df[col] = encoders[col].transform(df[col])

        encoded = df.values
        prob = model.predict_proba(encoded)[0][1]

        prediction = "Diabetic" if prob >= 0.65 else "Non-Diabetic"

        return jsonify({
            "prediction": prediction,
            "confidence": round(prob * 100, 1)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
