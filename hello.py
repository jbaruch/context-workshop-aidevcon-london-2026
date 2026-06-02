import argparse


def greet(name="World"):
    return f"Hello, {name}!"


def main():
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument("--name", default="World", help="Name to greet (default: World)")
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
