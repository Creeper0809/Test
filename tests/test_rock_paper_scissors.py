"""Deterministic round, match and CLI tests for rock-paper-scissors."""

from __future__ import annotations

import io
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from app.rock_paper_scissors import judge_round, main


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "app" / "rock_paper_scissors.py"


class RoundTests(unittest.TestCase):
    def test_all_nine_outcomes(self) -> None:
        cases = (
            ("가위", "가위", 0),
            ("가위", "바위", -1),
            ("가위", "보", 1),
            ("바위", "가위", 1),
            ("바위", "바위", 0),
            ("바위", "보", -1),
            ("보", "가위", -1),
            ("보", "바위", 1),
            ("보", "보", 0),
        )
        for player, computer, expected in cases:
            with self.subTest(player=player, computer=computer):
                self.assertEqual(judge_round(player, computer), expected)

    def test_rejects_unsupported_moves(self) -> None:
        for player, computer in (("rock", "가위"), ("가위", "")):
            with self.subTest(player=player, computer=computer):
                with self.assertRaises(ValueError):
                    judge_round(player, computer)


class MatchTests(unittest.TestCase):
    def run_game(
        self, player_moves: list[str | BaseException], computer_moves: list[str]
    ) -> tuple[int, str, str, list[str], int]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("builtins.input", side_effect=player_moves) as player_input,
            patch(
                "app.rock_paper_scissors.random.choice", side_effect=computer_moves
            ) as computer_choice,
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            status = main()

        prompts = [call.args[0] for call in player_input.call_args_list]
        for call in computer_choice.call_args_list:
            self.assertEqual(call.args, (("가위", "바위", "보"),))
        return status, stdout.getvalue(), stderr.getvalue(), prompts, computer_choice.call_count

    def test_player_wins_two_to_zero_and_stops_early(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["가위", "보", "바위"], ["보", "바위", "가위"]
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("플레이어: 가위 | 컴퓨터: 보", output)
        self.assertIn("최종 승자: 플레이어 (2:0)", output)
        self.assertEqual(len(prompts), 2)
        self.assertEqual(choices, 2)

    def test_computer_wins_two_to_zero_and_stops_early(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["가위", "보", "바위"], ["바위", "가위", "가위"]
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("최종 승자: 컴퓨터 (0:2)", output)
        self.assertEqual(len(prompts), 2)
        self.assertEqual(choices, 2)

    def test_player_wins_on_third_decisive_round(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["가위", "가위", "보"], ["보", "바위", "바위"]
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("현재 점수: 플레이어 1 - 컴퓨터 1", output)
        self.assertIn("최종 승자: 플레이어 (2:1)", output)
        self.assertEqual(prompts, [f"{number}판 (가위/바위/보): " for number in (1, 2, 3)])
        self.assertEqual(choices, 3)

    def test_computer_wins_on_third_decisive_round(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["가위", "가위", "보"], ["보", "바위", "가위"]
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("최종 승자: 컴퓨터 (1:2)", output)
        self.assertEqual(len(prompts), 3)
        self.assertEqual(choices, 3)

    def test_draw_replays_round_without_changing_score(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["바위", "가위", "보", "바위", "가위"],
            ["바위", "보", "보", "보", "보"],
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertEqual(output.count("이번 판: 무승부"), 2)
        self.assertIn("현재 점수: 플레이어 0 - 컴퓨터 0", output)
        self.assertEqual(output.count("현재 점수: 플레이어 1 - 컴퓨터 0"), 2)
        self.assertIn("최종 승자: 플레이어 (2:1)", output)
        self.assertEqual(prompts, [f"{number}판 (가위/바위/보): " for number in (1, 1, 2, 2, 3)])
        self.assertEqual(choices, 5)

    def test_invalid_and_blank_input_do_not_consume_round_or_choice(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["rock", "", "   ", "가위", "보"], ["보", "바위"]
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertEqual(output.count("잘못된 입력입니다."), 3)
        self.assertIn("최종 승자: 플레이어 (2:0)", output)
        self.assertEqual(prompts, [f"{number}판 (가위/바위/보): " for number in (1, 1, 1, 1, 2)])
        self.assertEqual(choices, 2)

    def test_accepts_surrounding_whitespace(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["  가위  ", "\t보\t"], ["보", "바위"]
        )

        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("최종 승자: 플레이어 (2:0)", output)
        self.assertEqual(len(prompts), 2)
        self.assertEqual(choices, 2)

    def test_eof_mid_match_cancels_without_declaring_winner(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            ["가위", EOFError()], ["보"]
        )

        self.assertEqual(status, 1)
        self.assertIn("현재 점수: 플레이어 1 - 컴퓨터 0", output)
        self.assertNotIn("최종 승자:", output)
        self.assertIn("게임을 중단합니다.", errors)
        self.assertEqual(len(prompts), 2)
        self.assertEqual(choices, 1)

    def test_keyboard_interrupt_cancels_without_declaring_winner(self) -> None:
        status, output, errors, prompts, choices = self.run_game(
            [KeyboardInterrupt()], []
        )

        self.assertEqual(status, 1)
        self.assertNotIn("최종 승자:", output)
        self.assertIn("게임을 중단합니다.", errors)
        self.assertEqual(len(prompts), 1)
        self.assertEqual(choices, 0)


class ScriptTests(unittest.TestCase):
    def test_direct_script_prompts_and_handles_invalid_input_then_eof(self) -> None:
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT)],
            input="잘못된 선택\n",
            encoding="utf-8",
            capture_output=True,
            cwd=ROOT,
            timeout=10,
            check=False,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("가위바위보 3세판", result.stdout)
        self.assertEqual(result.stdout.count("1판 (가위/바위/보): "), 2)
        self.assertIn("잘못된 입력입니다.", result.stdout)
        self.assertNotIn("최종 승자:", result.stdout)
        self.assertIn("게임을 중단합니다.", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
