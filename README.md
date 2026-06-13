# 🛡️ Agentic SOC & Enterprise MLOps Pipeline


---

## 🚀 Overview

**Agentic SOC & Enterprise MLOps Pipeline** is a production-grade cybersecurity intelligence platform that combines the speed of Machine Learning with the reasoning capabilities of Generative AI.

Traditional Intrusion Detection Systems (IDS) can identify suspicious traffic but often fail to explain *why* a threat was detected. Security analysts are forced to manually investigate logs, URLs, and feature vectors, resulting in alert fatigue and slower response times.

This project solves that problem through a **hybrid ML + GenAI architecture**:

* ⚡ Machine Learning performs high-speed threat classification.
* 🧠 Generative AI performs contextual threat analysis.
* 📊 FastAPI exposes scalable prediction APIs.
* 🔄 MLOps pipelines automate ingestion, validation, transformation, training, and deployment.
* 📄 Executive-level security reports are generated automatically for detected threats.

---

# 🎯 Problem Statement

Modern cybersecurity systems generate thousands of alerts every day.

Most detection systems simply output:

```text
1  -> Safe
-1 -> Malicious
```

without providing:

* Why was the traffic flagged?
* Which features indicate phishing behavior?
* What vulnerabilities were detected?
* What actions should analysts take?

As a result:

* Security teams waste hours investigating alerts.
* False positives consume analyst time.
* Threat triage becomes difficult at scale.

---

# 💡 Solution Architecture

The system follows a **Separation of Concerns (SoC)** architecture.

### Layer 1: ML Threat Detection Engine

A trained Random Forest model processes incoming traffic and determines whether a sample is malicious.

### Layer 2: Agentic Security Analyst

Only suspicious samples are forwarded to a LangChain-powered AI Agent.

The agent:

* Reads feature vectors
* Understands threat indicators
* Generates human-readable reports
* Recommends remediation actions

This dramatically reduces LLM cost while maintaining explainability.

---

# 🏗️ System Architecture

```mermaid
graph TD

A[Raw Network Traffic CSV/JSON]
--> B[FastAPI Backend]

B --> C[Data Preprocessing]

C --> D[Random Forest Classifier]

D -->|Safe Traffic| E[Allow & Log]

D -->|Threat Detected| F[LangChain Agent]

F --> G[OpenAI LLM]

G --> H[Threat Intelligence Report]

H --> I[Dashboard / API Client]
```

---

# 🔄 Complete MLOps Lifecycle

This project is built around a modular enterprise MLOps architecture.

---

## 1️⃣ Data Ingestion

### Responsibilities

* Connect to MongoDB Atlas
* Fetch latest phishing datasets
* Convert raw records into DataFrames
* Train/Test split generation

### File

```bash
components/data_ingestion.py
```

---

## 2️⃣ Data Validation

Incoming datasets are validated against predefined schemas.

### Validation Checks

* Missing columns
* Incorrect datatypes
* Null value thresholds
* Dataset integrity

### File

```bash
components/data_validation.py
```

If validation fails, the pipeline stops automatically.

---

## 3️⃣ Data Transformation

Raw data is transformed into model-ready features.

### Techniques

#### Missing Value Handling

```python
SimpleImputer
```

#### Feature Scaling

```python
StandardScaler
```

Artifacts generated:

```text
preprocessor.pkl
```

### File

```bash
components/data_transformation.py
```

---

## 4️⃣ Model Training

Multiple algorithms can be evaluated.

Current production model:

```text
Random Forest Classifier
```

Reasons:

* Strong tabular-data performance
* Fast inference
* Robust to noise
* Feature importance support

Generated artifact:

```text
model.pkl
```

### File

```bash
components/model_trainer.py
```

---

## 5️⃣ Model Deployment

The trained model is deployed through FastAPI endpoints.

Features:

* Batch prediction
* Real-time prediction
* Threat report generation

---

# 📊 Model Performance

The cybersecurity domain heavily penalizes False Negatives.

A missed phishing attack can result in:

* Credential theft
* Financial loss
* Enterprise compromise

Therefore, the model is optimized for **Recall** while maintaining high precision.

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | ~97%   |
| Precision | ~96.1% |
| Recall    | ~97.8% |
| F1 Score  | ~97%   |

---

# 🔍 Feature Dictionary

The model evaluates 30+ URL and network characteristics.

### Example Features

| Feature          | Meaning                                       |
| ---------------- | --------------------------------------------- |
| URL_Length       | Excessively long URLs often indicate phishing |
| having_At_Symbol | Attackers use @ to mask domains               |
| Prefix_Suffix    | Hyphens often indicate spoofed domains        |
| SSLfinal_State   | Verifies SSL certificate legitimacy           |
| Request_URL      | External object loading behavior              |
| DNS_Record       | Missing DNS records are suspicious            |

