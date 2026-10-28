from __future__ import annotations

import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def seasonal_naive(history: np.ndarray, horizon: int, season_length: int = 7) -> np.ndarray:
    history = np.asarray(history, dtype=float).reshape(-1)
    if len(history) < season_length:
        raise ValueError("History must contain at least one full seasonal cycle.")
    pattern = history[-season_length:]
    repeats = int(np.ceil(horizon / season_length))
    return np.tile(pattern, repeats)[:horizon]


def rolling_seasonal_naive(train: np.ndarray, test: np.ndarray, season_length: int = 7) -> np.ndarray:
    history = list(np.asarray(train, dtype=float).reshape(-1))
    preds = []
    for actual in np.asarray(test, dtype=float).reshape(-1):
        preds.append(history[-season_length])
        history.append(float(actual))
    return np.asarray(preds)


def arima_forecast(train: np.ndarray, horizon: int, order: tuple[int, int, int] = (2, 1, 2)) -> np.ndarray:
    model = ARIMA(np.asarray(train, dtype=float), order=order)
    fitted = model.fit()
    return np.asarray(fitted.forecast(steps=horizon), dtype=float)
