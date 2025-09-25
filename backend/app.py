from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# ------------------ Paths ------------------
MODEL_PATH = "diabetes_bilayered_model.h5"
SCALER_PATH = "scaler.pkl"
ENCODER_PATH = "encoder.pkl"

# ------------------ Load model, scaler, encoders ------------------
model = load_model(MODEL_PATH)

with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

with open(ENCODER_PATH, 'rb') as f:
    encoders = pickle.load(f)

# ------------------ API Routes ------------------
@app.route('/')
def index():
    return "✅ Diabetes Prediction API is running!"

@app.route('/predict', methods=['POST'])
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

        # Build DataFrame
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
        confidence = round(pred_prob * 100, 1)  # convert to percentage

        prediction = 'Diabetic' if pred_prob >= 0.5 else 'Non-Diabetic'

        # Risk factors from raw input
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


if __name__ == '__main__':
    app.run(debug=True)
