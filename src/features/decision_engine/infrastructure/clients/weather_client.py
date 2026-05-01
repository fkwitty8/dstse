import requests
from typing import Dict
from datetime import datetime

class WeatherAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def predict(self, datetime_obj: datetime, dry_bulb: float, wet_bulb: float,
                humidity: float, wind_speed: float) -> Dict[str, any]:
        payload = {
            "datetime": datetime_obj.strftime("%Y-%m-%d %H:%M:%S"),
            "dry_bulb": dry_bulb,
            "wet_bulb": wet_bulb,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
        print("predicting weather with payload:", payload)
        print("weather_predicting_url2:", self.base_url)
        response = requests.post(f"{self.base_url}/predict_weather", json=payload)
        print("weather response:", response)
        response.raise_for_status()
        return response.json()