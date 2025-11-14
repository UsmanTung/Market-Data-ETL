from conc_extract import ThreadedExtractor
from conc_transform import ThreadedTransformer


def main():
    extractor = ThreadedExtractor(["NVDA"], [100])
    transformer = ThreadedTransformer()
    extractor.start()
    transformer.start()
    extractor.join()
    transformer.join()


if __name__ == "__main__":
    main()