import re
import validators


def format_url(url: str):
    """
    Helper function to format url according to http protocol patterns.
    :param url: user input string
    :return: formatted string with "http://" added if it was missing
    """
    if not re.match('(?:http|https)://', url):
        return 'http://{}'.format(url)
    return url


def validate_url(url):
    """
    Validates if url is valid using this lib: https://validators.readthedocs.io/
    :param url: http url in form of string
    :return: True if url is valid. Otherwise it returns ValidationFailure object (see lib doc for more detail).
    """
    return validators.url(url)
