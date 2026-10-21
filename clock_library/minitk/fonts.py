"""Big font: digits and a few symbols drawn with block characters (3 rows)."""

BIG_FONT = {
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
    "-": ["   ", "▀▀▀", "   "],
    " ": ["  ", "  ", "  "],
}
UNKNOWN = ["▀▀█", " ▄▀", " ▄ "]  # drawn for characters the font does not have


def big_lines(text):
    """The 3 rows of a text drawn with the big font."""
    rows = ["", "", ""]
    for index, char in enumerate(text):
        glyph = BIG_FONT.get(char, UNKNOWN)
        for row in range(3):
            rows[row] += (" " if index else "") + glyph[row]
    return rows
