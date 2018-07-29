# Browser OneTab Extraction

## Chrome

This section is applicable for both Chrome and Chromium web browsers. The two may both exist on the same system and both may be imported in the URL Manager application. 

1. Open Chrome.
2. Change to the desired profile username.
3. Open the Onetab extension. Right-click the Onetab icon, then click _Display OneTab_. This should take you to a URL like _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall/onetab.html_. The long value in the middle is the extension's ID.
4. _Ctrl+Shift+I_ to Inspect the page.
5. Get the Extension's data.
    - Either               
       1. Open the _Console_ tab.
       2. Enter `console.log(localStorage.state);` and copy the result to the clipboard.
    - Or
        1. Open the _Application_ tab.
        2. Under _Storage_ then _Local Storage_, click on _chrome-extension://chphlpgkkbolifaimnlloiipkdnihall_.
        3. Where the Key is _state_, double-click the value in _Value_ and copy the content to the clipboard.
6. Create a next text file somewhere and paste the copied single-line string into a tempory file. e.g. `~/temp.json`
7. Prettify the contents of the JSON file and save it to the project.
    ```bash
    $ cat ~/temp.json | python -m json.tool > path/to/repo/url_manager/var/lib/raw/onetab_chrome_myco_personal.json
    ```
8. Go back to step 2 and repeat for your other Chrome profiles, as desired.
