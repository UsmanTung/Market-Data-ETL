from live_extract import LiveExtractor
from live_transform import LiveTransformer
import live_load

def main():

    tickers = ["NVDA"]
    startingPrices = [100.0, 200.0, 300.0, 400.0, 500.0]
    #start = "2025-11-09"
    #end = "2025-11-11"

    #fetcher = DataFetcher(tickers, start, end, interval="1d")
    #fetcher.fetch()
    #print(f"Data fetched and saved to ./data/raw")

    extractor = LiveExtractor(tickers, startingPrices)
    rawDataPath = extractor.stream_to_csv(15)

    # Writes to ./processed/
    transformer = LiveTransformer(rawDataPath)
    ohlcvData= transformer.aggregate_to_ohlcv("1s")

    live_load.app.run(debug=True)




if __name__ == "__main__":
    main()