Values are generally represented as:

```text
1   -> Legitimate
0   -> Suspicious
-1  -> Malicious
```

---

# 🤖 Agentic GenAI Layer

Sending every request directly to an LLM would be:

* Expensive
* Slow
* Inefficient

Instead:

```text
Traffic
   ↓
ML Model
   ↓
Only Threats
   ↓
LLM Agent
```

This architecture significantly reduces:

* API costs
* Inference latency
* Infrastructure requirements

while preserving explainability.

---

## Agent Workflow

### Step 1

Receive flagged feature vector:

```json
{
  "URL_Length": -1,
  "SSLfinal_State": -1,
  "having_At_Symbol": 1
}
```

### Step 2

Inject data into a constrained prompt template.

### Step 3

Analyze threat indicators.

### Step 4

Generate executive-level incident report.

---

## Generated Report Sections

### Threat Summary

High-level explanation of the attack.

### Key Vulnerabilities

Identified phishing indicators.

### Risk Assessment

Potential impact.

### Recommended Actions

Suggested remediation steps.

---

# 🛠️ Technology Stack

| Layer            | Technologies                  |
| ---------------- | ----------------------------- |
| Machine Learning | Scikit-Learn, Pandas, NumPy   |
| Generative AI    | LangChain, OpenAI             |
| Backend          | FastAPI, Uvicorn              |
| Validation       | Pydantic                      |
| Database         | MongoDB Atlas                 |
| Frontend         | HTML, TailwindCSS, JavaScript |
| Deployment       | Render                        |
| Containerization | Docker                        |
| Version Control  | Git & GitHub                  |

---

# 📁 Repository Structure

```text
network-security-mlops/
│
├── artifacts/
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── network_security/
│
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│
│   ├── logging/
│   │   └── logger.py
│
│   └── exception.py
│
├── templates/
│   └── index.html
│
├── Network_Data/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation & Setup

## Prerequisites

Install:

* Python 3.10+
* Git
* Docker

You'll also need:

* MongoDB Atlas URI
* OpenAI API Key

---

## Clone Repository

```bash
git clone https://github.com/Aditya3113/network-security-mlops.git

cd network-security-mlops
```

---

## Environment Variables

Create a `.env` file:

```env
MONGO_DB_URL="mongodb+srv://username:password@cluster.mongodb.net/"

OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxx"
```

---

# 🐳 Run with Docker

Build image:

```bash
docker build -t agentic-soc .
```

Run container:

```bash
docker run -p 8000:8000 --env-file .env agentic-soc
```

Application:

```text
http://localhost:8000
```

---

# 💻 Local Development Setup

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

---

# 📡 API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

---

## POST /predict

Batch phishing prediction.

### Request

```multipart
file = phishingData.csv
```

### Response

Returns CSV with:

```text
Prediction
```

column appended.

---

## POST /analyze-incident

Generate AI threat report.

### Request

```json
{
  "URL_Length": -1,
  "having_At_Symbol": 1,
  "SSLfinal_State": -1,
  "Prefix_Suffix": 1
}
```

### Response

```json
{
  "report": "Threat Level: High ..."
}
```

---

# 🔮 Future Roadmap

### Multi-Agent Security Teams

* [ ] CrewAI Integration
* [ ] LangGraph Integration
* [ ] Automated Incident Response Agents

### Enterprise Security Automation

* [ ] Auto-generated Firewall Rules
* [ ] Auto-generated SIEM Reports
* [ ] Threat Intelligence Enrichment

### Self-Healing MLOps

* [ ] Data Drift Detection
* [ ] Model Drift Detection
* [ ] Automatic Retraining Pipelines

### DevOps

* [ ] GitHub Actions CI/CD
* [ ] Automated Docker Builds
* [ ] Kubernetes Deployment

### LLM Enhancements

* [ ] Ollama Integration
* [ ] Llama 3 Support
* [ ] Air-Gapped Enterprise Deployment

---

# 🌟 Key Highlights

✅ End-to-End MLOps Pipeline

✅ Explainable AI Security Reports

✅ FastAPI Production APIs

✅ MongoDB Atlas Integration

✅ Dockerized Deployment

✅ LangChain Agent Architecture

✅ Enterprise-Ready Design

---

# 👨‍💻 Author

### Aditya Pandey

**Information Technology Undergraduate**
**Indian Institute of Information Technology (IIIT) Una**

**GitHub**

```text
https://github.com/Aditya3113
```

**LinkedIn**

```text
https://linkedin.com/in/aditya3113pandey
```

---

# ⭐ Support

If you found this project useful, consider:

⭐ Starring the repository

🍴 Forking the project

🛠️ Contributing improvements

📢 Sharing it with fellow developers

---
