from pydantic import BaseModel, Field

class WeatherPredictionRequest(BaseModel):
    datetime: str = Field(..., description="Target datetime in ISO format, e.g., '2023-03-24 10:30:00'")
    dry_bulb: float = Field(..., description="Dry bulb temperature (°C)")
    wet_bulb: float = Field(..., description="Wet bulb temperature (°C)")
    humidity: float = Field(..., description="Relative humidity (%)")
    wind_speed: float = Field(..., description="Wind speed (m/s)")

class WeatherPredictionResponse(BaseModel):
    bn_category: str = Field(..., description="Bayesian Network category: Good, Moderate, Bad")
    confidence: float = Field(..., description="Confidence score (0-1)")
    rainfall_mm: float = Field(..., description="Predicted rainfall amount (mm)")