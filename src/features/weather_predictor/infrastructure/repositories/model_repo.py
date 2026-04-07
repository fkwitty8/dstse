import os
import pickle
import json
import joblib

from ...domain.repository import WeatherModelRepository

class FileBasedWeatherModelRepository(WeatherModelRepository):
    def __init__(self, model_dir: str):
        self.model_dir = model_dir

    def load_regressor(self):
        print(f"Looking for regressor in {self.model_dir}... in FILE BASED REPO")
        return joblib.load(os.path.join(self.model_dir, "rf_regressor.pkl"))

    def load_scaler(self):
        print(f"Looking for scaler in {self.model_dir}... in FILE BASED REPO")
        return joblib.load(os.path.join(self.model_dir, "scaler.pkl"))

    def load_feature_columns(self):
        print(f"Looking for feature columns in {self.model_dir}... in FILE BASED REPO")
        with open(os.path.join(self.model_dir, "feature_columns.json"), 'r') as f:
            return json.load(f)

    def load_thresholds(self):
        print(f"Looking for rainfall thresholds in {self.model_dir}... in FILE BASED REPO")
        with open(os.path.join(self.model_dir, "rainfall_thresholds.pkl"), 'rb') as f:
            return pickle.load(f)