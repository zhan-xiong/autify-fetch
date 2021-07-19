import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Downloads a given set of URLs")
    parser.add_argument("-m", "--metadata", action="store_true")
    parser.add_argument("urls", nargs="*")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args.urls)
    print(args.metadata)
