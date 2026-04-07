import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# weather model artifacts and data paths
WEATHER_MODEL_DIR = os.path.join(BASE_DIR, "models", "weather","v0")
WEATHER_DATA_PATH = os.path.join(BASE_DIR, "data", "feature_store","reg_ts_categorised_weather_data_with_features.csv")

# traffic model artifacts path
TRAFFIC_MODEL_DIR = os.path.join(BASE_DIR, "models", "traffic","v0")
TRAFFIC_DATA_PATH = os.path.join(BASE_DIR, "data", "feature_store","traffic_data_with_features.csv")    

# BN model artifacts path
BN_MODEL_DIR = os.path.join(BASE_DIR, "models","causal_rsng_brain","bn","v0")

# svm policy model artifacts path
SVM_MODEL_DIR = os.path.join(BASE_DIR, "models", "policy_enforcer","v0","svm")

# api url
WEATHER_API_URL = "http://localhost:80"   # adjust as needed
TRAFFIC_API_URL = "http://localhost:81"   # adjust as needed
