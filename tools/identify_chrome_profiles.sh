#!/bin/bash
# For Google Chrome and Chromium browsers on the system, display the directory
# names for profiles along with the corresponding profile's display name
# (as normally seen in the top right corner of the browser window).


# Python command to extract the profile display name from a browser profile's
# preferences JSON file.
PY_CMD='import json, sys; print(json.load(sys.stdin)["profile"]["name"])'


for BROWSER in google-chrome chromium
do
  echo $BROWSER

  BROWSER_CONF_PATH="$HOME/.config/$BROWSER"

  FOUND=false

  if [ -d $BROWSER_CONF_PATH ]
    then
      for CHROME_USER in 'Default' 'Profile 1' 'Profile 2' 'Profile 3' 'Profile 4' \
        'Profile 5' 'Profile 6' 'Profile 7' 'Profile 8' 'Profile 9'
      do
        if [ -d "$BROWSER_CONF_PATH/$CHROME_USER" ]
          then
            FOUND=true
            PREF_PATH="$BROWSER_CONF_PATH/$CHROME_USER/Preferences"
            DISPLAY_NAME=$(cat "$PREF_PATH" | python -c "$PY_CMD")
            echo "  $CHROME_USER: $DISPLAY_NAME"
        fi

      if [ "$FOUND" = false ]
        then
          echo '0 profiles found'
      fi

      done
    else
      echo "Could not find config files - perhaps the browser is not installed"
    fi
  echo
done
