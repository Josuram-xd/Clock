"""Braille pixel grid: every terminal cell holds 2 x 4 dots, so drawings look smooth.

A dot is "on" when its bit is set in the cell's mask; the braille character of
that mask draws it. Each cell also remembers an owner (a color role or color)
chosen by the last thing that drew a dot in it.
"""

BRAILLE_BASE = 0x2800
DOT_BITS = ((0x01, 0x02, 0x04, 0x40), (0x08, 0x10, 0x20, 0x80))  # [x % 2][y % 4]
DOTS_X = 2  # dots per cell, horizontally
DOTS_Y = 4  # dots per cell, vertically


def create_braille(cols, rows):
    """Empty grid of cols x rows cells (cols * 2 by rows * 4 dots)."""
    return {
        "cols": cols,
        "rows": rows,
        "masks": [[0] * cols for _ in range(rows)],
        "owners": [[None] * cols for _ in range(rows)],
    }


def set_dot(braille, x, y, owner=None):
    """Turn one dot on (ignored outside the grid) and give its cell to `owner`."""
    x, y = round(x), round(y)
    column, row = x // DOTS_X, y // DOTS_Y
    if 0 <= x and 0 <= y and column < braille["cols"] and row < braille["rows"]:
        braille["masks"][row][column] |= DOT_BITS[x % DOTS_X][y % DOTS_Y]
        braille["owners"][row][column] = owner


def set_dots(braille, points, owner=None, thickness=1):
    """Turn on many (x, y) dots; thickness > 1 draws each as a small square."""
    for x, y in points:
        for dy in range(thickness):
            for dx in range(thickness):
                set_dot(braille, x + dx, y + dy, owner)


def clear_cell(braille, column, row):
    """Remove every dot of a cell (a character is going to be written there)."""
    braille["masks"][row][column] = 0
    braille["owners"][row][column] = None


def cell_char(braille, column, row):
    """The braille character of a cell, or a space if it has no dots."""
    mask = braille["masks"][row][column]
    return chr(BRAILLE_BASE + mask) if mask else " "
