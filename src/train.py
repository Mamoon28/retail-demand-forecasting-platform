from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

from src.baselines import arima_forecast, rolling_seasonal_naive
from src.config import settings
from src.extract import load_category_demand
from src.features import make_windows, regularise_daily_series, time_split
from src.metrics import regression_metrics
from src.model import build_lstm


def main() -> None:
    artifact_dir = Path(settings.model_artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    raw = load_category_demand(settings.forecast_category)
    df = regularise_daily_series(raw)
    values = df["units_sold"].astype(float).to_numpy()

    train_values, test_values = time_split(values, test_days=min(56, max(14, len(values) // 5)))

    naive_pred = rolling_seasonal_naive(train_values, test_values, season_length=7)
    naive_metrics = regression_metrics(test_values, naive_pred)

    arima_pred = arima_forecast(train_values, horizon=len(test_values))
    arima_metrics = regression_metrics(test_values, arima_pred)

    scaler = MinMaxScaler()
    scaler.fit(train_values.reshape(-1, 1))
    scaled_all = scaler.transform(values.reshape(-1, 1)).reshape(-1)

    split_idx = len(train_values)
    x_all, y_all = make_windows(scaled_all, settings.lookback_days)
    target_indices = np.arange(settings.lookback_days, len(scaled_all))
    train_mask = target_indices < split_idx
    test_mask = target_indices >= split_idx

    x_train = x_all[train_mask][..., np.newaxis]
    y_train = y_all[train_mask]
    x_test = x_all[test_mask][..., np.newaxis]
    y_test = y_all[test_mask]

    model = build_lstm(settings.lookback_days)
    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True)
    ]
    model.fit(
        x_train,
        y_train,
        validation_split=0.2,
        epochs=60,
        batch_size=32,
        shuffle=False,
        callbacks=callbacks,
        verbose=1,
    )

    pred_scaled = model.predict(x_test, verbose=0).reshape(-1, 1)
    lstm_pred = scaler.inverse_transform(pred_scaled).reshape(-1)
    lstm_true = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(-1)
    lstm_pred = np.clip(lstm_pred, 0, None)
    lstm_metrics = regression_metrics(lstm_true, lstm_pred)

    model.save(artifact_dir / "demand_lstm.keras")
    joblib.dump(scaler, artifact_dir / "scaler.pkl")

    metrics = {
        "category": settings.forecast_category,
        "lookback_days": settings.lookback_days,
        "test_days": int(len(test_values)),
        "seasonal_naive": naive_metrics,
        "arima_2_1_2": arima_metrics,
        "lstm": lstm_metrics,
    }
    (artifact_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    (artifact_dir / "metadata.json").write_text(
        json.dumps(
            {
                "category": settings.forecast_category,
                "lookback_days": settings.lookback_days,
                "forecast_horizon": settings.forecast_horizon,
                "last_training_date": str(df["order_date"].max().date()),
            },
            indent=2,
        )
    )

    plt.figure(figsize=(10, 4))
    plt.plot(lstm_true, label="Actual")
    plt.plot(lstm_pred, label="LSTM")
    plt.plot(naive_pred[-len(lstm_true) :], label="Seasonal naive", alpha=0.8)
    plt.title(f"Demand forecast evaluation — {settings.forecast_category}")
    plt.xlabel("Test day")
    plt.ylabel("Units sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig(artifact_dir / "forecast_evaluation.png", dpi=150)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
