"""SVG elements of the alarm: red mark on the dial and blinking notice."""

from mymath import hour_hand_angle
from core.alarm import seconds_until_alarm
from core.time_utils import from_seconds
from clock_svg.constants import CENTER_X, CENTER_Y, COLOR_ALARM
from clock_svg.elements import line_svg


def alarm_mark_svg(alarm_seconds):
    """Red mark over the hour marks at the alarm's angle."""
    hours, minutes, seconds = from_seconds(alarm_seconds)
    return line_svg(CENTER_X, CENTER_Y, 136, 152, hour_hand_angle(hours, minutes, seconds),
                    COLOR_ALARM, 5)


def alarm_notice_svg(time_seconds, alarm_seconds):
    """Hidden notice text ('¡ALARMA!' in the SVG) that blinks when the alarm rings."""
    start = seconds_until_alarm(time_seconds, alarm_seconds)
    return "\n".join([
        f'<text x="{CENTER_X}" y="275" text-anchor="middle" font-size="26" font-weight="bold" '
        f'fill="{COLOR_ALARM}" visibility="hidden">&#161;ALARMA!',
        f'  <set attributeName="visibility" to="visible" begin="{start}s"/>',
        f'  <animate attributeName="opacity" values="1;0;1" dur="1s" begin="{start}s" '
        f'repeatCount="indefinite"/>',
        "</text>",
    ])
