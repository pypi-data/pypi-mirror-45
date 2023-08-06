import termcolor

color_orange = '#ffb342'
color_blue = '#42a0ff'

from xtermcolor import colorize


def colorize_rgb(x, rgb):
    assert rgb.startswith('#')
    return colorize(x, int(rgb[1:], 16))


def color_ops(x):
    return colorize_rgb(x, color_blue)


def color_typename(x):
    return colorize_rgb(x, color_orange)


def color_par(x):
    return termcolor.colored(x, attrs=['dark'])
