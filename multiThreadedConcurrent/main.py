from conc_extract import ThreadedExtractor
from conc_transform import ThreadedTransformer
from conc_load import app


def main():
    extractor = ThreadedExtractor(["NVDA"], [100], interval=0.1, duration = 100)
    transformer = ThreadedTransformer()
    extractor.start()
    transformer.start()
    app.run(debug=True)


if __name__ == "__main__":
    main()