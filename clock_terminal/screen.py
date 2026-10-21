"""Clock 2 screen: the side panel and construction of the full image."""

from clock_terminal.ansi import (
    BELL,
    BOLD,
    CLEAR_BELOW,
    CLEAR_LINE,
    CURSOR_HOME,
    DIM,
    YELLOW,
    center_text,
    colorize,
    draw_box,
    pad_to,
)
from clock_terminal.dial import DIAL_COLS, draw_dial
from clock_terminal.digits import draw_digital
from clock_terminal.themes import current_theme
from core.alarm import seconds_until_alarm
from core.pacer import FRAMES_PER_SECOND
from core.stopwatch import describe_stopwatch, format_stopwatch
from core.time_utils import format_time, format_time_12h

PANEL_WIDTH = 31
SEPARATOR = " │ "
BOX_WIDTH = DIAL_COLS + len(SEPARATOR) + PANEL_WIDTH
BLINK_FRAME = FRAMES_PER_SECOND // 2  # the colon is hidden during the second half of a second


def clock_text(state):
    """Return (time text, caption) according to the chosen format."""
    if state["format_24h"]:
        return format_time(state["seconds"]), "formato 24 h"
    text, suffix = format_time_12h(state["seconds"])
    return text, suffix + " · formato 12 h"


def alarm_lines(state, theme):
    """Two lines with the alarm: its time and a countdown, or the ringing notice."""
    alarm = state["alarm"]
    if alarm["ringing"]:
        if state["frame"] < BLINK_FRAME:
            return [colorize("¡¡ ALARMA !!", theme["alert"]), "Ctrl+C → a para quitarla"]
        return ["", ""]
    if alarm["time"] is None:
        return ["ALARMA  ninguna", colorize("(Ctrl+C → a HH:MM:SS)", DIM)]
    left = seconds_until_alarm(state["seconds"], alarm["time"])
    return ["ALARMA  " + format_time(alarm["time"]), colorize("suena en " + format_time(left), DIM)]


def panel_lines(state, theme):
    """The 17 lines of the right panel: title, digital time, stopwatch, alarm, and status."""
    def center(text):
        return center_text(text, PANEL_WIDTH)

    text, caption = clock_text(state)
    digits = draw_digital(text, state["frame"] < BLINK_FRAME)
    stopwatch = state["stopwatch"]
    icon = "▶" if stopwatch["active"] else "■"
    speed = "calibrada" if state["calibrated"] else "sin calibrar"

    lines = [center(colorize("RELOJ DE TERMINAL", theme["title"])), ""]
    lines += [center(colorize(row, theme["digits"])) for row in digits]
    lines += [center(colorize(caption, DIM)), ""]
    lines += [
        center(colorize("CRONÓMETRO  ", theme["label"]) + format_stopwatch(stopwatch["seconds"])),
        center(icon + " " + describe_stopwatch(stopwatch)),
        "",
    ]
    lines += [center(line) for line in alarm_lines(state, theme)]
    lines += ["", center("Tema: " + theme["name"]), center("Velocidad: " + speed), ""]
    lines.append(center(colorize("Ctrl+C = pausa y menú", DIM)))
    return lines


def build_screen(state):
    """Build the full screen text: boxed dial and panel, plus the notice line."""
    theme = current_theme(state)
    dial = draw_dial(state["seconds"], theme)
    separator = colorize(SEPARATOR, theme["frame"])
    panel = panel_lines(state, theme)
    rows = [pad_to(d, DIAL_COLS) + separator + pad_to(p, PANEL_WIDTH) for d, p in zip(dial, panel)]
    output = draw_box(rows, BOX_WIDTH, theme["frame"])
    output.append(colorize(" " + state["message"], BOLD + YELLOW) if state["message"] else "")
    return output


def draw_screen(state):
    """Redraw the clock in place, without clearing the screen (no flicker)."""
    lines = [line + CLEAR_LINE for line in build_screen(state)]
    ring = BELL if state["alarm"]["ringing"] and state["frame"] == 0 else ""
    print(CURSOR_HOME + "\n".join(lines) + "\n" + CLEAR_BELOW + ring, end="", flush=True)
