import pandas as pd
import time
from threading import Thread
from collections import deque
from conc_extract import extractDeque

transformDeque = deque()

class ThreadedTransformer(Thread):
    def __init__(self, ticksPerBar=100):
        super().__init__(daemon=False)
        self.ticksPerBar = ticksPerBar
        self.currentCandle = None

    def run(self):
        while True:
            if not extractDeque:
                time.sleep(0.005)
                continue

            tick = extractDeque.popleft()

            ts = tick["Timestamp"]
            secondTs = ts.replace(microsecond=0)
            price = tick["Price"]
            volume = tick["Volume"]

            # Start new candle if none exists
            if self.currentCandle is None:
                self.currentStartTime = secondTs
                self.currentCandle = {
                    "Timestamp": ts,
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "volume": volume
                }
                continue

            # if 1 second passed finalize candle
            if (ts - self.currentStartTime).total_seconds() >= 1.0:
                transformDeque.append(self.currentCandle)

                # Start new candle
                self.currentStartTime = secondTs
                self.currentCandle = {
                    "Timestamp": ts,
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "volume": volume
                }
                continue

            # Update live candle
            self.currentCandle["Timestamp"] = ts
            self.currentCandle["close"] = price
            self.currentCandle["high"] = max(self.currentCandle["high"], price)
            self.currentCandle["low"] = min(self.currentCandle["low"], price)
            self.currentCandle["volume"] += volume
            #print(len(transformDeque))

