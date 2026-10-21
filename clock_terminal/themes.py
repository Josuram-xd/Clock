"""Color themes: each role of the screen (frame, hands, digits...) gets an ANSI color."""

from clock_terminal.ansi import (
    BLUE,
    BOLD,
    CYAN,
    GREEN,
    RED,
    WHITE,
    YELLOW,
    rgb,
)

THEMES = [
    {
        "name": "clásico",
        "frame": BLUE, "title": BOLD + CYAN, "ticks": WHITE, "numbers": CYAN,
        "hour": YELLOW, "minute": GREEN, "second": RED, "digits": BOLD + WHITE,
        "label": CYAN, "alert": BOLD + RED,
    },
    {
        "name": "neón",
        "frame": rgb(180, 80, 255), "title": BOLD + rgb(0, 255, 220),
        "ticks": rgb(120, 120, 160), "numbers": rgb(0, 220, 255),
        "hour": rgb(255, 60, 200), "minute": rgb(0, 255, 160),
        "second": rgb(255, 230, 0), "digits": BOLD + rgb(0, 255, 220),
        "label": rgb(180, 80, 255), "alert": BOLD + rgb(255, 40, 80),
    },
    {
        "name": "ámbar",
        "frame": rgb(200, 130, 0), "title": BOLD + rgb(255, 180, 0),
        "ticks": rgb(150, 100, 0), "numbers": rgb(230, 150, 0),
        "hour": rgb(255, 200, 60), "minute": rgb(255, 170, 0),
        "second": rgb(255, 110, 0), "digits": BOLD + rgb(255, 180, 0),
        "label": rgb(200, 130, 0), "alert": BOLD + rgb(255, 60, 0),
    },
    {
        "name": "hielo",
        "frame": rgb(90, 150, 220), "title": BOLD + rgb(190, 230, 255),
        "ticks": rgb(130, 160, 190), "numbers": rgb(160, 200, 240),
        "hour": rgb(255, 255, 255), "minute": rgb(150, 210, 255),
        "second": rgb(110, 200, 255), "digits": BOLD + rgb(220, 240, 255),
        "label": rgb(90, 150, 220), "alert": BOLD + rgb(255, 90, 110),
    },
]


def current_theme(state):
    """Theme selected in the state."""
    return THEMES[state["theme"] % len(THEMES)]
