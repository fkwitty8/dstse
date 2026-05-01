import pandas as pd
import numpy as np

# local host mode
# from ...domain.entities import WeatherObservation, WeatherPrediction
# from ...domain.repository import WeatherDataRepository, WeatherModelRepository
# from ...domain.services import FeatureEngineeringService

# for docker environment
from features.weather_predictor.domain.entities import WeatherObservation, WeatherPrediction
from features.weather_predictor.domain.entities import WeatherObservation, WeatherPrediction
from features.weather_predictor.domain.repository import WeatherDataRepository, WeatherModelRepository
from features.weather_predictor.domain.services import FeatureEngineeringService

class PredictWeatherUseCase:
    def __init__(
        self,
        data_repo: WeatherDataRepository,
        model_repo: WeatherModelRepository
    ):
        self.data_repo = data_repo
        self.model_repo = model_repo
        
        self._load_artifacts()

    def _load_artifacts(self):
       
        self.reg = self.model_repo.load_regressor()
    
        self.scaler = self.model_repo.load_scaler()
        
        self.feature_cols = self.model_repo.load_feature_columns()
        
        self.thresholds = self.model_repo.load_thresholds()

    def execute(self, target: pd.Timestamp, current_obs: WeatherObservation) -> WeatherPrediction:
        # Fetch history (last 3 hours)
        
        # Use 2023 as reference year (since our data is from 2023 alone)
        reference_year = 2023
        target_for_history = target.replace(year=reference_year)
        start_for_history = target_for_history - pd.Timedelta(hours=3)
        end_for_history = target_for_history
        
        # Fetch history using the reference year
        history_df = self.data_repo.get_observations(start_for_history, end_for_history)
        
        # start = target - pd.Timedelta(hours=3)
        # history_df = self.data_repo.get_observations(start, target)
        if history_df.empty:
            raise ValueError("No historical data available")

        # Build a combined DataFrame (history + current)
        history_df = history_df.sort_values('datetime')
        current_row = pd.DataFrame([{
            'datetime': target,
            'Dry bulb': current_obs.dry_bulb,
            'Wet bulb': current_obs.wet_bulb,
            'Humidity': current_obs.humidity,
            'Wind speed': current_obs.wind_speed,
            'Total Rainfall': 0.0
        }])
        combined = pd.concat([history_df, current_row], ignore_index=True).set_index('datetime')
        combined = combined.sort_index()

        # Compute features using domain service
        row = FeatureEngineeringService.compute_features(combined, target)

        # Prepare input for model
        X = row[self.feature_cols].values.reshape(1, -1)
        X_scaled = self.scaler.transform(X)

        # Predict
        log_rain = self.reg.predict(X_scaled)[0]
        rain_mm = np.expm1(log_rain)

        # Map to BN category and confidence
        bn_cat, confidence = self._map_to_bn_category(rain_mm)
        
        return WeatherPrediction(
            datetime=target,
            bn_category=bn_cat,
            confidence=confidence,
            rainfall_mm=rain_mm
        )

    def _map_to_bn_category(self, rain_mm: float):
        light = self.thresholds['light']
        moderate = self.thresholds['moderate']

        if rain_mm == 0:
            cat4 = 'No Rain'
        elif rain_mm <= light:
            cat4 = 'Light'
        elif rain_mm <= moderate:
            cat4 = 'Moderate'
        else:
            cat4 = 'Heavy'

        if cat4 in ['No Rain', 'Light']:
            bn = 'Good'
        elif cat4 == 'Moderate':
            bn = 'Moderate'
        else:
            bn = 'Bad'

        # Confidence
        if bn == 'Good':
            conf = 1 - min(rain_mm / light, 1.0)
        elif bn == 'Moderate':
            band = moderate - light
            mid = (light + moderate) / 2
            conf = 1 - (2 * abs(rain_mm - mid) / band)
        else:
            max_heavy = moderate * 2
            conf = min((rain_mm - moderate) / (max_heavy - moderate), 1.0)
        conf = max(0.0, min(1.0, conf))

        return bn, conf