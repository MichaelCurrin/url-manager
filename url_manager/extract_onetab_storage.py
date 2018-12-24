#!/usr/bin/env python3
"""
OneTab storage extractor.

Parse OneTab data stored in Firefox's JSON or Chrome's LevelDB storage,
then pretty print the user data.

See the docs/browsers_onetab_extraction.md file for instructions.
"""
import argparse
import json
import re
import os

import plyvel

from lib import BROWSER_PROFILE_DIRS


FIREFOX_ONETAB = "browser-extension-data/extension@one-tab.com/storage.js"
CHROME_ONETAB = "Local Storage/leveldb"

# The plyvel docs recommend referencing LevelDB keys in the
# binary form (which is how they are stored).
LEVELDB_ONETAB_KEY = b'_chrome-extension://chphlpgkkbolifaimnlloiipkdnihall\x00\x01state'


def parse_leveldb_bytes(data_bytes):
    """
    Parse LevelDB OneTab data from bytes to dict.

    The encoding of the bytes state data in the database is not UTF-8 or
    ASCII, so this function takes unreadable data and makes sense of it. This
    was done by inspection and experimenting until the result has a parsable
    JSON structure, clean URLs values and mostly clean titles (which can
    get overwritten later anyway by hand or reading fresh metadata from the
    site).

    The b"\x00" character is repeated throughout at every second character and
    shows as a box when printed. It could be a null character, but
    apparently the meaning of the character depends on the encoding so it could
    be anything. Dropping it mostly works well.

    When keeping it in during testing with `data.decode('ascii', errors=ignore)`
    meant that some important fields are garbled. When removing this character
    and not using `.decode`, the str representation looks much neater and is
    very useful. It has few symbols (punctuation, and emojis and escaped quotes)
    which need to be corrected.

    :param data_bytes: OneTab data as a bytes string, as retrieved from
        the Chrome LevelDB storage. This should be in a JSON format
        when viewed as a string.

    :return: dict of data.
    """
    data_bytes = data_bytes.replace(b"\x00", b"")

    # Get string representation of bytes to avoid issues caused by
    # decoding. Then remove the leading b" and trailing ".
    data_str = str(data_bytes)[2:-1]

    # Turn escaped double slash into single slash and
    # escaped single quotes to a single quote.
    data_str = data_str.replace("\\\\", "\\").replace("\\'", "'")

    # Remove carriage returns which sometimes appear in titles.
    # There is no "\n" after it in the cases seen. This replacment
    # could break Windows compatibility of this project.
    data_str = data_str.replace("\\r", "")

    # Remove any characters which still look like bytes.
    data_str = re.sub(r"\\x\w\w", "⍰", data_str)

    return json.loads(data_str)


def read_storage(browser, username):
    """
    Read OneTab JSON or leveldb data on disk and return as dict.

    Reads Chrome or Chromium leveldb database or a Firefox storage JSON.
    Note that the useful value in the Firefox storage is a string which needs
    parsing.

    :return data: dict of OneTab state data in the follow format:
        {
            "tabGroups": [
                {
                    "id": "GP57H3IsBnofq1DwAM6W5-",
                    "tabsMeta": [
                        {
                            "id": "vf9z57SxxWwoPBJk5ImBD0",
                            "url": "https://example.com",
                            "title": "Example website"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    :raises plyvel._plyvel.IOError: This error occurs if the database locked by
        another process which has it open still, such as script or your
        actual browser.
    """
    browser_profile_dir = BROWSER_PROFILE_DIRS[browser]
    chrome_like = (browser.startswith('Chrom'))
    in_path = os.path.join(browser_profile_dir, username,
                           CHROME_ONETAB if chrome_like else FIREFOX_ONETAB)

    if chrome_like:
        db = plyvel.DB(in_path)
        state_data_bytes = db.get(LEVELDB_ONETAB_KEY)
        data = parse_leveldb_bytes(state_data_bytes)
    else:
        with open(in_path) as f_in:
            raw_data = json.load(f_in)
        data = json.loads(raw_data['state'])

    return data


def main():
    """
    Command-line function to read OneTab storage file and print to std out.
    """
    parser = argparse.ArgumentParser("OneTab storage extractor")

    parser.add_argument(
        'BROWSER',
        choices=['Chrome', 'Chromium', 'Firefox']
    )
    parser.add_argument(
        'USERNAME',
        help="You browser account username. e.g. 'Default' or 'Profile 1' for"
             " Chrome or 'abcdef.default' for Firefox."
    )

    args = parser.parse_args()

    data = read_storage(args.BROWSER, args.USERNAME)
    print(json.dumps(data, indent=4))


if __name__ == '__main__':
    main()
