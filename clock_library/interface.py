"""Window of clock 1, built with minitk exactly like a tkinter program would be:
a title bar, the watch face, three cards (time, stopwatch, alarm), buttons, and a status bar."""

from clock_library import minitk as tk
from clock_library.dial import (
    CANVAS_COLS,
    CANVAS_ROWS,
    WINDOW_BACKGROUND,
    create_hands,
    draw_face,
    update_dial,
)
from core.alarm import seconds_until_alarm
from core.stopwatch import describe_stopwatch, format_stopwatch
from core.time_utils import SECONDS_PER_DAY, format_time, format_time_12h

CARD_WIDTH = 33  # text width inside each card
WINDOW_WIDTH = CANVAS_COLS + CARD_WIDTH + 2  # cells between the window borders
NOTICE_MS = 5000

BAR_BACKGROUND = "#111a2e"
BORDER = "#334155"
CARD_BACKGROUND = "#131c2e"
TRACK = "#1f2a44"
TEXT = "#e2e8f0"
DIM = "#64748b"
ACCENT = "#38bdf8"
GREEN = "#4ade80"
AMBER = "#fbbf24"
ALARM_COLOR = "#f43f5e"
HINT = "Ctrl+C: pausa y menú de teclas"

# (button text, key, action name, background color); one inner list per row of buttons
BUTTON_ROWS = [
    [("▶ Cronómetro", "c", "stopwatch", "#166534"), ("↺ Reiniciar", "r", "reset", "#334155"),
     ("♪ Alarma", "a", "alarm", "#92400e"), ("✕ Quitar", "x", "clear_alarm", "#7f1d1d")],
    [("Hora", "h", "set_time", "#1e3a8a"), ("Avanzar", "n", "advance", "#334155"),
     ("12/24 h", "f", "format", "#334155"), ("Autotest", "v", "selftest", "#4c1d95"),
     ("Salir", "q", "quit", "#991b1b")],
]


def split_line(left, right, width):
    """One line of `width` characters with `left` at the start and `right` at the end."""
    return left + " " * max(1, width - len(left) - len(right)) + right


