"""
score.py
Version : 1.0

Tap Timing Score Calculator

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from models import (
    EstimateResult,
    ScoreResult,
)

# ==========================================================
# Achievement Weight
# ==========================================================

AMAZING_PLUS_WEIGHT = 1.01
AMAZING_WEIGHT = 1.00
PERFECT_WEIGHT = 0.90


# ==========================================================
# Overall Weight
# ==========================================================

PRECISION_WEIGHT = 0.80
BALANCE_WEIGHT = 0.20

# ==========================================================
# Rank Border
# Version 1.3
# ==========================================================

RANK_TABLE = [

    (86.0, "SSS+"),
    (84.0, "SSS"),
    (82.0, "SS+"),
    (80.0, "SS"),
    (78.0, "S+"),
    (76.0, "S"),
    (74.0, "AAA+"),
    (72.0, "AAA"),
    (70.0, "AA+"),
    (68.0, "AA"),
    (66.0, "A+"),
    (64.0, "A"),
    (62.0, "BBB"),
    (60.0, "BB"),
    (58.0, "B"),
    (56.0, "CCC"),
    (54.0, "CC"),
    (52.0, "C"),
    (50.0, "D"),
    (48.0, "E"),
    (0.0, "F"),

]

# ==========================================================
# Precision Grade Border
# Version 1.3
# ==========================================================

PRECISION_GRADE_TABLE = [

    (88.0, "SSS"),
    (86.0, "SS"),
    (84.0, "S"),
    (82.0, "AAA"),
    (80.0, "AA"),
    (78.0, "A"),
    (76.0, "BBB"),
    (74.0, "BB"),
    (72.0, "B"),
    (70.0, "CCC"),
    (68.0, "CC"),
    (64.0, "C"),
    (60.0, "D"),
    (56.0, "E"),
    (0.0, "F"),

]

# ==========================================================
# Balance Grade Border
# Version 1.3
# ==========================================================

BALANCE_GRADE_TABLE = [

    (97.0, "SSS"),
    (94.0, "SS"),
    (87.0, "S"),
    (80.0, "AAA"),
    (71.0, "AA"),
    (62.0, "A"),
    (53.0, "BBB"),
    (44.0, "BB"),
    (37.0, "B"),
    (30.0, "CCC"),
    (25.0, "CC"),
    (20.0, "C"),
    (15.0, "D"),
    (12.0, "E"),
    (0.0, "F"),

]

# ==========================================================
# Calculator
# ==========================================================

class ScoreCalculator:
    """
    Score Calculator

    ・ACHIEVEMENT
    ・Precision
    ・Balance
    ・Overall Score
    ・Rank
    ・Grade
    """

    # ======================================================
    # Achievement
    # ======================================================

    def calculate_achievement(
        self,
        estimate: EstimateResult,
        total_notes: int
    ) -> float:
        """
        独自ACHIEVEMENT

        AMAZING+ × 1.01
        AMAZING  × 1.00
        PERFECT  × 0.90

        理論値
            101.000%
        """

        if total_notes <= 0:
            return 0.0

        score = 0.0

        score += (
            estimate.amazing_plus
            * AMAZING_PLUS_WEIGHT
        )

        score += (
            estimate.amazing
            * AMAZING_WEIGHT
        )

        score += (
            estimate.perfect
            * PERFECT_WEIGHT
        )

        achievement = (
            score
            / total_notes
            * 100.0
        )

        return round(
            achievement,
            3
        )

    # ======================================================
    # Precision
    # ======================================================

    def calculate_precision(
        self,
        estimate: EstimateResult
    ) -> float:
        """
        Precision

        グラフ高さのみから計算する。

        3本の場合：
            [0] = SLOW
            [1] = CENTER
            [2] = FAST

        2本の場合も、
            [SLOW, CENTER, 0]
            または
            [0, CENTER, FAST]
        の3要素へ正規化されている。

        Precision =
            CENTER
            / (SLOW + CENTER + FAST)
            × 100

        Total Notes および推定ノーツ数は使用しない。
        """

        ratios = estimate.height_ratio

        if len(ratios) != 3:
            return 0.0

        slow_ratio = ratios[0]
        center_ratio = ratios[1]
        fast_ratio = ratios[2]

        highest_ratio = (
            slow_ratio
            + center_ratio
            + fast_ratio
        )

        if highest_ratio <= 0:
            return 0.0

        precision = (
            center_ratio
            / highest_ratio
            * 100.0
        )

        return round(
            precision,
            3
        )
    
    # ======================================================
    # Precision Grade
    # ======================================================

    def calculate_precision_grade(
        self,
        precision: float
    ) -> str:
        """
        Precision を SSS～F へ変換する。
        """

        for border, grade in PRECISION_GRADE_TABLE:

            if precision >= border:

                return grade

        return "F"

    # ======================================================
    # Balance Grade
    # ======================================================

    def calculate_balance_grade(
        self,
        balance: float
    ) -> str:
        """
        Balance を SSS～F へ変換する。
        """

        for border, grade in BALANCE_GRADE_TABLE:

            if balance >= border:

                return grade

        return "F"
    
    # ======================================================
    # Balance
    # ======================================================

    def calculate_balance(
        self,
        estimate: EstimateResult
    ) -> float:
        """
        Balance

        グラフ高さのみから計算する。

        [0] = SLOW
        [1] = AMAZING+
        [2] = FAST

        SLOW / FAST のグラフ高さが
        どれだけ均等かを評価する。

        100%:
            SLOW と FAST が同じ高さ

        0%:
            SLOW または FAST の一方しか存在しない

        Total Notes および推定ノーツ数は使用しない。
        """

        if not estimate.balance_available:
            return 0.0

        ratios = estimate.height_ratio

        if len(ratios) < 3:
            return 0.0

        slow_ratio = ratios[0]
        fast_ratio = ratios[2]

        total = (
            slow_ratio
            + fast_ratio
        )

        if total <= 0:
            return 100.0

        difference = abs(
            slow_ratio
            - fast_ratio
        )

        balance = (
            1.0
            - difference / total
        ) * 100.0

        balance = max(
            0.0,
            min(
                100.0,
                balance
            )
        )

        return round(
            balance,
            3
        )
    
    # ======================================================
    # Overall Score
    # ======================================================

    def calculate_overall(
        self,
        precision: float,
        balance: float
    ) -> float:
        """
        総合評価
        """

        overall = (

            precision
            * PRECISION_WEIGHT

            +

            balance
            * BALANCE_WEIGHT

        )

        return round(
            overall,
            3
        )
    
    # ======================================================
    # Rank
    # ======================================================

    def calculate_rank(
        self,
        overall: float
    ) -> str:
        """
        Overall Score を Rank へ変換する。

        Version 1.0
        """

        for border, rank in RANK_TABLE:

            if overall >= border:
                return rank

        return "E"
    
    # ======================================================
    # Score
    # ======================================================

    def score(
        self,
        estimate: EstimateResult,
        total_notes: int
    ) -> ScoreResult:

        achievement = self.calculate_achievement(
            estimate,
            total_notes
        )

        precision = self.calculate_precision(
            estimate
        )

        balance = self.calculate_balance(
            estimate
        )

        precision_grade = self.calculate_precision_grade(
            precision
        )

        if estimate.balance_available:

            balance_grade = self.calculate_balance_grade(
                balance
            )

        else:

            balance_grade = "N/A"

        if estimate.balance_available:

            overall = self.calculate_overall(
                precision,
                balance
            )

        else:

            overall = round(
                precision,
                3
            )

        rank = self.calculate_rank(
            overall
        )

        return ScoreResult(

            achievement=achievement,

            precision=precision,

            precision_grade=precision_grade,

            balance=balance,

            balance_grade=balance_grade,

            balance_available=estimate.balance_available,

            overall_score=overall,

            rank=rank

        )

# ==========================================================
# Utility
# ==========================================================

_calculator = ScoreCalculator()


def score(
    estimate: EstimateResult,
    total_notes: int
) -> ScoreResult:
    """
    ScoreCalculator簡易呼び出し
    """

    return _calculator.score(

        estimate=estimate,

        total_notes=total_notes

    )