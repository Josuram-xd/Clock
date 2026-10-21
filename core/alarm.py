"""Alarm: state and operations, including midnight wrap-around."""

from core.time_utils import SECONDS_PER_DAY


def create_alarm():
    """Alarm with no time set and not ringing."""
    return {"time": None, "ringing": False}


def set_alarm(alarm, seconds):
    """Set the alarm time (seconds of the day)."""
    alarm["time"] = seconds


def clear_alarm(alarm):
    """Remove the set time and silence the alarm if it was ringing."""
    alarm["time"] = None
    alarm["ringing"] = False


def alarm_matches(alarm, seconds):
    """True if an alarm is set and it is the given time."""
    return alarm["time"] is not None and alarm["time"] == seconds


def seconds_until_alarm(current_seconds, alarm_time):
    """Seconds remaining (1 to 86400) until the alarm, wrapping past midnight."""
    remaining = (alarm_time - current_seconds) % SECONDS_PER_DAY
    return remaining if remaining > 0 else SECONDS_PER_DAY
