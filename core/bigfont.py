"""Big font: digits drawn with full blocks, 4 columns wide and 5 rows tall.

Shared by the terminal clock and by minitk's Label(font="big").
"""

FONT_ROWS = 5

BIG_FONT = {
    "0": ["████", "█  █", "█  █", "█  █", "████"],
    "1": [" ██ ", "  █ ", "  █ ", "  █ ", "████"],
    "2": ["████", "   █", "████", "█   ", "████"],
    "3": ["████", "   █", " ███", "   █", "████"],
    "4": ["█  █", "█  █", "████", "   █", "   █"],
    "5": ["████", "█   ", "████", "   █", "████"],
    "6": ["████", "█   ", "████", "█  █", "████"],
    "7": ["████", "   █", "  █ ", " █  ", " █  "],
    "8": ["████", "█  █", "████", "█  █", "████"],
    "9": ["████", "█  █", "████", "   █", "████"],
    ":": [" ", "█", " ", "█", " "],
    "-": ["    ", "    ", "████", "    ", "    "],
    " ": ["  "] * FONT_ROWS,
}
BLANK_COLON = [" "] * FONT_ROWS
UNKNOWN = ["████", "   █", " ██ ", "    ", " █  "]  # a question mark, for missing characters


def big_lines(text, colon_visible=True):
    """The rows of a text drawn with the big font, one space between characters.

    With colon_visible=False the colons are blank, which makes them blink.
    """
    rows = [""] * FONT_ROWS
    for index, char in enumerate(text):
        glyph = BIG_FONT.get(char, UNKNOWN)
        if char == ":" and not colon_visible:
            glyph = BLANK_COLON
        for row in range(FONT_ROWS):
            rows[row] += (" " if index else "") + glyph[row]
    return rows
