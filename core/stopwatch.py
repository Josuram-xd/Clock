"""Stopwatch: state and operations, without interface."""


def create_stopwatch():
    """Stopwatch stopped at 00:00."""
    return {"seconds": 0, "active": False}


def start_stopwatch(stopwatch):
    """Start or resume the stopwatch."""
    stopwatch["active"] = True


def stop_stopwatch(stopwatch):
    """Stop the stopwatch, keeping the elapsed time."""
    stopwatch["active"] = False


def reset_stopwatch(stopwatch):
    """Return to 00:00 and leave the stopwatch stopped."""
    stopwatch["seconds"] = 0
    stopwatch["active"] = False


def advance_stopwatch(stopwatch, seconds=1):
    """Add seconds only if the stopwatch is running."""
    if stopwatch["active"]:
        stopwatch["seconds"] += seconds


def format_stopwatch(seconds):
    """Elapsed seconds -> 'MM:SS'."""
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def describe_stopwatch(stopwatch):
    """'en marcha' or 'parado' depending on the state."""
    return "en marcha" if stopwatch["active"] else "parado"
