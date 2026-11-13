from __future__ import annotations

import csv
import gzip
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pachinko_simulation import run_simulation, PITY_SPINS


class PachinkoSimulationTests(unittest.TestCase):
    def test_small_reproducible_simulation_exports_consistent_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_simulation(
                trials=5000,
                seed=20261111,
                dataset_path=ROOT / "output" / "ranking_batch_results.csv",
                output_dir=temp_dir,
            )
            self.assertEqual(result["count"], 5000)
            self.assertEqual(result["seed"], 20261111)
            self.assertEqual(sum(result["rank_counts"].values()), 5000)
            self.assertEqual(sum(x["count"] for x in result["rush_hit_count_distribution"]), 5000)
            self.assertEqual(sum(x["count"] for x in result["rush_notes_distribution"]), 5000)
            self.assertEqual(sum(x["count"] for x in result["total_notes_distribution"]), 5000)
            self.assertEqual(sum(result["rush_payout_counts"].values()), sum(
                x["rush_hits"] * x["count"] for x in result["rush_hit_count_distribution"]
            ))
            self.assertAlmostEqual(sum(x["percentage"] for x in result["histogram"]), 100.0, places=9)
            self.assertGreaterEqual(result["simulated_pity_count"], 0)
            self.assertLessEqual(result["simulated_pity_count"], 5000)
            self.assertEqual(result["pity_spins"], 150)
            self.assertIn("theoretical_pity_percentage", result)
            self.assertAlmostEqual(result["theoretical_time_rush_entry_percentage"], 97.8556871186, places=6)

            csv_path = Path(temp_dir) / "pachinko_simulation_1m.csv.gz"
            with gzip.open(csv_path, "rt", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 5000)
            pity_rows = [row for row in rows if row["initial_type"] == "PITY TIME"]
            self.assertTrue(all(row["initial_overall"] == "" for row in pity_rows))
            self.assertTrue(all(int(row["initial_spins"]) >= PITY_SPINS for row in pity_rows))
            self.assertTrue(all(int(row["initial_payout_notes"]) == 6000 for row in pity_rows))

            saved = json.loads((Path(temp_dir) / "pachinko_simulation_1m_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["count"], 5000)
            self.assertIn("files", saved)


if __name__ == "__main__":
    unittest.main()
