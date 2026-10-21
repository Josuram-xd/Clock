"""Canvas: draw lines, ovals, rectangles, and text with tkinter-style items.

One terminal cell is 1 pixel wide and 2 pixels tall (two stacked half blocks),
so pixels are almost square. Coordinates start at the top-left corner, with y
growing downward, as in tkinter. Text items use cell positions: x is the
column and y is the pixel row, so it lands on row y // 2.
"""

from clock_library.minitk import raster
from clock_library.minitk.colors import parse_color
from clock_library.minitk.widgets import Widget

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

    def create_oval(self, x0, y0, x1, y1, outline="white", fill=None, tags=()):
        """Ellipse inscribed in the box (x0, y0)-(x1, y1)."""
        return self._create("oval", (x0, y0, x1, y1), outline=outline, fill=fill, tags=tags)

    def create_rectangle(self, x0, y0, x1, y1, outline="white", fill=None, tags=()):
        """Rectangle with an optional fill color."""
        return self._create("rectangle", (x0, y0, x1, y1), outline=outline, fill=fill, tags=tags)

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

    def _plot(self, pixels, points, color, thickness=1):
        reach = (thickness - 1) // 2
        for x, y in points:
            for dy in range(-reach, thickness - reach):
                for dx in range(-reach, thickness - reach):
                    column, row = x + dx, y + dy
                    if 0 <= column < self.width and 0 <= row < self.height * 2:
                        pixels[row][column] = color

    def _rasterize(self, pixels, texts):
        for item in self._items.values():
            kind, coords, options = item["kind"], item["coords"], item["options"]
            if kind == "text":
                texts.append((coords, options))
                continue
            outline_points, fill_points = SHAPES[kind]
            if kind == "line":
                self._plot(pixels, outline_points(*coords), parse_color(options["fill"]),
                           options["width"])
                continue
            fill = parse_color(options["fill"])
            if fill is not None:
                self._plot(pixels, fill_points(*coords), fill)
            outline = parse_color(options["outline"])
            if outline is not None:
                self._plot(pixels, outline_points(*coords), outline)

    def draw(self, surface, x, y, width, height):
        background = parse_color(self.options["bg"])
        pixels = [[background] * self.width for _ in range(self.height * 2)]
        texts = []
        self._rasterize(pixels, texts)
        for row in range(min(self.height, height)):
            for column in range(min(self.width, width)):
                top, bottom = pixels[row * 2][column], pixels[row * 2 + 1][column]
                if top == bottom:
                    surface.put(x + column, y + row, " ", None, top)
                else:
                    surface.put(x + column, y + row, "▀", top, bottom)
        for (text_x, text_y), options in texts:
            self._draw_text(surface, x, y, pixels, text_x, text_y, options)

    def _draw_text(self, surface, x, y, pixels, text_x, text_y, options):
        text = options["text"]
        start = round(text_x)
        if options["anchor"] == "center":
            start -= len(text) // 2
        elif options["anchor"] == "e":
            start -= len(text) - 1
        row = round(text_y) // 2
        for offset, char in enumerate(text):
            column = start + offset
            if 0 <= column < self.width and 0 <= row < self.height:
                top, bottom = pixels[row * 2][column], pixels[row * 2 + 1][column]
                background = top if top == bottom else parse_color(self.options["bg"])
                surface.put(x + column, y + row, char, parse_color(options["fill"]),
                            background, options["bold"])
