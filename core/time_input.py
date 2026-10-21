"""Console helper to ask for a time of day: optional seconds, am/pm, and no colons needed."""

from core.time_utils import apply_meridiem, is_ambiguous_hour, parse_clock_time

EXAMPLES = "Ejemplos: 14:30, 14:30:15, 2:30 pm, 7am, 1430, 230pm."


def ask_time_of_day(prompt, allow_empty=False):
    """Ask until the answer is a valid time; return seconds of the day.

    An hour from 1 to 12 typed without am/pm gets a follow-up question; Enter there
    keeps it as typed (24 h). With allow_empty=True an empty answer (or Ctrl+C) cancels and returns None.
    """
    while True:
        try:
            text = input(prompt)
        except (EOFError, KeyboardInterrupt):
            if allow_empty:
                return None  # cancelled from a menu
            raise
        if allow_empty and text.strip() == "":
            return None
        seconds = parse_clock_time(text)
        if seconds is None:
            print("Hora no válida. " + EXAMPLES)
            continue
        if is_ambiguous_hour(text, seconds):
            answer = input("¿AM o PM? (a/p, Enter = dejarla como 24 h): ").strip().lower()
            if answer[:1] in ("a", "p"):
                seconds = apply_meridiem(seconds, answer[:1] + "m")
        return seconds
