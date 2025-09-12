import os

############################## DATA INGESTION ######################
# set GOOGLE_APPLICATION_CREDTIALS=E:\mlops\project_1\mlops-471718-d66733c85e06.json

RAW_DIR  = "artifacts/raw" # directory to save raw data
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv") # path to save raw data
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv") # path to save train data
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv") # path to save test data

CONFIG_PATH = "config/config.yaml" # path to config file because the bucket info is there


############################## Data Processing ######################
PROCESSED_DIR = "artifacts/processed" # directory to save processed data
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv") # path to save processed train data
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv") # path to save processed test data

############################### Model Training ######################
MODEL_OUTPUT_PATH = "artifacts/model/lgbm_model.pkl" # directory to save model