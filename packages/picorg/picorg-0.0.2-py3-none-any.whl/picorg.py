import argparse

from rename import do_work as do_rename
from duplicates import find_duplicates as do_duplicates


def main():
    parser = argparse.ArgumentParser(
        description="A script that helps you organize your pictures."
    )
    parser.add_argument(
        "-a",
        "--action",
        choices=["rename", "duplicates"],
        required=True,
        help="The action to execute.",
    )

    args = parser.parse_args()

    if args.action == "rename":
        do_rename()
    elif args.action == "duplicates":
        do_duplicates()


if __name__ == "__main__":
    main()
