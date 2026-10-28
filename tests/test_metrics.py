import numpy as np

from src.metrics import regression_metrics


def test_regression_metrics_perfect_prediction():
    y = np.array([1, 2, 3], dtype=float)
    metrics = regression_metrics(y, y)
    assert metrics["mae"] == 0.0
    assert metrics["rmse"] == 0.0
    assert metrics["mape_pct"] == 0.0
