"""
Lib validators module.

For more info:
    http://www.formencode.org/en/latest/modules/validators.html#simple-validators
    http://www.formencode.org/en/1.2-branch/Validator.html
"""
from formencode.validators import Regex


class LowerCaseStr(Regex):
    """
    Validate strings which are used for certain text fields in the db model.

    By default, an error is valid if the regex pattern is not matched. This is
    done by setting accept_python to False. Set this to True on initialisation
    to convert to lowercase without raising an error.
    """

    accept_python = False

    min = 3

    regex = r"^[a-z][-a-z]+$"

    messages = {
        'invalid': "A lowercase string of only alpha characters is required."
            " Hypens are allowed after the first character."
    }


def test():
    """
    Test function to raise a formencode.Invalid error.
    """
    LowerCaseStr().from_python('ABC')


if __name__ == '__main__':
    test()
