"""Tests for integer exponentiation utilities."""

from __future__ import annotations

import unittest

from app.power import power


class PowerTests(unittest.TestCase):
    def test_raises_positive_base_to_positive_exponent(self) -> None:
        self.assertEqual(power(2, 10), 1024)

    def test_handles_negative_and_zero_bases(self) -> None:
        self.assertEqual(power(-3, 3), -27)
        self.assertEqual(power(-3, 4), 81)
        self.assertEqual(power(0, 5), 0)

    def test_zero_exponent_returns_one(self) -> None:
        self.assertEqual(power(7, 0), 1)
        self.assertEqual(power(-7, 0), 1)
        self.assertEqual(power(0, 0), 1)

    def test_calculates_large_integers_exactly(self) -> None:
        self.assertEqual(power(2, 4096), 2**4096)
        self.assertIsInstance(power(2, 4096), int)

    def test_rejects_negative_exponent(self) -> None:
        with self.assertRaises(ValueError):
            power(2, -1)

    def test_rejects_non_integer_base(self) -> None:
        for invalid_base in (True, False, 2.0, "2", None):
            with self.subTest(base=invalid_base):
                with self.assertRaises(TypeError):
                    power(invalid_base, 3)  # type: ignore[arg-type]

    def test_rejects_non_integer_exponent(self) -> None:
        for invalid_exponent in (True, False, 3.0, "3", None):
            with self.subTest(exponent=invalid_exponent):
                with self.assertRaises(TypeError):
                    power(2, invalid_exponent)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
