# Browser Bookmark Extraction


Export bookmark data from web browsers and save as text files. These can then by parsed added to the database, using the URL Manager application.

## Chrome

This section is applicable for both Chrome and Chromium web browsers. The two may both exist on the same system and both may be imported in the URL Manager application.

Before continuing, follow the [Identify Chrome Profiles](identify_chrome_profiles.md) instructions.

### Copy an existing JSON file

Choose a user from Chrome or Chromium which you want to include in the project. In the example below, the 'Research' user from Chrome is used.

Put a link to the user's Preferences file in the project. The linked file will always point to the most up to date data in the original file. Note the file naming convention of area, browser name and then profile name.

```bash
$ ln -s ~/.config/google-chrome/Profile\ 3/Bookmarks \
    url_manager/var/lib/raw/bookmarks_chrome_research.json
```

Or, make a copy of the preferences data in the project. Though, this duplicated file will not be updated if the original changes so this is not recommended unless you want to experiment with editing the copy by hand.

```bash
$ cp ~/.config/google-chrome/Profile\ 3/Bookmarks \
    url_manager/var/lib/raw/bookmarks_chrome_research.json
```

You now have a reference to a single user's bookmarks in your project. Repeat the steps for all users which you want to import into the URL Manager application.


Those steps above could be automated with a script, but then that will require handling OS and browser types and requiring inputs for username or display name (internally lookup username) and then a way to generate a filename or link name with some input.

### Export as JSON using JavaScript

You can also use JavaScript to export Chrome (or Chromium) bookmarks to a text file, in JSON format. This is more tedious than the above method, but is included anyway for intrest.

1. Open Chrome.
1. Choose the Chrome user for which you want to get bookmarks for.
1. Enable bookmark permissions for a Chrome extension, as required by the [Chrome Bookmarks API](https://developer.chrome.com/extensions/bookmarks). Either edit the manifest file on existing extension, but it is easy enough find one which has permissions already. Therefore install [Bookmarks to JSON Extension](https://chrome.google.com/webstore/detail/bookmarks-to-json/ladccghgadelmlkjfkdjhjlinhogaibi?hl=en-GB) in Chrome. This can be used directly by clicking on the icon, then _Options_ and _Export_, however the output info is limited.
1. Click the _Bookmarks to JSON Extension_ icon and Options item.
1. Open the developer console (`ctrl+shift+i`).
1. Open the JavaScript _Console_ tab.
1. To get the data as single string indented to 4 spaces, paste the following in and press enter:
    ```javascript
    > chrome.bookmarks.getTree(function (tree) { console.log(JSON.stringify(tree, null, 4)) ;  } ) ;
    ```
1. Click _Copy_ at the end to copy the entire result to the clipboard.
1. Paste in a text editor and save as `.json` file.

### Export as XML

It is possible to export Chrome bookmarks to a XML file using the browser's Bookmark Manager and built-in Export functionality. 

But the file seems to follow a format of self-closing tags which is not understood by parsers and therefore this is not practical to use. 

This was the case when attempting to parse with these 3 methods:

- Online [XML to JSON converter](http://www.utilities-online.info/xmltojson/#.WuD0KDPRY0M) failed to process
- Python package `xmltodict`: failed to process
- Python package `bs4` (BeautifulSoup4): file was processed, but tags were incorrectly nested too deeply due to a lack of closing tags.

Therefore using neither straight XML or parsing XML to JSON is supported in this project. However, if other parsers can be used or upgrading to newer versions works, then I'll be able to use the XML export.

## Firefox

To be completed.

There doesn't seem to a way to export bookmarks within Firefox.

