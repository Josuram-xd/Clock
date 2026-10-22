"""What each button does: callbacks that change the state and refresh the window."""

from clock_library import minitk as tk
from clock_library.state import advance
from core.alarm import clear_alarm, set_alarm
from core.stopwatch import reset_stopwatch, start_stopwatch, stop_stopwatch
from core.time_input import ask_time_of_day
from core.time_utils import format_time
from mymath import verify_library

ADVANCE_LIMIT = 604800  # one week in seconds


def build_actions(root, state, ui):
    """Return the callbacks by name, ready to be given to the buttons."""

    def done(message):
        ui.show_notice(message)
        ui.refresh(state)

    def toggle_stopwatch():
        stopwatch = state["stopwatch"]
        if stopwatch["active"]:
            stop_stopwatch(stopwatch)
            done("Cronómetro parado.")
        else:
            start_stopwatch(stopwatch)
            done("Cronómetro en marcha.")

    def reset():
        reset_stopwatch(state["stopwatch"])
        done("Cronómetro reiniciado.")

    def set_alarm_time():
        print("── Alarma ──")
        seconds = ask_time_of_day("Hora de la alarma (ej. 7:30 am, 1430; vacío = cancelar): ",
                                  allow_empty=True)
        if seconds is None:
            return
        set_alarm(state["alarm"], seconds)
        done("Alarma fijada a " + format_time(seconds) + ".")

    def remove_alarm():
        clear_alarm(state["alarm"])
        done("Alarma quitada.")

    def set_time():
        print("── Hora ──")
        seconds = ask_time_of_day("Nueva hora (ej. 2:30 pm, 1430; vacío = cancelar): ",
                                  allow_empty=True)
        if seconds is None:
            return
        state["seconds"] = seconds
        done("Hora cambiada a " + format_time(seconds) + ".")

    def advance_seconds():
        amount = tk.askinteger("Avanzar", "Segundos a avanzar (vacío = cancelar):",
                               0, ADVANCE_LIMIT)
        if amount is None:
            return
        if advance(state, amount):
            root.bell()
        done("Avanzados " + str(amount) + " s.")

    def toggle_format():
        state["format_24h"] = not state["format_24h"]
        done("Formato " + ("24 h." if state["format_24h"] else "12 h."))

    def self_test():
        verify_library()
        tk.showinfo("Autotest", "Fin del autotest de mymath.")

    return {
        "stopwatch": toggle_stopwatch,
        "reset": reset,
        "alarm": set_alarm_time,
        "clear_alarm": remove_alarm,
        "set_time": set_time,
        "advance": advance_seconds,
        "format": toggle_format,
        "selftest": self_test,
        "quit": root.quit,
    }
