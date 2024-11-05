from src.Premium_Price_Prediction import logger
from src.Premium_Price_Prediction.pipeline.data_ingestion_pipeline import (DataIngestionTrainingPipeline)
from src.Premium_Price_Prediction.pipeline.data_preprocessing_pipeline import (DataPreprocessingTrainingPipeline)
from src.Premium_Price_Prediction.pipeline.feature_engineering_pipeline import (FeatureEngineeringTrainingPipeline)
from src.Premium_Price_Prediction.pipeline.model_evaluation_pipeline import (ModelEvaluationTrainingPipeline)
STAGE_NAME = "Data Ingestion Stage"


try:
        logger.info(f">>>>>>>>>>>Starting {STAGE_NAME}<<<<<<<<<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.initiate_data_ingestion()
        logger.info(f">>>>>>>>>{STAGE_NAME} completed successfully.<<<<<<<<<<<<<<<")
except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e

STAGE_NAME = "Data Pre-processing Stage"

try:
        logger.info(f">>>>>>>>>>> Starting {STAGE_NAME} <<<<<<<<<<<<")
        pipeline = DataPreprocessingTrainingPipeline()
        pipeline.initiate_data_preprocessing()
        logger.info(f">>>>>>>>>{STAGE_NAME} completed successfully.<<<<<<<<<<<<<<<")
except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e


STAGE_NAME = "Data Feature Engineering Stage"

try:
        logger.info(f">>>>>>>>>>> Starting {STAGE_NAME} <<<<<<<<<<<<")
        pipeline = FeatureEngineeringTrainingPipeline()
        pipeline.initiate_feature_engineering()
        logger.info(f">>>>>>>>>{STAGE_NAME} completed successfully.<<<<<<<<<<<<<<<")
except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e

STAGE_NAME = "Model Evaluation  Stage"

try:
        logger.info(f">>>>>>>>>>> Starting {STAGE_NAME} <<<<<<<<<<<<")
        pipeline = ModelEvaluationTrainingPipeline()
        pipeline.initiate_model_evaluation()
        logger.info(f">>>>>>>>>{STAGE_NAME} completed successfully.<<<<<<<<<<<<<<<")
except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e