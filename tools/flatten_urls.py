#!/usr/bin/env python
"""
Extract URLs from text and return as a formatted list of URLs.

Expect text input on stdin, such as piped in from a text file, which could have
a URL anywhere in a line, even for JSON or CSV file. Extract a URL from
each line where available. A URL is must with the http(s) protocol and
terminate with a line ending, a newline, white space, a comma or a double
quote. A word boundary character could not be used as it matches on valid
URL symbols (?, &, #) and there are a lot of those. Anything before and after
the URL on the line is ignored.

Once all the URLs are extracted, remove duplicates, sort and then print the list
to stdout with a header so it can be read as a CSV.
"""
import re
import sys


URL_PATTERN = re.compile(r'(https?://.+?)(?:$|[\n\s,\"])')


def main():
    """
    Main command-line function.
    """
    url_set = set()
    for line in sys.stdin:
        match = URL_PATTERN.search(line)
        if match:
            # Non-capturing groups are still included in .group() so rather
            # specify the 1st (and only) group by index.
            url_set.update([match.group(1)])

    print('url')
    for url in sorted(url_set):
        print(url)


if __name__ == '__main__':
    main()
