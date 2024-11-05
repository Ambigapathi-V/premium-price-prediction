from src.Premium_Price_Prediction.config.configuration import ConfigurationManager
from src.Premium_Price_Prediction.components.data_preprocessing import DataPreprocessing
from src.Premium_Price_Prediction import logger

STAGE_NAME = "Data Preprocessing Stage"

class DataPreprocessingTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_data_preprocessing(self):
        config = ConfigurationManager()
        data_preprocessing_config = config.get_data_preprocessing_config()
        data_preprocessing = DataPreprocessing(data_preprocessing_config)
        data_preprocessing.load_data()  
        data_preprocessing.preprocess()  
        data_preprocessing.apply_iqr_treatment()  
        data_preprocessing.save_data() 
if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>> Starting {STAGE_NAME} <<<<<<<<<<<<")
        pipeline = DataPreprocessingTrainingPipeline()
        pipeline.initiate_data_preprocessing()
        logger.info(f"{STAGE_NAME} completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e
