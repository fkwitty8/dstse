from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware  # LINE 1: ADD THIS
import pandas as pd

from domain.entities import WeatherObservation
from application.usecases.predict_weather import PredictWeatherUseCase
from infrastructure.repositories.weather_data_repo import CsvWeatherDataRepository
from infrastructure.repositories.model_repo import FileBasedWeatherModelRepository
from config import WEATHER_MODEL_DIR, WEATHER_DATA_PATH
from prsntn.wthr_dto import WeatherPredictionRequest, WeatherPredictionResponse

print("Use case initialized. API is ready to serve requests.")
app = FastAPI(title="Weather Prediction Service", version="1.0")

# LINES 2-4: ADD THIS CORS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize dependencies (YOUR EXISTING CODE - NO CHANGES)
print("Loading model and data repositories...")
data_repo = CsvWeatherDataRepository(WEATHER_DATA_PATH)
print("Data repository initialized.")
model_repo = FileBasedWeatherModelRepository(WEATHER_MODEL_DIR)
print("Model repository initialized.")
use_case = PredictWeatherUseCase(data_repo, model_repo)

# YOUR EXISTING ENDPOINTS - NO CHANGES
@app.post("/predict_weather", response_model=WeatherPredictionResponse)
async def predict_weather(request: WeatherPredictionRequest):
    print("api called with:", request)
    try:
        target = pd.Timestamp(request.datetime)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format.")

    current_obs = WeatherObservation(
        datetime=target,
        dry_bulb=request.dry_bulb,
        wet_bulb=request.wet_bulb,
        humidity=request.humidity,
        wind_speed=request.wind_speed,
        total_rainfall=0.0
    )

    try:
        print("Executing use case with target:", target, "and current_obs:", current_obs)
        prediction = use_case.execute(target, current_obs)
        print("successfully got prediction from use case:", prediction)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    return WeatherPredictionResponse(
        bn_category=prediction.bn_category,
        confidence=prediction.confidence,
        rainfall_mm=prediction.rainfall_mm
    )

@app.get("/health")
async def health():
    return {"status": "ok"}