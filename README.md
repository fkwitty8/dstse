# DSTSE - Dynamic Scheduling and Traffic-Synchronized Education



## 📌 Overview

The **Dynamic Scheduling and Traffic-Synchronized Education (DSTSE)** system is an intelligent lecture management platform that predicts weather conditions and traffic congestion to recommend optimal lecture statuses (Scheduled, Online, Rescheduled, Cancelled). It combines:

- **Random Forest models** for weather and traffic prediction
- **Bayesian Network** for causal reasoning and auditability
- **Support Vector Machine (SVM)** for policy enforcement

The system is designed for high‑stakes institutional environments where decisions must be both accurate and explainable.

---

## 🏗️ System Architecture

────────────────────────────────────────────────────────────────────────────┐
│ DSTSE SYSTEM ARCHITECTURE │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Weather │ │ Traffic │ │ Timetable │ │
│ │ Sensors │ │ Docks │ │ (Lectures) │ │
│ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Data │ │ Data │ │ Feature │ │
│ │ Preprocessing│ │ Preprocessing│ │ Extraction │ │
│ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Random │ │ Random │ │ Lecture │ │
│ │ Forest │ │ Forest │ │ Context │ │
│ │ Regressor │ │ Classifier │ │ (Importance,│ │
│ └──────┬───────┘ └──────┬───────┘ │ Location) │ │
│ │ │ └──────┬───────┘ │
│ ▼ ▼ │ │
│ ┌──────────────┐ ┌──────────────┐ │ │
│ │ Weather │ │ Traffic │ │ │
│ │ Category │ │ Congestion │ │ │
│ │ (Good/Mod/Bad)│ │ (Low/Norm/High)│ │ │
│ └──────┬───────┘ └──────┬───────┘ │ │
│ │ │ │ │
│ └─────────┬─────────┘ │ │
│ ▼ │ │
│ ┌─────────────────────┐ │ │
│ │ Bayesian Network │◄───────────────┘ │
│ │ (Causal Reasoning)│ │
│ └──────────┬──────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────┐ ┌──────────────┐ │
│ │ Delay Probability │───►│ SVM │ │
│ │ (0.0 – 1.0) │ │ Policy │ │
│ └─────────────────────┘ │ Enforcer │ │
│ └──────┬───────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────┐ │
│ │ Final Decision │ │
│ │ Scheduled | Online | │ │
│ │ Rescheduled | Cancelled │ │
│ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
