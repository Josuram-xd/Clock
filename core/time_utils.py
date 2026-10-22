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


def split_meridiem(text):
    """('7:30', 'pm') for '7:30 PM'. The suffix is '' when there is none."""
    cleaned = text.strip().lower().replace(".", "").replace(" ", "")
    for suffix in ("am", "pm", "a", "p"):
        if cleaned.endswith(suffix):
            return cleaned[:-len(suffix)], suffix[0] + "m"
    return cleaned, ""


# Where to cut colon-less digits: '930' -> 9:30, '1430' -> 14:30, '93015' -> 9:30:15
DIGIT_CUTS = {1: (), 2: (), 3: (1,), 4: (2,), 5: (1, 3), 6: (2, 4)}


def split_digits(body):
    """(hours, minutes, seconds) texts from '14:30', '7:05:09' or colon-less digits
    such as '1430' or '143000'. None if the text does not have that shape."""
    if ":" in body:
        parts = body.split(":")
        if len(parts) not in (2, 3) or any(not 1 <= len(part) <= 2 for part in parts):
            return None
    elif len(body) in DIGIT_CUTS:
        parts, start = [], 0
        for cut in DIGIT_CUTS[len(body)] + (len(body),):
            parts.append(body[start:cut])
            start = cut
    else:
        return None
    if any(not part or not all("0" <= c <= "9" for c in part) for part in parts):
        return None
    return parts + ["0"] * (3 - len(parts))


def parse_clock_time(text):
    """Seconds of the day for what a person types, or None if it is not a time.

    Accepts '14:30', '14:30:15', '2:30 pm', '7am', '12:00 a.m.' and colon-less
    digits like '1430' or '143015'. Seconds are optional. With am/pm the hour
    must be 1 to 12; without it, 0 to 23.
    """
    body, meridiem = split_meridiem(text)
    parts = split_digits(body)
    if parts is None:
        return None
    hours, minutes, seconds = (int(part) for part in parts)
    if minutes > 59 or seconds > 59:
        return None
    if meridiem:
        if not 1 <= hours <= 12:
            return None
        hours = hours % 12 + (12 if meridiem == "pm" else 0)
    elif hours > 23:
        return None
    return to_seconds(hours, minutes, seconds)


def is_ambiguous_hour(text, seconds):
    """True if the text had no am/pm and its hour is 1 to 12 (it could be either half of the day)."""
    return split_meridiem(text)[1] == "" and 1 <= from_seconds(seconds)[0] <= 12


def apply_meridiem(seconds, meridiem):
    """Read a time typed with hours 1 to 12 as AM or PM ('am' / 'pm')."""
    hours, minutes, secs = from_seconds(seconds)
    return to_seconds(hours % 12 + (12 if meridiem == "pm" else 0), minutes, secs)
