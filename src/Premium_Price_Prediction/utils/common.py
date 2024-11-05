import os
import yaml
from src.Premium_Price_Prediction import logger
import json
import pandas as pd
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a yaml file and returns a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the yaml file.
    
    Raises:
        ValueError: if yaml file is empty or malformed
    
    Returns:
        ConfigBox: A ConfigBox object containing the parsed data.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file : {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty or malformed")
    except Exception as e:
        logger.error(f"Error occurred while reading YAML file : {path_to_yaml}")
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories in the given path if they don't exist.
    
    Args:
        path_to_directories (list): A list of directories to be created.
        verbose (bool): A flag to indicate whether to print info messages.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory {path} created successfully.")

@ensure_annotations
def save_json(path: Path, data ):
    """
    Saves a dictionary to a JSON file.
    
    Args:
        path (Path): The path where the JSON file should be saved.
        data (dict): The dictionary to be saved.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved successfully at {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file and returns a ConfigBox object.
    
    Args:
        path (Path): The path to the JSON file.
    
    Returns:
        ConfigBox: A ConfigBox object containing the parsed data.
    """
    with open(path) as f:
        content = json.load(f)
        
    logger.info(f"JSON file successfully loaded from {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves a Python object to a binary file.
    
    Args:
        data (Any): The Python object to be saved.
        path (Path): The path where the binary file should be saved.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved successfully at {path}")
    
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            joblib.dump(obj, file_obj)

    except Exception as e:
        logger.error(f"Error occurred while saving object to {file_path}")
        raise e 

def load_df(file_path : Path) -> pd.DataFrame:
    try:
        df= pd.read_csv(file_path)
        logger.info(f"Dataframe loaded successfully from {file_path}")
        return df 
    except Exception as e:
        logger.error(f"Error occurred while loading dataframe from {file_path}")
        raise e 
  