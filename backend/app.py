from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import os
import joblib

# ------------------ App Setup ------------------
app = Flask(__name__)
CORS(app)

# ⭐ Safe path (works local + cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "diabetes_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "encoder.pkl")
TARGET_ENCODER_PATH = os.path.join(BASE_DIR, "target_encoder.pkl")

# ⭐ Lazy load
model = None
encoders = None
target_encoder = None

def load_files():
    global model, encoders, target_encoder
    if model is None:
        print("🔄 Loading model...")
        model = joblib.load(MODEL_PATH)

        with open(ENCODER_PATH, "rb") as f:
            encoders = pickle.load(f)

        with open(TARGET_ENCODER_PATH, "rb") as f:
            target_encoder = pickle.load(f)

        print("✅ Model loaded")

# ================= ROOT =================
@app.route('/')
def home():
    return "✅ Diabetes Prediction API is running!"

# ================= PREDICT =================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        load_files()

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
            df[col] = encoders[col].transform(df[col])

        encoded = df.values
        prob = model.predict_proba(encoded)[0][1]

        prediction = "Diabetic" if prob >= 0.65 else "Non-Diabetic"

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

# ⭐ Required for local run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
