"""Clock 1 state and time advance (time of day, stopwatch, alarm, and format)."""

from core.alarm import create_alarm, tick_alarm
from core.stopwatch import advance_stopwatch, create_stopwatch
from core.time_utils import next_second


def create_state(start_seconds):
    """Clock state: time of day, stopwatch, alarm, and 24 h / 12 h format."""
    return {
        "seconds": start_seconds,
        "format_24h": True,
        "stopwatch": create_stopwatch(),
        "alarm": create_alarm(),
    }


def advance_one_second(state):
    """Advance 1 s. Return True if the alarm starts ringing on that second."""
    state["seconds"] = next_second(state["seconds"])
    advance_stopwatch(state["stopwatch"])
    return tick_alarm(state["alarm"], state["seconds"])


def advance(state, amount):
    """Advance 'amount' seconds. Return True if the alarm started ringing meanwhile."""
    rang = False
    for _ in range(amount):
        if advance_one_second(state):
            rang = True
    return rang
