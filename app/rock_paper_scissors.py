"""Play a best-of-three rock-paper-scissors match against the computer."""

from __future__ import annotations

import random
import sys


CHOICES = ("가위", "바위", "보")
WINNING_PAIRS = {("가위", "보"), ("바위", "가위"), ("보", "바위")}


def judge_round(player: str, computer: str) -> int:
    """Return 1 for a player win, -1 for a loss, or 0 for a draw."""

    if player not in CHOICES or computer not in CHOICES:
        raise ValueError("가위, 바위, 보 중 하나를 선택하세요.")
    if player == computer:
        return 0
    return 1 if (player, computer) in WINNING_PAIRS else -1


def main() -> int:
    """Read Korean moves until either side wins two decisive rounds."""

    player_wins = 0
    computer_wins = 0
    print("가위바위보 3세판: 먼저 2승을 거두면 승리합니다. 무승부는 다시 진행합니다.")

    while player_wins < 2 and computer_wins < 2:
        round_number = player_wins + computer_wins + 1
        try:
            player = input(f"{round_number}판 (가위/바위/보): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("입력이 종료되어 게임을 중단합니다.", file=sys.stderr)
            return 1

        if player not in CHOICES:
            print("잘못된 입력입니다. 가위, 바위, 보 중 하나를 입력하세요.")
            continue

        computer = random.choice(CHOICES)
        result = judge_round(player, computer)
        print(f"플레이어: {player} | 컴퓨터: {computer}")
        if result == 1:
            player_wins += 1
            print("이번 판: 승리")
        elif result == -1:
            computer_wins += 1
            print("이번 판: 패배")
        else:
            print("이번 판: 무승부. 같은 판을 다시 진행합니다.")
        print(f"현재 점수: 플레이어 {player_wins} - 컴퓨터 {computer_wins}")

    winner = "플레이어" if player_wins == 2 else "컴퓨터"
    print(f"최종 승자: {winner} ({player_wins}:{computer_wins})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
