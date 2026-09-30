"""Functional tests for the multiplication script."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from app.multiply import multiply


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "app" / "multiply.py"


class MultiplyTests(unittest.TestCase):
    def test_multiplies_positive_integers(self) -> None:
        self.assertEqual(multiply(2, 3), 6)

    def test_multiplies_negative_and_zero_values(self) -> None:
        self.assertEqual(multiply(-7, 0), 0)
        self.assertEqual(multiply(-4, -6), 24)


class MultiplyScriptTests(unittest.TestCase):
    def run_script(self, user_input: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=user_input,
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )

    def test_prints_product_from_single_line_input(self) -> None:
        result = self.run_script("10 20\n")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "200\n")
        self.assertEqual(result.stderr, "")

    def test_accepts_whitespace_separated_input(self) -> None:
        result = self.run_script("-3\n8\n")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "-24\n")

    def test_rejects_missing_operand(self) -> None:
        result = self.run_script("4\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("exactly two integers", result.stderr)

    def test_rejects_non_integer_input(self) -> None:
        result = self.run_script("one 2\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("exactly two integers", result.stderr)


if __name__ == "__main__":
    unittest.main()
