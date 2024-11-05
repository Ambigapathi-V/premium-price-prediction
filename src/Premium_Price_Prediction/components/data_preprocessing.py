import os
import pandas as pd
from src.Premium_Price_Prediction import logger
from sklearn.model_selection import train_test_split
from src.Premium_Price_Prediction.entity.config_entity import DataPreprocessingconfig


class DataPreprocessing:
    def __init__(self, config: DataPreprocessingconfig):
        # Initialize configuration attributes
        self.input_path: str = config.input_path
        self.output_path: str = config.output_path
        self.preprocess_column: str = config.preprocess_column
        self.X_train_filepath: str = config.X_train_filepath
        self.X_test_filepath: str = config.X_test_filepath
        self.y_train_filepath: str = config.y_train_filepath
        self.y_test_filepath: str = config.y_test_filepath
        self.raw_filepath: str = config.raw_filepath
        self.df: pd.DataFrame = None  # DataFrame to hold combined data

    def load_data(self) -> None:
        """Load data from a CSV file."""
        try:
            self.df = pd.read_csv(self.raw_filepath)
            logger.info(f"Loaded data from {self.raw_filepath} with shape {self.df.shape}")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise e

    def preprocess(self) -> pd.DataFrame:
        """Preprocess the data by handling missing values and duplicates."""
        try:
            if self.df is None:
                self.load_data()

            self.handle_missing_values()
            self.standardize_column_names()
            self.remove_duplicates()

            return self.df

        except Exception as e:
            logger.error(f"Error during preprocessing: {str(e)}")
            raise e

    def handle_missing_values(self) -> None:
        """Handle missing values in the DataFrame."""
        missing_values = self.df.isna().sum().sum()
        logger.info(f"Total missing values before dropping: {missing_values}")
        self.df.dropna(inplace=True)
        logger.info(f"Dropped missing values; remaining rows: {self.df.shape[0]}")

    def standardize_column_names(self) -> None:
        """Standardize column names by replacing spaces with underscores and converting to lowercase."""
        self.df.columns = self.df.columns.str.replace(" ", "_").str.lower()
        logger.info("Standardized column names")

    def remove_duplicates(self) -> None:
        """Remove duplicate rows from the DataFrame."""
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df.drop_duplicates(inplace=True)
            logger.info(f"Dropped {duplicates} duplicate rows; remaining rows: {self.df.shape[0]}")
        else:
            logger.info("No duplicate rows found")
            
    def save_data(self) -> None:
        """Save the processed training and testing datasets to specified output paths."""
        try:
            os.makedirs(self.output_path, exist_ok=True)
            logger.info("Train-test split initiated")
            X = self.df.drop(columns=[self.preprocess_column])  # Create a new DataFrame without the target column
            y = self.df[self.preprocess_column]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            X_train.to_csv(self.X_train_filepath, index=False, header=True)
            X_test.to_csv(self.X_test_filepath, index=False, header=True)
            y_train.to_csv(self.y_train_filepath, index=False, header=True)
            y_test.to_csv(self.y_test_filepath, index=False, header=True)
            logger.info("Data saved to train and test files successfully")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise e
    def iqr_bounds(self, column_name: str) -> tuple:
        """Calculate the IQR bounds for a given column."""
        q1 = self.df[column_name].quantile(0.25)
        q3 = self.df[column_name].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return lower_bound, upper_bound

    def apply_iqr_treatment(self) -> pd.DataFrame:
        """Apply IQR treatment to the specified column in the DataFrame."""
        try:
            if self.df is None:
                self.load_data()

            # Log the DataFrame type before processing
            logger.info(f"Type of `self.df` before IQR treatment: {type(self.df)}")

            # Check if the preprocess_column exists
            if self.preprocess_column not in self.df.columns:
                logger.error(f"Column '{self.preprocess_column}' does not exist in the DataFrame.")
                raise KeyError(f"Column '{self.preprocess_column}' does not exist in the DataFrame.")

            lower, upper = self.iqr_bounds(self.preprocess_column)
            self.df[self.preprocess_column] = self.df[self.preprocess_column].clip(lower=lower, upper=upper)
            logger.info(f"IQR treatment applied on column '{self.preprocess_column}' with bounds {lower} and {upper}")

            # Check the DataFrame type again after clipping
            logger.info(f"Type of `self.df` after clipping: {type(self.df)}")

            self.remove_extreme_outliers()

            # Ensure `self.df` remains a DataFrame
            logger.info(f"Type of `self.df` after removing extreme outliers: {type(self.df)}")

            # Standardize 'smoking_status' values if present
            self.standardize_smoking_status()

            return self.df

        except KeyError as ke:
            logger.error(f"KeyError: {str(ke)}")
            raise
        except Exception as e:
            logger.error(f"Error during IQR treatment: {str(e)}")
            raise e

    def remove_extreme_outliers(self) -> None:
        """Remove extreme outliers based on the 99.9th percentile."""
        try:
            quantile_threshold = self.df[self.preprocess_column].quantile(0.999)
            extreme_outliers = self.df[self.df[self.preprocess_column] > quantile_threshold].shape[0]
            
            # Ensure we keep `self.df` as a DataFrame by filtering it correctly
            self.df = self.df[self.df[self.preprocess_column] <= quantile_threshold].copy()  # Use `.copy()` to avoid potential chaining issues
            logger.info(f"Removed {extreme_outliers} extreme outliers beyond 99.9th percentile for '{self.preprocess_column}'")
        except Exception as e:
            logger.error(f"Error removing extreme outliers: {str(e)}")
            raise e

    def standardize_smoking_status(self) -> None:
        """Standardize values in the 'smoking_status' column if it exists."""
        if 'smoking_status' in self.df.columns:
            self.df['smoking_status'] = self.df['smoking_status'].replace({
                'Not Smoking': 'No Smoking',
                'Does Not Smoke': 'No Smoking',
                'Smoking=0': 'No Smoking'
            })
            logger.info("Standardized values in 'smoking_status' column to unify non-smoking labels")
