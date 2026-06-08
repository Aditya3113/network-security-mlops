import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pymongo import MongoClient

from network_security.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.constant import DATABASE_NAME, COLLECTION_NAME

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise e

    def export_collection_to_dataframe(self) -> pd.DataFrame:
        """
        Reads raw dataset collections directly out of MongoDB Atlas
        """
        try:
            mongo_db_url = os.getenv("MONGO_DB_URL")
            if mongo_db_url is None:
                raise Exception("MONGO_DB_URL environment variable is not set.")
                
            client = MongoClient(mongo_db_url)
            collection = client[DATABASE_NAME][COLLECTION_NAME]
            
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)
                
            df.replace({"na": np.nan}, inplace=True)
            return df
            
        except Exception as e:
            raise e

    def split_data_as_train_test(self, df: pd.DataFrame) -> DataIngestionArtifact:
        """
        Performs a deterministic split and saves output CSV files
        """
        try:
            train_set, test_set = train_test_split(
                df, 
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            
            logger.info("Performed train test split on the dataframe.")
            
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            
            logger.info("Exported train and test file artifacts successfully.")
            
            return DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            
        except Exception as e:
            raise e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logger.info("Starting data ingestion process...")
            df = self.export_collection_to_dataframe()
            
            feature_store_path = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_path, exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False, header=True)
            
            data_ingestion_artifact = self.split_data_as_train_test(df)
            return data_ingestion_artifact
            
        except Exception as e:
            raise e