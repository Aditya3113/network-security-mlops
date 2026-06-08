import sys
import os
from dotenv import load_dotenv

load_dotenv()

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig, TrainingPipelineConfig
from network_security.exception import NetworkSecurityException
from network_security.logging import logger

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
       
        logger.info("Starting Data Ingestion Phase...")
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logger.info("Data Ingestion Completed Successfully!")
        print(data_ingestion_artifact)

        logger.info("Starting Data Validation Phase...")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("Data Validation Completed Successfully!")
        print(data_validation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)