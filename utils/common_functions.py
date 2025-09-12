# contains functions that are used in different files

import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

# function to read yaml file
def read_yaml(file_path: str) -> dict:
    """reads a yaml file and returns the content as a dictionary"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file is not found in the path: {file_path}")
        
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {file_path} loaded successfully")
            return config
    except Exception as e:
        logger.error(f"Error occurred while reading the YAML file: {file_path}")
        raise CustomException(f"Failed to read YAML file", e)

# function to load data from a csv file 
def load_data(file_path: str) -> pd.DataFrame:
    """loads data from a csv file and returns a pandas DataFrame"""
    try:
        logger.info(f"Loading data from file: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file is not found in the path: {file_path}")
        
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error occurred while loading data from the file: {file_path}")
        raise CustomException(f"Failed to load data from {file_path}", e)