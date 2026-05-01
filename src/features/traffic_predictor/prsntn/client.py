import requests

def predict_traffic(datetime_str, road):
    """
    Calls the Unified AI Suite to predict traffic congestion.
    """
    url = "http://localhost:80/traffic/predict_traffic"
    payload = {
        "datetime": datetime_str,
        "road": road
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise error for 4xx or 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Test the Traffic Prediction
road_to_test = "Bombo Road"
time_to_test = "2026-03-30 08:30:00"  # Monday Morning Rush Hour

print(f"Testing traffic prediction for {road_to_test} at {time_to_test}...")
result = predict_traffic(time_to_test, road_to_test)

if "error" not in result:
    print(f"--- Traffic Report for {result['road']} ---")
    print(f"Status:     {result['congestion']}")
    print(f"Confidence: {result['confidence']:.2%}")
else:
    print(f"Prediction failed: {result['error']}")