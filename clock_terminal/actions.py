"""User input for Clock 2: asks for data and runs the pressed key."""

from clock_terminal.state import advance
from core.alarm import alarm_matches, clear_alarm, set_alarm
from core.stopwatch import reset_stopwatch, start_stopwatch, stop_stopwatch
from core.time_utils import format_time, parse_time

ADVANCE_LIMIT = 604800  # one week in seconds


def read_int(text, minimum, maximum):
    """Convert text to an integer within [minimum, maximum]. Return None if invalid."""
    try:
        value = int(text)
    except ValueError:
        return None
    if value < minimum or value > maximum:
        return None
    return value


def ask_start_time():
    """Ask for the start time and repeat until it is valid."""
    while True:
        seconds = parse_time(input("Hora inicial (HH:MM:SS): "), two_digits=False)
        if seconds is not None:
            return seconds
        print("Hora no válida. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def action_advance_seconds(state):
    """Ask how many seconds to advance and advance them."""
    amount = read_int(input("Segundos a avanzar (0-604800): "), 0, ADVANCE_LIMIT)
    if amount is None:
        state["message"] = "Cantidad no válida."
        return
    advance(state, amount)
    state["message"] = "Avanzados " + str(amount) + " s."


def action_stopwatch(state):
    """Start, stop, or reset the stopwatch."""
    option = input("Cronómetro: [i] iniciar  [p] parar  [r] reiniciar: ").strip().lower()
    stopwatch = state["stopwatch"]
    if option == "i":
        start_stopwatch(stopwatch)
        state["message"] = "Cronómetro en marcha."
    elif option == "p":
        stop_stopwatch(stopwatch)
        state["message"] = "Cronómetro parado."
    elif option == "r":
        reset_stopwatch(stopwatch)
        state["message"] = "Cronómetro reiniciado."
    else:
        state["message"] = "Opción de cronómetro no válida."


def action_alarm(state):
    """Set the alarm, or clear it if the input is left empty."""
    alarm = state["alarm"]
    text = input("Alarma HH:MM:SS (vacío = quitar): ").strip()
    if text == "":
        clear_alarm(alarm)
        state["message"] = "Alarma quitada."
        return
    seconds = parse_time(text, two_digits=False)
    if seconds is None:
        state["message"] = "Hora de alarma no válida."
        return
    set_alarm(alarm, seconds)
    alarm["ringing"] = alarm_matches(alarm, state["seconds"])
    state["message"] = "Alarma fijada a " + format_time(seconds) + "."


def process_option(state, option):
    """Run the action for the pressed key. Return False if the user quits."""
    if option == "":
        advance(state, 1)
    elif option == "n":
        action_advance_seconds(state)
    elif option == "c":
        action_stopwatch(state)
    elif option == "a":
        action_alarm(state)
    elif option == "f":
        state["format_24h"] = not state["format_24h"]
    elif option == "q":
        return False
    else:
        state["message"] = "Opción no válida: " + option
    return True
