
import pandas as pd

from ..repository.traffic_repository import ITrafficRepository

class PredictTrafficUseCase:
    def __init__(self, repository: ITrafficRepository):
        self.repository = repository

    def execute(self, dt_value: str, road: str):
        # Validation and conversion
        dt = pd.to_datetime(dt_value)
        
        print(f"Executing use case with datetime: {dt} and road: {road}")
        return self.repository.get_prediction(dt, road)