import numpy as np

from src.baselines import seasonal_naive


def test_seasonal_naive_repeats_last_week():
    history = np.arange(1, 15)
    pred = seasonal_naive(history, horizon=10, season_length=7)
    assert pred.tolist() == [8, 9, 10, 11, 12, 13, 14, 8, 9, 10]
