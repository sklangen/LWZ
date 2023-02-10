from urllib.request import urlopen
from babel.dates import format_date
from calendar import month_abbr
import json


month_names = month_abbr[5:] + month_abbr[1:5]


class LWZException(Exception):
    pass


def int_or_default(string, default=None):
    if string == '' or string.isspace():
        return default
    return int(string)


def http_get(url):
    resource = urlopen(url)
    return resource.read().decode(resource.headers.get_content_charset())


def http_get_ndjson(url):
    resource = urlopen(url)
    for line in resource:
        yield json.loads(line.decode())


def escape_umlaute(s: str) -> str:
    return s.replace('ä', 'ae') \
            .replace('ö', 'oe') \
            .replace('ü', 'ue') \
            .replace('Ä', 'Ae') \
            .replace('Ö', 'Oe') \
            .replace('Ü', 'Ue') 


def format_month_date(d):
    return format_date(d, 'MMM yyyy', locale='de_DE')
