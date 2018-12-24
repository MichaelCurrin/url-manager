#!/usr/bin/env bash -e
# Show pairs of account name and display name for each Chrome-related user
# on the system.
#
# The Preferences JSON file for each available account in the config data
# is parsed and the display name. This works for Chrome and Chromium on
# both Mac and Linux.
#
# Documented config data paths:
#   https://chromium.googlesource.com/chromium/src/+/HEAD/docs/user_data_dir.md

# Extract the Chrome profile's display name from a JSON
# preferences JSON file given on stdin.
PY_CMD='import json, sys; print(json.load(sys.stdin)["profile"]["name"])'

if [ "$(uname)" == 'Darwin' ]; then
  CHROME_PATH="$HOME/Library/Application Support/Google/Chrome"
  CHROMIUM_PATH="$HOME/Library/Application Support/Chromium"
else
  CHROME_PATH="$HOME/.config/google-chrome"
  CHROMIUM_PATH="$HOME/.config/chromium"
fi

for BROWSER_PATH in "$CHROME_PATH" "$CHROMIUM_PATH"
do
  echo -e $(basename "$BROWSER_PATH")

  if [ -d "$BROWSER_PATH" ]
    then
      for USERNAME in 'Default' 'Profile 1' 'Profile 2' 'Profile 3' \
        'Profile 4' 'Profile 5' 'Profile 6' 'Profile 7' 'Profile 8' 'Profile 9'
      do
        USER_CONFIG="$BROWSER_PATH/$USERNAME"
        if [ -d "$USER_CONFIG" ]
          then
            DISPLAY_NAME=$(python -c "$PY_CMD" < "$USER_CONFIG/Preferences")
            echo "  $USERNAME: $DISPLAY_NAME"
        fi
      done

    else
      echo "  Appears to not be installed"
    fi
  echo
done
