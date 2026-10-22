"""Modern watch face drawn on a minitk Canvas: metallic rim, shaded disc, baton markers,
tapered hands with shadows, and a gold hub. The face is static; hands move with coords()."""

from core.time_utils import from_seconds
from mymath import (
    hand_angle,
    hour_hand_angle,
    minute_hand_angle,
    polar_point,
    second_hand_angle,
)

CANVAS_COLS = 40
CANVAS_ROWS = 20  # two pixels per row: the canvas is 40 x 40 pixels
CENTER = 20.0
RADIUS = 19.6

WINDOW_BACKGROUND = "#0b1220"
RIM_LAYERS = [(19.6, "#e2e8f0"), (18.7, "#64748b"), (18.0, "#1e293b")]
FACE_LAYERS = [(17.4, "#162036"), (15.0, "#131c30"), (12.0, "#101829"), (8.0, "#0d1424"),
               (4.0, "#0b1120")]  # from the edge to the center: a soft radial shading
BATON = "#f1f5f9"
SMALL_BATON = "#94a3b8"
MINUTE_DOT = "#475569"
HOUR_HAND = "#f8fafc"
MINUTE_HAND = "#7dd3fc"
SECOND_HAND = "#f43f5e"
HUB = "#fbbf24"
SHADOW = "#04070d"
ALARM_MARK = "#fb923c"

HOUR_LENGTH = 9.5
MINUTE_LENGTH = 14.5
SECOND_LENGTH = 16.0
SECOND_TAIL = 4.5
SHADOW_OFFSET = 0.9


def to_pixel(radius, degrees):
    """Pixel at 'radius' from the center, degrees clockwise from 12 (pixel y grows down)."""
    dx, dy = polar_point(0, 0, radius, degrees)
    return CENTER + dx, CENTER - dy


def hand_polygon(length, base_width, tip_width, degrees, tail=0.0, offset=0.0):
    """Flat x, y coordinates of a tapered hand: wide at the base, narrow at the tip."""
    ux, uy = polar_point(0, 0, 1, degrees)
    uy = -uy  # screen y points down
    nx, ny = -uy, ux  # perpendicular to the hand
    base_x, base_y = CENTER - ux * tail + offset, CENTER - uy * tail + offset
    tip_x, tip_y = CENTER + ux * length + offset, CENTER + uy * length + offset
    half_base, half_tip = base_width / 2, tip_width / 2
    return [base_x + nx * half_base, base_y + ny * half_base,
            tip_x + nx * half_tip, tip_y + ny * half_tip,
            tip_x - nx * half_tip, tip_y - ny * half_tip,
            base_x - nx * half_base, base_y - ny * half_base]


def draw_face(canvas):
    """Rim, shaded disc, and the baton markers (these items never change)."""
    for radius, color in RIM_LAYERS + FACE_LAYERS:
        canvas.create_oval(CENTER - radius, CENTER - radius, CENTER + radius, CENTER + radius,
                           fill=color)
    for minute in range(60):
        degrees = hand_angle(minute, 60)
        if minute % 15 == 0:
            inner, width, color = 12.2, 2.4, BATON
        elif minute % 5 == 0:
            inner, width, color = 13.6, 1.5, SMALL_BATON
        else:
            canvas.create_line(*to_pixel(16.3, degrees), *to_pixel(16.3, degrees),
                               fill=MINUTE_DOT, width=0.8)
            continue
        canvas.create_line(*to_pixel(inner, degrees), *to_pixel(16.6, degrees),
                           fill=color, width=width)


def create_hands(canvas):
    """Create the alarm mark and the hands (shadows first). Return their item ids by name."""
    blank = (CENTER,) * 8
    hands = {"alarm": canvas.create_polygon(*blank, fill=None)}
    hands["hour_shadow"] = canvas.create_polygon(*blank, fill=SHADOW)
    hands["minute_shadow"] = canvas.create_polygon(*blank, fill=SHADOW)
    hands["hour"] = canvas.create_polygon(*blank, fill=HOUR_HAND)
    hands["minute"] = canvas.create_polygon(*blank, fill=MINUTE_HAND)
    hands["second"] = canvas.create_line(CENTER, CENTER, CENTER, CENTER, fill=SECOND_HAND,
                                         width=0.9)
    canvas.create_oval(CENTER - 2, CENTER - 2, CENTER + 2, CENTER + 2, fill=HUB)
    canvas.create_oval(CENTER - 0.8, CENTER - 0.8, CENTER + 0.8, CENTER + 0.8,
                       fill=WINDOW_BACKGROUND)
    return hands


def alarm_marker(degrees):
    """Flat coordinates of a small diamond on the rim at an angle."""
    outer, inner = to_pixel(18.6, degrees), to_pixel(15.6, degrees)
    left, right = to_pixel(17.1, degrees - 4), to_pixel(17.1, degrees + 4)
    return [outer[0], outer[1], right[0], right[1], inner[0], inner[1], left[0], left[1]]


def update_dial(canvas, hands, total_seconds, alarm_time):
    """Move the hands to a time of day and place (or hide) the alarm mark."""
    hours, minutes, seconds = from_seconds(total_seconds)
    # The hour hand moves in whole minutes (seconds are not counted).
    hour_angle = hour_hand_angle(hours, minutes, 0)
    minute_angle = minute_hand_angle(minutes, seconds)
    canvas.coords(hands["hour"], *hand_polygon(HOUR_LENGTH, 2.8, 1.3, hour_angle, 2.0))
    canvas.coords(hands["hour_shadow"],
                  *hand_polygon(HOUR_LENGTH, 2.8, 1.3, hour_angle, 2.0, SHADOW_OFFSET))
    canvas.coords(hands["minute"], *hand_polygon(MINUTE_LENGTH, 2.0, 0.9, minute_angle, 2.5))
    canvas.coords(hands["minute_shadow"],
                  *hand_polygon(MINUTE_LENGTH, 2.0, 0.9, minute_angle, 2.5, SHADOW_OFFSET))
    second_angle = second_hand_angle(seconds)
    canvas.coords(hands["second"], *to_pixel(-SECOND_TAIL, second_angle),
                  *to_pixel(SECOND_LENGTH, second_angle))
    if alarm_time is None:
        canvas.itemconfigure(hands["alarm"], fill=None)
        return
    alarm_hours, alarm_minutes, alarm_seconds = from_seconds(alarm_time)
    canvas.coords(hands["alarm"],
                  *alarm_marker(hour_hand_angle(alarm_hours, alarm_minutes, alarm_seconds)))
    canvas.itemconfigure(hands["alarm"], fill=ALARM_MARK)
