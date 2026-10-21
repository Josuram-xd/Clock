"""Analog dial on a grid of colored cells: ticks, numerals, and hands with real lines."""

from clock_terminal.ansi import colorize
from core.time_utils import from_seconds
from mymath import (
    cosine,
    degrees_to_radians,
    hand_angle,
    hour_hand_angle,
    minute_hand_angle,
    second_hand_angle,
    sine,
)

DIAL_COLS = 33
DIAL_ROWS = 17
CENTER_COL = 16
CENTER_ROW = 8
RADIUS_COLS = 16.0  # a cell is about twice as tall as wide: 2 columns per row
RADIUS_ROWS = 8.0

HOUR_LENGTH = 0.45
MINUTE_LENGTH = 0.68
SECOND_LENGTH = 0.9
NUMBER_RADIUS = 0.76


def create_grid():
    """Empty grid: every cell is a (character, role) pair; role None means no color."""
    return [[(" ", None)] * DIAL_COLS for _ in range(DIAL_ROWS)]


def polar_cell(fraction, degrees):
    """(column, row) at a fraction (0 to 1) of the dial radius, degrees clockwise from 12."""
    angle = degrees_to_radians(degrees)
    column = round(CENTER_COL + fraction * RADIUS_COLS * sine(angle))
    row = round(CENTER_ROW - fraction * RADIUS_ROWS * cosine(angle))
    return column, row


def put(grid, column, row, char, role):
    """Write a cell if it falls inside the grid."""
    if 0 <= column < DIAL_COLS and 0 <= row < DIAL_ROWS:
        grid[row][column] = (char, role)


def line_cells(start_col, start_row, end_col, end_row):
    """Cells of the straight line between two cells (DDA algorithm)."""
    steps = max(abs(end_col - start_col), abs(end_row - start_row))
    if steps == 0:
        return [(start_col, start_row)]
    return [
        (round(start_col + (end_col - start_col) * step / steps),
         round(start_row + (end_row - start_row) * step / steps))
        for step in range(steps + 1)
    ]


def hand_glyph(degrees, thick):
    """Line character that follows the direction of a hand."""
    direction = degrees % 180
    if direction < 22.5 or direction >= 157.5:
        return "┃" if thick else "│"
    if direction < 67.5:
        return "╱"
    if direction < 112.5:
        return "━" if thick else "─"
    return "╲"


def draw_hand(grid, degrees, length, role, thick=False):
    """Draw a hand from the center to a fraction of the radius."""
    end_col, end_row = polar_cell(length, degrees)
    glyph = hand_glyph(degrees, thick)
    for column, row in line_cells(CENTER_COL, CENTER_ROW, end_col, end_row):
        put(grid, column, row, glyph, role)


def draw_marks(grid):
    """60 ticks on the rim: a dot per minute and a bullet per hour."""
    for minute in range(60):
        column, row = polar_cell(1.0, hand_angle(minute, 60))
        put(grid, column, row, "•" if minute % 5 == 0 else "·", "ticks")


def draw_numerals(grid):
    """Numbers 1 to 12 inside the rim."""
    for hour in range(1, 13):
        column, row = polar_cell(NUMBER_RADIUS, hand_angle(hour, 12))
        text = str(hour)
        start = column - (len(text) - 1) // 2
        for offset, char in enumerate(text):
            put(grid, start + offset, row, char, "numbers")


def build_grid(total_seconds):
    """Compose the dial grid for a time of day."""
    hours, minutes, seconds = from_seconds(total_seconds)
    grid = create_grid()
    draw_marks(grid)
    draw_numerals(grid)
    # The hour hand moves in whole minutes (seconds are not counted).
    draw_hand(grid, hour_hand_angle(hours, minutes, 0), HOUR_LENGTH, "hour", thick=True)
    draw_hand(grid, minute_hand_angle(minutes, seconds), MINUTE_LENGTH, "minute")
    draw_hand(grid, second_hand_angle(seconds), SECOND_LENGTH, "second")
    put(grid, CENTER_COL, CENTER_ROW, "●", "second")
    return grid


def draw_dial(total_seconds, theme):
    """Return the lines of the dial, colored with the roles of a theme."""
    lines = []
    for row in build_grid(total_seconds):
        pieces = []
        for char, role in row:
            pieces.append(colorize(char, theme[role]) if role else char)
        lines.append("".join(pieces))
    return lines
