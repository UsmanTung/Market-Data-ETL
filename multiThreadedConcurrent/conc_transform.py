# transformer.py
import pandas as pd
import time
from threading import Thread
from collections import deque
from conc_extract import extractDeque

transformDeque = deque()

class ThreadedTransformer(Thread):
    def __init__(self, ticks_per_bar=10):
        super().__init__(daemon=False)
        self.ticks_per_bar = ticks_per_bar

    def run(self):
        while True:
            if len(extractDeque) < self.ticks_per_bar:
                time.sleep(0.025)
                continue

            ticks = list(extractDeque)[-self.ticks_per_bar:]
            df = pd.DataFrame(ticks)
            df = df.sort_values("Timestamp")
            ohlcv = {
                "Timestamp": df["Timestamp"].iloc[-1],
                "Ticker": df["Ticker"].iloc[0],
                "open": df["Price"].iloc[0],
                "high": df["Price"].max(),
                "low": df["Price"].min(),
                "close": df["Price"].iloc[-1],
                "volume": df["Volume"].sum(),
            }
            transformDeque.append(ohlcv)
            time.sleep(0.05)
            #print(len(transformDeque))

