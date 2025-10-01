from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
import os

# ------------------ App Setup ------------------
app = Flask(__name__)
CORS(app)

# ------------------ Paths ------------------
BASE_DIR = os.path.dirname(__file__)  # backend folder
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_bilayered_model.h5")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "encoder.pkl")

# ------------------ Load Model & Pickles ------------------
try:
    model = load_model(MODEL_PATH)
except Exception as e:
    raise Exception(f"Error loading model: {e}")

try:
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
except Exception as e:
    raise Exception(f"Error loading scaler: {e}")

try:
    with open(ENCODER_PATH, 'rb') as f:
        encoders = pickle.load(f)
except Exception as e:
    raise Exception(f"Error loading encoders: {e}")

# ------------------ Routes ------------------
@app.route("/")
def index():
    return "✅ Diabetes Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    try:
        # Map frontend keys to dataset column names
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

        # Map booleans to strings used in training
        bool_map = {True: 'Yes', False: 'No'}

        # Build DataFrame from input
        row = {}
        for key, col in feature_map.items():
            value = data.get(key)
            if value is None:
                return jsonify({"error": f"Missing field: {key}"}), 400

            if isinstance(value, bool):
                value = bool_map[value]  # True/False → Yes/No
            elif key == 'gender':
                value = str(value).capitalize()  # Male/Female

            row[col] = [value]

        df = pd.DataFrame(row)

        # Encode features using saved LabelEncoders
        for col in df.columns:
            le = encoders[col]
            if df[col][0] not in le.classes_:
                return jsonify({"error": f"Invalid value '{df[col][0]}' for column '{col}'"}), 400
            df[col] = le.transform(df[col])

        # Scale features
        X_scaled = scaler.transform(df)

        # Predict
        pred_prob = float(model.predict(X_scaled)[0][0])
        confidence = round(pred_prob * 100, 1)  # percentage
        prediction = 'Diabetic' if pred_prob >= 0.5 else 'Non-Diabetic'

        # Extract risk factors
        risk_features_map = {
            'polyuria': 'Polyuria',
            'polydipsia': 'Polydipsia',
            'suddenWeightLoss': 'Sudden Weight Loss',
            'partialParesis': 'Partial Paresis',
            'visualBlurring': 'Visual Blurring',
            'alopecia': 'Alopecia',
            'irritability': 'Irritability'
        }
        risk_factors = [name for key, name in risk_features_map.items() if data.get(key)]

        # Recommendations
        recommendations = [
            "Consult with a healthcare provider immediately",
            "Consider blood glucose testing",
            "Monitor your diet and exercise regularly",
            "Keep a symptom diary"
        ] if prediction == 'Diabetic' else [
            "Continue maintaining a healthy lifestyle",
            "Regular checkups with healthcare provider",
            "Monitor for any new symptoms",
            "Keep a balanced diet and exercise routine"
        ]

        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "riskFactors": risk_factors,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ------------------ Run App ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
