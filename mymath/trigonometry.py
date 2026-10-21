"""Custom trigonometry: PI, angle reduction, and sine/cosine via Taylor series."""

PI = 3.141592653589793
TAU = 2 * PI
NUM_TERMS = 12  # Terms of the Taylor series (minimum 10)


def reduce_angle(angle):
    """Reduce an angle in radians to the interval [-PI, PI]."""
    turns = round(angle / TAU)
    reduced = angle - turns * TAU
    if reduced > PI:
        reduced -= TAU
    elif reduced < -PI:
        reduced += TAU
    return reduced


def sine(angle):
    """Sine by Taylor series: x - x^3/3! + x^5/5! - ..."""
    x = reduce_angle(angle)
    term = x
    total = x
    for n in range(1, NUM_TERMS):
        term = -term * x * x / ((2 * n) * (2 * n + 1))
        total += term
    return total


def cosine(angle):
    """Cosine by Taylor series: 1 - x^2/2! + x^4/4! - ..."""
    x = reduce_angle(angle)
    term = 1.0
    total = 1.0
    for n in range(1, NUM_TERMS):
        term = -term * x * x / ((2 * n - 1) * (2 * n))
        total += term
    return total


def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    return degrees * PI / 180
