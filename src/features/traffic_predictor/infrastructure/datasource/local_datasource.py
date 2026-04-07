import joblib
import json
import os

class LocalTrafficModelDataSource:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def load_metadata(self):
        with open(os.path.join(self.base_path, "clsf", "metadata.json"), 'r') as f:
            return json.load(f)

    def load_pickle(self, sub_path: str):
        return joblib.load(os.path.join(self.base_path, sub_path))