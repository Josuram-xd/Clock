"""SVG elements of the stopwatch: mini-dial with its hand and label."""

from mymath import second_hand_angle
from clock_svg.constants import (
    COLOR_MINUTE_MARK,
    COLOR_OUTER_BEZEL,
    COLOR_SECOND_HAND,
    COLOR_SECONDARY_TEXT,
    COLOR_STOPWATCH_FACE,
    STOPWATCH_CX,
    STOPWATCH_CY,
    STOPWATCH_R,
)
from clock_svg.elements import hand, line_svg


def stopwatch_svg(seconds):
    """Stopwatch mini-dial with its label; the hand turns every 60 s."""
    parts = [
        f'<circle cx="{STOPWATCH_CX}" cy="{STOPWATCH_CY}" r="{STOPWATCH_R}" '
        f'fill="{COLOR_STOPWATCH_FACE}" stroke="{COLOR_OUTER_BEZEL}" stroke-width="2"/>'
    ]
    for i in range(12):
        parts.append(line_svg(STOPWATCH_CX, STOPWATCH_CY, 28, 33, i * 30, COLOR_MINUTE_MARK, 1.5))
    parts.append(hand(STOPWATCH_CX, STOPWATCH_CY, 30, 5, 1.5, COLOR_SECOND_HAND,
                      second_hand_angle(seconds % 60), 60))
    parts.append(
        f'<circle cx="{STOPWATCH_CX}" cy="{STOPWATCH_CY}" r="2.5" '
        f'fill="{COLOR_SECOND_HAND}"/>'
    )
    minutes, secs = seconds // 60, seconds % 60
    parts.append(
        f'<text x="{STOPWATCH_CX}" y="470" text-anchor="middle" font-size="12" '
        f'letter-spacing="2" fill="{COLOR_SECONDARY_TEXT}">CRONO {minutes}:{secs:02d}</text>'
    )
    return "\n".join(parts)
