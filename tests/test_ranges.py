"""Tests for integer range helpers."""

from __future__ import annotations

import unittest

from app.ranges import clamp


class ClampTests(unittest.TestCase):
    def test_returns_value_inside_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamps_value_below_lower_bound(self) -> None:
        self.assertEqual(clamp(-1, 0, 10), 0)

    def test_clamps_value_above_upper_bound(self) -> None:
        self.assertEqual(clamp(11, 0, 10), 10)

    def test_includes_lower_bound(self) -> None:
        self.assertEqual(clamp(0, 0, 10), 0)

    def test_includes_upper_bound(self) -> None:
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_handles_negative_range(self) -> None:
        for value, expected in ((-5, -5), (-11, -10), (0, -1)):
            with self.subTest(value=value):
                self.assertEqual(clamp(value, -10, -1), expected)

    def test_handles_equal_bounds(self) -> None:
        for value in (2, 3, 4):
            with self.subTest(value=value):
                self.assertEqual(clamp(value, 3, 3), 3)

    def test_handles_arbitrarily_large_integers(self) -> None:
        limit = 10**100
        for value, expected in (
            (-limit - 1, -limit),
            (-limit, -limit),
            (0, 0),
            (limit, limit),
            (limit + 1, limit),
        ):
            with self.subTest(value=value):
                self.assertEqual(clamp(value, -limit, limit), expected)

    def test_rejects_reversed_bounds(self) -> None:
        for arguments in ((5, 10, 0), (-5, -1, -10)):
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    clamp(*arguments)

    def test_rejects_non_integer_in_each_argument(self) -> None:
        for position in range(3):
            for invalid in (1.0, "1", None, 1 + 0j, [], {}, ()):
                arguments = [5, 0, 10]
                arguments[position] = invalid
                with self.subTest(position=position, invalid=invalid):
                    with self.assertRaises(TypeError):
                        clamp(*arguments)

    def test_rejects_bool_in_each_argument(self) -> None:
        for position in range(3):
            for invalid in (False, True):
                arguments = [5, 0, 10]
                arguments[position] = invalid
                with self.subTest(position=position, invalid=invalid):
                    with self.assertRaises(TypeError):
                        clamp(*arguments)

    def test_rejects_invalid_type_before_reversed_bounds(self) -> None:
        for invalid in (None, 1.0, False, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(TypeError):
                    clamp(invalid, 10, 0)

    def test_accepts_integer_subclasses(self) -> None:
        class Integer(int):
            pass

        value, lower, upper = Integer(5), Integer(0), Integer(10)
        self.assertIs(clamp(value, lower, upper), value)
        self.assertIs(clamp(Integer(-1), lower, upper), lower)
        self.assertIs(clamp(Integer(11), lower, upper), upper)


if __name__ == "__main__":
    unittest.main()
