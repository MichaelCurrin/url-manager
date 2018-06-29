"""
Lib convert application file.

The docs for Google bookmark time simply says it is recorded as milliseconds
since the epoch. Further research on StackOverflow shows that the epoch here
is NOT the unix timestamp epoch time.

    https://stackoverflow.com/questions/539900/google-bookmark-export-date-format
    "Chrome uses a modified form of the Windows Time format
    ("Windows epoch") for its timestamps, both in the Bookmarks file
    and the history files. The Windows Time format is the number of
    100ns-es since January 1, 1601. The Chrome format is the number of
    microseconds since the same date, and thus 1/10 as large."

Also explained here:
    http://fileformats.archiveteam.org/wiki/Chrome_bookmarks

But, I had success with a formula provided in this blog post:
    http://linuxsleuthing.blogspot.co.za/2011/06/decoding-google-chrome-timestamps-in.html

    >>> chrome_epoch = 13169330714873550
    >>> unix_timestamp = chrome_epoch / 1000000 - 11644473600
    1524857114.8735504
    >>> datetime.datetime.fromtimestamp(unix_timestamp)
    datetime.datetime(2018, 4, 27, 21, 25, 14, 873550)
"""
import datetime


# The desired format for datetime values in output JSON files.
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def from_chrome_time(chrome_epoch):
    """
    Convert time from Chrome's epoch format to a datetime object.

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
