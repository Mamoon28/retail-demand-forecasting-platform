import numpy as np
import pandas as pd

from src.features import make_windows, regularise_daily_series, time_split


def test_regularise_daily_series_fills_missing_dates():
    df = pd.DataFrame(
        {
            "order_date": ["2026-01-01", "2026-01-03"],
            "product_category": ["A", "A"],
            "units_sold": [3, 5],
        }
    )
    out = regularise_daily_series(df)
    assert len(out) == 3
    assert out.loc[1, "units_sold"] == 0


def test_make_windows_shape():
    x, y = make_windows(np.arange(10), lookback=3)
    assert x.shape == (7, 3)
    assert y.shape == (7,)
    assert x[0].tolist() == [0.0, 1.0, 2.0]
    assert y[0] == 3.0


def test_time_split_is_chronological():
    train, test = time_split(np.arange(20), test_days=5)
    assert train[-1] == 14
    assert test[0] == 15
