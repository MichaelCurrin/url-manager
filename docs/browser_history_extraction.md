# Browser history extraction


## Chrome

How to get your history out of the History file. Based on [guide](http://giantdorks.org/alain/export-chrome-or-chromium-browsing-history-on-linux/).

_Note that it's easier to sync to Google after signing into the browser and then download the history across all machines. But if you need history specfic to a machine or are not signed into Chrome, this will work. For visualizing data from a downloaded file, see [History report](https://github.com/MichaelCurrin/history-report)._


### Find the history file

On Linux:

```
~/.config/google-chrome/$PROFILE/History
```

Where `$PROFILE` is `Default`, `Profile 1` or `Profile 2` etc.

Replace `google-chrome` with `chromium` if needed.

The file is a SQLite file.

If Chrome is open the file will be locked, you'll might want to copy the file and then access that.

### Query it

```sh
QUERY="
    SELECT
        CASE last_visit_time
            WHEN 0
            THEN 'n/a'
            ELSE
            datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime')
        END AS last_visited,
       url
    FROM urls
    ORDER BY last_visit_time DESC
"

sqlite3 History -header -csv "$QUERY" > /tmp/history.json
```

Open the JSON file.
