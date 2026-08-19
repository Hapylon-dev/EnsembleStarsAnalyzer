"""
validator.py
Version : 1.0 Final Edition

Result Validator

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from models import ValidationResult


# ==========================================================
# Validator
# ==========================================================

class Validator:
    """
    リザルト解析可否判定
    """

    def __init__(self):

        pass

    # ======================================================
    # Validate
    # ======================================================

    def validate(
        self,
        amazing: int,
        perfect: int,
        great: int,
        good: int,
        bad: int,
        miss: int
    ) -> ValidationResult:
        """
        解析可能か判定する
        """

        result = ValidationResult()

        # --------------------------------------------------
        # Judgment Validation
        # --------------------------------------------------

        if (
            great > 0 or
            good > 0 or
            bad > 0 or
            miss > 0
        ):

            result.valid = False

            result.message = (
                "GREAT以下の判定が存在するため解析対象外です。"
            )

            return result

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        result.valid = True

        result.message = "OK"

        return result


# ==========================================================
# Utility
# ==========================================================

_validator = Validator()


def validate(
    amazing: int,
    perfect: int,
    great: int,
    good: int,
    bad: int,
    miss: int
) -> ValidationResult:
    """
    Validator簡易呼び出し
    """

    return _validator.validate(
        amazing,
        perfect,
        great,
        good,
        bad,
        miss
    )