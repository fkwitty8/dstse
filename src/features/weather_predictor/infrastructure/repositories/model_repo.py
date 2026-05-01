import os
import pickle
import json
import joblib

# local host mode
# from ...domain.repository import WeatherModelRepository

# for docker environment
from features.weather_predictor.domain.repository import WeatherModelRepository

class FileBasedWeatherModelRepository(WeatherModelRepository):
    def __init__(self, model_dir: str):
        self.model_dir = model_dir

    def load_regressor(self):
        
        return joblib.load(os.path.join(self.model_dir, "rf_regressor.pkl"))

    def load_scaler(self):
        
        return joblib.load(os.path.join(self.model_dir, "scaler.pkl"))

    def load_feature_columns(self):
       
        with open(os.path.join(self.model_dir, "feature_columns.json"), 'r') as f:
            return json.load(f)

    def load_thresholds(self):
       
        with open(os.path.join(self.model_dir, "rainfall_thresholds.pkl"), 'rb') as f:
            return pickle.load(f)