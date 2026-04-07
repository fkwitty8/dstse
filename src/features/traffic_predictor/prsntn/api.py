from fastapi import HTTPException, FastAPI
import pandas as pd
from ....config import TRAFFIC_DATA_PATH, TRAFFIC_MODEL_DIR  # Import config
import os

# 1. Import new DTOs
from .traffic_dto import TrafficPredictionRequest, TrafficPredictionResponse
from ..infrastructure.datasource.local_datasource import LocalTrafficModelDataSource
from ..infrastructure.repositories.traffic_model_repo_impl import SklearnTrafficRepository
from ..domain.usecases.predict_traffic_usecase import PredictTrafficUseCase

# 2. Composition Root (Initialize dependencies properly)

traffic_model_path = os.path.join(TRAFFIC_MODEL_DIR) 
ds = LocalTrafficModelDataSource(traffic_model_path)
repo = SklearnTrafficRepository(ds)
use_case = PredictTrafficUseCase(repo)

app = FastAPI(title="Weather Prediction Service", version="1.0")

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
    