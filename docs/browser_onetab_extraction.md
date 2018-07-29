# Browser OneTab Extraction

How to get OneTab data from your browsers so that you can easily import into the URL Manager application.

Note that OneTab does allow you to export URLs in its own format, however result is not in JSON structure and also omits some metadata.

## Chrome

This section is applicable for both Chrome and Chromium web browsers. The two may both exist on the same system and both may be imported in the URL Manager application. 

1. Open Chrome.
2. Change to the desired profile username.
3. Open the Onetab extension. Right-click the Onetab icon, then click _Display OneTab_. This should take you to a URL like _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/onetab.html_. The long value in the middle is the extension's ID.
4. _Ctrl+Shift+I_ to Inspect the page.
5. Get the Extension's data.
    - Either               
       1. Open the _Console_ tab.
       2. Enter `console.log(localStorage.state);`.
       3. Click _Copy_ in the bottom right. This ensures you get all the data rather than possibly truncated output.
    - Or
        1. Open the _Application_ tab.
        2. Under _Storage_ then _Local Storage_, click on _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall_.
        3. Where the Key is _state_, double-click the the corresponding value on the right then copy the content to the clipboard.
6. Create a next text file somewhere and paste the copied single-line string into a tempory file. e.g. `~/temp.json`. The file will start like this:
    ```
    {"tabGroups":[{"id":"...","tabsMeta":[{"id":"...","url": ...
    ```
7. The following command will prettify the contents of the JSON file and save it to the project.
    ```bash
    $ # In this example, I am at a machine at the company 'mycompany' and the profile has data for personal use.
    $ cat ~/temp.json | python -m json.tool > path/to/repo/url_manager/var/lib/raw/onetab_chrome_mycompany_personal.json
    $ # If you open the new file it should looke something like this:
    {
        "tabGroups": [
            {
                "createDate": 1526645339880,
                "id": "...",
                "label": "...",
                "locked": false,
                "starred": false,
                "tabsMeta": [
                    {
                        "id": "...",
                        "title": "...",
                        "url": "https://..."
                    },
                    ...
                ]
                ...
            }
        ]
    }
    ```
8. Go back to step 2 and repeat for your other Chrome profiles, as desired.
