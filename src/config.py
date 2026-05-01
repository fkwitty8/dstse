import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# weather model artifacts and data paths
WEATHER_MODEL_DIR = os.path.join(BASE_DIR, "models", "weather", "v0")
WEATHER_DATA_PATH = os.path.join(BASE_DIR, "data", "feature_store","reg_ts_categorised_weather_data_with_features.csv")

# traffic model artifacts path
TRAFFIC_MODEL_DIR = os.path.join(BASE_DIR, "models", "traffic")
TRAFFIC_DATA_PATH = os.path.join(BASE_DIR, "data", "feature_store","traffic_data_with_features.csv")    

# BN model artifacts path
BN_MODEL_DIR = os.path.join(BASE_DIR, "models","causual_rsng_brain","bn","v0")

# svm policy model artifacts path
SVM_MODEL_DIR = os.path.join(BASE_DIR, "models", "policy_enforcer","svm","v0")

# api url
# WEATHER_API_URL = "http://localhost:80"   
# TRAFFIC_API_URL = "http://localhost:81"  

WEATHER_API_URL = os.getenv("WEATHER_API_URL", "http://localhost:80")
TRAFFIC_API_URL = os.getenv("TRAFFIC_API_URL", "http://localhost:81")


print(f"WEATHER_MODEL_DIR = {WEATHER_MODEL_DIR}")
print(f"WEATHER_DATA_PATH = {WEATHER_DATA_PATH}")
print(f"TRAFFIC_MODEL_DIR = {TRAFFIC_MODEL_DIR}")
print(f"TRAFFIC_DATA_PATH = {TRAFFIC_DATA_PATH}")
print(f"BN_MODEL_DIR = {BN_MODEL_DIR}")
print(f"SVM_MODEL_DIR = {SVM_MODEL_DIR}")