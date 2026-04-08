from fastapi import HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware  # LINE 1: ADD THIS
import pandas as pd
from config import TRAFFIC_DATA_PATH, TRAFFIC_MODEL_DIR  # Import config
import os

# 1. Import new DTOs
from traffic_dto import TrafficPredictionRequest, TrafficPredictionResponse
from infrastructure.datasource.local_datasource import LocalTrafficModelDataSource
from infrastructure.repositories.traffic_model_repo_impl import SklearnTrafficRepository
from domain.usecases.predict_traffic_usecase import PredictTrafficUseCase

# 2. Composition Root (Initialize dependencies properly)

traffic_model_path = os.path.join(TRAFFIC_MODEL_DIR) 
ds = LocalTrafficModelDataSource(traffic_model_path)
repo = SklearnTrafficRepository(ds)
use_case = PredictTrafficUseCase(repo)

app = FastAPI(title="Weather Prediction Service", version="1.0")

# LINES 2-4: ADD THIS CORS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict_traffic", response_model=TrafficPredictionResponse)
async def predict_traffic(request: TrafficPredictionRequest):
    try:
        # 3. Add Validation (Just like did in Weather)
        print(f"Received request: {request}")
        target_dt = request.datetime
        
        print(f"Parsed datetime: {target_dt}, Road: {request.road}")
        result = use_case.execute(target_dt, request.road)
        
        print(f"Prediction result: Congestion={result.congestion}, Confidence={result.confidence}")
        return TrafficPredictionResponse(
            road=request.road,
            congestion=result.congestion.value,
            confidence=round(result.confidence, 2)
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# OPTIONAL: Add health check (not required but helpful)
@app.get("/health")
async def health():
    return {"status": "ok"}