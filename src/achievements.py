"""Achievement labels derived from existing analysis outputs; never alters scores."""
from __future__ import annotations


def generate_achievement_titles(
    *, amazing_plus: int, amazing: int, precision: float, balance: float,
    balance_available: bool, fast: int, slow: int, rank: str,
) -> list[str]:
    titles: list[str] = []
    amazing_total = max(0, int(amazing_plus)) + max(0, int(amazing))
    if amazing_total and int(amazing_plus) / amazing_total >= 0.80:
        titles.append("AMAZING Specialist")
    if float(precision) >= 90.0:
        titles.append("Precision Master")
    if balance_available and float(balance) >= 90.0:
        titles.append("Perfect Balance")
    timing_total = max(0, int(fast)) + max(0, int(slow))
    if timing_total and abs(int(fast) - int(slow)) / timing_total <= 0.05:
        titles.append("Rhythm Master")
    if str(rank).upper() in {"SSS", "SSS+"}:
        titles.append("SSS Collector")
    return titles
