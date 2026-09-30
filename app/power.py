"""Integer exponentiation utilities."""

from __future__ import annotations


def power(base: int, exponent: int) -> int:
    """Return ``base`` raised to a non-negative integer ``exponent``.

    Both arguments must be integers, with booleans explicitly excluded.
    """

    if isinstance(base, bool) or not isinstance(base, int):
        raise TypeError("base must be an integer")
    if isinstance(exponent, bool) or not isinstance(exponent, int):
        raise TypeError("exponent must be an integer")
    if exponent < 0:
        raise ValueError("exponent must be non-negative")

    result = 1
    factor = base
    remaining = exponent
    while remaining:
        if remaining & 1:
            result *= factor
        remaining >>= 1
        if remaining:
            factor *= factor

    return result
