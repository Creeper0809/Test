"""Read two integers from standard input and print their sum."""

from __future__ import annotations

import sys
from collections.abc import Sequence


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""

    return a + b


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line program using whitespace-separated standard input."""

    del argv  # The program intentionally accepts its operands through stdin.
    values = sys.stdin.read().split()
    if len(values) != 2:
        print("expected exactly two integers", file=sys.stderr)
        return 1

    try:
        a, b = (int(value) for value in values)
    except ValueError:
        print("expected exactly two integers", file=sys.stderr)
        return 1

    print(add(a, b))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
