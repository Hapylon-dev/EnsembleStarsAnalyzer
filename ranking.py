"""Ranking calculation utilities for EnsembleStarsAnalyzer Version 1.3."""
from __future__ import annotations

import csv
from bisect import bisect_right
from pathlib import Path

RANKING_BASE_COUNT = 1799
RANKING_BASE_DATE = "2026-08-25"
RANKING_PAGE_SIZE = 50
RANKING_PAGE_COUNT = 36

# 上位率の小さい順。説明画面にもこの値をそのまま使用する。
RANKING_TITLE_THRESHOLDS = (
    (5.0, "🌈", "レインボーランカー"),
    (10.0, "💎", "ダイヤモンドランカー"),
    (15.0, "🤍", "プラチナランカー"),
    (20.0, "💛", "ゴールドランカー"),
    (25.0, "🩶", "シルバーランカー"),
    (30.0, "🤎", "ブロンズランカー"),
    (50.0, "🟣", "パープルランカー"),
    (60.0, "🔴", "レッドランカー"),
    (70.0, "🟠", "オレンジランカー"),
    (80.0, "🟢", "グリーンランカー"),
    (90.0, "🔵", "ブルーランカー"),
    (100.0, "⚪", "ホワイトランカー"),
)


def _default_csv_path() -> Path:
    root = Path(__file__).resolve().parent
    candidates = (
        root / "output" / "ranking_batch_results.csv",
        root / "data" / "ranking" / "ranking_batch_results.csv",
    )
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def load_ranking_base(csv_path: str | Path | None = None) -> list[dict]:
    """Load the fixed 1,799-result ranking base without modifying it."""
    path = Path(csv_path) if csv_path is not None else _default_csv_path()
    if not path.exists():
        raise FileNotFoundError(
            f"ランキング基準データが見つかりません: {path}"
        )

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    rows = [row for row in rows if row.get("status") == "OK"]
    if len(rows) != RANKING_BASE_COUNT:
        raise ValueError(
            "ランキング基準データの件数が仕様と一致しません: "
            f"{len(rows)}件（期待値 {RANKING_BASE_COUNT}件）"
        )

    # ranking_position が付与済みなら、その順序を正式な基準順として使用。
    # 念のため未付与でも Overall 降順 + 元の行順で再構築する。
    if all(str(row.get("ranking_position", "")).isdigit() for row in rows):
        rows.sort(key=lambda row: int(row["ranking_position"]))
    else:
        rows.sort(key=lambda row: float(row["overall_score"]), reverse=True)

    return rows


def calculate_ranking(overall_score: float, base_rows: list[dict]) -> dict:
    """Compare one new analysis result with the fixed 1,799-result base."""
    if len(base_rows) != RANKING_BASE_COUNT:
        raise ValueError(
            f"ランキング基準データは{RANKING_BASE_COUNT}件必要です。"
        )

    score = float(overall_score)

    # 同一Overallは既存基準データを先にする。
    # したがって、現在の解析結果は「高いOverallの件数 + 同点件数 + 1位」。
    higher_count = sum(float(row["overall_score"]) > score for row in base_rows)
    equal_count = sum(float(row["overall_score"]) == score for row in base_rows)
    position = higher_count + equal_count + 1

    comparison_total = RANKING_BASE_COUNT + 1
    top_percent = position / comparison_total * 100.0

    title_emoji = "⚪"
    title_name = "ホワイトランカー"
    for threshold, emoji, name in RANKING_TITLE_THRESHOLDS:
        if top_percent <= threshold:
            title_emoji = emoji
            title_name = name
            break

    return {
        "ranking_position": position,
        "comparison_total": comparison_total,
        "ranking_top_percent": top_percent,
        "ranking_title_emoji": title_emoji,
        "ranking_title": title_name,
        "ranking_base_count": RANKING_BASE_COUNT,
        "ranking_base_date": RANKING_BASE_DATE,
    }

def build_rank_distribution(base_rows: list[dict]) -> dict[str, int]:
    """Build the fixed 1,799-result Overall rank distribution."""

    if len(base_rows) != RANKING_BASE_COUNT:
        raise ValueError(
            f"ランキング基準データは{RANKING_BASE_COUNT}件必要です。"
        )

    distribution: dict[str, int] = {}

    for row in base_rows:
        rank = str(row.get("rank", "")).strip()

        if not rank:
            continue

        distribution[rank] = distribution.get(rank, 0) + 1

    return distribution
