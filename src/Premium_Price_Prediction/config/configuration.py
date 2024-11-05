from src.Premium_Price_Prediction.constants import *
from src.Premium_Price_Prediction.utils.common import read_yaml, create_directories
from src.Premium_Price_Prediction.entity.config_entity import (DataIngestionconfig, DataPreprocessingconfig,FeatureEngineeringConfig,ModelEvaluationConfig)

class ConfigurationManager:
    def __init__(self, 
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionconfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionconfig(
            root_dir=config.root_dir,
            input_path=config.input_path,
            output_path=config.output_path,
            raw_data_path=config.raw_data_path,
            train_data_path=config.train_data_path,
            test_data_path=config.test_data_path,  # Fixed colon to equal sign
            
        )
        return data_ingestion_config

    def __init__(self, 
                    config_filepath = CONFIG_FILE_PATH,
                    params_filepath = PARAMS_FILE_PATH,
                    schema_filepath = SCHEMA_FILE_PATH):
            self.config = read_yaml(config_filepath)
            self.params = read_yaml(params_filepath)
            self.schema = read_yaml(schema_filepath)
            
            create_directories([self.config.artifacts_root])
            
    def get_data_preprocessing_config(self)->DataPreprocessingconfig:
            config = self.config.data_preprocessing
            create_directories([config.root_dir])
            
            data_preprocessing_config = DataPreprocessingconfig(
                root_dir = config.root_dir,
                input_path = config.input_path,
                output_path = config.output_path,
                preprocess_column = config.preprocess_column,
                X_train_filepath = config.X_train_filepath,
                X_test_filepath = config.X_test_filepath,
                y_train_filepath = config.y_train_filepath,
                y_test_filepath = config.y_test_filepath,
                raw_filepath = config.raw_filepath,
                
            )
            return data_preprocessing_config
            
    def __init__(self, 
                 config_filepath=CONFIG_FILE_PATH, 
                 params_filepath=PARAMS_FILE_PATH, 
                 schema_filepath=SCHEMA_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
    
    def get_feature_engineering_config(self) -> FeatureEngineeringConfig:
        config = self.config.feature_engineering
        create_directories([config.root_dir])

        
        feature_engineering_config = FeatureEngineeringConfig(
            root_dir=Path(config["root_dir"]),
            input_path=Path(config["input_path"]),
            output_path=Path(config["output_path"]),
            model_path=Path(config["model_path"]),
            test_filepath=Path(config["test_filepath"]),
            train_filepath=Path(config["train_filepath"]),
            target_column = config["target_column"]
        )
        return feature_engineering_config
    def __init__(self, 
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
        
    def get_model_evaluation(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        create_directories([config.root_dir])
        
        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            X_train_filepath = config.X_train_filepath,
            X_test_filepath = config.X_test_filepath,
            y_train_filepath = config.y_train_filepath,
            y_test_filepath = config.y_test_filepath,
            model_path=config.model_path,
            target_column = config.target_column
        )
        return model_evaluation_config
