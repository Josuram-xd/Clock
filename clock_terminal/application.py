"""Main program for Clock 2: ask the time, run the live clock, open the menu on Ctrl+C."""

from clock_terminal.ansi import CLEAR_SCREEN, CYAN, HIDE_CURSOR, SHOW_CURSOR, colorize
from clock_terminal.commands import ask_start_time, pause_menu
from clock_terminal.live import run_clock
from clock_terminal.state import create_state


def main_loop():
    """Alternate between the running clock and the pause menu until the user quits."""
    print(CLEAR_SCREEN + colorize("Reloj de terminal.", CYAN))
    print("El reloj corre solo. Ctrl+C lo pausa y abre el menú (alarma, cronómetro, tema...).")
    print("Si va muy rápido o muy lento: Ctrl+C y luego el comando k (calibrar).")
    state = create_state(ask_start_time())
    print(CLEAR_SCREEN + HIDE_CURSOR, end="")
    keep_running = True
    while keep_running:
        run_clock(state)
        print(SHOW_CURSOR, end="")
        keep_running = pause_menu(state)
        print(HIDE_CURSOR, end="")
    print(SHOW_CURSOR + "\nHasta luego.")


def main():
    """Run the clock and always give the cursor back, even if the input is closed."""
    try:
        main_loop()
    except (EOFError, KeyboardInterrupt):
        print(SHOW_CURSOR + "\nHasta luego.")
    finally:
        print(SHOW_CURSOR, end="")
