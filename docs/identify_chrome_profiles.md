# Identify Chrome Profiles

Instructions to get an overview of where your Chrome and Chromium profiles are on your system and how the directory and display names are paired.

Navigate to the browser's config data.

```bash
$ cd ~/.config/google-chrome
$ # OR
$ cd ~/.config/chromium
```

You will probably have a `Default` user and possibly directories for additional users, starting from `Profile 1`. In the example below, `Profile 2` was deleted from within the browser and the later profiles do not have their numbering adjusted.

```bash
$ ls -d Default
Default
$ ls -d Profile*
Profile 1   Profile 3
```

As you can see from the output, the username as displayed in Chrome is not unfortunately obsured. However, each profile does has a Preferences file in JSON format, which includes the display name as a value. For convenience, this project provides an [Identify Chrome Profiles](/tools/identify_chrome_profiles.sh) tool to easily scan your browser profile directory names and show them against their display names.

```bash
$ cd path/to/repo
$ ./tools/identify_chrome_profiles.sh
google-chrome
Default: Personal
Profile 1: Research
Profile 3: Work

chromium
Default: First user
Profile 1: Second user
```

In the above example, there are 3 Chrome and 1 Chromium user present on this system. Arbitrarily, up to 10 profiles of each are supported by this tool.
