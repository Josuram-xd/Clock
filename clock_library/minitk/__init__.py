"""minitk: a tiny tkinter-style toolkit drawn in the terminal, built without imports.

Same ideas as tkinter: a Tk window, Frame / Label / Button / Canvas widgets placed
with pack(), timers with after(), key bindings with bind(), and mainloop().
Colors are names or '#rrggbb'. Everything is printed with ANSI codes.
"""

from clock_library.minitk.canvas import Canvas
from clock_library.minitk.dialogs import askinteger, askstring, showinfo
from clock_library.minitk.widgets import Button, Frame, Label
from clock_library.minitk.window import Event, Tk

__all__ = [
    "Button",
    "Canvas",
    "Event",
    "Frame",
    "Label",
    "Tk",
    "askinteger",
    "askstring",
    "showinfo",
]
