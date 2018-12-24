# Identify Chrome Profiles

Instructions to get an overview of where your Chrome and Chromium profiles are on your system and how the directory and display names are paired.

Your browser user data is stored in a location based on whether you are using Chrome or Chromium and Linux of macOS. Those cases are handled with the instructions below.


## Match names and paths

Below are two approaches to identify all pairs names and paths for your Chrome-like browsers.


### The automated way

This uses the [Identify Chrome Profiles](/tools/identify_chrome_profiles.sh) tool, which is a standlone script which can be run from anywhere.

Within each browser, the directory for the profile is shown against the browser user display name.

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


## The manual way

This is a slower alternative and involves using the actual browser.

1. Open Chrome (or Chromium).
2. Switch to a profile.
3. Enter the following URL: _chrome://version/_
4. And then see the _Profile Path_ field and note the value for the profile.
5. Repeat for remaining browser and users.

Example output for two browsers.

```
Google Chrome   68.0.3440.84 (Official Build) (64-bit)
...
Profile Path    /home/michael/.config/google-chrome/Profile 3
```

```
Chromium    68.0.3440.75 (Developer Build) ...
...
Profile Path    /home/michael/.config/chromium/Default
```
