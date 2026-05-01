from abc import ABC, abstractmethod
import pandas as pd

class WeatherDataRepository(ABC):
    """Interface for fetching historical weather data."""
    @abstractmethod
    def get_observations(self, start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
        """Return DataFrame with columns: datetime, Dry bulb, Wet bulb, Humidity, Wind speed, Total Rainfall."""
        pass

class WeatherModelRepository(ABC):
    """Interface for loading the trained model, scaler, and thresholds."""
    @abstractmethod
    def load_regressor(self):
        pass

    @abstractmethod
    def load_scaler(self):
        pass

    @abstractmethod
    def load_feature_columns(self):
        pass

    @abstractmethod
    def load_thresholds(self):
        pass