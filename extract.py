import yfinance as yf
import pandas as pd
from pathlib import Path


class DataFetcher:
    def __init__(self, tickers, start, end, interval):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.interval = interval
        Path("data/raw").mkdir(parents=True, exist_ok=True)

    def fetch(self):
        data = yf.download(
            self.tickers,
            start=self.start,
            end=self.end,
            interval=self.interval,
            group_by="ticker",
            auto_adjust=True
        )
        for ticker in self.tickers:
            df = data[ticker].dropna()
            path = Path(f"data/raw/{ticker}.csv")
            df.to_csv(path)
        return data