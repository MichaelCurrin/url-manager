"""
Lib convert application file.
"""
import datetime


# The desired format for datetime values in output JSON files.
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def from_chrome_time(chrome_epoch):
    """
    Convert timestamp from Chrome's epoch format to a datetime object.

    Chrome stores timestamps for bookmark and history records in the
    Chrome epoch format.
        See answer at: https://stackoverflow.com/questions/539900/google-bookmark-export-date-format
            "Chrome uses a modified form of the Windows Time format
            ("Windows epoch") for its timestamps, both in the Bookmarks file
            and the history files. The Windows Time format is the number of
            100ns-es since January 1, 1601. The Chrome format is the number of
            microseconds since the same date, and thus 1/10 as large."
        See also:
            http://fileformats.archiveteam.org/wiki/Chrome_bookmarks

    A Chrome epoch value can be converted to a unixtimestamp format using
    a formula described here in a blog post:
        http://linuxsleuthing.blogspot.co.za/2011/06/decoding-google-chrome-timestamps-in.html

    @param chrome_epoch: Numeric value for Chrome epoch time, as int, float
        or str.

    @return: datetime.datetime object created from the input value.
    """
    chrome_epoch = float(chrome_epoch)
    unix_timestamp = chrome_epoch / 1000000 - 11644473600

    return datetime.datetime.fromtimestamp(unix_timestamp)


def from_onetab_time(onetab_epoch):
    """
    Convert time from Onetab's epoch to Python datetime object.

    @param onetab_epoch: Numeric value for the OneTab browser extension's
        epoch time. This follows the unix timestamp standard, but in
        milliseconds.

    @return: datetime.datetime object for the input value.
    """
    seconds = float(onetab_epoch) / 1000

    return datetime.datetime.fromtimestamp(seconds)
