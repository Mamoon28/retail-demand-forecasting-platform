from __future__ import annotations

from tensorflow import keras


def build_lstm(lookback: int) -> keras.Model:
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(lookback, 1)),
            keras.layers.LSTM(64, return_sequences=True),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(32),
            keras.layers.Dense(16, activation="relu"),
            keras.layers.Dense(1),
        ]
    )
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="mse",
        metrics=[keras.metrics.MeanAbsoluteError(name="mae")],
    )
    return model
