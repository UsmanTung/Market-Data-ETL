from conc_extract import ThreadedExtractor
from conc_transform import ThreadedTransformer
import conc_load
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run multi-threaded market simulator.")
    parser.add_argument(
        "--duration",
        type=int,
        default=60,                   # default = 1 minute
        help="Duration to run the simulator in seconds (default: 60)"
    )
    args = parser.parse_args()

    interval = 0.001
    duration = args.duration
    extractor = ThreadedExtractor(["NVDA"], [100], interval=interval, duration = duration)
    transformer = ThreadedTransformer(int(1/interval))

    extractor.start()
    transformer.start()

    conc_load.init_callbacks(transformer)
    conc_load.app.run(debug=True)


if __name__ == "__main__":
    main()