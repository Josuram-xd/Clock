"""Live loop of clock 2: the clock runs by itself until the user presses Ctrl+C."""

from clock_terminal.screen import BLINK_FRAME, draw_screen
from clock_terminal.state import step_frame
from core.pacer import wait_frame


def run_clock(state):
    """Run frames and redraw until Ctrl+C. The screen is drawn when the second
    changes and again when the colon blinks, not on every frame."""
    try:
        while True:
            if state["frame"] in (0, BLINK_FRAME):
                draw_screen(state)
            wait_frame(state["pacer"])
            step_frame(state)
    except KeyboardInterrupt:
        pass
