"""Time of day: HH:MM:SS validation, conversion to seconds, and formats."""

SECONDS_PER_DAY = 86400


def to_seconds(hours, minutes, seconds):
    """Convert hours, minutes, and seconds into seconds since midnight."""
    return hours * 3600 + minutes * 60 + seconds


def from_seconds(total):
    """Return (hours, minutes, seconds) from seconds since midnight."""
    return total // 3600, (total % 3600) // 60, total % 60


def parse_time(text, two_digits=True):
    """Seconds of the day for 'HH:MM:SS', or None if the text is not valid.

    With two_digits=True each part must have exactly two digits ('07:05:09');
    with False short parts are also accepted ('7:5:9').
    """
    parts = text.strip().split(":")
    if len(parts) != 3:
        return None
    for part in parts:
        ascii_only = part != "" and all("0" <= c <= "9" for c in part)
        if not ascii_only or (two_digits and len(part) != 2):
            return None
    hours, minutes, seconds = (int(part) for part in parts)
    if hours > 23 or minutes > 59 or seconds > 59:
        return None
    return to_seconds(hours, minutes, seconds)


def next_second(total):
    """Seconds of the day one second later (wraps to 0 after midnight)."""
    return (total + 1) % SECONDS_PER_DAY


def format_time(total):
    """Seconds of the day -> 'HH:MM:SS' in 24-hour format."""
    hours, minutes, seconds = from_seconds(total)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_time_12h(total):
    """Seconds of the day -> ('HH:MM:SS' in 12-hour format, 'AM' or 'PM')."""
    hours, minutes, seconds = from_seconds(total)
    suffix = "AM" if hours < 12 else "PM"
    hours_12 = hours % 12 or 12
    return f"{hours_12:02d}:{minutes:02d}:{seconds:02d}", suffix
