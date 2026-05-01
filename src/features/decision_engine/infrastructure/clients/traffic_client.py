import requests

import requests
from typing import Dict
from datetime import datetime

class TrafficAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def predict(self, datetime_obj: datetime, road_name: str) -> Dict[str, any]:
        # if the traffic API expects a JSON with datetime and road
        payload = {
            "datetime": datetime_obj.strftime("%Y-%m-%d %H:%M:%S"),
            "road": road_name
        }
        print("predicting weather with payload:", payload)
        print("weather_predicting_url2:", self.base_url)
        
        response = requests.post(f"{self.base_url}/predict_traffic", json=payload)
        print("weather response:", response)
        response.raise_for_status()
        return response.json()
