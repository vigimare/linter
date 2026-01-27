import argparse
from os.path import isfile
from typing import cast

from linter import Linter
from linter.exceptions import LinterError, LinterSuccess


def parse_args():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--xsd-path", type=str, default="./xsd", help="Path to xsd files")
    _ = parser.add_argument("--xml-files", nargs="+", required=True, help="XML files to validate")
    return parser.parse_args()


def main():
    args = parse_args()

    xml_files: list[str] = args.xml_files
    xsd_path: str = cast(str, args.xsd_path)

    existing_files = [file for file in xml_files if isfile(file)]
    #print([isfile(file) for file in xml_files])
    if not existing_files:
        raise FileNotFoundError(f"Failed to find any of the specified XML files '{xml_files}'")

    linter = Linter(xsd_path)
    print("Linting complete")
    success = []
    error = []
    for file in existing_files:
        result = linter.validate(file)
        if isinstance(result, LinterSuccess):
            success.append((file, str(result)))
        if isinstance(result, LinterError):
            error.append((file, str(result)))
    print("Successful files:")
    for file, msg in success:
        print(f"  {file} - {msg}")
    if error:
        print("\nFailed files:")
        for file, msg in error:
            print(f"  {file} - {msg}")


if __name__ == "__main__":
    main()
