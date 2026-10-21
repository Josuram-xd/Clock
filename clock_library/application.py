"""Main program for clock 1: ask the time, build the window, and let a timer move the clock."""

from clock_library import minitk as tk
from clock_library.actions import build_actions
from clock_library.interface import ClockUi
from clock_library.state import advance_one_second, create_state
from core.time_input import ask_time_of_day

TICK_MS = 1000


def ask_start_time():
    """Ask for the start time (24 h, or 12 h with am/pm) until it is valid."""
    return ask_time_of_day("Hora actual (ej. 14:30, 2:30 pm, 1430): ")


def run(start_seconds):
    """Build the window and run it until the user quits."""
    state = create_state(start_seconds)
    root = tk.Tk("Reloj")
    actions = {}
    ui = ClockUi(root, actions)
    actions.update(build_actions(root, state, ui))

    def tick():
        root.after(TICK_MS, tick)  # reschedule first: a Ctrl+C in here must not stop the clock
        if advance_one_second(state):
            root.bell()
            ui.show_notice("¡Alarma!")
        ui.refresh(state)

    ui.refresh(state)
    root.after(TICK_MS, tick)
    root.mainloop()


def main():
    """Run the clock and exit gracefully if the input is closed."""
    print("Reloj con minitk (una mini-librería tipo tkinter, sin imports).")
    print("El reloj corre solo. Ctrl+C lo pausa y abre el menú de teclas.")
    print("Si va muy rápido o muy lento: Ctrl+C y luego «calibrar».")
    try:
        run(ask_start_time())
    except (EOFError, KeyboardInterrupt):
        print("\nReloj apagado.")
        return
    print("Reloj apagado. ¡Hasta luego!")
