"""Analog dial drawn on a minitk Canvas: a static face and hands moved with coords()."""

from core.time_utils import from_seconds
from mymath import (
    hand_angle,
    hour_hand_angle,
    minute_hand_angle,
    polar_point,
    second_hand_angle,
)

CANVAS_COLS = 32
CANVAS_ROWS = 16  # a row is 2 pixels tall, so the canvas is 32 x 32 pixels
CENTER = 16
RADIUS = 15
NUMBER_RADIUS = 11.5
HOUR_LENGTH = 7
MINUTE_LENGTH = 10.5
SECOND_LENGTH = 13
ALARM_RADIUS = 15

BACKGROUND = "navy"
BEZEL = "slate"
HOUR_TICK = "silver"
MINUTE_TICK = "gray"
NUMBER = "cyan"
HOUR_HAND = "white"
MINUTE_HAND = "green"
SECOND_HAND = "red"
ALARM_MARK = "orange"


def to_pixel(radius, degrees):
    """Pixel at 'radius' from the center, degrees clockwise from 12 (pixel y grows down)."""
    dx, dy = polar_point(0, 0, radius, degrees)
    return CENTER + dx, CENTER - dy


def draw_face(canvas):
    """Bezel, 60 ticks, and the numbers 1 to 12 (these items never change)."""
    canvas.create_oval(0, 0, 2 * CENTER - 1, 2 * CENTER - 1, outline=BEZEL)
    for minute in range(60):
        degrees = hand_angle(minute, 60)
        if minute % 5 == 0:
            x0, y0 = to_pixel(RADIUS - 3, degrees)
            x1, y1 = to_pixel(RADIUS - 1, degrees)
            canvas.create_line(x0, y0, x1, y1, fill=HOUR_TICK)
        else:
            x, y = to_pixel(RADIUS - 1, degrees)
            canvas.create_line(x, y, x, y, fill=MINUTE_TICK)
    for hour in range(1, 13):
        x, y = to_pixel(NUMBER_RADIUS, hand_angle(hour, 12))
        canvas.create_text(x, y, text=str(hour), fill=NUMBER, bold=True)


def create_hands(canvas):
    """Create the alarm mark and the three hands. Return their item ids by name."""
    hands = {"alarm": canvas.create_oval(0, 0, 0, 0, outline=None, fill=None)}
    hands["hour"] = canvas.create_line(CENTER, CENTER, CENTER, CENTER, fill=HOUR_HAND, width=2)
    hands["minute"] = canvas.create_line(CENTER, CENTER, CENTER, CENTER, fill=MINUTE_HAND)
    hands["second"] = canvas.create_line(CENTER, CENTER, CENTER, CENTER, fill=SECOND_HAND)
    canvas.create_oval(CENTER - 1, CENTER - 1, CENTER + 1, CENTER + 1,
                       outline=SECOND_HAND, fill=SECOND_HAND)
    return hands


def place_hand(canvas, item, length, degrees):
    """Point a hand from the center to its tip."""
    x, y = to_pixel(length, degrees)
    canvas.coords(item, CENTER, CENTER, x, y)


def update_dial(canvas, hands, total_seconds, alarm_time):
    """Move the hands to a time of day and place (or hide) the alarm mark."""
    hours, minutes, seconds = from_seconds(total_seconds)
    # The hour hand moves in whole minutes (seconds are not counted).
    place_hand(canvas, hands["hour"], HOUR_LENGTH, hour_hand_angle(hours, minutes, 0))
    place_hand(canvas, hands["minute"], MINUTE_LENGTH, minute_hand_angle(minutes, seconds))
    place_hand(canvas, hands["second"], SECOND_LENGTH, second_hand_angle(seconds))
    if alarm_time is None:
        canvas.itemconfigure(hands["alarm"], outline=None, fill=None)
        return
    alarm_hours, alarm_minutes, alarm_seconds = from_seconds(alarm_time)
    x, y = to_pixel(ALARM_RADIUS - 1,
                    hour_hand_angle(alarm_hours, alarm_minutes, alarm_seconds))
    canvas.coords(hands["alarm"], x - 1, y - 1, x + 1, y + 1)
    canvas.itemconfigure(hands["alarm"], outline=ALARM_MARK, fill=ALARM_MARK)
