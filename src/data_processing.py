import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import load_data, read_yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)


class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        self.random_seed = self.config.get('random_seed', 42)

        os.makedirs(self.processed_dir, exist_ok=True)

        logger.info("DataProcessor initialized")

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing")

            logger.info("Dropping columns")
            df.drop(columns=self.config['data_processing']['drop_columns'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Applying label encoding to categorical columns")

            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {class_label: int_label for class_label, int_label in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))}

            logger.info("Label Mappings are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Doing skewness correction on numerical columns")

            skewness_threshold = self.config['data_processing'].get('skewness_threshold', 5)
            skewness = df[num_cols].apply(lambda x: x.skew()).abs()

            for col in skewness[skewness > skewness_threshold].index:
                df[col] = np.log1p(df[col])

            return df
        except Exception as e:
            logger.error("Error in preprocessing data")
            raise CustomException("Error in preprocessing data", e)
        
    def balance_data(self, df):
        try:
            logger.info("Handling imbalanced data using SMOTE")
            X = df.drop(columns=[self.config['data_processing']['target_column']])
            y = df[self.config['data_processing']['target_column']]

            smote = SMOTE(random_state=self.random_seed)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df[self.config['data_processing']['target_column']] = y_resampled

            logger.info("Data balancing completed")
            return balanced_df
        except Exception as e:
            logger.error("Error in balancing data")
            raise CustomException("Error in balancing data", e)
        
    def select_features(self, df):
        try:
            logger.info("Starting feature selection step")
            X = df.drop(columns=[self.config['data_processing']['target_column']])
            y = df[self.config['data_processing']['target_column']]

            model = RandomForestClassifier(random_state=self.random_seed)
            model.fit(X, y)
            feature_importances = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': feature_importances
            }).sort_values(by='Importance', ascending=False)

            num_features_to_select = self.config['data_processing'].get('no_of_features', 10)

            selected_features = feature_importance_df['Feature'].head(num_features_to_select).tolist()

            logger.info(f"Selected top {num_features_to_select} features: {selected_features}")

            top_features_df = df[selected_features + [self.config['data_processing']['target_column']]]

            logger.info(f"features selection completed successfully")

            return top_features_df

        except Exception as e:
            logger.error("Error in feature selection")
            raise CustomException("Error in feature selection", e)

    def save_data(self, df, filepath):
        try:
            logger.info(f"saving data in processed folder")
            df.to_csv(filepath, index=False)

            logger.info(f"Data saved successfully at {filepath}")
        except Exception as e:
            logger.error("Error in saving data")
            raise CustomException("Error in saving data", e)
        
    def process(self):
        try:
            logger.info("Loading data from raw directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing completed successfully")
        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        finally:
            logger.info("Data processing process ended")

if __name__ == "__main__":
    processor = DataProcessor(
        train_path=TRAIN_FILE_PATH,
        test_path=TEST_FILE_PATH,
        processed_dir=PROCESSED_DIR,
        config_path=CONFIG_PATH
    )
    processor.process()
