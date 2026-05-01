from fastapi import HTTPException, FastAPI
import pandas as pd
from config import  TRAFFIC_MODEL_DIR  # Import config
import os

# # local host mode
# from ..traffic_dto import TrafficPredictionRequest, TrafficPredictionResponse
# from ..infrastructure.datasource.local_datasource import LocalTrafficModelDataSource
# from ..infrastructure.repositories.traffic_model_repo_impl import SklearnTrafficRepository
# from ..domain.usecases.predict_traffic_usecase import PredictTrafficUseCase

# for docker environment
#  Import new DTOs
from features.traffic_predictor.prsntn.traffic_dto import TrafficPredictionRequest, TrafficPredictionResponse
from features.traffic_predictor.infrastructure.datasource.local_datasource import LocalTrafficModelDataSource
from features.traffic_predictor.infrastructure.repositories.traffic_model_repo_impl import SklearnTrafficRepository
from features.traffic_predictor.domain.usecases.predict_traffic_usecase import PredictTrafficUseCase

# Composition Root (Initialize dependencies )

traffic_model_path = os.path.join(TRAFFIC_MODEL_DIR) 
ds = LocalTrafficModelDataSource(traffic_model_path)
repo = SklearnTrafficRepository(ds)
use_case = PredictTrafficUseCase(repo)

app = FastAPI(title="Weather Prediction Service", version="1.0")

@app.post("/predict_traffic", response_model=TrafficPredictionResponse)
async def predict_traffic(request: TrafficPredictionRequest):
    try:
        # Add Validation (Just like i did in Weather)
        
        target_dt = request.datetime

        result = use_case.execute(target_dt, request.road)
        
        return TrafficPredictionResponse(
            road=request.road,
            congestion=result.congestion.value,
            confidence=round(result.confidence, 2)
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    