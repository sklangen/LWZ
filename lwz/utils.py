from urllib.request import urlopen


def int_or_default(string, default=None):
    if string == '' or string.isspace():
        return default
    return int(string)

def http_get(url):
    resource = urlopen(url)
    return resource.read().decode(resource.headers.get_content_charset())

