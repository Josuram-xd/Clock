"""ANSI colors and text helpers: visible length, centering, and boxes."""

ESC = "\033"
CLEAR_SCREEN = ESC + "[2J" + ESC + "[H"
RESET = ESC + "[0m"
BOLD = ESC + "[1m"
RED = ESC + "[31m"
RED_BLINK = ESC + "[5;1;31m"
GREEN = ESC + "[32m"
YELLOW = ESC + "[33m"
BLUE = ESC + "[34m"
CYAN = ESC + "[36m"
WHITE = ESC + "[97m"


def visible_length(text):
    """Count the visible characters, ignoring ANSI sequences."""
    total = 0
    in_sequence = False
    for char in text:
        if char == ESC:
            in_sequence = True
        elif in_sequence:
            if char == "m":
                in_sequence = False
        else:
            total += 1
    return total


def colorize(text, color):
    """Wrap the text in an ANSI color and reset it at the end."""
    return color + text + RESET


def center_text(text, width):
    """Center a text (with or without color) within a given width."""
    padding = (width - visible_length(text)) // 2
    if padding < 0:
        padding = 0
    return " " * padding + text


def draw_box(lines, width):
    """Draw a box with unicode borders. A None line is a separator."""
    border = colorize("║", BLUE)
    output = [colorize("╔" + "═" * width + "╗", BLUE)]
    for line in lines:
        if line is None:
            output.append(colorize("╟" + "─" * width + "╢", BLUE))
            continue
        padding = width - visible_length(line)
        output.append(border + line + " " * padding + border)
    output.append(colorize("╚" + "═" * width + "╝", BLUE))
    return output
