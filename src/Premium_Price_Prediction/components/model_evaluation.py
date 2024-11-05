import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from typing import Dict
from src.Premium_Price_Prediction import logger
from joblib import dump
import os
from src.Premium_Price_Prediction.config.configuration import ModelEvaluationConfig

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.X_train_filepath = config.X_train_filepath
        self.X_test_filepath = config.X_test_filepath
        self.y_train_filepath = config.y_train_filepath
        self.y_test_filepath = config.y_test_filepath
        self.target_column = config.target_column
        self.model_path = config.model_path
        
        logger.info("ModelEvaluation initialized with train filepath: %s, test filepath: %s", self.X_train_filepath, self.X_test_filepath)

    def evaluate_models(self, X_train, y_train, X_test, y_test, models):
        """Evaluate multiple regression models and return their R2 scores."""
        try:
            report = {}
            logger.info("Starting model evaluation for %d models.", len(models))

            for model_name, model in models.items():
                logger.info("Evaluating model: %s", model_name)

                # Fit the model on training data
                model.fit(X_train, y_train)

                # Predict on training and testing data
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                # Calculate R2 scores
                train_model_score = r2_score(y_train, y_train_pred)
                test_model_score = r2_score(y_test, y_test_pred)

                report[model_name] = test_model_score
                logger.info(f"{model_name} - Train R2: {train_model_score:.4f}, Test R2: {test_model_score:.4f}")

            logger.info("Model evaluation completed.")
            return report

        except Exception as e:
            logger.error(f"Model Evaluation Error: {str(e)}")
            raise

    def evaluate_model(self):
        """Load data, train models, and evaluate their performance."""
        try:
            logger.info("Loading training and testing data.")
            # Load train and test data
            X_train = pd.read_csv(self.X_train_filepath)
            y_train = pd.read_csv(self.y_train_filepath)
            X_test = pd.read_csv(self.X_test_filepath)
            y_test = pd.read_csv(self.y_test_filepath)

            logger.info("Data loaded successfully.")

            # Define models
            models = {
                "Linear Regression": LinearRegression(),
               
            }

            # Evaluate models and get model report
            model_report = self.evaluate_models(X_train, y_train, X_test, y_test, models)

            # Get the best model
            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise ValueError("No suitable model found with R2 score above 0.6")

            logger.info(f"Best model: {best_model_name} with R2 score: {best_model_score:.4f}")

            # Save the best model
            self.save_object(file_path=self.model_path, obj=best_model)

            # Final prediction and R2 score on test set
            predicted = best_model.predict(X_test)
            final_r2 = r2_score(y_test, predicted)
            logger.info(f"Final R2 score on test set: {final_r2:.4f}")
            return final_r2

        except Exception as e:
            logger.error(f"Error in model evaluation: {str(e)}")
            raise

    def save_object(self, file_path, obj):
        """Save the model object to the specified file path."""
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        dump(obj, file_path)
        logger.info(f"Model saved to {file_path}")
