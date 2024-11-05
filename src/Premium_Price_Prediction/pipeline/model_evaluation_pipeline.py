from src.Premium_Price_Prediction.config.configuration import ConfigurationManager
from src.Premium_Price_Prediction.components.model_evaluation import ModelEvaluation
from src.Premium_Price_Prediction import logger

STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_model_evaluation(self):
        config = ConfigurationManager()
        model_evalution_config = config.get_model_evaluation()

        model_evaluation = ModelEvaluation(model_evalution_config)
        model_evaluation.evaluate_model()
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>> Starting {STAGE_NAME} <<<<<<<<<<<<")
        pipeline = ModelEvaluationTrainingPipeline()
        pipeline.initiate_model_evaluation()
        logger.info(f"{STAGE_NAME} completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred during {STAGE_NAME}: {str(e)}")
        raise e
