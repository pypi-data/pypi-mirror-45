from typing import *

from .coloring import get_length_on_screen

__all__ = ['indent']


def indent(s: str, prefix: str, first: Optional[str] = None) -> str:
    if not isinstance(s, str):
        s = u'{}'.format(s)

    assert isinstance(prefix, str), type(prefix)
    try:
        lines = s.split('\n')
    except UnicodeDecodeError:
        print(type(s))  # XXX
        print(s)  # XXX
        lines = [s]
    if not lines:
        return u''

    if first is None:
        first = prefix


    m = max(get_length_on_screen(prefix), get_length_on_screen(first))

    prefix = ' ' * (m - get_length_on_screen(prefix)) + prefix
    first = ' ' * (m - get_length_on_screen(first)) + first

    # differnet first prefix
    res = [u'%s%s' % (prefix, line.rstrip()) for line in lines]
    res[0] = u'%s%s' % (first, lines[0].rstrip())
    return '\n'.join(res)
