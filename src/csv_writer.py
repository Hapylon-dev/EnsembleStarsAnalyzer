"""
csv_writer.py
Version : 1.0 Final Edition

CSV Writer

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import csv

import config
from models import EstimateResult


# ==========================================================
# CSV Writer
# ==========================================================

class CSVWriter:
    """
    CSV保存
    """

    def __init__(self):

        self.output_dir = Path(config.OUTPUT_DIR)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.csv_path = self.output_dir / "result.csv"

    # ======================================================
    # Header
    # ======================================================

    def write_header(self) -> None:
        """
        ヘッダー作成
        """

        if self.csv_path.exists():
            return

        with open(
            self.csv_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                "DateTime",
                "Music",
                "Difficulty",
                "Level",
                "LiveType",
                "TotalNotes",
                "Amazing",
                "Perfect",
                "Great",
                "Good",
                "Bad",
                "Miss",
                "Slow",
                "Fast",
                "AmazingPlus",
                "AmazingSlow",
                "AmazingFast",
                "AmazingSlowFast",
                "PerfectSlow",
                "PerfectFast",
                "PerfectSlowFast",
                "BalanceAvailable",
                "EstimatedAccuracy"
            ])

    # ======================================================
    # Save
    # ======================================================

    def save(
        self,
        music: str,
        difficulty: str,
        level: int,
        live_type: str,
        total_notes: int,
        amazing: int,
        perfect: int,
        great: int,
        good: int,
        bad: int,
        miss: int,
        slow: int,
        fast: int,
        result: EstimateResult
    ) -> None:
        """
        CSV保存
        """

        self.write_header()

        with open(
            self.csv_path,
            "a",
            newline="",
            encoding="utf-8-sig"
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                music,
                difficulty,
                level,
                live_type,
                total_notes,
                amazing,
                perfect,
                great,
                good,
                bad,
                miss,
                slow,
                fast,
                result.amazing_plus,
                result.amazing_slow,
                result.amazing_fast,
                result.amazing,
                result.perfect_slow,
                result.perfect_fast,
                result.perfect,
                result.balance_available,
                result.estimated_accuracy
            ])


# ==========================================================
# Utility
# ==========================================================

_writer = CSVWriter()


def save(
    music: str,
    difficulty: str,
    level: int,
    live_type: str,
    total_notes: int,
    amazing: int,
    perfect: int,
    great: int,
    good: int,
    bad: int,
    miss: int,
    slow: int,
    fast: int,
    result: EstimateResult
) -> None:
    """
    CSV簡易保存
    """

    _writer.save(
        music,
        difficulty,
        level,
        live_type,
        total_notes,
        amazing,
        perfect,
        great,
        good,
        bad,
        miss,
        slow,
        fast,
        result
    )