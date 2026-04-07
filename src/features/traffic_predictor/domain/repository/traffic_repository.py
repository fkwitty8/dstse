from abc import ABC, abstractmethod
from datetime import datetime
from ..entities.traffic_entity import TrafficPrediction

class ITrafficRepository(ABC):
    @abstractmethod
    def get_prediction(self, dt: datetime, road: str) -> TrafficPrediction:
        pass