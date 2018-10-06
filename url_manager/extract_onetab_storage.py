#!/usr/bin/env python3
"""
OneTab Firefox data extractor.

See the docs/browsers_onetab_extraction.md file for instructions.
"""
import json
import sys


def pretty_print(json_in_path):
    """
    Expect a Onetab JSON path, remove unneeded data and pretty print to stdout.

    @return: None
    """
    with open(json_in_path) as f_in:
        raw_data = json.load(f_in)

    user_data = json.loads(raw_data['state'])
    print(json.dumps(user_data, indent=4))


def main(args):
    """
    Command-line function to read OneTab storage file and print to std out.
    """
    if not args or (set(('-h', '--help')) & set(args)):
        print("Usage: {file} STORAGE_JSON_PATH".format(file=__file__))
    else:
        json_in_path = args.pop(0)
        pretty_print(json_in_path)


if __name__ == '__main__':
    main(sys.argv[1:])
