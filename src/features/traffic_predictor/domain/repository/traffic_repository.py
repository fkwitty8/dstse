from abc import ABC, abstractmethod
from datetime import datetime

# local host mode
# from ..entities.traffic_entity import TrafficPrediction

from features.traffic_predictor.domain.entities.traffic_entity import TrafficPrediction

class ITrafficRepository(ABC):
    @abstractmethod
    def get_prediction(self, dt: datetime, road: str) -> TrafficPrediction:
        pass