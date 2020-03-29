import argparse
from pdf_to_tiff import convert


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input path")
    parser.add_argument("--output", help="output path")
    args = parser.parse_args()

    convert(args.input, args.output)
