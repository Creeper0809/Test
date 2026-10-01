"""Tests for shift-based modular exponentiation."""

from __future__ import annotations

import unittest

from app.modular import modular_pow


class ModularPowTests(unittest.TestCase):
    def test_known_results(self) -> None:
        self.assertEqual(modular_pow(2, 10, 1000), 24)
        self.assertEqual(modular_pow(3, 13, 17), 12)
        self.assertEqual(modular_pow(7, 1, 5), 2)

    def test_zero_exponent(self) -> None:
        for base in (-11, 0, 13):
            with self.subTest(base=base):
                self.assertEqual(modular_pow(base, 0, 7), 1)
                self.assertEqual(modular_pow(base, 0, -7), -6)

    def test_zero_base_with_positive_exponent(self) -> None:
        self.assertEqual(modular_pow(0, 13, 7), 0)
        self.assertEqual(modular_pow(0, 8, -7), 0)

    def test_unit_moduli(self) -> None:
        for modulus in (-1, 1):
            for exponent in (0, 1, 37):
                with self.subTest(modulus=modulus, exponent=exponent):
                    self.assertEqual(modular_pow(5, exponent, modulus), 0)

    def test_negative_bases(self) -> None:
        self.assertEqual(modular_pow(-2, 5, 13), 7)
        self.assertEqual(modular_pow(-2, 6, 13), 12)

    def test_negative_moduli(self) -> None:
        self.assertEqual(modular_pow(2, 10, -1000), -976)
        self.assertEqual(modular_pow(-2, 5, -13), -6)

    def test_matches_builtin_pow_for_small_inputs(self) -> None:
        for base in range(-6, 7):
            for exponent in range(17):
                for modulus in (-13, -5, -1, 1, 2, 5, 13):
                    with self.subTest(base=base, exponent=exponent, modulus=modulus):
                        self.assertEqual(
                            modular_pow(base, exponent, modulus),
                            pow(base, exponent, modulus),
                        )

    def test_sparse_and_dense_exponent_bits(self) -> None:
        for exponent in (1 << 64, (1 << 64) - 1, (1 << 64) + (1 << 31) + 1):
            with self.subTest(exponent=exponent):
                self.assertEqual(
                    modular_pow(17, exponent, 1_000_000_007),
                    pow(17, exponent, 1_000_000_007),
                )

    def test_large_integers(self) -> None:
        base = 10**150 + 39
        modulus = 10**40 + 7
        self.assertEqual(modular_pow(base, 257, modulus), pow(base, 257, modulus))

    def test_huge_exponent(self) -> None:
        exponent = (1 << 4096) + (1 << 2048) + 1
        self.assertEqual(
            modular_pow(17, exponent, 1_000_000_007),
            pow(17, exponent, 1_000_000_007),
        )

    def test_consumes_exponent_with_logarithmic_right_shifts(self) -> None:
        shifts: list[int] = []

        class ShiftCountingInt(int):
            def __rshift__(self, count: int) -> ShiftCountingInt:
                shifts.append(count)
                return ShiftCountingInt(int(self) >> count)

        exponent = ShiftCountingInt((1 << 128) + 17)
        self.assertEqual(
            modular_pow(3, exponent, 101), pow(3, exponent, 101)
        )
        self.assertEqual(shifts, [1] * exponent.bit_length())

    def test_accepts_integer_subclasses(self) -> None:
        class Integer(int):
            pass

        self.assertEqual(modular_pow(Integer(3), Integer(13), Integer(17)), 12)

    def test_rejects_negative_exponents(self) -> None:
        for exponent in (-1, -37):
            with self.subTest(exponent=exponent):
                with self.assertRaises(ValueError):
                    modular_pow(2, exponent, 7)

    def test_rejects_zero_modulus(self) -> None:
        for exponent in (0, 3):
            with self.subTest(exponent=exponent):
                with self.assertRaises(ValueError):
                    modular_pow(2, exponent, 0)

    def test_rejects_non_integer_arguments(self) -> None:
        for invalid in (False, True, 1.0, "1", None, 1j, [], {}):
            for position in range(3):
                arguments = [2, 3, 7]
                arguments[position] = invalid
                with self.subTest(invalid=invalid, position=position):
                    with self.assertRaises(TypeError):
                        modular_pow(*arguments)


if __name__ == "__main__":
    unittest.main()
