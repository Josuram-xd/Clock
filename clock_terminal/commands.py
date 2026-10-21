"""Pause menu of clock 2: commands typed after Ctrl+C."""

from clock_terminal.ansi import CLEAR_SCREEN, CYAN, colorize
from clock_terminal.live import run_clock
from clock_terminal.screen import draw_screen
from clock_terminal.state import advance, set_message
from clock_terminal.themes import THEMES
from core.alarm import alarm_matches, clear_alarm, set_alarm, silence_alarm
from core.pacer import MIN_CALIBRATION_SECONDS, finish_calibration, start_calibration
from core.stopwatch import reset_stopwatch, start_stopwatch, stop_stopwatch
from core.time_utils import format_time, parse_time

ADVANCE_LIMIT = 604800  # one week in seconds

MENU = """Reloj en pausa. Escribe un comando (Enter = seguir):
  h [HH:MM:SS]   cambiar la hora            n [N]   avanzar N segundos
  c [i|p|r]      cronómetro: iniciar, parar, reiniciar
  a [HH:MM:SS]   fijar la alarma (a quitar = silenciar y borrar)
  f              12 h / 24 h                t       cambiar el tema
  k              calibrar la velocidad      q       salir"""


def ask_start_time():
    """Ask for the start time and repeat until it is valid."""
    while True:
        seconds = parse_time(input("Hora actual (HH:MM:SS): "), two_digits=False)
        if seconds is not None:
            return seconds
        print("Hora no válida. Usa HH:MM:SS (00-23, 00-59, 00-59).")


def argument_or_ask(argument, question):
    """The typed argument, or the answer to a question when it was left out."""
    return argument if argument else input(question).strip()


def cmd_time(state, argument):
    """Set the time of the day."""
    seconds = parse_time(argument_or_ask(argument, "Nueva hora (HH:MM:SS): "), two_digits=False)
    if seconds is None:
        set_message(state, "Hora no válida.")
        return
    state["seconds"] = seconds
    state["frame"] = 0
    set_message(state, "Hora cambiada a " + format_time(seconds) + ".")


def cmd_advance(state, argument):
    """Advance N seconds at once."""
    text = argument_or_ask(argument, "Segundos a avanzar (0-604800): ")
    if not text.isdecimal() or int(text) > ADVANCE_LIMIT:
        set_message(state, "Cantidad no válida.")
        return
    advance(state, int(text))
    set_message(state, "Avanzados " + text + " s.")


def cmd_stopwatch(state, argument):
    """Start, stop, or reset the stopwatch."""
    option = argument_or_ask(argument, "Cronómetro: [i] iniciar  [p] parar  [r] reiniciar: ").lower()
    stopwatch = state["stopwatch"]
    if option == "i":
        start_stopwatch(stopwatch)
        set_message(state, "Cronómetro en marcha.")
    elif option == "p":
        stop_stopwatch(stopwatch)
        set_message(state, "Cronómetro parado.")
    elif option == "r":
        reset_stopwatch(stopwatch)
        set_message(state, "Cronómetro reiniciado.")
    else:
        set_message(state, "Opción de cronómetro no válida.")


def cmd_alarm(state, argument):
    """Set the alarm; 'quitar' (or an empty answer) silences and clears it."""
    alarm = state["alarm"]
    text = argument_or_ask(argument, "Alarma HH:MM:SS (vacío = quitar): ")
    if text == "" or text.lower() == "quitar":
        clear_alarm(alarm)
        set_message(state, "Alarma quitada.")
        return
    seconds = parse_time(text, two_digits=False)
    if seconds is None:
        set_message(state, "Hora de alarma no válida.")
        return
    set_alarm(alarm, seconds)
    silence_alarm(alarm)
    if alarm_matches(alarm, state["seconds"]):
        alarm["time"] = None  # it is that time right now: it would only ring tomorrow
    set_message(state, "Alarma fijada a " + format_time(seconds) + ".")


def cmd_format(state, argument):
    """Switch between 12 h and 24 h."""
    state["format_24h"] = not state["format_24h"]
    set_message(state, "Formato " + ("24 h." if state["format_24h"] else "12 h."))


def cmd_theme(state, argument):
    """Switch to the next color theme."""
    state["theme"] = (state["theme"] + 1) % len(THEMES)
    set_message(state, "Tema: " + THEMES[state["theme"]]["name"] + ".")


def cmd_calibrate(state, argument):
    """Correct the speed: run the clock while the user times it with a stopwatch."""
    print("Calibración: inicia un cronómetro real (el del celular sirve) y pulsa Enter.")
    print(f"Deja correr el reloj al menos {MIN_CALIBRATION_SECONDS} s (mejor 30 s o más) "
          "y pulsa Ctrl+C en el instante en que pares tu cronómetro.")
    input("Enter para empezar... ")
    start_calibration(state["pacer"])
    run_clock(state)
    print()
    try:
        real_seconds = float(input("¿Cuántos segundos marcó tu cronómetro? ").replace(",", "."))
    except ValueError:
        set_message(state, "Calibración cancelada: número no válido.")
        return
    accuracy = finish_calibration(state["pacer"], real_seconds)
    if accuracy is None:
        set_message(state, f"Medida muy corta (mínimo {MIN_CALIBRATION_SECONDS} s): sin cambios.")
        return
    state["calibrated"] = True
    set_message(state, f"Calibrado (el reloj iba al {accuracy} %). Repite para afinar.")


COMMANDS = {
    "h": cmd_time,
    "n": cmd_advance,
    "c": cmd_stopwatch,
    "a": cmd_alarm,
    "f": cmd_format,
    "t": cmd_theme,
    "k": cmd_calibrate,
}


def run_command(state, line):
    """Run one typed command. Return False if the user wants to quit."""
    name, _, argument = line.strip().partition(" ")
    name = name.lower()
    if name == "q":
        return False
    command = COMMANDS.get(name)
    if command is None:
        set_message(state, "Comando no válido: " + name)
    else:
        command(state, argument.strip())
    return True


def pause_menu(state):
    """Show the clock frozen with the menu. Return False when the user quits."""
    while True:
        print(CLEAR_SCREEN, end="")
        draw_screen(state)
        print(colorize(MENU, CYAN))
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            return False
        if line.strip() == "":
            return True
        if not run_command(state, line):
            return False
