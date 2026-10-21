"""Colored ASCII analog dial: elliptical outline, marks, and hands."""

from clock_terminal.ansi import BOLD, GREEN, RED, YELLOW, colorize
from core.time_utils import from_seconds
from mymath import (
    cosine,
    degrees_to_radians,
    hour_hand_angle,
    minute_hand_angle,
    second_hand_angle,
    sine,
)

DIAL_WIDTH = 25
DIAL_HEIGHT = 13
CENTER_COL = 12
CENTER_ROW = 6
RADIUS_COL = 12.0  # horizontal radius in columns
RADIUS_ROW = 6.0   # vertical radius in rows (a cell is ~2x taller: 2:1 ratio)


def place_cell(grid, degrees, radius, character, color):
    """Place a character in the grid at a given radial distance and angle.

    The angle is measured in degrees clockwise from 12 o'clock.
    """
    angle = degrees_to_radians(degrees)
    column = round(CENTER_COL + radius * RADIUS_COL * sine(angle))
    row = round(CENTER_ROW - radius * RADIUS_ROW * cosine(angle))
    if 0 <= row < DIAL_HEIGHT and 0 <= column < DIAL_WIDTH:
        if color:
            grid[row][column] = colorize(character, color)
        else:
            grid[row][column] = character


def draw_hand(grid, degrees, length, character, color):
    """Draw a hand from the center out to the given length (0 to 1)."""
    step = 0.0
    while step <= length:
        place_cell(grid, degrees, step, character, color)
        step += 0.02


def mark_outline(grid):
    """Draw the elliptical outline of the dial using the ellipse equation."""
    for row in range(DIAL_HEIGHT):
        for column in range(DIAL_WIDTH):
            dx = (column - CENTER_COL) / RADIUS_COL
            dy = (row - CENTER_ROW) / RADIUS_ROW
            distance2 = dx * dx + dy * dy
            if abs(distance2 - 1.0) < 0.12:
                grid[row][column] = "."


def draw_dial(total_seconds):
    """Return the ASCII lines of the dial with its three hands."""
    hours, minutes, clock_seconds = from_seconds(total_seconds)
    grid = [[" "] * DIAL_WIDTH for _ in range(DIAL_HEIGHT)]
    mark_outline(grid)
    for mark in range(12):
        place_cell(grid, mark * 30, 0.9, "+", BOLD)

    # The hour hand moves in whole minutes (seconds are not counted).
    draw_hand(grid, hour_hand_angle(hours, minutes, 0), 0.5, "#", YELLOW)
    draw_hand(grid, minute_hand_angle(minutes, clock_seconds), 0.8, "=", GREEN)
    draw_hand(grid, second_hand_angle(clock_seconds), 0.9, "*", RED)
    grid[CENTER_ROW][CENTER_COL] = colorize("o", BOLD)

    return ["".join(row) for row in grid]
