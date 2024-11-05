import streamlit as st
import pandas as pd
from joblib import load

# Load the pre-trained model and preprocessor
model = load('artifacts/model_evaluation/models/best_model.joblib')
preprocessor = load('artifacts/feature_engineering/preprocessor.joblib')

def calculate_normalized_risk(medical_history: str) -> float:
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    
    diseases = medical_history.lower().split(" & ") if isinstance(medical_history, str) else []
    total_risk_score = sum(risk_scores.get(disease.strip(), 0) for disease in diseases)

    max_score = 14
    min_score = 0
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score) if max_score > min_score else 0
    return normalized_risk_score

def preprocess(input_df: pd.DataFrame) -> pd.DataFrame:
    if 'medical_history' in input_df.columns:
        input_df['normalized_risk_score'] = input_df['medical_history'].apply(calculate_normalized_risk)
    return preprocessor.transform(input_df)

st.title('Health Insurance Cost Predictor')

# Define options for categorical variables
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Create a layout for inputs
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input('Age', min_value=18, step=1, max_value=100)
with row1[1]:
    number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20)
with row1[2]:
    income_lakhs = st.number_input('Income in Lakhs', step=1, min_value=0, max_value=200)

with row2[0]:
    genetical_risk = st.number_input('Genetical Risk', step=1, min_value=0, max_value=5)
with row2[1]:
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
with row2[2]:
    employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])

with row3[0]:
    gender = st.selectbox('Gender', categorical_options['Gender'])
with row3[1]:
    marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
with row3[2]:
    bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])

with row4[0]:
    smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
with row4[1]:
    region = st.selectbox('Region', categorical_options['Region'])
with row4[2]:
    medical_history = st.selectbox('Medical History', categorical_options['Medical History'])

# Add input for income level
income_level = st.selectbox('Income Level', ['Low', 'Medium', 'High'])

# Collect inputs into a dictionary with exact column names as expected by the model
input_df = {
    'age': age,
    'number_of_dependants': number_of_dependants,
    'income_lakhs': income_lakhs,
    'genetical_risk': genetical_risk,
    'insurance_plan': insurance_plan,
    'employment_status': employment_status,
    'gender': gender,
    'marital_status': marital_status,
    'bmi_category': bmi_category,
    'smoking_status': smoking_status,
    'region': region,
    'medical_history': medical_history,
    'annual_premium_amount': 0,  # Default value or add input if necessary
    'income_level': income_level,  # Add the income_level input here
    'normalized_risk_score': 0  # Default value or add input if necessary
}

# Make a prediction when the button is clicked
if st.button('Predict'):
    try:
        # Preprocess the input data
        processed_data = preprocess(pd.DataFrame([input_df]))

        # Make predictions
        predictions = model.predict(processed_data)
        predicted_cost = round(predictions[0][0])  # Extract the scalar value and round

        st.success(f'Predicted Health Insurance Cost: ₹{predicted_cost:,}')

    except Exception as e:
        st.error(f"Error occurred: {e}")
