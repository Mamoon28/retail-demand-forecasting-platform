from __future__ import annotations

import numpy as np
import pandas as pd


def regularise_daily_series(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing calendar dates so zeros represent days with no observed sales."""
    out = df.copy()
    out["order_date"] = pd.to_datetime(out["order_date"])
    out = out.sort_values("order_date")
    full_range = pd.date_range(out["order_date"].min(), out["order_date"].max(), freq="D")
    out = out.set_index("order_date").reindex(full_range)
    out.index.name = "order_date"

    for col in ["units_sold", "orders", "gross_revenue"]:
        if col in out.columns:
            out[col] = out[col].fillna(0)

    if "average_selling_price" in out.columns:
        out["average_selling_price"] = out["average_selling_price"].ffill().bfill()

    if "product_category" in out.columns:
        out["product_category"] = out["product_category"].ffill().bfill()

    return out.reset_index()


def make_windows(values: np.ndarray, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    """Convert a 1D demand series into supervised lookback windows."""
    values = np.asarray(values, dtype=np.float32).reshape(-1)
    if len(values) <= lookback:
        raise ValueError("Series must be longer than lookback window.")

    x, y = [], []
    for idx in range(lookback, len(values)):
        x.append(values[idx - lookback : idx])
        y.append(values[idx])
    return np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.float32)


def time_split(values: np.ndarray, test_days: int = 56) -> tuple[np.ndarray, np.ndarray]:
    """Chronological split to avoid time-series leakage."""
    values = np.asarray(values, dtype=np.float32)
    if len(values) <= test_days:
        raise ValueError("Series is too short for requested test window.")
    return values[:-test_days], values[-test_days:]
