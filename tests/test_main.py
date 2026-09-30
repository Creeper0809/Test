"""Functional tests for the addition script."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from app.main import add


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "app" / "main.py"


class AddTests(unittest.TestCase):
    def test_adds_positive_integers(self) -> None:
        self.assertEqual(add(2, 3), 5)

    def test_adds_negative_and_zero_values(self) -> None:
        self.assertEqual(add(-7, 0), -7)
        self.assertEqual(add(-4, -6), -10)


class ScriptTests(unittest.TestCase):
    def run_script(self, user_input: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=user_input,
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )

    def test_prints_sum_from_single_line_input(self) -> None:
        result = self.run_script("10 20\n")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "30\n")
        self.assertEqual(result.stderr, "")

    def test_accepts_whitespace_separated_input(self) -> None:
        result = self.run_script("-3\n8\n")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "5\n")

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
