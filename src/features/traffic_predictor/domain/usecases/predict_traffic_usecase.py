
import pandas as pd

# local host mode
# from ..repository.traffic_repository import ITrafficRepository

# for docker environment
from features.traffic_predictor.domain.repository.traffic_repository import ITrafficRepository

class PredictTrafficUseCase:
    def __init__(self, repository: ITrafficRepository):
        self.repository = repository

    def execute(self, dt_value: str, road: str):
        # Validation and conversion
        dt = pd.to_datetime(dt_value)
        
        return self.repository.get_prediction(dt, road)