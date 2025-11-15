from conc_extract import ThreadedExtractor
from conc_transform import ThreadedTransformer
import conc_load
def main():
    interval = 0.002
    extractor = ThreadedExtractor(["NVDA"], [100], interval=interval, duration = 30)
    transformer = ThreadedTransformer(int(1/interval))

    extractor.start()
    transformer.start()

    conc_load.init_callbacks(transformer)
    conc_load.app.run(debug=True)


if __name__ == "__main__":
    main()