# DSTSE - Dynamic Scheduling and Traffic-Synchronized Education



## 📌 Overview

The **Dynamic Scheduling and Traffic-Synchronized Education (DSTSE)** system is an intelligent lecture management platform that predicts weather conditions and traffic congestion to recommend optimal lecture statuses (Scheduled, Online, Rescheduled, Cancelled). It combines:

- **Random Forest models** for weather and traffic prediction
- **Bayesian Network** for causal reasoning and auditability
- **Support Vector Machine (SVM)** for policy enforcement

The system is designed for high‑stakes institutional environments where decisions must be both accurate and explainable.

---

## 🏗️ System Architecture


---

## 📁 Project Structure
src/
├── features/
│ ├── weather_predictor/ # Weather prediction microservice
│ │ ├── domain/ # Entities, value objects, repositories
│ │ ├── infrastructure/ # Data repositories, model loading
│ │ ├── application/ # Use cases
│ │ └── prsntn/ # FastAPI router, CLI client
│ ├── traffic_predictor/ # Traffic prediction microservice
│ │ └── ... (similar structure)
│ └── decision_engine/ # Decision engine microservice
│ └── ... (similar structure)
├── models/ # Trained models (weather, traffic, BN, SVM)
├── static/ # Frontend UI (HTML/CSS/JS)
├── config.py # Configuration (paths, API URLs)
└── main.py # (Optional) Monolithic entry point
