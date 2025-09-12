import pandas as pd
import os
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config): # this config is from yaml file
        self.random_seed = config.get('random_seed', 42)
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucklet_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']
        
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and file {self.file_name}")

    def download_csv_from_gcp(self):
        """this function downloads the csv file from gcp bucket and saves it in raw data directory"""
        try:
            logger.info("Started downloading csv file from gcp bucket")
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Data csv file is downloaded from gcp bucket to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error("Error occurred while downloading file from gcp bucket")
            raise CustomException("Failed to read the csv file from GCP", e)
        
    def split_data(self):
        """this function splits the data into train and test data"""
        try:
            logger.info("Data Splitting started")
            data = pd.read_csv(RAW_FILE_PATH)
            # splitting the data
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=self.random_seed)

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train and Test data are saved at {TRAIN_FILE_PATH} and {TEST_FILE_PATH}")
        except Exception as e:
            logger.error("Error occurred while splitting the data")
            raise CustomException("Failed to split the data into train and test sets", e)
        
    def run(self):
        """this function runs the data ingestion"""
        try:
            logger.info("Running Data Ingestion process")
            self.download_csv_from_gcp()
            self.split_data()
            logger.info("Data Ingestion process is completed")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        finally:
            logger.info("Data Ingestion process ended")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
