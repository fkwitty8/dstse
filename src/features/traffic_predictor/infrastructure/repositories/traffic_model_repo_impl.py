import pandas as pd
import numpy as np
from datetime import datetime

# local host mode
# from ..domain.entities.traffic_entity import TrafficPrediction, TrafficCategory
# from ..domain.repository.traffic_repository import ITrafficRepository

from features.traffic_predictor.domain.entities.traffic_entity import TrafficPrediction, TrafficCategory
from features.traffic_predictor.domain.repository.traffic_repository import ITrafficRepository

class SklearnTrafficRepository(ITrafficRepository):
    def __init__(self, data_source):
        self.ds = data_source
        self.metadata = self.ds.load_metadata()
        self.feature_cols = self.metadata['feature_columns']
        self.model_type = self.metadata['model_type']

    def get_prediction(self, dt: datetime, road: str) -> TrafficPrediction:
        
        # we defaulted this allow for manual testing with any date, but the model was trained on 2023 data, so we need to ensure the year is 2023 for feature consistency
        if dt.year != 2023:
            dt = dt.replace(year=2023)

        # Feature Engineering
        features = self._engineer_features(dt, road)
        

        # Ensure correct column order for sklearn
        X_pred = pd.DataFrame([features])[self.feature_cols]

        # Dynamic Execution based on metadata
        if self.model_type == 'classifier':
            return self._predict_classifier(X_pred)
        else:
            return self._predict_regressor(X_pred)

    def _engineer_features(self, dt: datetime, road: str):
        # Base time-based features
        feat = {
            'hour': dt.hour,
            'day_of_week': dt.dayofweek,
            'is_weekend': 1 if dt.dayofweek >= 5 else 0,
            'is_rush_hour': 1 if (7 <= dt.hour <= 9) or (16 <= dt.hour <= 19) else 0,
            'month': dt.month
        }

        # Dynamic Road One-Hot Encoding
        road_cols = [col for col in self.feature_cols if col.startswith('road_')]
        if road_cols:
            # Initialize all as 0
            for col in road_cols:
                feat[col] = 0
            # Set target road to 1
            road_dummy = f"road_{road}"
            if road_dummy in road_cols:
                feat[road_dummy] = 1
                
        return feat

    def _predict_classifier(self, X_pred) -> TrafficPrediction:
        # Load classifier specific artifacts
        model = self.ds.load_pickle("clsf/v0/classifier.pkl")
        encoder = self.ds.load_pickle("clsf/v0/label_encoder.pkl")
        
        pred_encoded = model.predict(X_pred)[0]
        probabilities = model.predict_proba(X_pred)[0]
        
        label = encoder.inverse_transform([pred_encoded])[0]
        confidence = float(probabilities[pred_encoded])
        
        return TrafficPrediction(
            congestion=TrafficCategory(label), 
            confidence=confidence
        )

    def _predict_regressor(self, X_pred) -> TrafficPrediction:
        model = self.ds.load_pickle("reg/v0/regressor.pkl")
        count = model.predict(X_pred)[0]
        th = self.metadata['thresholds']
        
        # Mapping logic (The "Confidence Math" from the script)
        if count <= th['low']:
            cat = TrafficCategory.LOW
            conf = 1 - (count / th['low'])
        elif count <= th['normal']:
            cat = TrafficCategory.NORMAL
            band_width = th['normal'] - th['low']
            mid_point = (th['low'] + th['normal']) / 2
            conf = 1 - (2 * abs(count - mid_point) / band_width)
        else:
            cat = TrafficCategory.VERY_HIGH
            typical_range = th['normal'] * 0.5
            conf = min(1.0, (count - th['normal']) / typical_range)
            
        return TrafficPrediction(
            congestion=cat, 
            confidence=max(0.0, min(1.0, float(conf)))
        ) 
    
    