from dataclasses import dataclass
from enum import Enum

class TrafficCategory(Enum):
    LOW = "Low"
    NORMAL = "Normal"
    VERY_HIGH = "Very High"

@dataclass
class TrafficPrediction:
    congestion: TrafficCategory
    confidence: float