# Identify Chrome Profiles

Instructions to get an overview of where your Chrome and Chromium profiles are on your system and how the directory and display names are paired.

Navigate to the browser's config data.

```bash
$ cd ~/.config/google-chrome
$ # OR
$ cd ~/.config/chromium
```

You should have one user directory called `Default`. You might also have directories for additional users, such as `Profile 2`. 

```bash
$ ls -d Default
Default
$ ls -d Profile*
Profile 3   Profile 5
```

Unfortunately the user name as displayed in Chrome is not obvious from here. However, each profile has a Preferences file in JSON format and that includes the display name. For convenience, this project provides an [Identify Chrome Profiles](/tools/identify_chrome_profiles.sh) tool to easily scan your browser profile directory names and show them against their display names.

```bash
$ cd path/to/repo
$ ./tools/identify_chrome_profiles.sh
google-chrome
Default: Personal
Profile 3: Research
Profile 4: Work

chromium
Default: Person 1
```

In the above example, there are 3 Chrome and 1 Chromium user present on this system. Arbitrarily, up to 9 profiles of each are supported by this tool.
