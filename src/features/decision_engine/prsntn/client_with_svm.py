import requests

def predict_lecture(datetime_str, road_name, dry_bulb, wet_bulb, humidity, wind_speed, importance="Normal"):
    url = "http://localhost:82/predict_decision"
    payload = {
        "datetime": datetime_str,
        "road_name": road_name,
        "dry_bulb": dry_bulb,
        "wet_bulb": wet_bulb,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "importance": importance
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    result = predict_lecture(
        "2023-03-24 10:30:00", "Bombo Road", 26.0, 21.0, 72.0, 6.0,
        importance="Important"
    )
    print(f"Decision: {result['decision']}")
    print(f"Probabilities: {result['probabilities']}")
    print(f"Explanation: {result['explanation']}")