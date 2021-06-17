#!/usr/bin/env python3
"""
OneTab storage extractor.

Parse OneTab data stored in Firefox's JSON file or Chrome's LevelDB
storage, then pretty print the OneTab user data as JSON.

See the docs/browsers_onetab_extraction.md file for instructions.
"""
import argparse
import json
import os
import re
import sys

import plyvel

from lib import BROWSER_PROFILE_DIRS
from lib.config import AppConf

conf = AppConf()

# Path to OneTab data within a directory for a browser user. This
# is for both Linux and Mac.
FIREFOX_ONETAB = "browser-extension-data/extension@one-tab.com/storage.js"
CHROME_ONETAB = "Local Storage/leveldb"

# The plyvel docs recommend referencing LevelDB keys in the
# binary form (which is how they are stored).
LEVELDB_ONETAB_KEY = (
    b"_chrome-extension://chphlpgkkbolifaimnlloiipkdnihall\x00\x01state"
)


def parse_leveldb_bytes(data_bytes):
    """
    Parse LevelDB OneTab data from bytes to dict.

    The bytes data is first cleaned then parsed as JSON. On a parsing error,
    write out raw and cleaned inputs to the debug directory,
    print the error message and exit with an error status code.

    The encoding of the bytes state data in the database is not UTF-8 or
    ASCII, so this function takes unreadable data and makes sense of it. This
    was done by inspection and experimenting until the result has a parsable
    JSON structure, clean URLs values and mostly clean titles (which can
    get overwritten later anyway by hand or reading fresh metadata from the
    site).

    The b"\x00" character is repeated throughout at every second character and
    shows as a box when printed. It could be a null character, but
    apparently the meaning of the character depends on the encoding, so it could
    be anything. Dropping it completely mostly works well.
    When keeping it in during testing with `data.decode('ascii', errors=ignore)`
    meant that some functional JSON values were garbled. When replacing this
    character and not using `.decode`, the str representation as used below
    looks much neater and is very useful. It has a few unimportant
    symbols (punctuation, and emojis and escaped quotes) in titles
    which could be corrected later or ignored - getting a fresh title would be
    easier.

    :param data_bytes: OneTab data as a bytes string, as retrieved from
        the Chrome LevelDB storage. This should be in a JSON format
        when viewed as a string.

    :return: dict of data.
    """
    # Remove this very common but somehow non-functional character.
    data_bytes = data_bytes.replace(b"\x00", b"")

    # Get string representation of bytes to avoid issues caused by
    # decoding. Then remove the leading b" and trailing ".
    raw_str = str(data_bytes)[2:-1]

    # Convert double backlash to single. This handles cases like '\\"' => '\"'.
    data_str = raw_str.replace("\\\\", "\\")

    # Edgecase handled by inspection on a title about union and intersection,
    data_str = data_str.replace('(*")', "(&)")
    data_str = data_str.replace('()")', "(|)")

    # Unescape single quote.
    data_str = data_str.replace(r"\'", r"'")

    # Remove literal markers for carriage returns which sometimes appear in
    # titles. There are no "\n" characters after it in the cases observed.
    data_str = data_str.replace("\\r", "")

    # Handle cases where the original data has a unicode character such as
    # '•' (b'\xe2\x80\xa2') which is unnecessarily converted to double quotes,
    # even while in the bytes form. The cases of it had a space on each side
    # so in this limited solution we replace that double quote only and not
    # the double quotes which are functional, since there is no other way for
    # now.
    data_str = data_str.replace(' " ', " ⍰ ")

    # Remove any characters which still look like bytes.
    data_str = re.sub(r"\\x\w\w", "⍰", data_str)

    data_str = data_str.replace("\\⍰", "⍰")

    try:
        return json.loads(data_str)
    except json.JSONDecodeError as e:
        print(f"{type(e).__name__}: {str(e)}")

        var_dir = conf.get("text_files", "debug")
        raw_path = os.path.join(var_dir, "leveldb_onetab_raw.json")
        cleaned_path = os.path.join(var_dir, "leveldb_onetab_cleaned.json")
        with open(raw_path, "w") as f_out:
            f_out.writelines(raw_str)
        with open(cleaned_path, "w") as f_out:
            f_out.writelines(data_str)
        print(f"Wrote raw data to: {raw_path}")
        print(
            f"Wrote cleaned data containing JSON formatting error to:"
            f" {cleaned_path}"
        )

        sys.exit(1)


def read_storage(browser, username):
    """
    Read OneTab JSON or LevelDB data on disk and return as dict.

    Read Chrome or Chromium leveldb database or a Firefox storage JSON
    for a specified browser user.

    :browser: Name of browser. This must be one of the keys of
        BROWSER_PROFILE_DIRS otherwise an error will be raised.
    :username: Name of browser user for the specified browser. An
        error will be raised if this is not valid.

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
    :raises plyvel._plyvel.IOError: Occurs if the file does not exist or the
        database is locked by another process which has it open still, such as
        a script or your actual browser.
    :raises FileNotFoundError: If the Firefox file cannot be found to the given
        username.
    """
    browser_profile_dir = BROWSER_PROFILE_DIRS[browser]
    is_chrome_like = browser.startswith("Chrom")
    in_path = os.path.join(
        browser_profile_dir,
        username,
        CHROME_ONETAB if is_chrome_like else FIREFOX_ONETAB,
    )

    if is_chrome_like:
        db = plyvel.DB(in_path)
        state_data_bytes = db.get(LEVELDB_ONETAB_KEY)
        data = parse_leveldb_bytes(state_data_bytes)
    else:
        with open(in_path) as f_in:
            raw_data = json.load(f_in)
        # The value within the JSON is a plain string and also needs parsing.
        data = json.loads(raw_data["state"])

    return data


def main():
    """
    Command-line function to read OneTab storage file and print to std out.
    """
    parser = argparse.ArgumentParser("OneTab storage extractor")

    parser.add_argument("BROWSER", choices=sorted(BROWSER_PROFILE_DIRS.keys()))
    parser.add_argument(
        "USERNAME",
        help="You browser account username. e.g. 'Default' or 'Profile 1' for"
        " Chrome or 'abcdef.default' for Firefox. See browser_onetab_extraction.md in docs.",
    )

    args = parser.parse_args()

    data = read_storage(args.BROWSER, args.USERNAME)
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
