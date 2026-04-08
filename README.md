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
git clone https://github.com/yourusername/dstse.git
cd dstse

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
