"""User input for clock 3: time, optional alarm and optional stopwatch."""

from core.time_utils import parse_time


def ask_time(prompt, optional=False):
    """Ask for a time (in seconds of the day) until it is valid. If optional, Enter gives None."""
    while True:
        text = input(prompt)
        if optional and text.strip() == "":
            return None
        value = parse_time(text, two_digits=False)
        if value is not None:
            return value
        print("Formato no válido. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def ask_yes_no(prompt):
    """Ask until 's' or 'n' is received. Returns True for 's'."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("s", "n"):
            return answer == "s"
        print("Responde s o n.")


def ask_stopwatch_seconds():
    """Ask for the stopwatch starting seconds (an integer of 0 or more)."""
    while True:
        text = input("Duración de arranque del cronómetro en segundos: ").strip()
        if text.isdecimal():
            return int(text)
        print("Escribe un número entero de segundos (0 o más).")


def ask_stopwatch():
    """Return None if no stopwatch is wanted; otherwise its starting seconds."""
    if not ask_yes_no("¿Quieres cronómetro? (s/n): "):
        return None
    return ask_stopwatch_seconds()
