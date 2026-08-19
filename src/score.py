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

    (85.6, "SSS+"),
    (84.4, "SSS"),
    (83.2, "SS+"),
    (82.0, "SS"),
    (80.8, "S+"),
    (79.6, "S"),

    (78.4, "AAA+"),
    (77.2, "AAA"),
    (76.0, "AA+"),
    (74.8, "AA"),
    (73.6, "A+"),
    (72.4, "A"),

    (71.2, "BBB+"),
    (70.0, "BBB"),
    (68.8, "BB+"),
    (67.6, "BB"),
    (66.4, "B+"),
    (65.2, "B"),

    (64.0, "CCC+"),
    (62.8, "CCC"),
    (61.6, "CC+"),
    (60.4, "CC"),
    (59.2, "C+"),
    (58.0, "C"),

    (56.8, "DDD+"),
    (55.6, "DDD"),
    (54.4, "DD+"),
    (53.2, "DD"),
    (52.0, "D+"),
    (50.8, "D"),

    (49.6, "EEE+"),
    (48.4, "EEE"),
    (47.2, "EE+"),
    (46.0, "EE"),
    (44.8, "E+"),
    (43.6, "E"),

    (0.0, "F"),

]

# ==========================================================
# Precision Grade Border
# Version 1.3
# ==========================================================

PRECISION_GRADE_TABLE = [

    (84.0, "SSS"),
    (82.0, "SS"),
    (80.0, "S"),
    (78.0, "AAA"),
    (76.0, "AA"),
    (74.0, "A"),
    (72.0, "BBB"),
    (70.0, "BB"),
    (68.0, "B"),
    (66.0, "CCC"),
    (64.0, "CC"),
    (62.0, "C"),
    (60.0, "DDD"),
    (58.0, "DD"),
    (56.0, "D"),
    (54.0, "EEE"),
    (52.0, "EE"),
    (50.0, "E"),
    (0.0, "F"),

]

# ==========================================================
# Balance Grade Border
# Version 1.3
# ==========================================================

BALANCE_GRADE_TABLE = [

    (98.0, "SSS"),
    (94.0, "SS"),
    (90.0, "S"),
    (86.0, "AAA"),
    (82.0, "AA"),
    (78.0, "A"),
    (74.0, "BBB"),
    (70.0, "BB"),
    (66.0, "B"),
    (62.0, "CCC"),
    (58.0, "CC"),
    (54.0, "C"),
    (50.0, "DDD"),
    (46.0, "DD"),
    (42.0, "D"),
    (38.0, "EEE"),
    (34.0, "EE"),
    (30.0, "E"),
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

        AMAZING+ が最高判定内で占める割合を計算する。
        """

        highest = (

            estimate.amazing_plus

            + estimate.amazing

        )

        if highest <= 0:

            return 0.0

        precision = (

            estimate.amazing_plus

            / highest

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
        Precision を SS～E へ変換する。
        """

        for border, grade in PRECISION_GRADE_TABLE:

            if precision >= border:

                return grade

        return "E"

    # ======================================================
    # Balance Grade
    # ======================================================

    def calculate_balance_grade(
        self,
        balance: float
    ) -> str:
        """
        Balance を SS～E へ変換する。
        """

        for border, grade in BALANCE_GRADE_TABLE:

            if balance >= border:

                return grade

        return "E"
    
    # ======================================================
    # Balance
    # ======================================================

    def calculate_balance(
        self,
        estimate: EstimateResult
    ) -> float:
        """
        Balance

        FAST と SLOW の偏りを評価する。

        100% に近いほど
        左右の入力バランスが良い。

        SLOW / FAST 両側のバーを検出できない場合は、
        Balanceを評価対象外とする。
        """

        if not estimate.balance_available:
            return 0.0

        total = (

            estimate.fast

            + estimate.slow

        )

        if total <= 0:

            return 100.0

        difference = abs(

            estimate.fast

            - estimate.slow

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