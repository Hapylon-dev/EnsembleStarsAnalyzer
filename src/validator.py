"""Input/result eligibility checks for supported live-result screenshots.

The validator is not currently part of the main analysis path. Its API is kept
small and explicit so future validation rules can be added without changing
the score estimator.
"""
from __future__ import annotations

from models import ValidationResult


class Validator:
    """Validate judgement eligibility and an optional challenge-rate rule."""

    def validate(
        self,
        amazing: int,
        perfect: int,
        great: int,
        good: int,
        bad: int,
        miss: int,
        *,
        challenge_rate: float | None = None,
        minimum_challenge_rate: float | None = None,
    ) -> ValidationResult:
        values = {
            "AMAZING": int(amazing),
            "PERFECT": int(perfect),
            "GREAT": int(great),
            "GOOD": int(good),
            "BAD": int(bad),
            "MISS": int(miss),
        }
        if any(value < 0 for value in values.values()):
            raise ValueError("判定数に負の値は指定できません。")

        judge_ok = not any(values[name] > 0 for name in ("GREAT", "GOOD", "BAD", "MISS"))

        # Thresholds are opt-in. Do not invent a challenge-rate criterion when
        # the caller has not supplied one.
        challenge_rate_ok = True
        if minimum_challenge_rate is not None:
            if challenge_rate is None:
                challenge_rate_ok = False
            else:
                challenge_rate_ok = float(challenge_rate) >= float(minimum_challenge_rate)

        is_target = judge_ok and challenge_rate_ok
        messages: list[str] = []
        if not judge_ok:
            messages.append("GREAT以下の判定が存在するため解析対象外です。")
        if not challenge_rate_ok:
            messages.append("チャレンジレートが指定された基準を満たしていません。")

        challenge_text = (
            "未確認" if challenge_rate is None
            else f"{float(challenge_rate):.3f}%"
        )
        return ValidationResult(
            is_target=is_target,
            challenge_rate_ok=challenge_rate_ok,
            judge_ok=judge_ok,
            challenge_rate_text=challenge_text,
            judge_values=values,
            message="\n".join(messages) if messages else "OK",
        )


_validator = Validator()


def validate(
    amazing: int,
    perfect: int,
    great: int,
    good: int,
    bad: int,
    miss: int,
    *,
    challenge_rate: float | None = None,
    minimum_challenge_rate: float | None = None,
) -> ValidationResult:
    """Convenience wrapper for :class:`Validator`."""
    return _validator.validate(
        amazing, perfect, great, good, bad, miss,
        challenge_rate=challenge_rate,
        minimum_challenge_rate=minimum_challenge_rate,
    )
