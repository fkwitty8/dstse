import requests
import json

def predict_weather(datetime_str, dry_bulb, wet_bulb, humidity, wind_speed):
    response = requests.post(
        "http://localhost:80/predict_weather",
        json={
            "datetime": datetime_str,
            "dry_bulb": dry_bulb,
            "wet_bulb": wet_bulb,
            "humidity": humidity,
            "wind_speed": wind_speed
        }
    )
    return response.json()

# Test
result = predict_weather("2023-03-24 13:30:00", 26.0, 21.0, 72.0, 6.0)

print(f"result: {json.dumps(result, indent=2)}")
print(f"Weather category: {result['bn_category']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Rainfall: {result['rainfall_mm']:.2f} mm")
print("results:", result)