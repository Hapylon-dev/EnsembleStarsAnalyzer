"""Reproducible OVERALL PACHINKO Monte Carlo simulation."""
from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path
from typing import Any

import numpy as np

from pachinko_rank import RANK_THRESHOLDS, get_pachinko_rank

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = PROJECT_ROOT / "output" / "ranking_batch_results.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "simulation"
TRIALS = 1_000_000
DEFAULT_SEED = 20261111
PITY_SPINS = 150
INITIAL_HIT_PROBABILITY = 1 / 34.6
RUSH_HIT_PROBABILITY = 1 / 73
# Aggregate simulation horizon: 116 main ST spins + up to 4 reserve draws.
RUSH_ST = 120
INITIAL_PAYOUT_WEIGHTS = ((300, 14), (1500, 29), (3000, 8), (4500, 1))
RUSH_PAYOUT_WEIGHTS = ((300, 20), (1500, 50), (3000, 15), (4500, 10), (6000, 5))


def _load_jackpot_values(path: Path) -> list[tuple[float, int]]:
    values: list[tuple[float, int]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("status") != "OK":
                continue
            value = float(row["overall_score"])
            triple = f"{value:.3f}".split(".")[1]
            if len(triple) == 3 and len(set(triple)) == 1:
                digit = int(triple[0])
                payout = 1500 if triple == "000" else 4500 if digit == 7 else 300 if digit % 2 == 0 else 3000
                values.append((value, payout))
    if len(values) != 52:
        raise ValueError(f"初当たりデータは52件必要です（{len(values)}件）")
    return values


def run_simulation(
    trials: int = TRIALS,
    seed: int = DEFAULT_SEED,
    dataset_path: str | Path = DEFAULT_DATASET,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
) -> dict[str, Any]:
    """Run a deterministic simulation matching the app's 1,799-value initial draw pool.

    Initial jackpots are sampled from the 52 matching OVERALL values in the fixed
    source dataset. A 150th consecutive miss becomes Pity Time. Each RUSH segment
    ends at the first hit within 120 spins or after 120 misses; a hit resets ST.
    """
    if int(trials) <= 0:
        raise ValueError("試行件数は1以上にしてください")
    trials = int(trials)
    seed = int(seed)
    rng = np.random.default_rng(seed)

    jackpots = _load_jackpot_values(Path(dataset_path))
    jackpot_values = np.asarray([item[0] for item in jackpots], dtype=np.float64)
    jackpot_payouts = np.asarray([item[1] for item in jackpots], dtype=np.int64)

    # Match the actual browser game: one draw from the fixed 1,799-value pool per spin.
    initial_probability = len(jackpots) / 1799
    first_hit_spins = rng.geometric(initial_probability, size=trials)
    pity_mask = first_hit_spins > PITY_SPINS
    initial_spins = np.minimum(first_hit_spins, PITY_SPINS).astype(np.int16)
    initial_type = np.where(pity_mask, "PITY TIME", "NORMAL")
    initial_overall = np.full(trials, np.nan, dtype=np.float64)
    initial_payout = np.full(trials, 6000, dtype=np.int64)

    normal_indices = np.flatnonzero(~pity_mask)
    selected_jackpots = rng.integers(0, len(jackpots), size=len(normal_indices))
    initial_overall[normal_indices] = jackpot_values[selected_jackpots]
    initial_payout[normal_indices] = jackpot_payouts[selected_jackpots]

    rush_hits = np.zeros(trials, dtype=np.int16)
    rush_notes = np.zeros(trials, dtype=np.int64)
    rush_spins = np.zeros(trials, dtype=np.int32)
    rush_payout_counts = {str(value): 0 for value, _ in RUSH_PAYOUT_WEIGHTS}
    active = np.ones(trials, dtype=bool)
    rush_amounts = np.asarray([v for v, _ in RUSH_PAYOUT_WEIGHTS], dtype=np.int64)
    rush_probabilities = np.asarray([w for _, w in RUSH_PAYOUT_WEIGHTS], dtype=np.float64) / 100.0

    # Geometric waiting times avoid simulating every miss while preserving exact ST semantics.
    while active.any():
        indices = np.flatnonzero(active)
        waits = rng.geometric(RUSH_HIT_PROBABILITY, size=len(indices))
        spins_used = np.minimum(waits, RUSH_ST)
        rush_spins[indices] += spins_used
        hit_mask = waits <= RUSH_ST
        hit_indices = indices[hit_mask]
        if hit_indices.size:
            payouts = rng.choice(rush_amounts, size=hit_indices.size, p=rush_probabilities)
            rush_hits[hit_indices] += 1
            rush_notes[hit_indices] += payouts
            unique_payouts, unique_counts = np.unique(payouts, return_counts=True)
            for payout, payout_count in zip(unique_payouts, unique_counts):
                rush_payout_counts[str(int(payout))] += int(payout_count)
        active[indices[~hit_mask]] = False

    total_notes = initial_payout + rush_notes
    rank_names = [get_pachinko_rank(int(value)) for value in total_notes]
    rank_order = [rank for _, rank in RANK_THRESHOLDS]
    rank_counts = {rank: int(rank_names.count(rank)) for rank in rank_order}
    payout_values, payout_counts = np.unique(initial_payout, return_counts=True)
    pity_count = int(pity_mask.sum())
    normal_count = trials - pity_count

    p_theory = (1 - INITIAL_HIT_PROBABILITY) ** PITY_SPINS
    normal_initial_ev = sum(v * w for v, w in INITIAL_PAYOUT_WEIGHTS) / sum(w for _, w in INITIAL_PAYOUT_WEIGHTS)
    rush_continuation = 1 - (1 - RUSH_HIT_PROBABILITY) ** RUSH_ST
    rush_hits_ev = rush_continuation / (1 - rush_continuation)
    rush_payout_ev = sum(v * w for v, w in RUSH_PAYOUT_WEIGHTS) / 100
    rush_notes_ev = rush_hits_ev * rush_payout_ev
    initial_notes_ev = (1 - p_theory) * normal_initial_ev + p_theory * 6000

    histogram = [
        {"rank": rank, "count": rank_counts[rank], "percentage": rank_counts[rank] / trials * 100}
        for rank in rank_order
    ]
    rush_hit_values, rush_hit_counts = np.unique(rush_hits, return_counts=True)
    rush_note_values, rush_note_counts = np.unique(rush_notes, return_counts=True)
    total_note_values, total_note_counts = np.unique(total_notes, return_counts=True)
    summary: dict[str, Any] = {
        "count": trials,
        "seed": seed,
        "initial_draw_pool_count": 1799,
        "initial_jackpot_pool_count": len(jackpots),
        "initial_hit_probability_actual": initial_probability,
        "initial_hit_probability_display": INITIAL_HIT_PROBABILITY,
        "pity_spins": PITY_SPINS,
        "theoretical_pity_percentage": p_theory * 100,
        "simulated_pity_count": pity_count,
        "simulated_pity_percentage": pity_count / trials * 100,
        "normal_initial_count": normal_count,
        "normal_initial_percentage": normal_count / trials * 100,
        "initial_payout_counts": {str(int(k)): int(v) for k, v in zip(payout_values, payout_counts)},
        "rush_payout_distribution_percent": {str(v): w for v, w in RUSH_PAYOUT_WEIGHTS},
        "rush_payout_counts": rush_payout_counts,
        "rush_hit_count_distribution": [
            {"rush_hits": int(v), "count": int(c), "percentage": float(c) / trials * 100}
            for v, c in zip(rush_hit_values, rush_hit_counts)
        ],
        "rush_notes_distribution": [
            {"rush_notes": int(v), "count": int(c), "percentage": float(c) / trials * 100}
            for v, c in zip(rush_note_values, rush_note_counts)
        ],
        "total_notes_distribution": [
            {"total_notes": int(v), "count": int(c), "percentage": float(c) / trials * 100}
            for v, c in zip(total_note_values, total_note_counts)
        ],
        "average_initial_notes_theoretical": initial_notes_ev,
        "average_initial_notes_simulated": float(initial_payout.mean()),
        "average_rush_hits_theoretical": rush_hits_ev,
        "average_rush_hits_simulated": float(rush_hits.mean()),
        "average_rush_notes_theoretical": rush_notes_ev,
        "average_rush_notes_simulated": float(rush_notes.mean()),
        "average_total_notes_theoretical": initial_notes_ev + rush_notes_ev,
        "average_total_notes_simulated": float(total_notes.mean()),
        "average_rush_spins_simulated": float(rush_spins.mean()),
        "rank_counts": rank_counts,
        "histogram": histogram,
        "max_total_notes": int(total_notes.max()),
        "rank_thresholds": [{"rank": rank, "minimum_notes": minimum} for minimum, rank in RANK_THRESHOLDS],
        "simulation_method": "fixed 1,799-value OVERALL pool; 150 consecutive misses trigger Pity Time; RUSH 1/73 with 116 main ST spins + up to 4 reserve draws (max 120)",
    }

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "pachinko_simulation_1m.csv.gz"
    summary_path = output / "pachinko_simulation_1m_summary.json"
    hist_path = output / "pachinko_rank_histogram_1m.csv"

    with gzip.open(csv_path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "case_id", "initial_type", "initial_spins", "initial_overall",
            "initial_payout_notes", "rush_hits", "rush_payout_notes",
            "rush_spins", "total_notes", "rank",
        ])
        for index in range(trials):
            overall = "" if np.isnan(initial_overall[index]) else f"{initial_overall[index]:.3f}"
            writer.writerow([
                index + 1, initial_type[index], int(initial_spins[index]), overall,
                int(initial_payout[index]), int(rush_hits[index]), int(rush_notes[index]),
                int(rush_spins[index]), int(total_notes[index]), rank_names[index],
            ])

    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with hist_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["RANK", "件数", "割合(%)"])
        for item in histogram:
            writer.writerow([item["rank"], item["count"], f'{item["percentage"]:.4f}'])

    summary["files"] = {
        "individual_trials": csv_path.name,
        "summary": summary_path.name,
        "histogram": hist_path.name,
    }
    # Rewrite summary after adding output filenames.
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def load_simulation_summary(path: str | Path | None = None) -> dict[str, Any] | None:
    summary_path = Path(path) if path else DEFAULT_OUTPUT_DIR / "pachinko_simulation_1m_summary.json"
    if not summary_path.exists():
        return None
    return json.loads(summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    report = run_simulation()
    print(json.dumps({
        "count": report["count"],
        "seed": report["seed"],
        "simulated_pity_count": report["simulated_pity_count"],
        "simulated_pity_percentage": report["simulated_pity_percentage"],
        "average_total_notes_simulated": report["average_total_notes_simulated"],
    }, ensure_ascii=False, indent=2))
