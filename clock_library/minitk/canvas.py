"""Canvas: draw lines, ovals, rectangles, and text with tkinter-style items.

Every terminal cell is a 2 x 4 grid of braille dots, so the canvas is
width * 2 by height * 4 pixels and its pixels are square. Coordinates start at
the top-left corner, with y growing downward, as in tkinter. Text items are
written on whole cells: x // 2 is the column and y // 4 is the row. Items are
drawn in the order they were created; where two touch the same cell, the later
one owns it.
"""

from clock_library.minitk.colors import parse_color
from clock_library.minitk.widgets import Widget
from core.braille import DOTS_X, DOTS_Y, cell_char, clear_cell, create_braille, set_dots
from mymath import raster

SHAPES = {
    "line": (raster.line_points, None),
    "oval": (raster.ellipse_outline, raster.ellipse_fill),
    "rectangle": (raster.rectangle_outline, raster.rectangle_fill),
}


class Canvas(Widget):
    """Widget with a drawing area of width x height cells."""

    def __init__(self, master, width=40, height=12, bg="black"):
        super().__init__(master)
        self.width = width
        self.height = height
        self.options["bg"] = bg
        self._items = {}
        self._next_id = 1

    @property
    def pixel_width(self):
        """Width of the drawing area in pixels."""
        return self.width * DOTS_X

    @property
    def pixel_height(self):
        """Height of the drawing area in pixels."""
        return self.height * DOTS_Y

    # -- creating and editing items ---------------------------------------

    def _create(self, kind, coords, **options):
        item_id = self._next_id
        self._next_id += 1
        self._items[item_id] = {"kind": kind, "coords": list(coords), "options": options}
        self.mark_changed()
        return item_id

    def create_line(self, x0, y0, x1, y1, fill="white", width=1, tags=()):
        """Straight line; width is the thickness in pixels."""
        return self._create("line", (x0, y0, x1, y1), fill=fill, width=width, tags=tags)

    def create_oval(self, x0, y0, x1, y1, outline="white", fill=None, width=1, tags=()):
        """Ellipse inscribed in the box (x0, y0)-(x1, y1)."""
        return self._create("oval", (x0, y0, x1, y1), outline=outline, fill=fill, width=width,
                            tags=tags)

    def create_rectangle(self, x0, y0, x1, y1, outline="white", fill=None, width=1, tags=()):
        """Rectangle with an optional fill color."""
        return self._create("rectangle", (x0, y0, x1, y1), outline=outline, fill=fill,
                            width=width, tags=tags)

    def create_text(self, x, y, text="", fill="white", anchor="center", bold=False, tags=()):
        """Text anchored at 'center', 'w' (starts at x) or 'e' (ends at x)."""
        return self._create("text", (x, y), text=text, fill=fill, anchor=anchor, bold=bold,
                            tags=tags)

    def _matching(self, target):
        if target == "all":
            return list(self._items)
        if isinstance(target, int):
            return [target] if target in self._items else []
        return [i for i, item in self._items.items() if target in item["options"]["tags"]]

    def delete(self, target):
        """Remove an item by id, by tag, or everything with 'all'."""
        for item_id in self._matching(target):
            del self._items[item_id]
        self.mark_changed()

    def coords(self, item_id, *new_coords):
        """Move an item to new coordinates, or return the current ones."""
        item = self._items[item_id]
        if not new_coords:
            return list(item["coords"])
        item["coords"] = list(new_coords)
        self.mark_changed()
        return None

    def itemconfigure(self, target, **options):
        """Change the options (fill, outline, text...) of one or several items."""
        for item_id in self._matching(target):
            self._items[item_id]["options"].update(options)
        self.mark_changed()

    # -- drawing ----------------------------------------------------------

    def natural_size(self):
        return self.width, self.height

    def _draw_shape(self, braille, item):
        kind, coords, options = item["kind"], item["coords"], item["options"]
        outline_points, fill_points = SHAPES[kind]
        thickness = options["width"]
        if kind == "line":
            color = parse_color(options["fill"])
            if color is not None:
                set_dots(braille, outline_points(*coords), color, thickness)
            return
        fill = parse_color(options["fill"])
        if fill is not None:
            set_dots(braille, fill_points(*coords), fill)
        outline = parse_color(options["outline"])
        if outline is not None:
            set_dots(braille, outline_points(*coords), outline, thickness)

    def _draw_text(self, braille, texts, item):
        options = item["options"]
        x, y = item["coords"]
        text = options["text"]
        start = round(x) // DOTS_X
        if options["anchor"] == "center":
            start -= len(text) // 2
        elif options["anchor"] == "e":
            start -= len(text) - 1
        row = round(y) // DOTS_Y
        for offset, char in enumerate(text):
            column = start + offset
            if 0 <= column < self.width and 0 <= row < self.height:
                clear_cell(braille, column, row)
                texts[(column, row)] = (char, parse_color(options["fill"]), options["bold"])

    def draw(self, surface, x, y, width, height):
        braille = create_braille(self.width, self.height)
        texts = {}
        for item in self._items.values():
            if item["kind"] == "text":
                self._draw_text(braille, texts, item)
            else:
                self._draw_shape(braille, item)
                # a shape that reaches a cell with text takes it over (later items are on top)
                for column, row in list(texts):
                    if braille["masks"][row][column]:
                        del texts[(column, row)]
        background = parse_color(self.options["bg"])
        for row in range(min(self.height, height)):
            for column in range(min(self.width, width)):
                if (column, row) in texts:
                    char, color, bold = texts[(column, row)]
                    surface.put(x + column, y + row, char, color, background, bold)
                else:
                    surface.put(x + column, y + row, cell_char(braille, column, row),
                                braille["owners"][row][column], background)
