from extract import DataFetcher

def main():

    tickers = ["NVDA"]
    start = "2025-11-09"
    end = "2025-11-11"

    fetcher = DataFetcher(tickers, start, end, interval="1d")
    fetcher.fetch()
    print(f"Data fetched and saved to ./data/raw")


if __name__ == "__main__":
    main()