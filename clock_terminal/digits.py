"""Digits drawn with block characters (3 rows) for the digital time."""

DIGIT_FONT = {
    "0": ["█▀█", "█ █", "█▄█"],
    "1": [" ▄█", "  █", "  ▀"],
    "2": ["▀▀█", "█▀▀", "▀▀▀"],
    "3": ["▀▀█", " ▄█", "▀▀▀"],
    "4": ["█ █", "▀▀█", "  ▀"],
    "5": ["█▀▀", "▀▀█", "▀▀▀"],
    "6": ["█▀▀", "█▀█", "▀▀▀"],
    "7": ["▀▀█", "  █", "  ▀"],
    "8": ["█▀█", "█▀█", "▀▀▀"],
    "9": ["█▀█", "▀▀█", "▀▀▀"],
    ":": ["▄", " ", "▀"],
}
BLANK_COLON = [" ", " ", " "]


def draw_digital(text, colon_visible=True):
    """Return the 3 rows of a text such as 'HH:MM:SS' drawn in blocks.

    With colon_visible=False the colons are blank, which makes them blink.
    """
    rows = ["", "", ""]
    for index, char in enumerate(text):
        glyph = DIGIT_FONT[char] if colon_visible or char != ":" else BLANK_COLON
        for row in range(3):
            if index > 0:
                rows[row] += " "
            rows[row] += glyph[row]
    return rows