class ClockUi:
    """Creates every widget and redraws their texts from the clock state.

    `actions` maps button names to callbacks; it is looked up when a button is
    pressed, so it can be filled in after the window is built.
    """

    def __init__(self, root, actions):
        self.root = root
        self.notice = ""
        self.notice_timer = None
        root.title("Reloj · minitk")
        root.hint = ""  # the status bar shows it inside the window
        root.configure(bg=WINDOW_BACKGROUND, border=BORDER)

        self.header = tk.Label(root, fg=ACCENT, bg=BAR_BACKGROUND, width=WINDOW_WIDTH,
                               anchor="w", bold=True)
        self.header.pack()

        body = tk.Frame(root)
        body.pack()
        self.canvas = tk.Canvas(body, width=CANVAS_COLS, height=CANVAS_ROWS,
                                bg=WINDOW_BACKGROUND)
        self.canvas.pack(side="left")
        draw_face(self.canvas)
        self.hands = create_hands(self.canvas)

        cards = tk.Frame(body)
        cards.pack(side="left", anchor="center")

        time_card = self._card(cards)
        self.time_title = self._label(time_card, fg=DIM, anchor="w")
        self.digital = self._label(time_card, fg="#e0f2fe", font="big", bold=True)
        self.seconds_bar = self._bar(time_card, ACCENT)
        self._spacer(cards)

        stopwatch_card = self._card(cards)
        self.stopwatch_title = self._label(stopwatch_card, fg=DIM, anchor="w")
        self.stopwatch = self._label(stopwatch_card, fg=GREEN, font="big", bold=True)
        self._spacer(cards)

        alarm_card = self._card(cards)
        self.alarm_title = self._label(alarm_card, fg=DIM, anchor="w")
        self.alarm = self._label(alarm_card, fg=TEXT, bold=True)
        self.alarm_bar = self._bar(alarm_card, AMBER)

        for row in BUTTON_ROWS:
            strip = tk.Frame(root)
            strip.pack(anchor="center")
            for text, key, name, color in row:
                tk.Button(strip, text=text, key=key, bg=color,
                          command=lambda name=name: actions[name]()).pack(side="left", padx=1)

        self.status = tk.Label(root, fg=DIM, bg=BAR_BACKGROUND, width=WINDOW_WIDTH, anchor="w")
        self.status.pack()

    def _card(self, master):
        card = tk.Frame(master, bg=CARD_BACKGROUND, padding=(1, 0))
        card.pack()
        return card

    def _label(self, card, fg, anchor="center", font="normal", bold=False):
        label = tk.Label(card, fg=fg, bg=CARD_BACKGROUND, width=CARD_WIDTH, anchor=anchor,
                         font=font, bold=bold)
        label.pack()
        return label

    def _bar(self, card, color):
        bar = tk.ProgressBar(card, width=CARD_WIDTH, fg=color, bg=TRACK)
        bar.pack()
        return bar

    def _spacer(self, master):
        tk.Label(master, width=CARD_WIDTH + 2).pack()

    def show_notice(self, text):
        """Show a short message in the status bar; it disappears after a few seconds."""
        if self.notice_timer is not None:
            self.root.after_cancel(self.notice_timer)
        self.notice = text
        self.notice_timer = self.root.after(NOTICE_MS, self.show_notice_clear)
        self._draw_status()

    def show_notice_clear(self):
        """Hide the message."""
        self.notice_timer = None
        self.notice = ""
        self._draw_status()

    def _draw_status(self):
        left = " " + self.notice if self.notice else ""
        self.status.configure(text=split_line(left, HINT + " ", WINDOW_WIDTH),
                              fg=AMBER if self.notice else DIM)

    def refresh(self, state):
        """Update the hands and every text from the state."""
        alarm = state["alarm"]
        update_dial(self.canvas, self.hands, state["seconds"], alarm["time"])

        if state["format_24h"]:
            text, caption = format_time(state["seconds"]), "24 h"
        else:
            text, suffix = format_time_12h(state["seconds"])
            caption = "12 h " + suffix
        self.header["text"] = split_line("  ◷  RELOJ ANALÓGICO", "● en vivo  ", WINDOW_WIDTH)
        self.time_title["text"] = split_line("HORA", caption, CARD_WIDTH)
        self.digital["text"] = text
        self.seconds_bar["value"] = state["seconds"] % 60 / 59

        stopwatch = state["stopwatch"]
        icon = "▶" if stopwatch["active"] else "■"
        self.stopwatch_title["text"] = split_line(
            "CRONÓMETRO", icon + " " + describe_stopwatch(stopwatch), CARD_WIDTH)
        self.stopwatch["text"] = format_stopwatch(stopwatch["seconds"])

        if alarm["ringing"]:
            blink = state["seconds"] % 2 == 0
            self.alarm_title["text"] = split_line("ALARMA", "tecla x para quitarla", CARD_WIDTH)
            self.alarm.configure(text="¡¡ ALARMA !!" if blink else "", fg=ALARM_COLOR)
            self.alarm_bar["value"] = 1.0
        elif alarm["time"] is None:
            self.alarm_title["text"] = split_line("ALARMA", "tecla a para fijarla", CARD_WIDTH)
            self.alarm.configure(text="ninguna", fg=DIM)
            self.alarm_bar["value"] = 0.0
        else:
            left = seconds_until_alarm(state["seconds"], alarm["time"])
            self.alarm_title["text"] = split_line("ALARMA", "suena en " + format_time(left),
                                                  CARD_WIDTH)
            self.alarm.configure(text=format_time(alarm["time"]), fg=TEXT)
            self.alarm_bar["value"] = 1 - left / SECONDS_PER_DAY
        self._draw_status()
