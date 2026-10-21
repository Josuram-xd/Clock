"""Display for clock 1: dial and digital readouts."""

from clock_library.dial import WIDTH, show_dial
from core.stopwatch import describe_stopwatch, format_stopwatch
from core.time_utils import format_time

MENU = """
[1] Avanzar 1 segundo
[2] Avanzar N segundos
[3] Cronómetro
[4] Fijar alarma
[5] Autotest de la librería
[0] Salir"""


def alarm_text(alarm):
    """Alarm time, or 'ninguna' when none is set."""
    return "ninguna" if alarm["time"] is None else format_time(alarm["time"])


def draw_screen(state):
    """Redraw the dial and the digital readouts."""
    stopwatch = state["stopwatch"]
    print("=" * WIDTH)
    show_dial(state["seconds"])
    print("=" * WIDTH)
    print(f"Hora digital: {format_time(state['seconds'])}")
    print(f"Cronómetro: {format_stopwatch(stopwatch['seconds'])} "
          f"({describe_stopwatch(stopwatch)})")
    print(f"Alarma: {alarm_text(state['alarm'])}")
