"""Clock 2 state and time advancement (clock, stopwatch, and alarm)."""

from core.alarm import alarm_matches, create_alarm
from core.stopwatch import advance_stopwatch, create_stopwatch
from core.time_utils import next_second


def create_state(start_seconds):
    """Create the dictionary that holds the whole application state."""
    return {
        "seconds": start_seconds,
        "format_24h": True,
        "stopwatch": create_stopwatch(),
        "alarm": create_alarm(),
        "blink": False,
        "message": "",
    }


def advance_one_second(state):
    """Advance the clock by one second and update the stopwatch and alarm."""
    state["seconds"] = next_second(state["seconds"])
    advance_stopwatch(state["stopwatch"])
    if alarm_matches(state["alarm"], state["seconds"]):
        state["alarm"]["ringing"] = True


def advance(state, amount):
    """Advance the clock by the given number of seconds."""
    for _ in range(amount):
        advance_one_second(state)
