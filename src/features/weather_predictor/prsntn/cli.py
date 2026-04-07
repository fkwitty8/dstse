import argparse
import pandas as pd

from ..infrastructure.repositories.weather_data_repo import CsvWeatherDataRepository
from ..domain.entities import WeatherObservation
from ..application.usecases.predict_weather import PredictWeatherUseCase
from ..infrastructure.repositories.model_repo import FileBasedWeatherModelRepository
from src.config import MODEL_DIR, DATA_PATH

def main():
    parser = argparse.ArgumentParser(description="Predict weather category for a given time.")
    parser.add_argument("datetime", help="Target datetime (e.g., '2023-03-24 10:30:00')")
    parser.add_argument("dry_bulb", type=float, help="Dry bulb temperature (°C)")
    parser.add_argument("wet_bulb", type=float, help="Wet bulb temperature (°C)")
    parser.add_argument("humidity", type=float, help="Relative humidity (%)")
    parser.add_argument("wind_speed", type=float, help="Wind speed (m/s)")
    args = parser.parse_args()

    target = pd.Timestamp(args.datetime)
    current_obs = WeatherObservation(
        datetime=target,
        dry_bulb=args.dry_bulb,
        wet_bulb=args.wet_bulb,
        humidity=args.humidity,
        wind_speed=args.wind_speed,
        total_rainfall=0.0
    )

    # Setup dependencies (could be injected, but simple for CLI)
    data_repo = CsvWeatherDataRepository(DATA_PATH)
    model_repo = FileBasedWeatherModelRepository(MODEL_DIR)
    use_case = PredictWeatherUseCase(data_repo, model_repo)

    try:
        pred = use_case.execute(target, current_obs)
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"BN Category: {pred.bn_category}")
    print(f"Confidence: {pred.confidence:.4f}")
    print(f"Rainfall: {pred.rainfall_mm:.4f} mm")

if __name__ == "__main__":
    main()