from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherObservation:
    datetime: datetime
    dry_bulb: float
    wet_bulb: float
    humidity: float
    wind_speed: float
    total_rainfall: float

@dataclass
class WeatherPrediction:
    datetime: datetime
    bn_category: str          # 'Good', 'Moderate', 'Bad'
    confidence: float
    rainfall_mm: float