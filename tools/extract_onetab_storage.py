#!/usr/bin/env python3
"""
OneTab JSON extractor.

Expects a path to a JSON OneTab file (such as the one created by the
Firefox OneTabe extension) and prints to stdout as a prettified JSON. This
can be redirected to a text file in the project. See the
docs/browsers_onetab_extraction.md file for instructions on input and output
paths.

This script cannot be used for Chrome's OneTab data, since that is stored in
.ldb (leveldb) format instead.

The writing out of a new file could be replaced by using a symlink or copy of
the original file and later getting the 'state' data.  However the steps for
this script are consistent with the Chrome approach applied, so it is easier
just to keep this the same.
"""
import json
import sys


def get_data(json_in_path):
    """
    Read in a specified OneTab JSON and return user data as a dict.

    FireFox OneTab data is stored in a JSON file. This must be parsed to lookup
    the 'storage' key's value. Then the value for storage key must be parsed
    from a JSON formatted string to a Python dict.

    @return user_data: dict of 'state' data within the parsed JSON file. The
        other keys have data which is not of interest for this project.
    """
    with open(json_in_path) as f_in:
        raw_data = json.load(f_in)

    user_data = json.loads(raw_data['state'])

    return user_data


def pretty_print(json_in_path):
    """
    Read data for the specified JSON file and pretty print to stdout.

    @return: None
    """
    user_data = get_data(json_in_path)
    print(json.dumps(user_data, indent=4))

    return None


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
