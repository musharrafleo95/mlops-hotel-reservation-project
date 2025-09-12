from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from config.path_config import *
from utils.common_functions import read_yaml
import os

import mlflow

# setting the environment variable for google application credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:/mlops/project_1/mlops-471718-d66733c85e06.json"
# setting the experiment name
mlflow.set_experiment("Hotel Booking Cancellation Prediction")
# tracking uri of file system defining using os path where mlflow related info will be stored
# mlflow.set_tracking_uri("file://" + os.path.abspath("mlruns"))



if __name__ == "__main__":
    ### 1. Data ingestion
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    ### 2. Data processing
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process()

    ### 3. Model training
    model_trainer = ModelTraining(
        train_path=PROCESSED_TRAIN_DATA_PATH,
        test_path=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    model_trainer.run()