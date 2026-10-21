"""Clock 2 state and time advancement (clock, stopwatch, alarm, and pacing)."""

from core.alarm import create_alarm, tick_alarm
from core.pacer import FRAMES_PER_SECOND, create_pacer
from core.stopwatch import advance_stopwatch, create_stopwatch
from core.time_utils import next_second

MESSAGE_SECONDS = 5  # how long a notice stays on screen


def create_state(start_seconds):
    """Create the dictionary that holds the whole application state."""
    return {
        "seconds": start_seconds,
        "frame": 0,  # frame inside the current second (0 to FRAMES_PER_SECOND - 1)
        "format_24h": True,
        "theme": 0,
        "stopwatch": create_stopwatch(),
        "alarm": create_alarm(),
        "pacer": create_pacer(),
        "calibrated": False,
        "message": "",
        "message_left": 0,
    }


def set_message(state, text):
    """Show a notice for a few seconds."""
    state["message"] = text
    state["message_left"] = MESSAGE_SECONDS


def advance_one_second(state):
    """Advance the clock by one second and update the stopwatch, alarm, and notice."""
    state["seconds"] = next_second(state["seconds"])
    advance_stopwatch(state["stopwatch"])
    if tick_alarm(state["alarm"], state["seconds"]):
        set_message(state, "¡Alarma!")
    if state["message_left"] > 0:
        state["message_left"] -= 1
        if state["message_left"] == 0:
            state["message"] = ""


def advance(state, amount):
    """Advance the clock by the given number of seconds."""
    for _ in range(amount):
        advance_one_second(state)


def step_frame(state):
    """Count one waited frame; every FRAMES_PER_SECOND frames the clock ticks."""
    state["frame"] += 1
    if state["frame"] >= FRAMES_PER_SECOND:
        state["frame"] = 0
        advance_one_second(state)
