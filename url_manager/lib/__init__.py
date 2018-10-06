"""
Lib module initialisation file.
"""
import platform
import os

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.path.pardir))


def is_linux():
    system = platform.system()
    if system == 'Linux':
        return True
    elif system == 'Darwin':
        return False
    else:
        raise ValueError(f"Only Linux and Mac are supported."
                         f" Your system is: {system}")


def browser_profile_dir(is_linux):
    """
    Return paths to profile data for supported browsers and the relevant OS.

    Values which are not yet completed return as None.
    """
    if is_linux:
        data = {
            'Firefox': "~/.mozilla/firefox",
            'Quantum': None,
            'Chrome': "~/.config/google-chrome",
            'Chromium': "~/.config/chromium"
        }
    else:
        data = {
            'Firefox': "~/Library/Application Support/Firefox/Profiles",
            'Quantum': None,
            'Chrome': "~/Library/Application Support/Google/Chrome",
            'Chromium': "~/Library/Application Support/Chromium"
        }
    for k, v in data.items():
        if v:
            data[k] = os.path.expanduser(v)

    return data


IS_LINUX = is_linux()
BROWSER_PROFILE_DIRS = browser_profile_dir(IS_LINUX)
