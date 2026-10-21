"""Clock 2 screen: status texts and construction of the full image."""

from clock_terminal.ansi import (
    BOLD,
    CLEAR_SCREEN,
    CYAN,
    RED_BLINK,
    WHITE,
    YELLOW,
    center_text,
    colorize,
    draw_box,
)
from clock_terminal.dial import draw_dial
from clock_terminal.digits import draw_digital
from core.stopwatch import describe_stopwatch, format_stopwatch
from core.time_utils import format_time, format_time_12h

BOX_WIDTH = 60


def clock_text(state):
    """Return (time text, AM/PM suffix) according to the chosen format."""
    if state["format_24h"]:
        return format_time(state["seconds"]), ""
    return format_time_12h(state["seconds"])


def stopwatch_text(state):
    """Return the stopwatch in MM:SS format with its status."""
    stopwatch = state["stopwatch"]
    return (format_stopwatch(stopwatch["seconds"])
            + " (" + describe_stopwatch(stopwatch) + ")")


def alarm_line(state):
    """Return the alarm line; it blinks in red while ringing."""
    alarm = state["alarm"]
    if alarm["ringing"]:
        if state["blink"]:
            return colorize("¡ALARMA!", RED_BLINK)
        return " " * len("¡ALARMA!")
    if alarm["time"] is None:
        return "Alarma: ninguna"
    return "Alarma: " + format_time(alarm["time"])


def box_lines(state):
    """Box content: title, dial, digital time, and status."""
    lines = [center_text(colorize("RELOJ DE TERMINAL", BOLD + CYAN), BOX_WIDTH), None]

    for row in draw_dial(state["seconds"]):
        lines.append(center_text(row, BOX_WIDTH))
    lines.append(None)

    text, suffix = clock_text(state)
    for row in draw_digital(text):
        lines.append(center_text(colorize(row, WHITE + BOLD), BOX_WIDTH))
    lines.append(center_text(suffix, BOX_WIDTH))
    lines.append(None)

    label = "24h" if state["format_24h"] else "12h"
    lines.append(" Formato: " + label + "   Cronómetro: " + stopwatch_text(state))
    lines.append(" " + alarm_line(state))
    return lines


def build_screen(state):
    """Build the full screen text (without clearing it)."""
    output = draw_box(box_lines(state), BOX_WIDTH)
    output.append(colorize(" [Enter] +1 s    [n] avanzar N s    [c] cronómetro", CYAN))
    output.append(colorize(" [a] alarma (vacío = quitar)    [f] 12h/24h    [q] salir", CYAN))
    if state["message"]:
        output.append(colorize(" " + state["message"], YELLOW))
    return "\n".join(output)


def draw_screen(state):
    """Clear the screen and draw the clock."""
    print(CLEAR_SCREEN + build_screen(state))
