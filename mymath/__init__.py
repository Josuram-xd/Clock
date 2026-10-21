"""Custom math library: trigonometry, polar geometry, and self-test."""

from mymath.geometry import (
    hand_angle,
    hour_hand_angle,
    minute_hand_angle,
    polar_point,
    second_hand_angle,
)
from mymath.trigonometry import (
    PI,
    cosine,
    degrees_to_radians,
    reduce_angle,
    sine,
)
from mymath.verification import verify_library

__all__ = [
    "PI",
    "cosine",
    "degrees_to_radians",
    "hand_angle",
    "hour_hand_angle",
    "minute_hand_angle",
    "polar_point",
    "reduce_angle",
    "second_hand_angle",
    "sine",
    "verify_library",
]
