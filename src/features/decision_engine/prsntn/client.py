import requests

def predict_lecture(datetime_str, road_name, dry_bulb, wet_bulb, humidity, wind_speed):
    """
    Call the decision engine API to get the final lecture status.
    """
    url = "http://localhost:82/decision/predict"   # adjust port if needed
    payload = {
        "datetime": datetime_str,
        "road_name": road_name,
        "dry_bulb": dry_bulb,
        "wet_bulb": wet_bulb,
        "humidity": humidity,
        "wind_speed": wind_speed
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()   # raises an error for 4xx/5xx responses
    return response.json()

# Example usage
if __name__ == "__main__":
    try:
        result = predict_lecture(
            "2023-03-24 10:30:00",
            "Bombo Road",
            26.0, 21.0, 72.0, 6.0
        )
        print(f"Decision: {result['decision']}")
        print(f"Probabilities: {result['probabilities']}")
        print(f"Explanation: {result['explanation']}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")