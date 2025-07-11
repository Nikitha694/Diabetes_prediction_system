import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model

# Load trained Keras model
model = load_model('diabetes_model.h5')

# Load encoders
with open('encoder.pkl', 'rb') as f:
    encoders = pickle.load(f)

# App title
st.title("🩺 Diabetes Shield")
st.write("Fill the form below to check the diabetes prediction.")

# Define user inputs in two columns
def user_input():
    input_data = {}

    col1, col2 = st.columns(2)
    with col1:
        input_data['Gender'] = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        input_data['Polyuria'] = st.selectbox("Polyuria (excessive urination)", ["Yes", "No"])

    col3, col4 = st.columns(2)
    with col3:
        input_data['Polydipsia'] = st.selectbox("Polydipsia (excessive thirst)", ["Yes", "No"])
    with col4:
        input_data['sudden weight loss'] = st.selectbox("Sudden Weight Loss", ["Yes", "No"])

    col5, col6 = st.columns(2)
    with col5:
        input_data['partial paresis'] = st.selectbox("Partial Paresis (muscle weakness)", ["Yes", "No"])
    with col6:
        input_data['visual blurring'] = st.selectbox("Visual Blurring", ["Yes", "No"])

    col7, col8 = st.columns(2)
    with col7:
        input_data['Alopecia'] = st.selectbox("Alopecia (hair loss)", ["Yes", "No"])
    with col8:
        input_data['Irritability'] = st.selectbox("Irritability", ["Yes", "No"])

    return input_data

# Get input
input_values = user_input()

# Predict button
if st.button("Predict"):
    try:
        # Encode inputs
        encoded = []
        for key in ['Polyuria', 'Gender', 'Polydipsia', 'sudden weight loss', 'partial paresis', 'visual blurring', 'Alopecia', 'Irritability']:
            le = encoders[key]
            encoded_val = le.transform([input_values[key]])[0]
            encoded.append(encoded_val)

        # Make prediction
        features = np.array(encoded).reshape(1, -1)
        prediction = model.predict(features)[0][0]
        result = "Positive (Diabetic)" if prediction >= 0.5 else "Negative (Non-Diabetic)"
        st.success(f"🧾 Prediction Result: **{result}**")
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")

# Sidebar feature descriptions
with st.sidebar.expander("ℹ️ Feature Descriptions"):
    st.markdown("""
    - **Polyuria**: Excessive or frequent urination  
    - **Gender**: Biological sex of the individual (Male/Female)  
    - **Polydipsia**: Excessive or abnormal thirst  
    - **Sudden Weight Loss**: Rapid loss of weight without trying  
    - **Partial Paresis**: Muscle weakness or partial loss of movement  
    - **Visual Blurring**: Making an image look less sharp and more unclear.
    - **Alopecia**: Sudden hair loss  
    - **Irritability**: Tendency to get easily annoyed or agitated  
    """)
