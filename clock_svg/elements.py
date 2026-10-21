"""SVG elements of the dial: lines, bezel, tick marks, numerals and hands."""

from mymath import polar_point
from clock_svg.constants import (
    CENTER_X,
    CENTER_Y,
    COLOR_FACE,
    COLOR_HOUR_MARK,
    COLOR_INNER_BEZEL,
    COLOR_MINUTE_MARK,
    COLOR_NUMBER,
    COLOR_OUTER_BEZEL,
)


def point_svg(cx, cy, radius, degrees):
    """Point at 'radius' from the center (cx, cy), in degrees clockwise from 12.

    The SVG Y axis points down, so the vertical offset is subtracted.
    """
    dx, dy = polar_point(0, 0, radius, degrees)
    return cx + dx, cy - dy


def line_svg(cx, cy, inner_radius, outer_radius, degrees, color, width):
    """Radial segment between two radii, at a given angle."""
    x1, y1 = point_svg(cx, cy, inner_radius, degrees)
    x2, y2 = point_svg(cx, cy, outer_radius, degrees)
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')


def bezel_svg():
    """Three concentric circles that give the dial its bezel effect."""
    return "\n".join([
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="170" fill="{COLOR_OUTER_BEZEL}"/>',
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="164" fill="{COLOR_INNER_BEZEL}"/>',
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="158" fill="{COLOR_FACE}"/>',
    ])


def tick_marks_svg():
    """60 tick marks; the hour ones (every 5) are thicker and longer."""
    parts = []
    for i in range(60):
        degrees = i * 6
        if i % 5 == 0:
            parts.append(line_svg(CENTER_X, CENTER_Y, 136, 152, degrees, COLOR_HOUR_MARK, 4))
        else:
            parts.append(line_svg(CENTER_X, CENTER_Y, 146, 152, degrees, COLOR_MINUTE_MARK, 1.5))
    return "\n".join(parts)


def numerals_svg():
    """Numerals 1 to 12, placed with our own trigonometric functions."""
    parts = []
    for hour in range(1, 13):
        x, y = point_svg(CENTER_X, CENTER_Y, 118, hour * 30)
        parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="22" fill="{COLOR_NUMBER}">{hour}</text>'
        )
    return "\n".join(parts)


def hand(cx, cy, length_up, length_down, width, color, angle, duration):
    """Hand in a group that rotates around (cx, cy).

    The animation starts at the current angle (from) and makes one full
    turn in 'duration' seconds, in an infinite loop.
    """
    start = f"{angle:.3f} {cx} {cy}"
    end = f"{angle + 360:.3f} {cx} {cy}"
    return "\n".join([
        "<g>",
        f'  <line x1="{cx}" y1="{cy + length_down}" x2="{cx}" y2="{cy - length_up}" '
        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>',
        f'  <animateTransform attributeName="transform" type="rotate" '
        f'from="{start}" to="{end}" dur="{duration}s" repeatCount="indefinite"/>',
        "</g>",
    ])
