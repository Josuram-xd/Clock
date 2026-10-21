"""Surface: a grid of terminal cells (character, foreground, background, bold)."""

from clock_library.minitk.colors import RESET, style_code

BLANK = (" ", None, None, False)


class Surface:
    """Everything is drawn here first and then printed as lines of text."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[BLANK] * width for _ in range(height)]

    def put(self, x, y, char, fg=None, bg=None, bold=False):
        """Write one cell. A bg of None keeps the background that was already there."""
        if 0 <= x < self.width and 0 <= y < self.height:
            if bg is None:
                bg = self.cells[y][x][2]
            self.cells[y][x] = (char, fg, bg, bold)

    def text(self, x, y, text, fg=None, bg=None, bold=False):
        """Write a string from (x, y) to the right."""
        for offset, char in enumerate(text):
            self.put(x + offset, y, char, fg, bg, bold)

    def fill(self, x, y, width, height, bg):
        """Paint a rectangle with a background color (clearing its characters)."""
        for row in range(y, y + height):
            for column in range(x, x + width):
                self.put(column, row, " ", None, bg)

    def border(self, x, y, width, height, fg, title=""):
        """Rectangle outline with a title on its top edge."""
        if width < 2 or height < 2:
            return
        top = "┌" + "─" * (width - 2) + "┐"
        if title:
            label = " " + title[:width - 6] + " "
            top = top[:2] + label + top[2 + len(label):]
        self.text(x, y, top, fg)
        self.text(x, y + height - 1, "└" + "─" * (width - 2) + "┘", fg)
        for row in range(y + 1, y + height - 1):
            self.put(x, row, "│", fg)
            self.put(x + width - 1, row, "│", fg)

    def lines(self):
        """The surface as lines of text with ANSI colors (runs of equal style share a code)."""
        output = []
        for row in self.cells:
            pieces = []
            style = None
            for char, fg, bg, bold in row:
                if (fg, bg, bold) != style:
                    style = (fg, bg, bold)
                    pieces.append(style_code(fg, bg, bold))
                pieces.append(char)
            output.append("".join(pieces) + RESET)
        return output
