import sys
import os
import io
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict, Any

from network_security.exception import NetworkSecurityException
from network_security.utils.main_utils import load_object
from network_security.components.incident_agent import IncidentReportAgent

load_dotenv()

app = FastAPI(title="Network Security MLOps API")

templates = Jinja2Templates(directory="templates")

class ThreatPayload(BaseModel):
    network_data: Dict[str, Any]

def get_latest_artifacts():
    artifacts_dir = "artifacts"
    if not os.path.exists(artifacts_dir):
        raise Exception("Artifacts directory not found. Please run main.py first.")
    
    timestamps = os.listdir(artifacts_dir)
    latest_folder = max(timestamps, key=lambda d: os.path.getmtime(os.path.join(artifacts_dir, d)))

    model_path = os.path.join(artifacts_dir, latest_folder, "model_trainer", "trained_model", "model.pkl")
    preprocessor_path = os.path.join(artifacts_dir, latest_folder, "data_transformation", "transformed_object", "preprocessing.pkl")

    return model_path, preprocessor_path

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/predict")
async def predict_batch(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        model_path, preprocessor_path = get_latest_artifacts()
        model = load_object(model_path)
        preprocessor = load_object(preprocessor_path)

        if 'Result' in df.columns:
            df_features = df.drop(columns=['Result'])
        else:
            df_features = df

        transformed_data = preprocessor.transform(df_features)
        predictions = model.predict(transformed_data)
        
        df['Prediction_Code'] = predictions
        df['Threat_Status'] = df['Prediction_Code'].map({-1: 'Phishing Detected', 1: 'Safe'})

        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename=Threat_Report_{file.filename}"
        
        return response
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/analyze-incident")
async def analyze_incident(payload: ThreatPayload):
    try:
        agent = IncidentReportAgent()
        report_markdown = agent.generate_report(payload.network_data)
        return {"status": "success", "report": report_markdown}
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)