from fastapi import FastAPI, HTTPException, APIRouter
import pandas as pd

# local host mode
# from ..domain.entities import WeatherObservation
# from ..application.usecases.predict_weather import PredictWeatherUseCase
# from ..infrastructure.repositories.weather_data_repo import CsvWeatherDataRepository
# from ..infrastructure.repositories.model_repo import FileBasedWeatherModelRepository
# from ....config import WEATHER_MODEL_DIR, WEATHER_DATA_PATH
# from ..prsntn.wthr_dto import WeatherPredictionRequest, WeatherPredictionResponse

# for docker environment
from features.weather_predictor.domain.entities import WeatherObservation
from features.weather_predictor.application.usecases.predict_weather import PredictWeatherUseCase
from features.weather_predictor.infrastructure.repositories.weather_data_repo import CsvWeatherDataRepository
from features.weather_predictor.infrastructure.repositories.model_repo import FileBasedWeatherModelRepository
from config import WEATHER_MODEL_DIR, WEATHER_DATA_PATH
from features.weather_predictor.prsntn.wthr_dto import WeatherPredictionRequest, WeatherPredictionResponse


app = FastAPI(title="Weather Prediction Service", version="1.0")

# Initialize dependencies

data_repo = CsvWeatherDataRepository(WEATHER_DATA_PATH)

model_repo = FileBasedWeatherModelRepository(WEATHER_MODEL_DIR)

use_case = PredictWeatherUseCase(data_repo, model_repo)

@app.post("/predict_weather", response_model=WeatherPredictionResponse)
async def predict_weather(request: WeatherPredictionRequest):
    
    try:
        target = pd.Timestamp(request.datetime)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format.")

    # Map DTO to domain entity
    current_obs = WeatherObservation(
        datetime=target,
        dry_bulb=request.dry_bulb,
        wet_bulb=request.wet_bulb,
        humidity=request.humidity,
        wind_speed=request.wind_speed,
        total_rainfall=0.0
    )

    try:
        
        prediction = use_case.execute(target, current_obs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    # Map domain result to DTO
    return WeatherPredictionResponse(
        bn_category=prediction.bn_category,
        confidence=prediction.confidence,
        rainfall_mm=prediction.rainfall_mm
    )

@app.get("/health")
async def health():
    return {"status": "ok"}