# DSTSE - Dynamic Spatio- Temporal Synchronisation Engine


## 📌 Overview

The **Dynamic Scheduling and Traffic-Synchronized Education (DSTSE)** system is an intelligent lecture management platform that predicts weather conditions and traffic congestion to recommend optimal lecture statuses (Scheduled, Online, Rescheduled, Cancelled). It combines:

- **Random Forest models** for weather and traffic prediction
- **Bayesian Network** for causal reasoning and auditability
- **Support Vector Machine (SVM)** for policy enforcement

The system is designed for high‑stakes institutional environments where decisions must be both accurate and explainable.

### Setup

```bash
# Clone the repository
git clone https://github.com/fkwitty8/dstse.git
cd dstse

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### 🚀 Running the Services

```bash
## Microservice Mode

bash
# Terminal 1 - Weather Service (port 80)
cd src
uvicorn features.weather_predictor.prsntn.api:app --reload --port 80

# Terminal 2 - Traffic Service (port 81)
cd src
uvicorn features.traffic_predictor.prsntn.api:app --reload --port 81

# Terminal 3 - Decision Service (port 82)
cd src
uvicorn features.decision_engine.prsntn.api:app --reload --port 82
```

### 📡 API Endpoints

#### 1. Weather Service (http://localhost:80)
```bash

Endpoint	        Method	  Description
/predict_weather	POST	    Predict weather category from atmospheric data
/health	          GET	      Health check

**Request body:**
json
{
  "datetime": "2023-03-24 10:30:00",
  "dry_bulb": 26.0,
  "wet_bulb": 21.0,
  "humidity": 72.0,
  "wind_speed": 6.0
}

**Response:**
json
{
  "bn_category": "Good",
  "confidence": 0.7775,
  "rainfall_mm": 0.3115
}
```
#### 2. Traffic Service (http://localhost:81)
```bash
Endpoint	        Method	  Description
/predict_traffic	POST	    Predict congestion from datetime and road
/health	          GET	      Health check

**Request body:**
json
{
  "datetime": "2023-03-24 10:30:00",
  "road": "Bombo Road"
}

**Response:**
json
{
  "congestion": "Normal",
  "confidence": 0.96
}
```
#### 3. Decision Service (http://localhost:82)
```bash
Endpoint	        Method	  Description
/predict_decision	POST	    Final lecture decision from weather, traffic, importance
/health	          GET	      Health check

**Request body:**
json
{
  "datetime": "2023-03-24 10:30:00",
  "road_name": "Bombo Road",
  "dry_bulb": 26.0,
  "wet_bulb": 21.0,
  "humidity": 72.0,
  "wind_speed": 6.0,
  "importance": "Normal"
}

**Response:**
json
{
  "decision": "Scheduled",
  "probabilities": {
    "Scheduled": 0.688,
    "Online": 0.174,
    "Rescheduled": 0.112,
    "Cancelled": 0.026
  },
  "explanation": "Weather: Good (conf=0.78), Traffic: Normal (conf=0.96), Delay prob: 0.31, Importance: Normal"
}
```

### 🖥️ User Interface

Access the web UI at http://localhost:5500 (if using Live Server).

https://docs/ui_screenshot.png



### 🙏 Acknowledgements

**Mr Ggaliwango Marvin** – For providing the use case, guidance and domain expertise 
**Bike Share Makerere University** - For Providing us with realistic traffic and weather data
**Open Source Libraries** – FastAPI, pgmpy, scikit‑learn, pandas, numpy



### 📧 Contact
For questions or collaboration, please open an issue on GitHub or contact the maintainers.
```bash
kiyimba.fahad@students.mak.ac.ug | kiyimbafwitty@gmail.com
mushabe.moses@students.mak.ac.ug | mosesmushabe9@gmail.com
ggaliwango.marvin@cit.ac.ug
```


### 📚 Citation
If you use this work in your research, please cite:

bibtex
@software{dstse2025,
  title = {DSTSE: Dynamic Spatio Temporal Synchronization Engine},
  author = {Kiyimba, fahad and Mushabe, Moses and Ggaliwango,Marvin},
  year = {2026},
  url = {https://github.com/fkwitty8/dstse},
}

Built with ❤️ for smarter, data‑driven education in the Global South.
