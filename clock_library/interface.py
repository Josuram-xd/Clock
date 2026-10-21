"""Window of clock 1, built with minitk exactly like a tkinter program would be."""

from clock_library import minitk as tk
from clock_library.dial import CANVAS_COLS, CANVAS_ROWS, create_hands, draw_face, update_dial
from core.alarm import seconds_until_alarm
from core.stopwatch import describe_stopwatch, format_stopwatch
from core.time_utils import format_time, format_time_12h

PANEL_WIDTH = 34
NOTICE_MS = 5000
ALARM_COLOR = "red"
TEXT_COLOR = "white"
DIM_COLOR = "gray"

# (button text, key, action name); one inner list per row of buttons
BUTTON_ROWS = [
    [("Cronómetro", "c", "stopwatch"), ("Reiniciar", "r", "reset"),
     ("Alarma", "a", "alarm"), ("Quitar alarma", "x", "clear_alarm")],
    [("Hora", "h", "set_time"), ("Avanzar", "n", "advance"), ("12/24 h", "f", "format"),
     ("Autotest", "v", "selftest"), ("Salir", "q", "quit")],
]


class ClockUi:
    """Creates every widget and redraws their texts from the clock state.

    `actions` maps button names to callbacks; it is looked up when a button is
    pressed, so it can be filled in after the window is built.
    """

    def __init__(self, root, actions):
        self.root = root
        self.notice_timer = None
        root.title("Reloj · minitk")
        body = tk.Frame(root)
        body.pack(pady=0)

        self.canvas = tk.Canvas(body, width=CANVAS_COLS, height=CANVAS_ROWS, bg="navy")
        self.canvas.pack(side="left")
        draw_face(self.canvas)
        self.hands = create_hands(self.canvas)

        panel = tk.Frame(body)
        panel.pack(side="left", padx=2)
        self.title = self._label(panel, "RELOJ ANALÓGICO", fg="cyan", bold=True)
        self.digital = tk.Label(panel, font="big", width=PANEL_WIDTH, bold=True)
        self.digital.pack(pady=1)
        self.caption = self._label(panel, "", fg=DIM_COLOR)
        self._label(panel, "")
        self.stopwatch = self._label(panel, "")
        self.alarm = self._label(panel, "")
        self.countdown = self._label(panel, "", fg=DIM_COLOR)
        self._label(panel, "")
        self.notice = self._label(panel, "", fg="yellow", bold=True)

        for row in BUTTON_ROWS:
            strip = tk.Frame(root)
            strip.pack(anchor="center")
            for text, key, name in row:
                tk.Button(strip, text=text, key=key,
                          command=lambda name=name: actions[name]()).pack(side="left", padx=1)

    def _label(self, master, text, fg=TEXT_COLOR, bold=False):
        label = tk.Label(master, text=text, fg=fg, width=PANEL_WIDTH, bold=bold)
        label.pack()
        return label

    def show_notice(self, text):
        """Show a short message in the panel; it disappears after a few seconds."""
        if self.notice_timer is not None:
            self.root.after_cancel(self.notice_timer)
        self.notice["text"] = text
        self.notice_timer = self.root.after(NOTICE_MS, self.show_notice_clear)

    def show_notice_clear(self):
        """Hide the message."""
        self.notice_timer = None
        self.notice["text"] = ""

    def refresh(self, state):
        """Update the hands and every text from the state."""
        alarm = state["alarm"]
        update_dial(self.canvas, self.hands, state["seconds"], alarm["time"])

        if state["format_24h"]:
            text, caption = format_time(state["seconds"]), "formato 24 h"
        else:
            text, suffix = format_time_12h(state["seconds"])
            caption = suffix + " · formato 12 h"
        self.digital["text"] = text
        self.caption["text"] = caption

        stopwatch = state["stopwatch"]
        icon = "▶" if stopwatch["active"] else "■"
        self.stopwatch["text"] = ("CRONÓMETRO  " + format_stopwatch(stopwatch["seconds"])
                                  + "  " + icon + " " + describe_stopwatch(stopwatch))

        if alarm["ringing"]:
            blink = state["seconds"] % 2 == 0
            self.alarm.configure(text="¡¡ ALARMA !!" if blink else "", fg=ALARM_COLOR)
            self.countdown["text"] = "tecla x para quitarla"
        elif alarm["time"] is None:
            self.alarm.configure(text="ALARMA  ninguna", fg=TEXT_COLOR)
            self.countdown["text"] = "(tecla a para fijarla)"
        else:
            self.alarm.configure(text="ALARMA  " + format_time(alarm["time"]), fg=TEXT_COLOR)
            left = seconds_until_alarm(state["seconds"], alarm["time"])
            self.countdown["text"] = "suena en " + format_time(left)
