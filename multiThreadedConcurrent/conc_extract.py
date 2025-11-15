
import numpy as np
import time
from datetime import datetime, timezone, timedelta
from threading import Thread
from collections import deque

extractDeque = deque()

class ThreadedExtractor(Thread):
    def __init__(self, tickers, startingPrices, interval=0.01, duration = 10):
        super().__init__(daemon=False)
        self.startingPrices = startingPrices
        self.tickers = tickers
        self.interval = interval
        self.current_prices = {t: s for t, s in zip(tickers, startingPrices)}
        self.duration = duration

    def run(self):
        curr = datetime.now(timezone.utc)
    
        while datetime.now(timezone.utc) - curr < timedelta(seconds=self.duration):
            
            for t in self.tickers:
                change = np.random.normal(0, 0.5)
                timestamp = datetime.now(timezone.utc)
                self.current_prices[t] = self.current_prices[t] + change
                extractDeque.append({
                    "Timestamp": timestamp,
                    "Ticker": t,
                    "Price": round(self.current_prices[t], 2),
                    "Volume": np.random.randint(100, 1000)
                })
            time.sleep(self.interval)
        #print(len(extractDeque))

