"""
backend/main.py — FastAPI service for the Student Performance Predictor.

Run locally:
    uvicorn main:app --reload --port 8000

Expects model.pkl (trained pipeline) and metrics.json (from ml/train.py)
to be present in this same directory — copy them over after training,
e.g.:  cp ../ml/model.pkl ../ml/metrics.json .
"""

import json
import os

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schema import PredictionResponse, StudentInput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")

app = FastAPI(
    title="Student Performance Predictor API",
    description="Predicts a student's final grade (G3, 0-20) from academic and social features.",
    version="1.0.0",
)

# Allow the React dev server / deployed frontend to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your deployed frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
top_features_global = []


@app.on_event("startup")
def load_artifacts():
    global model, top_features_global
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(
            f"model.pkl not found at {MODEL_PATH}. Run ml/train.py and copy the "
            "output here first."
        )
    model = joblib.load(MODEL_PATH)

    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH) as f:
            metrics = json.load(f)
        top_features_global = metrics.get("top_features") or []


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.get("/metrics")
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="metrics.json not found")
    with open(METRICS_PATH) as f:
        return json.load(f)


@app.post("/predict", response_model=PredictionResponse)
def predict(student: StudentInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    row = pd.DataFrame([student.model_dump()])
    predicted_g3 = float(model.predict(row)[0])
    predicted_g3 = max(0.0, min(20.0, predicted_g3))  # clamp to valid range

    percent = round(predicted_g3 / 20 * 100, 1)
    pass_fail = "Pass" if predicted_g3 >= 10 else "Fail"

    top_features = [
        {"feature": name, "importance": round(score, 4)}
        for name, score in top_features_global[:6]
    ]

    return PredictionResponse(
        predicted_g3=round(predicted_g3, 2),
        predicted_grade_percent=percent,
        pass_fail=pass_fail,
        top_features=top_features,
    )
