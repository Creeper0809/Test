"""Integer range helpers."""

from __future__ import annotations


def clamp(value: int, lower: int, upper: int) -> int:
    """Return value restricted to the inclusive range from lower to upper.

    Raise TypeError for non-integer arguments, including bool, and ValueError
    when lower is greater than upper.
    """

    for argument in (value, lower, upper):
        if isinstance(argument, bool) or not isinstance(argument, int):
            raise TypeError("value, lower, and upper must be integers")

    if lower > upper:
        raise ValueError("lower must be less than or equal to upper")

    if value < lower:
        return lower
    if value > upper:
        return upper
    return value
