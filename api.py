import logging
from flask import Flask, request, jsonify
from joblib import load
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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

@app.route("/")
def home():
    return "Welcome to the Machine Learning API!"

@app.route('/predict', methods=['POST'])
def make_prediction():
    try:
        # Receive JSON data
        data = request.get_json()
        logger.info("Received data: %s", data)

        # Convert data to DataFrame
        input_df = pd.DataFrame([data])

        # Ensure necessary columns exist
        expected_columns = ['age', 'number_of_dependants', 'income_lakhs', 'genetical_risk', 
                            'insurance_plan', 'employment_status', 'gender', 'marital_status', 
                            'bmi_category', 'smoking_status', 'region', 'medical_history']
        
        # Check for missing columns
        for col in expected_columns:
            if col not in input_df.columns:
                return jsonify({"error": f"Missing column: {col}"}), 400

        # Preprocess the input data
        processed_data = preprocess(input_df)
        logger.info("Processed data: %s", processed_data)

        # Make predictions
        predictions = model.predict(processed_data)
        logger.info("Predictions: %s", predictions)

        # Extract and round the predicted value
        predicted_cost = round(predictions[0][0])  # Extract the scalar value and round

        # Return the prediction in JSON format as a list
        return jsonify([{"predicted_cost": predicted_cost}])  # Changed to a list with a dictionary

    except Exception as e:
        logger.error('Error: %s', str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
