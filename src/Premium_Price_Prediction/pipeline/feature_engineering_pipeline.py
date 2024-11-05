from src.Premium_Price_Prediction.config.configuration import ConfigurationManager
from src.Premium_Price_Prediction.components.feature_engineering import FeatureEngineering
from src.Premium_Price_Prediction import logger

STAGE_NAME = "Data Feature Engineering Stage"

class FeatureEngineeringTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_feature_engineering(self):
        config = ConfigurationManager()
        feature_engineering_config = config.get_feature_engineering_config()  # Corrected variable name
        feature_engineering = FeatureEngineering(feature_engineering_config)
        feature_engineering.feature_engineering()
 
if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>> Starting {STAGE_NAME} <<<<<<<<<<<<")
        pipeline = FeatureEngineeringTrainingPipeline()
        pipeline.initiate_feature_engineering()
        logger.info(f"{STAGE_NAME} completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e
