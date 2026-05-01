import pandas as pd

# local host mode
# from ...domain.repository import WeatherDataRepository

# for docker environment
from features.weather_predictor.domain.repository import WeatherDataRepository

class CsvWeatherDataRepository(WeatherDataRepository):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_observations(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
        
        df = pd.read_csv(self.filepath, parse_dates=['datetime'])
        df = df.set_index('datetime')
    
        mask = (df.index >= start) & (df.index < end)
        result = df.loc[mask].reset_index()
        
        return result