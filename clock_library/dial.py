"""Analog dial in ASCII: canvas, ticks, numbers, and hands drawn with DDA."""

from core.time_utils import from_seconds
from mymath import (
    hand_angle,
    hour_hand_angle,
    minute_hand_angle,
    polar_point,
    second_hand_angle,
)

WIDTH = 41
HEIGHT = 21
CENTER_COL = 20
CENTER_ROW = 10
ASPECT_FACTOR = 2  # A cell is twice as tall as it is wide: the X axis is scaled by 2
RING_RADIUS = 10
NUMBER_RADIUS = 9
HOUR_LENGTH = 5
MINUTE_LENGTH = 7
SECOND_LENGTH = 8


def create_canvas():
    """Create a WIDTH x HEIGHT matrix of spaces."""
    return [[" "] * WIDTH for _ in range(HEIGHT)]


def put_char(canvas, column, row, char):
    """Write a character if the position falls inside the canvas."""
    if 0 <= column < WIDTH and 0 <= row < HEIGHT:
        canvas[row][column] = char


def to_cell(x, y):
    """Convert ideal coordinates (Y up) into (column, row)."""
    column = CENTER_COL + round(x * ASPECT_FACTOR)
    row = CENTER_ROW - round(y)
    return column, row


def point_to_cell(radius, angle_degrees):
    """Canvas cell at 'radius' from the center, at the given angle."""
    x, y = polar_point(0, 0, radius, angle_degrees)
    return to_cell(x, y)


def dda_line(start_col, start_row, end_col, end_row):
    """Cells of the line between two points, using the DDA algorithm."""
    delta_col = end_col - start_col
    delta_row = end_row - start_row
    steps = max(abs(delta_col), abs(delta_row))
    if steps == 0:
        return [(start_col, start_row)]
    cells = []
    for step in range(steps + 1):
        column = round(start_col + delta_col * step / steps)
        row = round(start_row + delta_row * step / steps)
        cells.append((column, row))
    return cells


def draw_ticks(canvas):
    """Ticks on the ring: '.' for minutes and '+' for each hour."""
    for minute in range(60):
        column, row = point_to_cell(RING_RADIUS, hand_angle(minute, 60))
        char = "+" if minute % 5 == 0 else "."
        put_char(canvas, column, row, char)


def draw_numbers(canvas):
    """Write the numbers 1 to 12 around the dial."""
    for hour in range(1, 13):
        column, row = point_to_cell(NUMBER_RADIUS, hand_angle(hour, 12))
        text = str(hour)
        start = column - len(text) // 2
        for index, char in enumerate(text):
            put_char(canvas, start + index, row, char)


def draw_hand(canvas, angle_degrees, length, char):
    """Draw a hand from the center to its tip."""
    end_col, end_row = point_to_cell(length, angle_degrees)
    for column, row in dda_line(CENTER_COL, CENTER_ROW, end_col, end_row):
        put_char(canvas, column, row, char)


def build_dial(total_seconds):
    """Compose the full canvas: ticks, numbers, and hands."""
    hours, minutes, seconds = from_seconds(total_seconds)
    canvas = create_canvas()
    draw_ticks(canvas)
    draw_numbers(canvas)
    draw_hand(canvas, second_hand_angle(seconds), SECOND_LENGTH, "s")
    draw_hand(canvas, minute_hand_angle(minutes, seconds), MINUTE_LENGTH, "M")
    # The hour hand advances in whole minutes (seconds are not counted).
    draw_hand(canvas, hour_hand_angle(hours, minutes, 0), HOUR_LENGTH, "H")
    put_char(canvas, CENTER_COL, CENTER_ROW, "O")
    return canvas


def show_dial(total_seconds):
    """Print the dial to the console."""
    for row in build_dial(total_seconds):
        print("".join(row).rstrip())
