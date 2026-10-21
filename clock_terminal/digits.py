"""Seven-segment style digits drawn with block characters (3 rows)."""

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
    ":": [" █ ", "   ", " █ "],
}


def draw_digital(text):
    """Return the 3 rows of a text such as 'HH:MM:SS' drawn in blocks."""
    rows = ["", "", ""]
    for index, char in enumerate(text):
        glyph = DIGIT_FONT[char]
        for row in range(3):
            if index > 0:
                rows[row] += "  "
            rows[row] += glyph[row]
    return rows
