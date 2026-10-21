"""ANSI escape codes and text helpers: colors, cursor, visible length, and boxes."""

ESC = "\033"
BELL = "\a"
RESET = ESC + "[0m"
BOLD = ESC + "[1m"
DIM = ESC + "[2m"
RED = ESC + "[31m"
RED_BLINK = ESC + "[5;1;31m"
GREEN = ESC + "[32m"
YELLOW = ESC + "[33m"
BLUE = ESC + "[34m"
MAGENTA = ESC + "[35m"
CYAN = ESC + "[36m"
WHITE = ESC + "[97m"

CLEAR_SCREEN = ESC + "[2J" + ESC + "[H"
CURSOR_HOME = ESC + "[H"
CLEAR_LINE = ESC + "[K"
CLEAR_BELOW = ESC + "[J"
HIDE_CURSOR = ESC + "[?25l"
SHOW_CURSOR = ESC + "[?25h"


def rgb(red, green, blue):
    """24-bit foreground color."""
    return f"{ESC}[38;2;{red};{green};{blue}m"


def visible_length(text):
    """Count the visible characters, ignoring ANSI sequences."""
    total = 0
    in_sequence = False
    for char in text:
        if char == ESC:
            in_sequence = True
        elif in_sequence:
            if char.isalpha():
                in_sequence = False
        else:
            total += 1
    return total


def colorize(text, color):
    """Wrap the text in an ANSI color and reset it at the end."""
    return color + text + RESET if color else text


def pad_to(text, width):
    """Pad a text (with or without color) with spaces up to a visible width."""
    return text + " " * max(0, width - visible_length(text))


def center_text(text, width):
    """Center a text (with or without color) within a given width."""
    padding = max(0, (width - visible_length(text)) // 2)
    return pad_to(" " * padding + text, width)


def draw_box(lines, width, color):
    """Draw a box with unicode borders. A None line is a separator."""
    border = colorize("║", color)
    output = [colorize("╔" + "═" * width + "╗", color)]
    for line in lines:
        if line is None:
            output.append(colorize("╟" + "─" * width + "╢", color))
        else:
            output.append(border + pad_to(line, width) + border)
    output.append(colorize("╚" + "═" * width + "╝", color))
    return output
