# 🛡️ Network Security System - End-to-End MLOps Pipeline

An end-to-end Machine Learning Operations (MLOps) project designed to classify malicious URLs. This system extracts network data, processes it through a modular machine learning pipeline, and will eventually be served via a FastAPI REST interface and deployed using Docker and AWS CI/CD workflows.

---

## 📊 Project Overview

This project builds a robust classification model trained on a dataset of URLs. Each URL is characterized by a set of lexical and network-based features (e.g., `URL_Length`, `having_IP_Address`, `SSLfinal_State`). The pipeline is designed for production, emphasizing reproducibility, modularity, and automated tracking.

### 🏗️ Current Pipeline Architecture
1. **Data Ingestion (Completed):** Connects securely to a MongoDB Atlas cluster, extracts raw URL feature data, performs a deterministic train-test split, and stores the structured artifacts.
2. **Data Validation (Upcoming):** Schema validation and statistical drift detection.
3. **Data Transformation (Upcoming):** Imputation and feature scaling.
4. **Model Training & Evaluation (Upcoming):** Model selection and experiment tracking via MLflow/DagsHub.
5. **API & Deployment (Upcoming):** FastAPI serving and AWS/Docker CI/CD deployment.

---

## 🛠️ Tech Stack

| Category | Tools / Technologies |
| :--- | :--- |
| **Language** | Python 3.x |
| **Database** | MongoDB Atlas |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (Upcoming) |
| **Tracking & Logging** | Custom Logger, MLflow (Upcoming) |
| **Web Framework** | FastAPI, Uvicorn (Upcoming) |

---

## 📁 Repository Structure

The codebase follows a highly modular, enterprise-grade directory structure:

```text
network-security-mlops/
├── network_security/             # Core Python Package
│   ├── components/               # Pipeline execution stages (e.g., data_ingestion.py)
│   ├── constant/                 # Global immutable variables
│   ├── entity/                   # Config and Artifact dataclasses
│   ├── exception/                # Custom error handling and traceback
│   ├── logging/                  # Centralized timestamped logging
│   ├── pipeline/                 # Orchestration of components
│   └── utils/                    # Shared helper functions
├── logs/                         # Execution logs (Git ignored)
├── artifacts/                    # Pipeline outputs and CSV splits (Git ignored)
├── .env                          # Secure environment variables (Git ignored)
├── main.py                       # Pipeline execution entry point
├── requirements.txt              # Project dependencies
└── setup.py                      # Local package installer
