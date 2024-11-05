import streamlit as st
import requests

# Flask API URL
FLASK_API_URL = "http://localhost:5000/predict"

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
    'income_level': '',  # Default value or add input if necessary
    'normalized_risk_score': 0  # Default value or add input if necessary
}

# Make a prediction when the button is clicked
if st.button('Predict'):
    try:
        # Send input to Flask API
        response = requests.post(FLASK_API_URL, json=input_df)
        if response.status_code == 200:
            prediction = response.json()
            predicted_cost = prediction[0]['predicted_cost'] if isinstance(prediction, list) else prediction['predicted_cost']
            st.success(f'Predicted Health Insurance Cost: ₹{predicted_cost:,}')

        else:
            error_message = response.json().get('error', 'Unknown error occurred.')
            st.error(f"Error: {error_message}")
    except Exception as e:
        st.error(f"Exception occurred: {e}")


