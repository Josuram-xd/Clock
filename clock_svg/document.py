"""Builder of the complete SVG document from the time, alarm and stopwatch."""

from mymath import hour_hand_angle, minute_hand_angle, second_hand_angle
from core.time_utils import format_time, from_seconds
from clock_svg.alarm_svg import alarm_mark_svg, alarm_notice_svg
from clock_svg.constants import (
    CANVAS_HEIGHT,
    CANVAS_WIDTH,
    CENTER_X,
    CENTER_Y,
    COLOR_ALARM_TEXT,
    COLOR_BACKGROUND,
    COLOR_HAND,
    COLOR_SECOND_HAND,
    FONT_MONO,
    FONT_TEXT,
)
from clock_svg.stopwatch_svg import stopwatch_svg
from clock_svg.elements import bezel_svg, hand, numerals_svg, tick_marks_svg


def hands_svg(time_seconds):
    """Hands starting from the given time, turning over 12 h, 1 h and 60 s."""
    hours, minutes, seconds = from_seconds(time_seconds)
    return [
        hand(CENTER_X, CENTER_Y, 90, 14, 7, COLOR_HAND,
             hour_hand_angle(hours, minutes, seconds), 43200),
        hand(CENTER_X, CENTER_Y, 136, 16, 4.5, COLOR_HAND,
             minute_hand_angle(minutes, seconds), 3600),
        hand(CENTER_X, CENTER_Y, 150, 36, 1.8, COLOR_SECOND_HAND,
             second_hand_angle(seconds), 60),
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="6" fill="{COLOR_SECOND_HAND}"/>',
    ]


def digital_texts_svg(time_seconds, alarm_seconds, x_digital):
    """Static digital time and, if there is an alarm, its label."""
    parts = [
        f'<text x="{x_digital}" y="418" text-anchor="middle" font-family="{FONT_MONO}" '
        f'font-size="30" fill="{COLOR_HAND}">{format_time(time_seconds)}</text>'
    ]
    if alarm_seconds is not None:
        parts.append(
            f'<text x="{x_digital}" y="448" text-anchor="middle" font-size="14" '
            f'fill="{COLOR_ALARM_TEXT}">Alarma {format_time(alarm_seconds)}</text>'
        )
    return parts


def build_svg(time_seconds, alarm_seconds, stopwatch_seconds):
    """Assemble the complete SVG document as text."""
    # With a stopwatch, the digital time moves left to make room for the mini-dial.
    x_digital = 120 if stopwatch_seconds is not None else CENTER_X

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" '
        f'width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" font-family="{FONT_TEXT}">',
        "  <title>Reloj SVG</title>",
        f'<rect x="0" y="0" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" '
        f'fill="{COLOR_BACKGROUND}"/>',
        bezel_svg(),
        tick_marks_svg(),
        numerals_svg(),
    ]
    if alarm_seconds is not None:
        parts.append(alarm_mark_svg(alarm_seconds))
    parts.extend(hands_svg(time_seconds))
    if alarm_seconds is not None:
        parts.append(alarm_notice_svg(time_seconds, alarm_seconds))
    parts.extend(digital_texts_svg(time_seconds, alarm_seconds, x_digital))
    if stopwatch_seconds is not None:
        parts.append(stopwatch_svg(stopwatch_seconds))

    parts.append("</svg>")
    return "\n".join(parts) + "\n"
