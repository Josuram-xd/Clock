"""Main program for Clock 2: screen loop and key handling."""

from clock_terminal.actions import ask_start_time, process_option
from clock_terminal.ansi import CLEAR_SCREEN, CYAN, colorize
from clock_terminal.screen import draw_screen
from clock_terminal.state import create_state


def main_loop():
    """Ask for the time, draw, and process keys until the user quits."""
    print(CLEAR_SCREEN + colorize("Bienvenido al reloj de terminal.", CYAN))
    state = create_state(ask_start_time())
    keep_running = True
    while keep_running:
        state["blink"] = not state["blink"]
        draw_screen(state)
        state["message"] = ""
        option = input("Opción: ").strip().lower()
        keep_running = process_option(state, option)
    print("Hasta luego.")


def main():
    """Run the clock and exit gracefully if the input is closed."""
    try:
        main_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego.")
