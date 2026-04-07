from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from ..domain.entities import Lecture
from ..infrastructure.clients.weather_client import WeatherAPIClient
from ..infrastructure.clients.traffic_client import TrafficAPIClient
from ..infrastructure.bn_repository import FileBasedBNRepository
from ..infrastructure.svm_policy import TrainedSVMPolicy
from ..application.usecases.predict_lecture_status import PredictLectureStatusUseCase
from ..domain.entities import LectureDecision
from ....config import WEATHER_API_URL, TRAFFIC_API_URL, BN_MODEL_DIR, SVM_MODEL_DIR

app = FastAPI(title="Lecture Decision Engine Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500","http://127.0.0.1:5500","http://10.149.6.46:5500"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise dependencies (in production, use dependency injection)
weather_client = WeatherAPIClient(WEATHER_API_URL)
traffic_client = TrafficAPIClient(TRAFFIC_API_URL)
bn_service = FileBasedBNRepository(BN_MODEL_DIR)
svm_service = TrainedSVMPolicy(SVM_MODEL_DIR)
use_case = PredictLectureStatusUseCase(weather_client, traffic_client, bn_service, svm_service)

class LectureDecisionRequest(BaseModel):
    datetime: str
    road_name: str
    dry_bulb: float
    wet_bulb: float
    humidity: float
    wind_speed: float
    importance: str = "Normal"
    
@app.post("/predict_decision", response_model=LectureDecision)
async def predict_lecture_status(request: LectureDecisionRequest):
    try:
        dt = pd.to_datetime(request.datetime)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format.")
    lecture = Lecture(
        datetime=dt,
        road_name=request.road_name,
        dry_bulb=request.dry_bulb,
        wet_bulb=request.wet_bulb,
        humidity=request.humidity,
        wind_speed=request.wind_speed,
        importance=request.importance
    )
    result = use_case.execute(lecture)
    return result