"""Styling Helper for Printing."""
import colorama


def pd_color_low_safety_margin_green(val):
    """Takes a scalar and returns a string with the css property color adjusted."""
    color = 'green' if 0 < val <= 0.3 else 'black'
    return 'color: %s' % color


def color_low_safety_margin_green(val):
    """Colorize specific value between 0 & 0.3."""
    color = colorama.Fore.GREEN if 0 < val <= 0.3 else colorama.Fore.WHITE
    return color + str('{:>.2%}'.format(val)) + colorama.Style.RESET_ALL
