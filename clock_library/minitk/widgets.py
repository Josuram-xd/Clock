"""Widgets: the base class, Frame (container with pack layout), Label, and Button."""

from clock_library.minitk.colors import parse_color
from clock_library.minitk.fonts import big_lines

PRESS_MS = 250  # how long a button stays highlighted after being invoked


class Widget:
    """Base of every widget: options, pack layout, and change tracking."""

    def __init__(self, master):
        self.master = master
        self.options = {}
        self.pack_options = {"side": "top", "padx": 0, "pady": 0, "fill": None, "anchor": "w"}
        self.children = []  # widgets packed inside, in order

    @property
    def root(self):
        """The Tk window this widget belongs to."""
        widget = self
        while widget.master is not None:
            widget = widget.master
        return widget

    def pack(self, side="top", padx=0, pady=0, fill=None, anchor="w"):
        """Place the widget in its master: stacked ('top') or in a row ('left').

        fill='x' / 'y' / 'both' stretches it over the free space of the master;
        anchor='w' or 'center' aligns a widget across its row or column
        (horizontally when stacked, vertically when in a row).
        """
        self.pack_options = {"side": side, "padx": padx, "pady": pady, "fill": fill,
                             "anchor": anchor}
        if self not in self.master.children:
            self.master.children.append(self)
        self.mark_changed()

    def pack_forget(self):
        """Remove the widget from the layout."""
        if self in self.master.children:
            self.master.children.remove(self)
        self.mark_changed()

    def configure(self, **options):
        """Change options such as text, fg, bg or command."""
        self.options.update(options)
        self.mark_changed()

    config = configure

    def cget(self, name):
        """Current value of an option."""
        return self.options[name]

    def __setitem__(self, name, value):
        self.configure(**{name: value})

    def __getitem__(self, name):
        return self.cget(name)

    def mark_changed(self):
        """Ask the window to redraw on the next frame."""
        self.root.changed = True

    def natural_size(self):
        """(width, height) in cells the widget would like to occupy."""
        return 0, 0

    def draw(self, surface, x, y, width, height):
        """Draw inside the rectangle that the layout assigned."""


def outer_size(widget):
    """Natural size of a widget including its pack padding."""
    width, height = widget.natural_size()
    return width + 2 * widget.pack_options["padx"], height + 2 * widget.pack_options["pady"]


class Frame(Widget):
    """Container that lays its children out in a column or a row."""

    def __init__(self, master, bg=None, border=None, title=""):
        super().__init__(master)
        self.options.update(bg=bg, border=border, title=title)

    def _inset(self):
        return 1 if self.options["border"] else 0

    def natural_size(self):
        sizes = [outer_size(child) for child in self.children]
        if not sizes:
            content_width = content_height = 0
        elif self.children[0].pack_options["side"] == "left":
            content_width = sum(width for width, _ in sizes)
            content_height = max(height for _, height in sizes)
        else:
            content_width = max(width for width, _ in sizes)
            content_height = sum(height for _, height in sizes)
        return content_width + 2 * self._inset(), content_height + 2 * self._inset()

    def draw(self, surface, x, y, width, height):
        background = parse_color(self.options["bg"])
        if background is not None:
            surface.fill(x, y, width, height, background)
        if self.options["border"]:
            surface.border(x, y, width, height, parse_color(self.options["border"]),
                           self.options["title"])
        inset = self._inset()
        left, top = x + inset, y + inset
        inner_width, inner_height = width - 2 * inset, height - 2 * inset
        row = bool(self.children) and self.children[0].pack_options["side"] == "left"
        cursor = 0
        for child in self.children:
            pad_x, pad_y = child.pack_options["padx"], child.pack_options["pady"]
            fill = child.pack_options["fill"]
            child_width, child_height = child.natural_size()
            if row:
                if fill in ("y", "both"):
                    child_height = inner_height - 2 * pad_y
                shift = 0
                if child.pack_options["anchor"] == "center":
                    shift = (inner_height - child_height - 2 * pad_y) // 2
                child.draw(surface, left + cursor + pad_x, top + shift + pad_y, child_width,
                           child_height)
                cursor += child_width + 2 * pad_x
            else:
                if fill in ("x", "both"):
                    child_width = inner_width - 2 * pad_x
                shift = 0
                if child.pack_options["anchor"] == "center":
                    shift = (inner_width - child_width - 2 * pad_x) // 2
                child.draw(surface, left + shift + pad_x, top + cursor + pad_y, child_width,
                           child_height)
                cursor += child_height + 2 * pad_y


class Label(Widget):
    """Static text (one or several lines). font='big' draws digits in large blocks."""

    def __init__(self, master, text="", fg="white", bg=None, anchor="center", width=0,
                 bold=False, font="normal"):
        super().__init__(master)
        self.options.update(text=text, fg=fg, bg=bg, anchor=anchor, width=width, bold=bold,
                            font=font)

    def _lines(self):
        text = str(self.options["text"])
        if self.options["font"] == "big":
            return big_lines(text)
        return text.split("\n")

    def natural_size(self):
        lines = self._lines()
        return max(self.options["width"], max(len(line) for line in lines)), len(lines)

    def draw(self, surface, x, y, width, height):
        background = parse_color(self.options["bg"])
        if background is not None:
            surface.fill(x, y, width, height, background)
        for index, line in enumerate(self._lines()[:height]):
            if self.options["anchor"] == "w":
                start = x
            elif self.options["anchor"] == "e":
                start = x + width - len(line)
            else:
                start = x + (width - len(line)) // 2
            surface.text(start, y + index, line, parse_color(self.options["fg"]), background,
                         self.options["bold"])


class Button(Widget):
    """Pressable button. 'key' is the key that invokes it (typed in the Ctrl+C menu)."""

    def __init__(self, master, text="", command=None, key=None, fg="white", bg="slate"):
        super().__init__(master)
        self.options.update(text=text, command=command, key=key, fg=fg, bg=bg)
        self.pressed = False
        root = self.root
        root.buttons.append(self)
        if key:
            root.bind("<Key-" + key + ">", lambda event: self.invoke())

    def label(self):
        """Text shown on the button, with its key."""
        key = self.options["key"]
        suffix = f" ({key})" if key else ""
        return " " + self.options["text"] + suffix + " "

    def natural_size(self):
        return len(self.label()), 1

    def invoke(self):
        """Press the button: highlight it for a moment and run its command."""
        self.pressed = True
        self.mark_changed()
        self.root.after(PRESS_MS, self._release)
        command = self.options["command"]
        if command is not None:
            command()

    def _release(self):
        self.pressed = False
        self.mark_changed()

    def draw(self, surface, x, y, width, height):
        background = parse_color(self.options["fg"] if self.pressed else self.options["bg"])
        foreground = parse_color(self.options["bg"] if self.pressed else self.options["fg"])
        surface.text(x, y, self.label().ljust(width), foreground, background, bold=True)
