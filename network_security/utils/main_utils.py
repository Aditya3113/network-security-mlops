import os
import sys
import yaml
import numpy as np
import pickle
from network_security.exception import NetworkSecurityException
from network_security.logging import logger
from sklearn.metrics import f1_score

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves a numpy array to a file.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_object(file_path: str, obj: object) -> None:
    """
    Serializes and saves a Python object (like a Scikit-Learn pipeline) using pickle.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Loads a numpy array from a file.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models: dict) -> dict:
    """
    Trains multiple models and returns a report of their F1 scores.
    """
    try:
        report = {}
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            model.fit(X_train, y_train)
            
            y_test_pred = model.predict(X_test)
            
            test_model_score = f1_score(y_test, y_test_pred)
            report[model_name] = test_model_score
            
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys)