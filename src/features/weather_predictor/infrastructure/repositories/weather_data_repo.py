import pandas as pd
from ...domain.repository import WeatherDataRepository

class CsvWeatherDataRepository(WeatherDataRepository):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_observations(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
        print(f"getting observations from {start} to {end}")
        df = pd.read_csv(self.filepath, parse_dates=['datetime'])
        df = df.set_index('datetime')
        print(f"CSV date range: {df.index.min()} to {df.index.max()}")
        mask = (df.index >= start) & (df.index < end)
        result = df.loc[mask].reset_index()
        print(f"Found {len(result)} rows")
        return result