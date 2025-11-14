from conc_extract import ThreadedExtractor


def main():
    extractor = ThreadedExtractor(["NVDA"], [100])
    extractor.start()
    extractor.join()


if __name__ == "__main__":
    main()