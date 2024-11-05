from src.Premium_Price_Prediction.config.configuration import ConfigurationManager
from src.Premium_Price_Prediction.components.data_ingestion import DataIngestion
from src.Premium_Price_Prediction import logger

class DataIngestionTrainingPipeline:
    def __init__(self, stage_name: str = "Data Ingestion Stage"):
        self.stage_name = stage_name
    
    def initiate_data_ingestion(self):
        """Initiates the data ingestion process."""
        try:
            config = ConfigurationManager() 
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.load_data()
            data_ingestion.save_data()
        
        except Exception as e:
            logger.error(f"Error during data ingestion initiation: {str(e)}")
            raise e

if __name__ == "__main__":
    try:
        pipeline = DataIngestionTrainingPipeline()
        logger.info(f">>>>>>>>>>>Starting {pipeline.stage_name}<<<<<<<<<<<<<")
        pipeline.initiate_data_ingestion()
        logger.info(f"{pipeline.stage_name} completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred during {pipeline.stage_name}: {str(e)}")
        raise e
