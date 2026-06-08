import os
import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score

from network_security.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.utils.main_utils import save_object, load_numpy_array_data, evaluate_models

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_model_object_and_report(self, train_array, test_array):
        try:
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(),
                "Logistic Regression": LogisticRegression(),
                "AdaBoost": AdaBoostClassifier(),
            }

            logger.info("Evaluating multiple models to find the best performer...")
            model_report: dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            logger.info(f"Best Model found: {best_model_name} with F1 Score: {best_model_score}")

            if best_model_score < self.model_trainer_config.expected_score:
                raise Exception("No best model found with a score higher than the expected baseline.")

            y_train_pred = best_model.predict(X_train)
            classification_train_metric = ClassificationMetricArtifact(
                f1_score=f1_score(y_train, y_train_pred),
                precision_score=precision_score(y_train, y_train_pred),
                recall_score=recall_score(y_train, y_train_pred)
            )

            y_test_pred = best_model.predict(X_test)
            classification_test_metric = ClassificationMetricArtifact(
                f1_score=f1_score(y_test, y_test_pred),
                precision_score=precision_score(y_test, y_test_pred),
                recall_score=recall_score(y_test, y_test_pred)
            )

            logger.info(f"Saving the best model: {best_model_name}")
            save_object(self.model_trainer_config.trained_model_file_path, obj=best_model)

            return best_model_name, classification_train_metric, classification_test_metric

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            best_model_name, metric_train, metric_test = self.get_model_object_and_report(
                train_array=train_arr, test_array=test_arr
            )

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=metric_train,
                test_metric_artifact=metric_test
            )

            logger.info(f"Model Trainer Artifact created: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)