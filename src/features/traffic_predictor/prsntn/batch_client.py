import requests
import pandas as pd
from tabulate import tabulate 

class TrafficBatchTester:
    def __init__(self, base_url="http://localhost:81"):
        self.url = f"{base_url}/predict_traffic"

    def run_scenarios(self, scenarios):
        results = []
        for sc in scenarios:
            payload = {"datetime": sc["time"], "road": sc["road"]}
            try:
                resp = requests.post(self.url, json=payload)
                data = resp.json()
                results.append({
                    "Road": sc["road"],
                    "Time": sc["time"],
                    "Context": sc["desc"],
                    "Prediction": data.get("congestion", "ERROR"),
                    "Confidence": f"{data.get('confidence', 0):.2%}"
                })
            except Exception as e:
                results.append({"Road": sc["road"], "Time": sc["time"], "Prediction": "FAILED"})
        
        print("\n" + "="*80)
        print("TRAFFIC MODEL SCENARIO TESTING")
        print("="*80)
        print(tabulate(results, headers="keys", tablefmt="grid"))

# Define test cases
test_scenarios = [
    {"road": "Bombo Road", "time": "2026-03-30 08:30:00", "desc": "Monday Morning Rush"},
    {"road": "Bombo Road", "time": "2026-03-30 23:30:00", "desc": "Monday Late Night"},
    {"road": "Northern Bypass", "time": "2026-04-05 10:00:00", "desc": "Sunday Morning"},
]

if __name__ == "__main__":
    tester = TrafficBatchTester()
    tester.run_scenarios(test_scenarios)