import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.Premium_Price_Prediction import logger
from src.Premium_Price_Prediction.entity.config_entity import FeatureEngineeringConfig
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path
from typing import Tuple


class FeatureEngineering:
    def __init__(self, config: FeatureEngineeringConfig):
        self.config = config
        self.train_df = None
        self.test_df = None
        self.preprocessor = None

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load training and testing datasets from specified file paths."""
        self.train_df = pd.read_csv(self.config.train_filepath)
        self.test_df = pd.read_csv(self.config.test_filepath)
        logger.info(f"Data loaded from {self.config.train_filepath} and {self.config.test_filepath}")
        return self.train_df, self.test_df

    def preprocess_medical_history(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the 'medical_history' column and compute risk scores."""
        risk_scores = {
            "diabetes": 6,
            "heart disease": 8,
            "high blood pressure": 6,
            "thyroid": 5,
            "no disease": 0,
            "none": 0
        }

        # Split and map risk scores
        df[['disease1', 'disease2']] = (
            df['medical_history'].str.split(" & ", expand=True).apply(lambda x: x.str.lower())
        ).fillna('none')

        df['total_risk_score'] = df[['disease1', 'disease2']].apply(
            lambda x: risk_scores.get(x['disease1'], 0) + risk_scores.get(x['disease2'], 0), axis=1
        )

        # Normalize risk scores
        max_score, min_score = df['total_risk_score'].max(), df['total_risk_score'].min()
        df['normalized_risk_score'] = (df['total_risk_score'] - min_score) / (max_score - min_score)
        logger.info("Risk scores calculated and normalized")
        df.drop(columns=['medical_history', 'disease1', 'disease2', 'total_risk_score'], inplace=True)
        return df

    def build_preprocessor(self):
        """Construct the preprocessing pipeline for numerical and categorical features."""
        # Identify numerical and categorical columns
        numerical_columns = self.train_df.select_dtypes(exclude=['object']).columns.tolist()
        categorical_columns = self.train_df.select_dtypes(include=['object']).columns.tolist()

        # Define preprocessing transformers
        numerical_transformer = Pipeline(steps=[('scaler', StandardScaler())])
        categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', drop="first"))])

        # Combine transformers into a preprocessor
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_columns),
                ('cat', categorical_transformer, categorical_columns)
            ],
            remainder='passthrough'
        )
        logger.info("Preprocessing pipeline built")

    def fit_transform_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Fit the preprocessor and transform the datasets."""
        X_train_transformed = self.preprocessor.fit_transform(self.train_df)
        X_test_transformed = self.preprocessor.transform(self.test_df)
        logger.info("Transformations applied to the dataset")
        return X_train_transformed, X_test_transformed

    def save_object(self, file_path: Path, obj):
        """Save an object to a specified file path using joblib."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            joblib.dump(obj, file_path)
            logger.info(f"Object saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save object to {file_path}: {str(e)}")
            raise  # Raise the exception after logging

    def save_preprocessor(self):
        """Save the preprocessor to a joblib file."""
        preprocessor_path = self.config.output_path / 'preprocessor.joblib'
        self.save_object(preprocessor_path, self.preprocessor)

    def feature_engineering(self) -> Tuple[np.ndarray, np.ndarray]:
        """Execute the feature engineering pipeline: load data, process, transform, and save."""
        try:
            # Load and preprocess medical history data
            self.train_df, self.test_df = self.load_data()

            # Preprocess medical history
            self.train_df = self.preprocess_medical_history(self.train_df)
            self.test_df = self.preprocess_medical_history(self.test_df)

            # Build the preprocessor
            self.build_preprocessor()

            # Fit and transform data
            train_data, test_data = self.fit_transform_data()

            # Save transformed data
            pd.DataFrame(train_data).to_csv(self.config.output_path / 'X_train.csv', index=False)
            pd.DataFrame(test_data).to_csv(self.config.output_path / 'X_test.csv', index=False)

            # Save the preprocessor
            self.save_preprocessor()

            logger.info("Transformed data saved successfully.")
            return train_data, test_data
        except Exception as e:
            logger.error(f"Error during feature engineering: {str(e)}")
            raise  # Maintain the original error handling for external catch
