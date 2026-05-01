import argparse
import pandas as pd
import sys
import os

# local host mode
# from ..domain.entities import Lecture
# from ..application.usecases.predict_lecture_status import PredictLectureStatusUseCase
# from ..infrastructure.clients.weather_client import WeatherAPIClient
# from ..infrastructure.clients.traffic_client import TrafficAPIClient
# from ..infrastructure.bn_repository import FileBasedBNRepository
# from ....config import BN_MODEL_DIR, WEATHER_API_URL, TRAFFIC_API_URL

# for docker environment
from features.decision_engine.domain.entities import Lecture
from features.decision_engine.application.usecases.predict_lecture_status import PredictLectureStatusUseCase
from infrastructure.clients.weather_client import WeatherAPIClient
from features.decision_engine.infrastructure.clients.traffic_client import TrafficAPIClient
from features.decision_engine.infrastructure.bn_repository import FileBasedBNRepository
from config import BN_MODEL_DIR, WEATHER_API_URL, TRAFFIC_API_URL

def main():
    parser = argparse.ArgumentParser(description="Predict lecture status based on weather and traffic.")
    parser.add_argument("datetime", help="Target datetime (e.g., '2023-03-24 10:30:00')")
    parser.add_argument("road_name", help="Name of the road (e.g., 'Bombo Road')")
    parser.add_argument("dry_bulb", type=float, help="Dry bulb temperature (°C)")
    parser.add_argument("wet_bulb", type=float, help="Wet bulb temperature (°C)")
    parser.add_argument("humidity", type=float, help="Relative humidity (%)")
    parser.add_argument("wind_speed", type=float, help="Wind speed (m/s)")
    args = parser.parse_args()

    dt = pd.Timestamp(args.datetime)
    lecture = Lecture(
        datetime=dt,
        road_name=args.road_name,
        dry_bulb=args.dry_bulb,
        wet_bulb=args.wet_bulb,
        humidity=args.humidity,
        wind_speed=args.wind_speed
    )

    # Initialize dependencies (using default URLs from config)
    weather_client = WeatherAPIClient(WEATHER_API_URL)
    traffic_client = TrafficAPIClient(TRAFFIC_API_URL)
    bn_service = FileBasedBNRepository(BN_MODEL_DIR)
    use_case = PredictLectureStatusUseCase(weather_client, traffic_client, bn_service)

    try:
        result = use_case.execute(lecture)
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"Decision: {result.decision}")
    print(f"Probabilities: {result.probabilities}")
    print(f"Explanation: {result.explanation}")

if __name__ == "__main__":
    main()