"""Clock 1 state and time advance (time of day, stopwatch, and alarm)."""

from core.alarm import alarm_matches, clear_alarm, create_alarm
from core.stopwatch import advance_stopwatch, create_stopwatch
from core.time_utils import next_second


def create_state(start_seconds):
    """Clock state: time of day, stopwatch, and alarm."""
    return {
        "seconds": start_seconds,
        "stopwatch": create_stopwatch(),
        "alarm": create_alarm(),
    }


def advance_one_second(state):
    """Advance 1 s. Return True if the alarm rings on that second."""
    state["seconds"] = next_second(state["seconds"])
    advance_stopwatch(state["stopwatch"])
    if alarm_matches(state["alarm"], state["seconds"]):
        clear_alarm(state["alarm"])
        return True
    return False


def advance(state, amount):
    """Advance 'amount' seconds. Return the alarm time if it rang, or None."""
    alarm_time = state["alarm"]["time"]
    rang = False
    for _ in range(amount):
        if advance_one_second(state):
            rang = True
    return alarm_time if rang else None
