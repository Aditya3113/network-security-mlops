import os

PIPELINE_NAME: str = "network_security"
ARTIFACT_DIR: str = "artifacts"

#Ingestion
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

#Database
DATABASE_NAME: str = "NetworkData"
COLLECTION_NAME: str = "NetworkStore"