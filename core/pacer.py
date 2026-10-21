"""Pacer: lets a clock run by itself without importing any time module.

There is no system clock, so a "wait" burns a fixed amount of CPU work. One
second is split into FRAMES_PER_SECOND frames so screens can animate and react
to Ctrl+C quickly. The work per second (spins) depends on the computer, so it
can be corrected by timing a run against a real stopwatch (calibration).
"""

FRAMES_PER_SECOND = 10
DEFAULT_SPINS = 107_000_000  # builtin sum(range(n)) iterations per real second (about right on a laptop)
MIN_SPINS = 1_000_000
MIN_CALIBRATION_SECONDS = 10  # shorter runs give too imprecise a measure


def create_pacer(spins=DEFAULT_SPINS):
    """Pacer state: speed and the frames counted since the last calibration mark."""
    return {"spins": spins, "frames": 0}


def wait_frame(pacer):
    """Burn about 1/FRAMES_PER_SECOND of a second of work and count the frame."""
    sum(range(pacer["spins"] // FRAMES_PER_SECOND))
    pacer["frames"] += 1


def start_calibration(pacer):
    """Begin measuring: forget the frames counted so far."""
    pacer["frames"] = 0


def finish_calibration(pacer, real_seconds):
    """Correct the speed after a run that really lasted real_seconds.

    Returns how accurate the clock was before the fix (100 = exact, 150 = it ran
    50% too fast), or None when the run was too short to trust (nothing changes).
    """
    frames = pacer["frames"]
    pacer["frames"] = 0
    if real_seconds < MIN_CALIBRATION_SECONDS or frames == 0:
        return None
    believed_seconds = frames / FRAMES_PER_SECOND
    # The clock counted `believed_seconds` while `real_seconds` really passed. If it
    # counted more than really passed it ran too fast, so each second needs more work.
    pacer["spins"] = max(MIN_SPINS, round(pacer["spins"] * believed_seconds / real_seconds))
    return round(believed_seconds / real_seconds * 100)
