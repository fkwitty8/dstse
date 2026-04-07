from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class Lecture:
    datetime: datetime
    road_name: str
    dry_bulb: float
    wet_bulb: float
    humidity: float
    wind_speed: float
    importance: str
    
@dataclass
class WeatherPrediction:
    category: str   # 'Good', 'Moderate', 'Bad'
    confidence: float
    rainfall_mm: float

@dataclass
class TrafficPrediction:
    category: str   # 'Low', 'Normal', 'Heavy'
    confidence: float

@dataclass
class LectureDecision:
    decision: str   # 'Scheduled', 'Online', 'Rescheduled', 'Cancelled'
    probabilities: Dict[str, float]   # probability distribution over decisions
    delay_probs: Dict[str, float]     # probability distribution over Delay states
    explanation: str