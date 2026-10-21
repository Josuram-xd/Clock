"""Main menu for clock 1: option loop."""

from clock_library.display import MENU, draw_screen
from clock_library.input_reader import (
    ask_seconds_to_advance,
    ask_start_time,
    configure_alarm,
    stopwatch_menu,
)
from clock_library.state import advance, create_state
from core.time_utils import format_time
from mymath import verify_library


def advance_and_notify(state, amount):
    """Advance the clock and announce it if the alarm rang."""
    alarm_time = advance(state, amount)
    if alarm_time is not None:
        print(f"¡ALARMA! Son las {format_time(alarm_time)}")


def run_option(option, state):
    """Run the action chosen in the menu."""
    if option == "1":
        advance_and_notify(state, 1)
    elif option == "2":
        advance_and_notify(state, ask_seconds_to_advance())
    elif option == "3":
        stopwatch_menu(state)
    elif option == "4":
        configure_alarm(state)
    elif option == "5":
        verify_library()
    else:
        print("Opción inválida.")


def main():
    """Main loop: draw, read the option, and run the action."""
    try:
        state = create_state(ask_start_time())
        while True:
            draw_screen(state)
            print(MENU)
            option = input("Opción: ").strip()
            if option == "0":
                break
            run_option(option, state)
        print("Reloj apagado. ¡Hasta luego!")
    except EOFError:
        print("\nNo hay más entrada. Saliendo.")
