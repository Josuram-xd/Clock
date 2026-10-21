"""Colors: names and '#rrggbb' strings to RGB tuples, and their ANSI 24-bit codes."""

ESC = "\033"
RESET = ESC + "[0m"

NAMED_COLORS = {
    "black": (0, 0, 0),
    "white": (240, 240, 240),
    "gray": (128, 128, 128),
    "red": (235, 64, 52),
    "green": (60, 200, 100),
    "blue": (70, 120, 240),
    "yellow": (250, 210, 50),
    "orange": (250, 150, 40),
    "cyan": (60, 210, 230),
    "magenta": (220, 80, 200),
    "navy": (15, 23, 42),
    "slate": (51, 65, 85),
    "silver": (200, 205, 215),
}


def parse_color(spec):
    """RGB tuple for a color name, '#rgb', '#rrggbb' or an (r, g, b) tuple. None stays None."""
    if spec is None or isinstance(spec, tuple):
        return spec
    text = spec.strip().lower()
    if text in NAMED_COLORS:
        return NAMED_COLORS[text]
    if text.startswith("#") and len(text) in (4, 7):
        digits = text[1:]
        size = len(digits) // 3
        try:
            parts = [int(digits[i * size:(i + 1) * size] * (3 - size), 16) for i in range(3)]
        except ValueError:
            parts = None
        if parts is not None:
            return tuple(parts)
    raise ValueError("color desconocido: " + str(spec))


def style_code(fg, bg, bold):
    """ANSI sequence that sets the foreground, background and weight."""
    code = RESET
    if bold:
        code += ESC + "[1m"
    if fg is not None:
        code += f"{ESC}[38;2;{fg[0]};{fg[1]};{fg[2]}m"
    if bg is not None:
        code += f"{ESC}[48;2;{bg[0]};{bg[1]};{bg[2]}m"
    return code
