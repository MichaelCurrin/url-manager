# Flatten URLs

The [flatten_urls.py](/tools/flatten_urls.py) tool can take a text file of URLs in various formats, extract just the URLs and write out a new CSV with a single column of URLs. See more details in the script's docstring.

Recommended usage to persist the parsed result as a CSV:

```bash
cd tools
./flatten_urls.py < path/to/bookmarks.json > path/to/flat_bookmark_urls.csv
```
