import argparse

DEFAULT_NAME = "World"


def greet(name=DEFAULT_NAME):
    return f"Hello, {name}!"


def main():
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument("--name", default=DEFAULT_NAME, help=f"Name to greet (default: {DEFAULT_NAME})")
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
