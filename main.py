import sys
import os
from dotenv import load_dotenv

load_dotenv()

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.entity.config_entity import (
    DataIngestionConfig, 
    DataValidationConfig, 
    DataTransformationConfig, 
    ModelTrainerConfig,
    TrainingPipelineConfig
)
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

        logger.info("Starting Data Validation Phase...")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("Data Validation Completed Successfully!")

        logger.info("Starting Data Transformation Phase...")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info("Data Transformation Completed Successfully!")

        logger.info("Starting Model Training Phase...")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logger.info("Model Training Completed Successfully!")
        print(model_trainer_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)