from __future__ import annotations
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
from fractions import Fraction
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pachinko import (COLOR_WEIGHTS, BASE_COLOR_WEIGHTS, COLOR_HIT_RATES, PAYOUT_WEIGHTS, ST_MAX, decimal_triple,
                      initial_payout, load_overall_values, PachinkoSession, expected_values)
from achievements import generate_achievement_titles
from pachinko_rank import get_pachinko_rank, RANK_THRESHOLDS, RANK_COLORS

class PachinkoTests(unittest.TestCase):
    def test_fixed_dataset_has_1799_values_and_new_initial_distribution(self):
        values = load_overall_values(ROOT / 'output' / 'ranking_batch_results.csv')
        self.assertEqual(len(values), 1799)
        triples = [decimal_triple(v) for v in values]
        self.assertEqual(sum(value is not None for value in triples), 52)
        payouts = [initial_payout(t) for t in triples if t is not None]
        self.assertEqual(payouts.count(300), 14)
        self.assertEqual(payouts.count(1500), 29)
        self.assertEqual(payouts.count(3000), 8)
        self.assertEqual(payouts.count(4500), 1)

    def test_weighted_rush_probability_is_exactly_one_in_73(self):
        weighted = sum(Fraction(str(w)) / Fraction(str(sum(weight for _, weight in COLOR_WEIGHTS))) * Fraction(str(COLOR_HIT_RATES[c])) for c, w in COLOR_WEIGHTS)
        self.assertAlmostEqual(float(weighted), 1 / 73, places=12)
        self.assertEqual(ST_MAX, 116)
        self.assertEqual(set(COLOR_HIT_RATES), {'blue', 'green', 'red', 'gold', 'rainbow'})
        self.assertGreaterEqual(COLOR_HIT_RATES['red'], 0.60)

    def test_upgrade_adjusted_hold_distribution_matches_targets(self):
        base = dict(BASE_COLOR_WEIGHTS)
        total = sum(base.values())
        base_p = [base[c] / total for c in ("blue", "green", "red", "gold", "rainbow")]
        final = [0.0] * 5
        for i, probability in enumerate(base_p):
            final[i] += probability * (1.0 if i == 4 else 0.98)
            if i < 4:
                final[i + 1] += probability * 0.02
        targets = [0.90, 0.09, 0.009, 0.0009, 0.0001]
        for actual, target in zip(final, targets):
            self.assertAlmostEqual(actual, target, places=9)
        overall = sum(final[i] * COLOR_HIT_RATES[c]
                      for i, c in enumerate(("blue", "green", "red", "gold", "rainbow")))
        self.assertAlmostEqual(overall, 1 / 73, places=12)

    def test_initial_payout_rules(self):
        self.assertEqual(initial_payout('000'), 1500)
        self.assertEqual(initial_payout('222'), 300)
        self.assertEqual(initial_payout('333'), 3000)
        self.assertEqual(initial_payout('777'), 4500)
        self.assertEqual(initial_payout('999'), 3000)

    def test_expected_values(self):
        ev = expected_values()
        self.assertAlmostEqual(ev['normal_initial_notes'], 1465.38461538, places=6)
        self.assertGreater(ev['initial_notes'], ev['normal_initial_notes'])
        self.assertGreater(ev['time_hit_probability'], 0.97)
        self.assertEqual(ev['time_spins'], 131)
        self.assertEqual(ev['rush_hit_notes'], 2010)
        self.assertAlmostEqual(ev['segment_continuation'], 0.8089459021, places=9)
        self.assertAlmostEqual(ev['rush_hits'], 4.2341196075, places=8)
        self.assertAlmostEqual(ev['rush_notes'], 8510.58041116, places=6)
        self.assertAlmostEqual(ev['total_notes'], ev['initial_notes'] + ev['rush_notes'], places=6)

    def test_pachinko_rank_has_21_tiers_and_300_notes_is_f(self):
        self.assertEqual(len(RANK_THRESHOLDS), 21)
        self.assertEqual(get_pachinko_rank(300), 'F')
        self.assertEqual(get_pachinko_rank(1499), 'F')
        self.assertEqual(get_pachinko_rank(1500), 'E')
        self.assertEqual(get_pachinko_rank(1800), 'D')
        self.assertEqual(get_pachinko_rank(60000), 'SSS+')
        self.assertEqual(get_pachinko_rank(59999), 'SSS')
        self.assertEqual(get_pachinko_rank(50400), 'SSS')
        self.assertEqual(get_pachinko_rank(44700), 'SS+')
        self.assertEqual(get_pachinko_rank(33300), 'S')

    def test_all_new_rank_boundaries(self):
        expected = [
            (60000, "SSS+"), (50400, "SSS"), (44700, "SS+"), (40500, "SS"),
            (36900, "S+"), (33300, "S"), (29700, "AAA+"), (26400, "AAA"),
            (23400, "AA+"), (20700, "AA"), (18300, "A+"), (15900, "A"),
            (14100, "BBB"), (12300, "BB"), (9900, "B"), (7800, "CCC"),
            (5400, "CC"), (3300, "C"), (1800, "D"), (1500, "E"), (300, "F"),
        ]
        for minimum, rank in expected:
            self.assertEqual(get_pachinko_rank(minimum), rank)

    def test_rank_color_groups_match_user_palette(self):
        self.assertEqual({RANK_COLORS[r] for r in ("SS+", "SS", "S+", "S")}, {"gold"})
        self.assertEqual({RANK_COLORS[r] for r in ("AAA+", "AAA", "AA+", "AA", "A+", "A")}, {"red"})
        self.assertEqual({RANK_COLORS[r] for r in ("BBB", "BB", "B")}, {"blue"})
        self.assertEqual({RANK_COLORS[r] for r in ("CCC", "CC", "C")}, {"green"})
        self.assertEqual([RANK_COLORS[r] for r in ("D", "E", "F")], ["pink", "purple", "gray"])

    def test_plus_and_non_plus_rank_pairs_share_colors(self):
        pairs = (("SSS+", "SSS"), ("SS+", "SS"), ("S+", "S"),
                 ("AAA+", "AAA"), ("AA+", "AA"), ("A+", "A"))
        for plus, plain in pairs:
            self.assertEqual(RANK_COLORS[plus], RANK_COLORS[plain])


    def test_unconsumed_holds_carry_over_after_rush_jackpot(self):
        session = PachinkoSession()
        session.in_rush = True
        session.st_remaining = 63
        session.holds = ["red", "gold", "blue", "green", "rainbow"]
        with (patch("pachinko.upgrade_hold_color", side_effect=lambda color, rng: (color, False)),
              patch("pachinko.hold_hits", return_value=True),
              patch("pachinko.draw_rush_payout", return_value=1500)):
            event = session.consume_hold()
        self.assertEqual(event["type"], "rush_jackpot")
        self.assertEqual(session.st_remaining, ST_MAX)
        self.assertEqual(session.holds, ["gold", "blue", "green", "rainbow"])

    def test_reserve_hit_keeps_rush_chain_and_notes_and_resets_st(self):
        session = PachinkoSession()
        session.in_rush = True
        session.st_remaining = 0
        session.reserve_spins = 0
        session.combo = 3
        session.rush_hits = 3
        session.rush_notes = 4500
        session.notes = 6000
        session.holds = ["red", "gold"]
        with (patch("pachinko.upgrade_hold_color", side_effect=lambda color, rng: (color, False)),
              patch("pachinko.hold_hits", return_value=True),
              patch("pachinko.draw_rush_payout", return_value=1500)):
            event = session.consume_hold()
        self.assertEqual(event["type"], "rush_jackpot")
        self.assertEqual(session.st_remaining, ST_MAX)
        self.assertEqual(session.combo, 4)
        self.assertEqual(session.rush_hits, 4)
        self.assertEqual(session.rush_notes, 6000)
        self.assertEqual(session.notes, 7500)
        self.assertEqual(session.holds, ["gold"])
        self.assertTrue(session.in_rush)
        self.assertFalse(session.ended)

    def test_decimal_triple_detection(self):
        self.assertEqual(decimal_triple(72.222), '222')
        self.assertEqual(decimal_triple(80.0), '000')
        self.assertIsNone(decimal_triple(72.224))

    def test_normal_miss_allows_another_independent_draw_and_counts_spins(self):
        class SequenceRng:
            def __init__(self): self.values = iter([72.224, 72.222])
            def choice(self, _values): return next(self.values)
        session = PachinkoSession(rng=SequenceRng())
        first = session.normal_spin([72.224, 72.222])
        self.assertEqual(first['type'], 'miss')
        second = session.normal_spin([72.224, 72.222])
        self.assertEqual(second['type'], 'initial_jackpot')
        self.assertEqual(second['spins'], 2)
        self.assertEqual(session.st_remaining, 116)
        self.assertEqual(session.payout_counts[300], 1)

    def test_achievement_does_not_change_score_and_uses_existing_values(self):
        got = generate_achievement_titles(amazing_plus=90, amazing=10, precision=91,
            balance=92, balance_available=True, fast=50, slow=50, rank='SSS')
        self.assertEqual(got, ['AMAZING Specialist', 'Precision Master', 'Perfect Balance',
                               'Rhythm Master', 'SSS Collector'])


    def test_pity_time_triggers_on_150th_consecutive_miss(self):
        class MissRng:
            def choice(self, _values):
                return 72.224
        session = PachinkoSession(rng=MissRng())
        for _ in range(149):
            event = session.normal_spin([72.224])
            self.assertEqual(event["type"], "miss")
        event = session.normal_spin([72.224])
        self.assertEqual(event["type"], "pity_time")
        self.assertEqual(event["spins"], 150)
        self.assertIsNone(session.initial_overall)
        self.assertEqual(session.initial_payout, 0)
        self.assertTrue(session.time_mode)
        self.assertEqual(session.last_event['type'], 'pity_time')
        self.assertEqual(session.notes, 0)
        self.assertEqual(session.payout_counts[6000], 0)
        self.assertFalse(session.in_rush)
        self.assertEqual(session.st_remaining, 0)

    def test_rush_payout_distribution_and_expected_value(self):
        self.assertEqual(PAYOUT_WEIGHTS, ((300, 200), (1500, 500), (3000, 150), (4500, 100), (6000, 50)))
        self.assertEqual(sum(w for _, w in PAYOUT_WEIGHTS), 1000)
        self.assertEqual(expected_values()["rush_hit_notes"], 2010)

    def test_new_rank_boundaries_are_exact(self):
        for minimum, rank in RANK_THRESHOLDS:
            self.assertEqual(get_pachinko_rank(minimum), rank)
            if minimum > 300:
                self.assertNotEqual(get_pachinko_rank(minimum - 1), rank)

    def test_st_is_116_plus_up_to_four_stored_reserve_holds(self):
        from pachinko import RESERVE_HOLDS, TOTAL_RUSH_DRAWS
        self.assertEqual((ST_MAX, RESERVE_HOLDS, TOTAL_RUSH_DRAWS), (116, 4, 120))
        session = PachinkoSession()
        session.in_rush = True
        session.st_remaining = 1
        session.segment_spins = 115
        session.holds = ["blue", "green", "red", "gold", "rainbow"]
        # The fifth pending item cannot exist at this point: only four reserve slots remain.
        self.assertFalse(session.add_hold())

    def test_reserve_holds_are_consumed_after_116_main_spins(self):
        session = PachinkoSession()
        session.in_rush = True
        session.st_remaining = 1
        session.segment_spins = 115
        session.holds = ["blue", "green", "red", "gold"]
        with patch("pachinko.upgrade_hold_color", side_effect=lambda color, rng: (color, False)), \
             patch("pachinko.hold_hits", return_value=False):
            event = session.consume_hold()
            self.assertEqual(event["type"], "rush_miss")
            self.assertEqual(session.st_remaining, 0)
            self.assertEqual(session.reserve_spins, 0)
            self.assertFalse(session.add_hold())
            for _ in range(2):
                event = session.consume_hold()
                self.assertEqual(event["type"], "rush_miss")
            event = session.consume_hold()
        self.assertEqual(event["type"], "rush_end")
        self.assertEqual(session.rush_spins, 4)
        self.assertTrue(session.ended)

if __name__ == '__main__': unittest.main()
