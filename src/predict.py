from __future__ import annotations

import numpy as np


def recursive_forecast(model, scaler, history: list[float], lookback: int, horizon: int) -> list[float]:
    if len(history) < lookback:
        raise ValueError(f"At least {lookback} historical observations are required.")

    working = [float(x) for x in history]
    predictions: list[float] = []

    for _ in range(horizon):
        window = np.asarray(working[-lookback:], dtype=np.float32).reshape(-1, 1)
        scaled = scaler.transform(window).reshape(1, lookback, 1)
        pred_scaled = float(model.predict(scaled, verbose=0).reshape(-1)[0])
        pred = float(scaler.inverse_transform([[pred_scaled]])[0, 0])
        pred = max(0.0, pred)
        predictions.append(pred)
        working.append(pred)

    return predictions
