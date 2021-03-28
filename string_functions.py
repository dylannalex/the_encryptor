import re


def is_password(string: str) -> bool:
    """ Checks if the passed string is a valid password.
    By this regex, this password should contain: atleast 1 number,
    1 lower case letter, 1 upper case letter and 1 special character &
    should be atleast 8 chars long. """

    if re.match(r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}[\]:;<>,.?/~_+-=|\\]).{8,32}$', string):
        return True
    return False


def indent(string, indentation):
    """ Returns the string but with the specified indentation. """

    return indentation * ' ' + string


def hide(string, char, sep=None):
    '''Replaces the string's characters with the specified char'''
    hidden_string = ''
    for i in string:
        if i == sep:
            hidden_string += sep
        else:
            hidden_string += char
    return hidden_string
