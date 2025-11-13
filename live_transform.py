import pandas as pd
from pathlib import Path

class LiveTransformer:
    def __init__(self, input_path, output_dir="data/processed"):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # Take data from live data stream from csv and aggregate into OHLCV in Parquet
    def aggregate_to_ohlcv(self, freq="1s"):
        df = pd.read_csv(self.input_path, parse_dates=["Timestamp"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df.set_index("Timestamp", inplace=True)
        price_ohlc = (
            df.groupby("Ticker")["Price"]
            .resample(freq)
            .ohlc()
            .dropna()
        )

        volume = (
            df.groupby("Ticker")["Volume"]
            .resample(freq)
            .sum()
            .dropna()
        )

        ohlcv = pd.concat([price_ohlc, volume], axis=1).reset_index()
        ohlcv.to_parquet(self.output_dir / f"ohlcv_{freq}.parquet")
        return ohlcv