import re
import validators


def format_url(url: str):
    if not re.match('(?:http|https)://', url):
        return 'http://{}'.format(url)
    return url


def validate_url(url):
    return validators.url(url)
