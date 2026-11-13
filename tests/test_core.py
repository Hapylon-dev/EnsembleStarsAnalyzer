"""Regression tests for stable scoring, eligibility checks and ranking."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from models import EstimateResult
from score import ScoreCalculator
from validator import validate
from ranking import load_ranking_base, calculate_ranking


class ScoreRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = ScoreCalculator()

    def test_achievement_uses_current_weights(self) -> None:
        estimate = EstimateResult(amazing_plus=714, amazing=144)
        self.assertEqual(self.calculator.calculate_achievement(estimate, 858), 100.832)

    def test_precision_uses_center_bar_ratio(self) -> None:
        estimate = EstimateResult(height_ratio=[10.0, 80.0, 10.0])
        self.assertEqual(self.calculator.calculate_precision(estimate), 80.0)

    def test_balance_is_unavailable_without_both_sides(self) -> None:
        estimate = EstimateResult(
            height_ratio=[20.0, 60.0, 20.0],
            balance_available=False,
        )
        result = self.calculator.score(estimate, 100)
        self.assertEqual(result.balance_grade, "N/A")
        self.assertEqual(result.overall_score, result.precision)

    def test_rank_boundaries(self) -> None:
        self.assertEqual(self.calculator.calculate_rank(86.0), "SSS+")
        self.assertEqual(self.calculator.calculate_rank(84.0), "SSS")
        self.assertEqual(self.calculator.calculate_rank(0.0), "F")


class ValidatorRegressionTests(unittest.TestCase):
    def test_valid_judgements_construct_dataclass_correctly(self) -> None:
        result = validate(10, 5, 0, 0, 0, 0)
        self.assertTrue(result.is_target)
        self.assertTrue(result.judge_ok)
        self.assertEqual(result.message, "OK")
        self.assertEqual(result.judge_values["AMAZING"], 10)

    def test_lower_judgement_is_rejected(self) -> None:
        result = validate(10, 5, 1, 0, 0, 0)
        self.assertFalse(result.is_target)
        self.assertFalse(result.judge_ok)
        self.assertIn("GREAT以下", result.message)

    def test_optional_challenge_rate_threshold(self) -> None:
        passed = validate(10, 5, 0, 0, 0, 0, challenge_rate=100.0, minimum_challenge_rate=100.0)
        failed = validate(10, 5, 0, 0, 0, 0, challenge_rate=99.9, minimum_challenge_rate=100.0)
        self.assertTrue(passed.challenge_rate_ok)
        self.assertFalse(failed.challenge_rate_ok)
        self.assertFalse(failed.is_target)

    def test_negative_judgement_count_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate(-1, 0, 0, 0, 0, 0)


class RankingRegressionTests(unittest.TestCase):
    def test_fixed_ranking_base_and_comparison_count(self) -> None:
        rows = load_ranking_base(ROOT / "output" / "ranking_batch_results.csv")
        self.assertEqual(len(rows), 1799)
        result = calculate_ranking(73.803, rows)
        self.assertEqual(result["comparison_total"], 1800)
        self.assertGreaterEqual(result["ranking_position"], 1)
        self.assertLessEqual(result["ranking_position"], 1800)


if __name__ == "__main__":
    unittest.main()
