"""Modular exponentiation using exponent bits and repeated squaring."""

from __future__ import annotations


def modular_pow(base: int, exponent: int, modulus: int) -> int:
    """Return base**exponent modulo modulus using bit shifts.

    Arguments must be integers other than bool; exponent must be nonnegative
    and modulus must be nonzero. Negative moduli follow Python's remainder
    convention. The loop takes O(exponent.bit_length()) iterations and reduces
    every product modulo modulus.
    """

    for name, value in (
        ("base", base), ("exponent", exponent), ("modulus", modulus)
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    if modulus == 0:
        raise ValueError("modulus must be nonzero")

    result = 1 % modulus
    factor = base % modulus
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = (result * factor) % modulus
        remaining >>= 1
        if remaining:
            factor = (factor * factor) % modulus

    return result
