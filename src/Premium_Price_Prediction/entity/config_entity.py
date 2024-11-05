from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

@dataclass
class DataIngestionconfig:
    root_dir : Path
    input_path: Path
    output_path : Path
    raw_data_path: Path
    test_data_path : Path
    train_data_path : Path

@dataclass
class DataPreprocessingconfig:
    root_dir: Path
    input_path: Path
    output_path: Path
    X_test_filepath: Path
    X_train_filepath: Path
    y_test_filepath: Path
    y_train_filepath: Path
    raw_filepath: Path
    preprocess_column: str

    
@dataclass
class FeatureEngineeringConfig:
    root_dir: Path
    input_path: Path
    output_path: Path
    model_path: Path
    test_filepath : Path
    train_filepath : Path
    target_column : str# The target column name for prediction
    
    
@dataclass
class ModelEvaluationConfig:
    root_dir : Path
    X_test_filepath: Path
    X_train_filepath: Path
    y_test_filepath: Path
    y_train_filepath: Path
    model_path : Path
    target_column : Path
