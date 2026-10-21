"""Digital readouts that keep counting inside the SVG, with no scripts.

Every digit is a set of <text> elements, one per possible value, and only one
is visible at a time. A discrete <animate> on `visibility` shows each value
during its slot of the cycle, and a negative `begin` starts the cycle in the
middle, at the time the user typed. A seconds-ones digit, for example, has ten
values, shows each for 1 s, and repeats every 10 s.
"""

from clock_svg.constants import FONT_MONO

CHAR_RATIO = 0.6  # width of a monospace character relative to its font size


def cycling_text(center_x, y, values, step, elapsed, size, color, anchor="middle"):
    """One <text> per value; value k is visible during seconds [k*step, (k+1)*step) of the cycle.

    `elapsed` is how many seconds into the cycle the page starts. Returns SVG lines.
    """
    count = len(values)
    offset = elapsed % (count * step)
    lines = []
    for index, value in enumerate(values):
        key_times = ["0"]
        if index > 0:
            key_times.append(f"{index / count:.6f}")
        if index < count - 1:
            key_times.append(f"{(index + 1) / count:.6f}")
        key_times.append("1")
        # hidden before the slot, visible during it, hidden after it
        if index == 0:
            visibility = ["visible", "hidden", "hidden"]
        elif index == count - 1:
            visibility = ["hidden", "visible", "visible"]
        else:
            visibility = ["hidden", "visible", "hidden", "hidden"]
        lines.append(
            f'<text x="{center_x:.2f}" y="{y}" text-anchor="{anchor}" font-family="{FONT_MONO}" '
            f'font-size="{size}" fill="{color}" visibility="hidden">{value}'
            f'<animate attributeName="visibility" calcMode="discrete" dur="{count * step}s" '
            f'begin="-{offset}s" repeatCount="indefinite" keyTimes="{";".join(key_times)}" '
            f'values="{";".join(visibility)}"/></text>'
        )
    return lines


def static_char(center_x, y, char, size, color, blink=False):
    """A fixed character (a colon); with blink=True it turns on and off every second."""
    animation = ""
    if blink:
        animation = ('<animate attributeName="opacity" calcMode="discrete" values="1;0" '
                     'keyTimes="0;0.5" dur="1s" repeatCount="indefinite"/>')
    return (f'<text x="{center_x:.2f}" y="{y}" text-anchor="middle" font-family="{FONT_MONO}" '
            f'font-size="{size}" fill="{color}">{char}{animation}</text>')


def clock_readout_svg(center_x, y, time_seconds, size, color, twelve_hour=False):
    """HH:MM:SS (and AM/PM in 12 h) centered at center_x, running from time_seconds."""
    char = size * CHAR_RATIO
    left = center_x - 4 * char  # 8 characters wide
    if twelve_hour:
        hours = [f"{hour % 12 or 12:02d}" for hour in range(24)]
    else:
        hours = [f"{hour:02d}" for hour in range(24)]
    tens, ones = list("012345"), list("0123456789")
    parts = cycling_text(left + 1.0 * char, y, hours, 3600, time_seconds, size, color)
    parts.append(static_char(left + 2.5 * char, y, ":", size, color, blink=True))
    parts += cycling_text(left + 3.5 * char, y, tens, 600, time_seconds, size, color)
    parts += cycling_text(left + 4.5 * char, y, ones, 60, time_seconds, size, color)
    parts.append(static_char(left + 5.5 * char, y, ":", size, color, blink=True))
    parts += cycling_text(left + 6.5 * char, y, tens, 10, time_seconds, size, color)
    parts += cycling_text(left + 7.5 * char, y, ones, 1, time_seconds, size, color)
    if twelve_hour:
        parts += cycling_text(left + 8 * char + 6, y, ["AM", "PM"], 43200, time_seconds,
                              round(size * 0.45), color, anchor="start")
    return parts


def stopwatch_readout_svg(center_x, y, seconds, size, color):
    """MM:SS of the stopwatch, counting up from `seconds` (it wraps after 100 minutes)."""
    char = size * CHAR_RATIO
    left = center_x - 2.5 * char  # 5 characters wide
    tens, ones = list("012345"), list("0123456789")
    parts = cycling_text(left + 0.5 * char, y, ones, 600, seconds, size, color)
    parts += cycling_text(left + 1.5 * char, y, ones, 60, seconds, size, color)
    parts.append(static_char(left + 2.5 * char, y, ":", size, color))
    parts += cycling_text(left + 3.5 * char, y, tens, 10, seconds, size, color)
    parts += cycling_text(left + 4.5 * char, y, ones, 1, seconds, size, color)
    return parts
