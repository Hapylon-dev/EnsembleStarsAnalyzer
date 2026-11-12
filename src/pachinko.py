"""OVERALL PACHINKO game rules and expected-value calculations."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import csv
import random

ST_MAX = 116
RESERVE_HOLDS = 4
TOTAL_RUSH_DRAWS = ST_MAX + RESERVE_HOLDS
RUSH_HIT_PROBABILITY = 1 / 73
PITY_SPINS = 150
PITY_PAYOUT = 6000
INITIAL_HIT_PROBABILITY = 1 / 34.6
PITY_PROBABILITY = (1 - INITIAL_HIT_PROBABILITY) ** PITY_SPINS
MAX_HOLDS = 5
RANKING_CSV = Path(__file__).resolve().parent.parent / "output" / "ranking_batch_results.csv"
# Target distribution AFTER the 1/50 one-step upgrade is applied.
COLOR_WEIGHTS = (("blue", 9000), ("green", 900), ("red", 90), ("gold", 9), ("rainbow", 1))
# Reverse-calibrated base distribution. A non-rainbow hold upgrades exactly
# one tier with probability 1/50; the resulting final distribution is exactly
# 90% / 9% / 0.9% / 0.09% / 0.01% (within floating-point precision).
BASE_COLOR_WEIGHTS = (
    ("blue", 1058841000), ("green", 84275100), ("red", 8868510),
    ("gold", 877851), ("rainbow", 97739),
)
# Conditional hit rates yield a weighted overall chance of exactly 1/73.
COLOR_HIT_RATES = {
    "blue": (1 / 73 - 0.09 * 0.03 - 0.009 * 0.60 - 0.0009 * 0.85 - 0.0001) / 0.90,
    "green": 0.03, "red": 0.60, "gold": 0.85, "rainbow": 1.0,
}
# Provisional total trigger rates for special RUSH presentation cues.
# The browser derives hit/miss conditional cue rates so P(hit | cue) remains 40%.
SPECIAL_EVENT_RATES = {"blue": 0.013, "green": 0.074, "red": 0.09, "gold": 0.115}
PAYOUT_WEIGHTS = ((300, 200), (1500, 500), (3000, 150), (4500, 100), (6000, 50))
INITIAL_PAYOUT_WEIGHTS = ((300, 14), (1500, 29), (3000, 8), (4500, 1))


def load_overall_values(csv_path: Path | str = RANKING_CSV) -> list[float]:
    with Path(csv_path).open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    values = [float(row["overall_score"]) for row in rows if row.get("status") == "OK"]
    if len(values) != 1799:
        raise ValueError(f"固定ランキングデータは1,799件必要です（{len(values)}件）")
    return values


def decimal_triple(value: float) -> str | None:
    digits = f"{float(value):.3f}".split(".")[1]
    return digits if len(digits) == 3 and len(set(digits)) == 1 else None


def initial_payout(triple: str) -> int:
    if triple == "000":
        return 1500
    digit = int(triple[0])
    if digit == 7:
        return 4500
    if digit % 2 == 0:
        return 300
    return 3000


def _weighted_choice(items, rng: random.Random):
    total = sum(weight for _, weight in items)
    point = rng.randrange(total)
    for value, weight in items:
        if point < weight:
            return value
        point -= weight
    raise RuntimeError("weighted choice failed")


def draw_hold_color(rng: random.Random) -> str:
    return _weighted_choice(BASE_COLOR_WEIGHTS, rng)


def upgrade_hold_color(color: str, rng: random.Random) -> tuple[str, bool]:
    if color == "rainbow" or rng.randrange(50) != 0:
        return color, False
    order = ("blue", "green", "red", "gold", "rainbow")
    return order[order.index(color) + 1], True


def hold_hits(color: str, rng: random.Random) -> bool:
    return rng.random() < COLOR_HIT_RATES[color]


def draw_rush_payout(rng: random.Random) -> int:
    return _weighted_choice(PAYOUT_WEIGHTS, rng)


def expected_values() -> dict:
    initial_ev = sum(amount * count for amount, count in INITIAL_PAYOUT_WEIGHTS) / 52
    rush_payout_ev = sum(amount * weight for amount, weight in PAYOUT_WEIGHTS) / 1000
    miss_run_probability = (72 / 73) ** TOTAL_RUSH_DRAWS
    continuation = 1 - miss_run_probability
    expected_rush_hits = continuation / miss_run_probability
    expected_rush_spins = 73 * expected_rush_hits
    rush_ev = expected_rush_hits * rush_payout_ev
    initial_ev_with_pity = (1 - PITY_PROBABILITY) * initial_ev + PITY_PROBABILITY * PITY_PAYOUT
    return {
        "normal_initial_notes": initial_ev,
        "initial_notes": initial_ev_with_pity,
        "pity_probability": PITY_PROBABILITY,
        "rush_hit_notes": rush_payout_ev,
        "rush_hits": expected_rush_hits,
        "rush_spins": expected_rush_spins,
        "rush_notes": rush_ev,
        "total_notes": initial_ev_with_pity + rush_ev,
        "segment_continuation": continuation,
        "color_hit_probability": sum(w / 1000 * COLOR_HIT_RATES[c] for c, w in COLOR_WEIGHTS),
    }


@dataclass
class PachinkoSession:
    rng: random.Random = field(default_factory=random.Random)
    notes: int = 0
    initial_overall: float | None = None
    initial_triple: str | None = None
    is_pity_time: bool = False
    initial_payout: int = 0
    initial_spins: int = 0
    in_rush: bool = False
    st_remaining: int = 0
    holds: list[str] = field(default_factory=list)
    combo: int = 0
    max_combo: int = 0
    rush_hits: int = 0
    rush_notes: int = 0
    rush_spins: int = 0
    segment_spins: int = 0
    reserve_spins: int = 0
    payout_counts: dict[int, int] = field(default_factory=lambda: {6000: 0, 4500: 0, 3000: 0, 1500: 0, 300: 0})
    ended: bool = False
    started_at: str = field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds"))
    last_event: dict = field(default_factory=dict)

    def normal_spin(self, overall_values: list[float]) -> dict:
        if self.in_rush or self.ended:
            raise RuntimeError("RUSH中または終了後は通常抽選できません")
        if not overall_values:
            raise ValueError("OVERALLデータが空です")
        self.initial_spins += 1
        value = self.rng.choice(overall_values)
        triple = decimal_triple(value)
        if not triple:
            if self.initial_spins < PITY_SPINS:
                self.last_event = {"type": "miss", "overall": value, "spins": self.initial_spins}
                return self.last_event.copy()
            self.is_pity_time = True
            self.initial_overall = None
            self.initial_triple = None
            self.initial_payout = PITY_PAYOUT
            self.notes += PITY_PAYOUT
            self.payout_counts[PITY_PAYOUT] += 1
            self.in_rush = True
            self.st_remaining = ST_MAX
            self.segment_spins = 0
            self.reserve_spins = 0
            self.last_event = {
                "type": "pity_time", "overall": None, "spins": self.initial_spins,
                "category": "PITY TIME", "payout": PITY_PAYOUT,
            }
            return self.last_event.copy()
        self.initial_overall = value
        self.initial_triple = triple
        self.initial_payout = initial_payout(triple)
        self.notes += self.initial_payout
        self.payout_counts[self.initial_payout] += 1
        self.in_rush = True
        self.st_remaining = ST_MAX
        self.segment_spins = 0
        self.reserve_spins = 0
        self.last_event = {"type": "initial_jackpot", "overall": value, "triple": triple,
                           "payout": self.initial_payout, "spins": self.initial_spins,
                           "category": self._category(triple)}
        return self.last_event.copy()

    @staticmethod
    def _category(triple: str) -> str:
        if triple == "000": return "ZERO JACKPOT"
        if triple[0] == "7": return "SEVEN JACKPOT"
        return "EVEN JACKPOT" if int(triple[0]) % 2 == 0 else "ODD JACKPOT"

    def add_hold(self) -> bool:
        if (not self.in_rush or self.ended or self.st_remaining <= 0
                or len(self.holds) >= MAX_HOLDS
                or self.segment_spins + len(self.holds) >= TOTAL_RUSH_DRAWS):
            return False
        self.holds.append(draw_hold_color(self.rng))
        return True

    def consume_hold(self) -> dict:
        if not self.in_rush or self.ended or not self.holds:
            return {"type": "idle"}
        base_color = self.holds.pop(0)
        color, upgrade_flash = upgrade_hold_color(base_color, self.rng)
        if self.st_remaining > 0:
            self.st_remaining -= 1
            self.segment_spins += 1
        else:
            # The four already-stored holds are the final reserve draws.
            self.reserve_spins += 1
        self.rush_spins += 1
        if hold_hits(color, self.rng):
            payout = draw_rush_payout(self.rng)
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            self.rush_hits += 1
            self.rush_notes += payout
            self.notes += payout
            self.payout_counts[payout] += 1
            # Keep the unconsumed holds: they carry into the next RUSH segment.
            self.st_remaining = ST_MAX
            self.segment_spins = 0
            self.reserve_spins = 0
            self.last_event = {"type": "rush_jackpot", "color": color, "upgrade_flash": upgrade_flash,
                               "payout": payout, "combo": self.combo, "st_remaining": ST_MAX}
        elif self.st_remaining <= 0 and (self.reserve_spins >= RESERVE_HOLDS or not self.holds):
            self.holds.clear(); self.in_rush = False; self.ended = True
            self.last_event = {"type": "rush_end", "color": color, "upgrade_flash": upgrade_flash, "st_remaining": 0}
        else:
            self.last_event = {"type": "rush_miss", "color": color, "upgrade_flash": upgrade_flash,
                               "st_remaining": self.st_remaining, "reserve_spins": self.reserve_spins}
        return self.last_event.copy()

    def result(self) -> dict:
        if not self.ended:
            raise RuntimeError("ゲーム終了前の結果は確定できません")
        return {"initial_overall": self.initial_overall, "initial_spins": self.initial_spins,
                "initial_triple": self.initial_triple, "initial_payout": self.initial_payout,
                "rush_hits": self.rush_hits, "max_combo": self.max_combo, "rush_notes": self.rush_notes,
                "total_notes": self.notes, "payout_counts": self.payout_counts.copy(),
                "rush_spins": self.rush_spins, "played_at": self.started_at,
                "initial_type": "PITY TIME" if self.is_pity_time else "NORMAL"}
