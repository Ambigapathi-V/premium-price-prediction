import os
import  urllib.request as request
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.Premium_Price_Prediction import logger  # Ensure the logger is correctly imported
from src.Premium_Price_Prediction.entity.config_entity import DataIngestionconfig  # Update the import statement

class DataIngestion:
    def __init__(self, config: DataIngestionconfig):
        self.input_path = config.input_path
        self.output_path = config.output_path  # Output path where files will be saved
        self.raw_data_path = config.raw_data_path  # Path for raw data
        self.train_data_path = config.train_data_path  # Path for training data
        self.test_data_path = config.test_data_path  # Path for testing data
        
    def load_data(self):
        """Loads data from an Excel file."""
        try:
            df = pd.read_excel(self.input_path)
            logger.info("Data loaded successfully.")
            return df  # Return the loaded DataFrame for further use
        except Exception as e:
            logger.error(f"Error occurred while loading data: {str(e)}")
            raise e
    
    def save_data(self) -> None:
        """Loads data and saves it in data ingestion artifacts.
        
        Raises:
            Exception: For any errors encountered while saving the data.
        """
        try:
            df = self.load_data()  # Load data
            
            # Ensure directory exists for output
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)  
            
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)  
            # Save the raw data
            df.to_csv(self.raw_data_path, index=False)
            logger.info(f"Raw data saved successfully in {self.raw_data_path}")

            # Train-test split
            logger.info("Train-test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            # Save train and test datasets
            os.makedirs(os.path.dirname(self.train_data_path), exist_ok=True)
            train_set.to_csv(self.train_data_path, index=False, header=True)

            os.makedirs(os.path.dirname(self.test_data_path), exist_ok=True)
            test_set.to_csv(self.test_data_path, index=False, header=True)

            logger.info("Ingestion of the data is completed")
            
        except Exception as e:
            logger.error(f"Error occurred while saving data: {str(e)}")
            raise e
