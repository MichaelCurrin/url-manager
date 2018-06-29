# Browser OneTab Extraction

## Chrome

This section is applicable for both Chrome and Chromium web browsers. The two may both exist on the same system and both may be imported in the URL Manager application. 

Before continuing, follow the [Identify Chrome Profiles](identify_chrome_profiles.md) instructions.

1. Open Chrome.
2. Change to the desired profile.
3. Open the Onetab extension. Right-click the Onetab icon, then click _Display OneTab_. This should take you to a URL like [chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/onetab.html](). The long value in the middle is the extension's ID.
4. _Ctrl+Shift+I_ to Inspect the page.
5. Get the Extension's data.
    - Either               
       1. Open the _Console_ tab.
       2. Enter `console.log(localStorage.state);` and copy the result to the clipboard. TODO: Or JSON pretty.
    - Or
        1. Open the _Application_ tab.
        2. Under Storage then Local Storage, click on _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall_.
        3. Where the Key is _state_, double-click the value in Value and copy the content to the clipboard.
6. Create a next text file somewhere and paste the copied single-line string into a tempory file. e.g. `~/temp.json`
7. Prettify the contents of the JSON file and save it to the project.
    ```bash
    $ cat ~/temp.json | python -m json.tool > path/to/repo/url_manager/var/lib/raw/onetab_chrome_myco_personal.json
    ```
