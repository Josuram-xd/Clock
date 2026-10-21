"""Clock geometry: polar points and hand angles."""

from mymath.trigonometry import cosine, degrees_to_radians, sine


def hand_angle(value, maximum):
    """Angle in degrees of a hand: 0 at 12 and clockwise."""
    return value / maximum * 360


def polar_point(cx, cy, radius, angle_degrees):
    """
    Return (x, y) at 'radius' from the center (cx, cy).
    The angle is measured from 12 clockwise and the Y axis points up.
    """
    radians = degrees_to_radians(angle_degrees)
    x = cx + radius * sine(radians)
    y = cy + radius * cosine(radians)
    return x, y


def second_hand_angle(seconds):
    """Angle in degrees of the seconds hand."""
    return seconds * 6.0


def minute_hand_angle(minutes, seconds):
    """Angle in degrees of the minutes hand."""
    return (minutes * 60 + seconds) * 0.1


def hour_hand_angle(hours, minutes, seconds):
    """Angle in degrees of the hours hand (12-hour dial)."""
    return (hours % 12) * 30 + minutes * 0.5 + seconds / 120
