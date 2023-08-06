import re

escape = re.compile('\x1b\[..?m')


def remove_escapes(s):
    return escape.sub("", s)


def get_length_on_screen(s):
    """ Returns the length of s without the escapes """
    return len(remove_escapes(s))
