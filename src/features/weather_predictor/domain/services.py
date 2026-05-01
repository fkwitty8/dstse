import pandas as pd
import numpy as np

class FeatureEngineeringService:
    """Domain service that computes lag and rolling features from a time series."""
    @staticmethod
    def compute_features(df: pd.DataFrame, target_time: pd.Timestamp) -> pd.Series:
        """
        Given a DataFrame with datetime index and columns:
        Dry bulb, Wet bulb, Humidity, Wind speed, Total Rainfall
        Compute all required features and return a Series for the target_time.
        """
        
        df = df.copy()
        df = df.sort_index()
        # Compute lags
        for lag in [1, 2, 3]:
            df[f'rainfall_lag_{lag}'] = df['Total Rainfall'].shift(lag)
            df[f'humidity_lag_{lag}'] = df['Humidity'].shift(lag)
            df[f'drybulb_lag_{lag}'] = df['Dry bulb'].shift(lag)

        # Rolling means
        df['rainfall_roll_3h'] = df['Total Rainfall'].rolling(window=3, min_periods=1).mean()
        df['humidity_roll_3h'] = df['Humidity'].rolling(window=3, min_periods=1).mean()
        df['drybulb_roll_3h'] = df['Dry bulb'].rolling(window=3, min_periods=1).mean()

        # Add basic time features
        row = df.loc[[target_time]].copy()
        row['dayofweek'] = target_time.weekday()
        row['hour'] = target_time.hour
        row['month'] = target_time.month
        row['day'] = target_time.day


        return row.iloc[0]  # return as Series