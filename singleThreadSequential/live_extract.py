
import pandas as pd
import numpy as np
import time
from datetime import datetime, timezone
from pathlib import Path

# Simulates a live data fetch

class LiveExtractor:
    def __init__(self, tickers, startingPrices, interval=0.1, output_dir="data/raw"):
        self.startingPrices = startingPrices
        self.tickers = tickers
        # seconds between updates
        self.interval = interval
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # simulate starting prices
        self.current_prices = {t: s for t, s in zip(tickers, startingPrices)}

    def __generate_tick(self):
        rows = []
        timestamp = datetime.now(timezone.utc)
        # Random price movements for each ticker
        for t in self.tickers:
            change = np.random.normal(0, 0.5)
            self.current_prices[t] = self.current_prices[t] + change
            rows.append({
                "Timestamp": timestamp,
                "Ticker": t,
                "Price": round(self.current_prices[t], 2),
                "Volume": np.random.randint(100, 1000)
            })
        return pd.DataFrame(rows)


    # Writes ticks to csv
    def stream_to_csv(self, duration=5):
        output_file = self.output_dir / "stream_ticks.csv"
        start_time = time.time()
        print(f"Simulating market data for {duration} seconds...")

        while time.time() - start_time < duration:
            df = self.__generate_tick()
            df.to_csv(output_file, mode='a', header=not output_file.exists(), index=False)
            print(f"[{datetime.now(timezone.utc)}] Appended {len(df)} new ticks.")
            time.sleep(self.interval)

        print(f"Finished. Data saved to {output_file}")
        return output_file
