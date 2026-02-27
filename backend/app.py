from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import os
import joblib


# ------------------ App Setup ------------------
app = Flask(__name__)
CORS(app)


# ================= LOAD FILES =================
model = joblib.load("diabetes_model.pkl")

with open("encoder.pkl", "rb") as f:
    encoders = pickle.load(f)

with open("target_encoder.pkl", "rb") as f:
    target_encoder = pickle.load(f)

# ================= ROOT =================
@app.route('/')
def home():
    return "✅ Diabetes Prediction API is running!"

# ================= PREDICT =================
@app.route('/predict', methods=['POST'])

def predict():
    data = request.get_json()

    try:
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

            if value is None:
                return jsonify({"error": f"Missing field: {key}"}), 400

            if isinstance(value, bool):
                value = bool_map[value]
            elif key == 'gender':
                value = str(value).capitalize()

            row[col] = [value]

        df = pd.DataFrame(row)

        # Encode
        for col in df.columns:
            le = encoders[col]
            df[col] = le.transform(df[col])

        # Predict

        encoded = df.values
        pred = model.predict(encoded)
        prob = model.predict_proba(encoded)[0][1]

        prob = model.predict_proba(encoded)[0][1]

        prediction = "Diabetic" if prob >= 0.65 else "Non-Diabetic"

        # Risk factors
        risk_map = {

            'polyuria': 'Polyuria',
            'polydipsia': 'Polydipsia',
            'suddenWeightLoss': 'Sudden Weight Loss',
            'partialParesis': 'Partial Paresis',
            'visualBlurring': 'Visual Blurring',
            'alopecia': 'Alopecia',
            'irritability': 'Irritability'
        }


        risk_factors = [v for k, v in risk_map.items() if data.get(k)]

        return jsonify({
            "prediction": prediction,
            "confidence": round(prob * 100, 1),
            "riskFactors": risk_factors,
            "recommendations": [
                "Consult doctor for further tests",
                "Maintain healthy lifestyle",
                "Monitor symptoms regularly"
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400




)
