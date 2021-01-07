import argparse
import os
import sys

import requests

from classes.AnkiApi import AnkiApi
from classes.Converter import Converter
from classes.Parser import Parser


def init_argparse():
    arg_parser = argparse.ArgumentParser(
        prog="ankify",
        usage="%(prog)s [FILE]...",
        description="Extract Anki cards from your Markdown notes."
    )

    arg_parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        type=str,
        help="the path to the file")

    return arg_parser


def create_cards(file_path):
    print(f"Starting to create cards from \"{file_path}\"!")

    abs_file_path = os.path.abspath(file_path)

    # We need to change working directory because images in file can have relative path
    os.chdir(os.path.dirname(abs_file_path))

    note_parser = Parser(abs_file_path)

    print("Getting cards from the file...")
    try:
        cards_list = note_parser.collect_cards()
    except ValueError as e:
        print(f'ERROR: {e.args[0]}')
        sys.exit()

    number_of_cards = len(cards_list)
    if number_of_cards == 0:
        print("ERROR: Cards weren't found in the file.\n")
        sys.exit()

    print(f"Found {number_of_cards} cards!")

    print("Converting cards to the html...")
    Converter.convert_cards(cards_list)

    print("Sending cards...")
    try:
        AnkiApi.add_cards(cards_list)
    except requests.exceptions.ConnectionError:
        print("ERROR: Couldn't connect to Anki. "
              "Please, check that Anki is working and you have AnkiConnect plugin installed.")
        sys.exit()


def main():
    arg_parser = init_argparse()
    args = arg_parser.parse_args()

    for file in args.files:
        if not os.path.isfile(file):
            print(f"The file specified doesn't exist: \"{file}\"")
            sys.exit()

    original_directory = os.getcwd()
    for file in args.files:
        create_cards(file)
        os.chdir(original_directory)


if __name__ == "__main__":
    main()
