import os
from datetime import datetime
from network_security.constant import *

class TrainingPipelineConfig:
    def __init__(self):
        self.timestamp: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = PIPELINE_NAME
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, self.timestamp)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, "network_data.csv"
        )
        self.train_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, "train.csv"
        )
        self.test_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, "test.csv"
        )
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, "train.csv")
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, "test.csv")
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, "train.csv")
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, "test.csv")
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            DATA_VALIDATION_DRIFT_REPORT_DIR,
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path: str = os.path.join(
            self.data_transformation_dir, 
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            "train.npy"
        )
        self.transformed_test_file_path: str = os.path.join(
            self.data_transformation_dir, 
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            "test.npy"
        )
        self.transformed_object_file_path: str = os.path.join(
            self.data_transformation_dir, 
            DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            PREPROCESSING_OBJECT_FILE_NAME
        )

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir,
            MODEL_TRAINER_TRAINED_MODEL_DIR,
            MODEL_TRAINER_TRAINED_MODEL_NAME
        )
        self.expected_score: float = MODEL_TRAINER_EXPECTED_SCORE
        self.over_fitting_threshold: float = MODEL_TRAINER_OVER_FITTING_THRESHOLD