
from dndbuddy_core import settings


def _color(string, ansi, bold=False):
    """Colors the given string with the given ANSI color index."""
    return "\x1b[1;{}m{}\x1b[0m".format(ansi, string)


def _color_wrap(string, ansi, bold=False):
    if settings.ANSI_COLORS:
        return _color(string, ansi, bold=bold)
    return string


def green(string, bold=False):
    return _color_wrap(string, 32, bold=bold)


def yellow(string, bold=False):
    return _color_wrap(string, 33, bold=bold)


def red(string, bold=False):
    return _color_wrap(string, 31, bold=bold)


def white(string, bold=False):
    return _color_wrap(string, 39, bold=bold)
