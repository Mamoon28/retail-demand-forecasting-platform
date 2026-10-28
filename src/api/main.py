from __future__ import annotations

import json
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from tensorflow import keras

from src.config import settings
from src.predict import recursive_forecast

app = FastAPI(
    title="Retail Demand Forecasting API",
    version="1.0.0",
    description="Serves short-horizon demand forecasts from a trained TensorFlow/Keras model.",
)

ARTIFACT_DIR = Path(settings.model_artifact_dir)
MODEL_PATH = ARTIFACT_DIR / "demand_lstm.keras"
SCALER_PATH = ARTIFACT_DIR / "scaler.pkl"
METADATA_PATH = ARTIFACT_DIR / "metadata.json"

model = None
scaler = None
metadata = None


class ForecastRequest(BaseModel):
    recent_units_sold: list[float] = Field(
        ...,
        description="Most recent daily demand observations, oldest to newest.",
    )
    horizon: int = Field(default=7, ge=1, le=30)


class ForecastResponse(BaseModel):
    category: str
    horizon: int
    forecast: list[float]


@app.on_event("startup")
def load_artifacts() -> None:
    global model, scaler, metadata
    if MODEL_PATH.exists() and SCALER_PATH.exists() and METADATA_PATH.exists():
        model = keras.models.load_model(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        metadata = json.loads(METADATA_PATH.read_text())


@app.get("/health")
def health() -> dict[str, str]:
    status = "ready" if model is not None else "model_not_loaded"
    return {"status": status}


@app.post("/predict", response_model=ForecastResponse)
def predict(request: ForecastRequest) -> ForecastResponse:
    if model is None or scaler is None or metadata is None:
        raise HTTPException(
            status_code=503, detail="Model artifacts are not loaded. Train the model first."
        )

    lookback = int(metadata["lookback_days"])
    if len(request.recent_units_sold) < lookback:
        raise HTTPException(
            status_code=422,
            detail=f"Provide at least {lookback} recent daily observations.",
        )

    values = recursive_forecast(
        model=model,
        scaler=scaler,
        history=request.recent_units_sold,
        lookback=lookback,
        horizon=request.horizon,
    )
    return ForecastResponse(
        category=str(metadata["category"]),
        horizon=request.horizon,
        forecast=[round(x, 2) for x in values],
    )
