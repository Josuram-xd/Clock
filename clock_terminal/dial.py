"""Analog dial drawn with braille dots: rim, ticks, numerals, hands, and the alarm mark."""

from clock_terminal.ansi import colorize
from core.braille import DOTS_X, DOTS_Y, cell_char, create_braille, set_dots
from core.time_utils import from_seconds
from mymath import (
    hand_angle,
    hour_hand_angle,
    minute_hand_angle,
    polar_point,
    second_hand_angle,
)
from mymath.raster import ellipse_fill, ellipse_outline, line_points

DIAL_COLS = 41
DIAL_ROWS = 21
CENTER_X = DIAL_COLS * DOTS_X / 2  # dot coordinates: a cell is 2 dots wide and 4 tall,
CENTER_Y = DIAL_ROWS * DOTS_Y / 2  # which makes the dots square
RADIUS = 40

HOUR_TICK = (RADIUS - 8, RADIUS - 2)
MINUTE_DOT_RADIUS = RADIUS - 4
NUMBER_RADIUS = 27
HOUR_LENGTH = 17
MINUTE_LENGTH = 27
SECOND_LENGTH = 33
SECOND_TAIL = 8


def to_dot(radius, degrees):
    """Dot at 'radius' dots from the center, degrees clockwise from 12 (y grows down)."""
    dx, dy = polar_point(0, 0, radius, degrees)
    return CENTER_X + dx, CENTER_Y - dy


def radial_line(inner, outer, degrees):
    """Dots of a segment between two radii at one angle."""
    start_x, start_y = to_dot(inner, degrees)
    end_x, end_y = to_dot(outer, degrees)
    return line_points(start_x, start_y, end_x, end_y)


def draw_face(braille):
    """Rim, a dot per minute and a bold tick per hour."""
    box = (CENTER_X - RADIUS, CENTER_Y - RADIUS, CENTER_X + RADIUS, CENTER_Y + RADIUS)
    set_dots(braille, ellipse_outline(*box), "bezel", thickness=1)
    for minute in range(60):
        degrees = hand_angle(minute, 60)
        if minute % 5 == 0:
            set_dots(braille, radial_line(*HOUR_TICK, degrees), "hour_tick", thickness=2)
        else:
            set_dots(braille, [to_dot(MINUTE_DOT_RADIUS, degrees)], "ticks")


def draw_hands(braille, total_seconds):
    """Hour and minute hands (thick), and the second hand with its tail and hub."""
    hours, minutes, seconds = from_seconds(total_seconds)
    # The hour hand moves in whole minutes (seconds are not counted).
    set_dots(braille, radial_line(0, HOUR_LENGTH, hour_hand_angle(hours, minutes, 0)),
             "hour", thickness=3)
    set_dots(braille, radial_line(0, MINUTE_LENGTH, minute_hand_angle(minutes, seconds)),
             "minute", thickness=1)
    angle = second_hand_angle(seconds)
    set_dots(braille, radial_line(-SECOND_TAIL, SECOND_LENGTH, angle), "second")
    set_dots(braille, ellipse_fill(CENTER_X - 2, CENTER_Y - 2, CENTER_X + 2, CENTER_Y + 2),
             "second")


def draw_alarm_mark(braille, alarm_time):
    """A filled dot on the rim at the angle of the alarm."""
    hours, minutes, seconds = from_seconds(alarm_time)
    x, y = to_dot(RADIUS - 1, hour_hand_angle(hours, minutes, seconds))
    set_dots(braille, ellipse_fill(x - 3, y - 3, x + 3, y + 3), "alert")


def build_cells(total_seconds, alarm_time=None):
    """Compose the dial as a grid of (character, role) cells.

    Layers, from back to front: face, numerals, alarm mark, hands.
    """
    face = create_braille(DIAL_COLS, DIAL_ROWS)
    draw_face(face)
    if alarm_time is not None:
        draw_alarm_mark(face, alarm_time)
    hands = create_braille(DIAL_COLS, DIAL_ROWS)
    draw_hands(hands, total_seconds)

    cells = [[(cell_char(face, c, r), face["owners"][r][c]) for c in range(DIAL_COLS)]
             for r in range(DIAL_ROWS)]
    for hour in range(1, 13):
        x, y = to_dot(NUMBER_RADIUS, hand_angle(hour, 12))
        column, row = round(x) // DOTS_X, round(y) // DOTS_Y
        text = str(hour)
        start = column - (len(text) - 1) // 2
        for offset, char in enumerate(text):
            cells[row][start + offset] = (char, "numbers")
    for row in range(DIAL_ROWS):
        for column in range(DIAL_COLS):
            if hands["masks"][row][column]:
                cells[row][column] = (cell_char(hands, column, row), hands["owners"][row][column])
    return cells


def draw_dial(total_seconds, theme, alarm_time=None):
    """Return the lines of the dial, colored with the roles of a theme.

    Neighbor cells of the same role share one color code."""
    lines = []
    for row in build_cells(total_seconds, alarm_time):
        pieces = []
        run, run_role = "", None
        for char, role in row:
            if role != run_role and run:
                pieces.append(colorize(run, theme[run_role]) if run_role else run)
                run = ""
            run_role = role
            run += char
        pieces.append(colorize(run, theme[run_role]) if run_role else run)
        lines.append("".join(pieces))
    return lines
