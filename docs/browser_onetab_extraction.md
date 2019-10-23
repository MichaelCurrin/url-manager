# Browser OneTab Extraction

How to get OneTab data from your browsers so that you can easily import into the URL Manager application.

Note that although OneTab itself _does_ allow you to export your URL data in its own text format. Within OneTab, you could go to _Export / Import URLs_ and see something like this.

```
https:/example.com | Example title
https://abc.com | ABC website

https://anothersite.com | Another title in a new section but with no section heading
```

However, the result is not in a JSON structure and also omits metadata like custom titles and times. Therefore this project's own data export process is preferred.


## Firefox

Find the location of OneTab data for your Firefox user accounts and make it available in the project. Note that this has only been tested for Firefox and not Firefox Quantum.

The approach below parses the `storage.json` and gets the value of 'state' field inside it.

1. Open Firefox.
2. Go to the [about:profiles](https://about:profiles) page. This will show you your Firefox users.
3. Choose the profile you want, look at the paths and copy the username from one. e.g. `abcd1234.default`
4. Follow the commands below to enter the browser and username and save the output. An example is shown below.
    ```bash
    $ # Use the full path to the raw directory and then provide a suitable name for the file.
    $ OUTPUT=~/PATH/TO/REPO/url_manager/var/lib/raw/onetab_firefox_abc_personal.json
    $ # Set your username as the second argument.
    $ ./extract_onetab_storage.py Firefox abcd1234.default > $OUTPUT
    ```
5. Go back to step 3 and repeat for other profiles as desired.


## Chrome

This section is applicable for both Chrome and Chromium browsers. The two may both exist on the same system and both may be imported into the URL Manager application.


### Python script approach

Find the location of OneTab data for your Chrome or Chromium user accounts and make it available in the project.

The approach below reads the OneTab extension data from Chrome's LevelDB storage then gets the value of 'state' field within it.

1. Get a list of usernames and display names on your system as covered by the [Identify Chrome Profiles](/docs/identify_chrome_profiles.md) doc.
2. Decide on the browser and username you want to target.
3. Follow the commands below to enter the browser and username and save the output. An example is shown below.
    ```bash
    $ # Use the full path to the raw directory and then provide a suitable name for the file.
    $ OUTPUT=~/PATH/TO/REPO/url_manager/var/lib/raw/onetab_chrome_abc_personal.json
    $ # Set your desired browser and display name as arguments. For example:
    $ ./extract_onetab_storage.py Chrome 'Profile 1' > $OUTPUT
    ```
4. Go back to step 2 and repeat for other browser and profile pairs as desired.


### Manual JS approach

This approach was initially created as a manual step which can be ignored if the step above is possible.

1. Open Chrome.
2. Open as the desired Chrome user.
3. Open the Onetab extension. Right-click the OneTab icon, then click _Display OneTab_. This should take you to a URL like _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/onetab.html_. The long value in the middle is the extension's ID.
4. Press _Ctrl+Shift+I_ to Inspect the page.
5. Get the Extension's data.
    - Either
       1. Open the _Console_ tab.
       2. Enter `console.log(localStorage.state);`.
       3. Click _Copy_ in the bottom right. This ensures you get all the data rather than possibly truncated output.
    - Or
        1. Open the _Application_ tab.
        2. Under _Storage_ then _Local Storage_, click on _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall_.
        3. Where the Key is _state_, double-click the the corresponding value on the right then copy the content to the clipboard.
6. Create a next text file somewhere and paste the copied single-line string into a temporary file. e.g. `~/temp.json`. The file will start like this:
    ```
    {"tabGroups":[{"id":"...","tabsMeta":[{"id":"...","url": ...
    ```
7. The following command will prettify the contents of the JSON file and save it to the project. The last two parts of the filename should indicate the location (such as the company where you work or 'private') and then the purpose of the profile (such as 'work', 'personal', 'programming' or 'research').
    ```bash
    $ cat ~/temp.json | python -m json.tool \
        > path/to/repo/url_manager/var/lib/raw/chrome_onetab_mycompany_personal.json
    $ # You can view the file if you want.
    $ view path/to/repo/url_manager/var/lib/raw/chrome_onetab__mycompany_personal.json
    {
        "tabGroups": [
            {
                "id": "...",
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
8. Go back to step 2 and repeat for your other profiles, as desired.
