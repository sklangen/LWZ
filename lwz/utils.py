
def int_or_default(string, default=None):
    if string == '' or string.isspace():
        return default
    return int(string)
