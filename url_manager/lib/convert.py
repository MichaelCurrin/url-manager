"""
Lib convert application file.
"""
import datetime


# The desired format for datetime values in output JSON files.
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def from_chrome_epoch(value):
    """
    Convert a timestamp from Chrome's epoch format to a datetime object.

    Conversion from Chrome epoch (such as for bookmark or history record)
    to unix timestamp is based on the formula here:
        http://linuxsleuthing.blogspot.co.za/2011/06/decoding-google-chrome-timestamps-in.html

    :param value: Timestamp value in Chrome epoch format. As either an
        int, float or str. e.g. 13182380056677741

        From: https://stackoverflow.com/questions/539900/google-bookmark-export-date-format
            "Chrome uses a modified form of the Windows Time format
            ("Windows epoch") for its timestamps, both in the Bookmarks file
            and the history files. The Windows Time format is the number of
            100ns-es since January 1, 1601. The Chrome format is the number of
            microseconds since the same date, and thus 1/10 as large."
        See also:
            http://fileformats.archiveteam.org/wiki/Chrome_bookmarks

    :return: datetime.datetime object created from value.
    """
    unix_timestamp = float(value) / 1000000 - 11644473600

    return datetime.datetime.fromtimestamp(unix_timestamp)


def from_onetab_time(value):
    """
    Convert time from Onetab's epoch to Python datetime object.

    :param value: Numeric value for the OneTab browser extension's
        epoch time. This follows the unix timestamp standard, but in
        milliseconds.

    :return: datetime.datetime object created from value.
    """
    seconds = float(value) / 1000

    return datetime.datetime.fromtimestamp(seconds)
