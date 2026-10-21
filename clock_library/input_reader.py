"""User input for clock 1: start time, seconds to advance, alarm, and stopwatch."""

from core.alarm import clear_alarm, set_alarm
from core.stopwatch import reset_stopwatch, start_stopwatch, stop_stopwatch
from core.time_utils import format_time, parse_time


def ask_start_time():
    """Ask for the start time until it is valid."""
    while True:
        seconds = parse_time(input("Hora inicial (HH:MM:SS): "))
        if seconds is not None:
            return seconds
        print("Hora inválida. Use HH:MM:SS con HH de 00 a 23 y MM/SS de 00 a 59.")


def ask_seconds_to_advance():
    """Ask for a positive integer number of seconds."""
    while True:
        text = input("Segundos a avanzar: ").strip()
        if text.isdecimal() and int(text) > 0:
            return int(text)
        print("Escriba un número entero mayor que 0.")


def configure_alarm(state):
    """Ask for the alarm time. An empty answer cancels the current alarm."""
    text = input("Hora de la alarma (HH:MM:SS, vacío para cancelar): ").strip()
    if text == "":
        clear_alarm(state["alarm"])
        print("Alarma cancelada.")
        return
    seconds = parse_time(text)
    if seconds is None:
        print("Hora inválida. Use el formato HH:MM:SS.")
        return
    set_alarm(state["alarm"], seconds)
    print(f"Alarma fijada a las {format_time(seconds)}.")


def stopwatch_menu(state):
    """Start/resume, stop, or reset the stopwatch."""
    print("  [1] iniciar/reanudar  [2] parar  [3] reiniciar (00:00)  [0] volver")
    option = input("Cronómetro> ").strip()
    stopwatch = state["stopwatch"]
    if option == "1":
        start_stopwatch(stopwatch)
    elif option == "2":
        stop_stopwatch(stopwatch)
    elif option == "3":
        reset_stopwatch(stopwatch)
    elif option != "0":
        print("Opción de cronómetro inválida.")
