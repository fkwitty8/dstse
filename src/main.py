# src/main.py
from fastapi import FastAPI
from src.features.weather_predictor.prsntn.api import router as weather_router
from src.features.traffic_predictor.prsntn.api import router as traffic_router
from src.features.decision_engine.prsntn.api import router as decision_router

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Urban Intelligence AI Suite",
    description="Unified API for Weather and Traffic Predictions",
    version="2.0.0"
)


# --- Register Feature Routers ---
print("Registering API routers for traffic...")
app.include_router(traffic_router)

print("Registering API routers for weather...")
app.include_router(weather_router)

print("Registering API router for decision")
app.include_router(decision_router)

app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Suite API",
        "features": ["/weather", "/traffic"],
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "online"}

