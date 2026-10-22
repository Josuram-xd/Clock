"""Canvas: draw lines, ovals, rectangles, polygons, and text with tkinter-style items.

Every terminal cell shows two stacked pixels (a half block with a foreground and
a background color), so the canvas is width x (height * 2) pixels, each with its
own true color, and the pixels are almost square. Coordinates start at the
top-left corner, with y growing downward, as in tkinter, and may be fractions.

Drawing is anti-aliased by supersampling: items are painted in the order they
were created on a grid SCALE times finer, then every SCALE x SCALE block is
averaged into one pixel. Text items are written on whole cells (x is the column,
y // 2 is the row) over the pixels.
"""

from clock_library.minitk.colors import parse_color
from clock_library.minitk.widgets import Widget
from mymath.raster import ellipse_points, ellipse_spans, line_polygon, polygon_spans

SCALE = 3  # supersampling factor
PIXELS_PER_ROW = 2


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
        return self.width

    @property
    def pixel_height(self):
        """Height of the drawing area in pixels."""
        return self.height * PIXELS_PER_ROW

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

    def create_oval(self, x0, y0, x1, y1, fill=None, outline=None, width=1, tags=()):
        """Ellipse inscribed in the box (x0, y0)-(x1, y1)."""
        return self._create("oval", (x0, y0, x1, y1), fill=fill, outline=outline, width=width,
                            tags=tags)

    def create_rectangle(self, x0, y0, x1, y1, fill=None, outline=None, width=1, tags=()):
        """Rectangle with an optional fill color and outline."""
        return self._create("rectangle", (x0, y0, x1, y1), fill=fill, outline=outline,
                            width=width, tags=tags)

    def create_polygon(self, *points, fill="white", outline=None, width=1, tags=()):
        """Filled polygon through the given x, y pairs (tkinter-style flat coordinates)."""
        return self._create("polygon", points, fill=fill, outline=outline, width=width,
                            tags=tags)

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

    @staticmethod
    def _paint(fine, spans, color):
        """Fill pixel spans of the supersampled grid, clipped to its borders."""
        fine_height, fine_width = len(fine), len(fine[0])
        for y, first, end in spans:
            first, end = max(first, 0), min(end, fine_width)
            if 0 <= y < fine_height and end > first:
                fine[y][first:end] = [color] * (end - first)

    @staticmethod
    def _scaled(points):
        return [(x * SCALE, y * SCALE) for x, y in points]

    def _stroke(self, fine, polyline, color, width, closed):
        """Paint a polyline as a chain of thick segments."""
        count = len(polyline)
        for index in range(count if closed else count - 1):
            (x0, y0), (x1, y1) = polyline[index], polyline[(index + 1) % count]
            self._paint(fine, polygon_spans(line_polygon(x0, y0, x1, y1, width * SCALE)), color)

    def _rasterize(self, fine, item):
        kind, coords, options = item["kind"], item["coords"], item["options"]
        fill, outline = parse_color(options["fill"]), parse_color(options.get("outline"))
        width = options["width"]
        if kind == "line":
            x0, y0, x1, y1 = coords
            points = self._scaled([(x0, y0), (x1, y1)])
            self._stroke(fine, points, fill, width, closed=False)
            return
        if kind == "oval":
            x0, y0, x1, y1 = coords
            center_x, center_y = (x0 + x1) / 2 * SCALE, (y0 + y1) / 2 * SCALE
            radius_x, radius_y = abs(x1 - x0) / 2 * SCALE, abs(y1 - y0) / 2 * SCALE
            if fill is not None:
                self._paint(fine, ellipse_spans(center_x, center_y, radius_x, radius_y), fill)
            if outline is not None:
                steps = max(24, round(4 * (radius_x + radius_y)))
                ring = ellipse_points(center_x, center_y, radius_x, radius_y, steps)
                self._stroke(fine, ring, outline, width, closed=True)
            return
        if kind == "rectangle":
            x0, y0, x1, y1 = coords
            points = self._scaled([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
        else:  # polygon
            points = self._scaled(list(zip(coords[0::2], coords[1::2])))
        if fill is not None:
            self._paint(fine, polygon_spans(points), fill)
        if outline is not None:
            self._stroke(fine, points, outline, width, closed=True)

    def _pixels(self):
        """Render every shape and average the supersampled grid into final pixels."""
        background = parse_color(self.options["bg"])
        fine = [[background] * (self.pixel_width * SCALE) for _ in range(self.pixel_height * SCALE)]
        for item in self._items.values():
            if item["kind"] != "text":
                self._rasterize(fine, item)
        area = SCALE * SCALE
        pixels = []
        for y in range(self.pixel_height):
            rows = fine[y * SCALE:(y + 1) * SCALE]
            line = []
            for x in range(self.pixel_width):
                first = rows[0][x * SCALE]
                red = green = blue = 0
                flat = True
                for row in rows:
                    for color in row[x * SCALE:(x + 1) * SCALE]:
                        flat = flat and color == first
                        red += color[0]
                        green += color[1]
                        blue += color[2]
                line.append(first if flat else (red // area, green // area, blue // area))
            pixels.append(line)
        return pixels

    def draw(self, surface, x, y, width, height):
        pixels = self._pixels()
        for row in range(min(self.height, height)):
            for column in range(min(self.width, width)):
                top, bottom = pixels[row * 2][column], pixels[row * 2 + 1][column]
                if top == bottom:
                    surface.put(x + column, y + row, " ", None, top)
                else:
                    surface.put(x + column, y + row, "▀", top, bottom)
        for item in self._items.values():
            if item["kind"] == "text":
                self._draw_text(surface, x, y, pixels, item)

    def _draw_text(self, surface, x, y, pixels, item):
        options = item["options"]
        text_x, text_y = item["coords"]
        text = options["text"]
        start = round(text_x)
        if options["anchor"] == "center":
            start -= len(text) // 2
        elif options["anchor"] == "e":
            start -= len(text) - 1
        row = round(text_y) // PIXELS_PER_ROW
        for offset, char in enumerate(text):
            column = start + offset
            if 0 <= column < self.width and 0 <= row < self.height:
                top, bottom = pixels[row * 2][column], pixels[row * 2 + 1][column]
                background = tuple((a + b) // 2 for a, b in zip(top, bottom))
                surface.put(x + column, y + row, char, parse_color(options["fill"]),
                            background, options["bold"])
