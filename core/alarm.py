"""Alarm: state and operations, including midnight wrap-around."""

from core.time_utils import SECONDS_PER_DAY

RING_DURATION = 20  # seconds an alarm keeps ringing before it silences itself


def create_alarm():
    """Alarm with no time set and not ringing."""
    return {"time": None, "ringing": False, "ring_left": 0}


def set_alarm(alarm, seconds):
    """Set the alarm time (seconds of the day)."""
    alarm["time"] = seconds


def clear_alarm(alarm):
    """Remove the set time and silence the alarm if it was ringing."""
    alarm["time"] = None
    silence_alarm(alarm)


def silence_alarm(alarm):
    """Stop ringing but keep the alarm set for the next day."""
    alarm["ringing"] = False
    alarm["ring_left"] = 0


def tick_alarm(alarm, seconds):
    """Call once per clock second. Return True on the second it starts ringing."""
    if alarm["ringing"]:
        alarm["ring_left"] -= 1
        if alarm["ring_left"] <= 0:
            silence_alarm(alarm)
        return False
    if alarm_matches(alarm, seconds):
        alarm["ringing"] = True
        alarm["ring_left"] = RING_DURATION
        return True
    return False


def alarm_matches(alarm, seconds):
    """True if an alarm is set and it is the given time."""
    return alarm["time"] is not None and alarm["time"] == seconds


def seconds_until_alarm(current_seconds, alarm_time):
    """Seconds remaining (1 to 86400) until the alarm, wrapping past midnight."""
    remaining = (alarm_time - current_seconds) % SECONDS_PER_DAY
    return remaining if remaining > 0 else SECONDS_PER_DAY
