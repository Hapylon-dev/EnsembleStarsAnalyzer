"""
estimate.py
Version : 1.0 Final Edition

Tap Timing Estimator

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from typing import List

import config

from models import (
    BarData,
    EstimateResult,
)


# ==========================================================
# Estimate
# ==========================================================

class Estimate:
    """
    タップタイミング推定
    """

    def __init__(self):

        pass

    # ======================================================
    # Normalize Height
    # ======================================================

    def normalize_height(
        self,
        bars: List[BarData]
    ) -> List[float]:
        """
        棒高さを最大値=1.0へ正規化
        """

        if len(bars) == 0:
            return []

        max_height = max(
            bar.height
            for bar in bars
        )

        if max_height <= 0:
            return [
                0.0
                for _ in bars
            ]

        normalized = []

        for bar in bars:

            normalized.append(
                bar.height / max_height
            )

        return normalized


    # ======================================================
    # Calculate Ratio
    # ======================================================

    def calculate_ratio(
        self,
        normalized: List[float]
    ) -> List[float]:
        """
        高さ割合を計算

        合計 = 1.0
        """

        if len(normalized) == 0:
            return []

        total = sum(normalized)

        if total <= 0:

            return [
                0.0
                for _ in normalized
            ]

        ratios = []

        for value in normalized:

            ratios.append(
                value / total
            )

        return ratios


    # ======================================================
    # Estimate Notes
    # ======================================================

    def estimate_notes(
        self,
        ratios: List[float],
        total_notes: int
    ) -> List[int]:
        """
        割合から推定ノーツ数を計算

        四捨五入前
        """

        estimated = []

        for ratio in ratios:

            estimated.append(
                ratio * total_notes
            )

        return estimated
    # ======================================================
    # Round Notes
    # ======================================================

    def round_notes(
        self,
        estimated: List[float]
    ) -> List[int]:
        """
        推定ノーツ数を四捨五入
        """

        rounded = []

        for value in estimated:

            rounded.append(
                int(round(value))
            )

        return rounded


    # ======================================================
    # Adjust Total
    # ======================================================

    def adjust_total(
        self,
        notes: List[int],
        total_notes: int
    ) -> List[int]:
        """
        合計ノーツ数を補正

        四捨五入による誤差を補正する
        """

        if len(notes) == 0:
            return notes

        diff = total_notes - sum(notes)

        if diff == 0:
            return notes

        # 最大値の棒へ補正
        index = notes.index(max(notes))

        notes[index] += diff

        return notes


    # ======================================================
    # Create Result
    # ======================================================

    def create_result(
        self,
        bars: List[BarData],
        total_notes: int
    ) -> EstimateResult:
        """
        EstimateResult生成
        """

        normalized = self.normalize_height(
            bars
        )

        if config.DEBUG_MODE:

            print()
            print("Normalized Height")

            for i, value in enumerate(normalized):

                print(
                    f"[{i}] {value:.4f}"
                )

        ratios = self.calculate_ratio(
            normalized
        )

        if config.DEBUG_MODE:

            print()
            print("Height Ratio")

            for i, value in enumerate(ratios):

                print(
                    f"[{i}] {value:.4f}"
                )

        estimated = self.estimate_notes(
            ratios,
            total_notes
        )

        if config.DEBUG_MODE:

            print()
            print("Estimated Notes (float)")

            for i, value in enumerate(estimated):

                print(
                    f"[{i}] {value:.2f}"
                )

        estimated = self.round_notes(
            estimated
        )

        estimated = self.adjust_total(
            estimated,
            total_notes
        )

        result = EstimateResult()

        if len(bars) > 0:

            result.max_height = max(
                bar.height
                for bar in bars
            )

        result.height_ratio = ratios

        result.estimated_notes = estimated

        return result
    # ======================================================
    # Distribution
    # ======================================================

    def create_distribution(
        self,
        bars: List[BarData],
        estimated: List[int]
    ) -> dict[str, int]:
        """
        検出されたバーの位置分類に基づいて、
        推定ノーツ数を判定区分へ割り当てる。

        Version 1.3:
        SLOW   -> AMAZING(SLOW)
        CENTER -> AMAZING+
        FAST   -> AMAZING(FAST)
        """

        distribution: dict[str, int] = {}

        if len(bars) == 0:
            return distribution

        if len(bars) != len(estimated):
            raise ValueError(
                "バー数と推定ノーツ数が一致しません。"
                f"bars={len(bars)}, "
                f"estimated={len(estimated)}"
            )

        label_map = {
            "SLOW": "AMAZING(SLOW)",
            "CENTER": "AMAZING+",
            "FAST": "AMAZING(FAST)",
        }

        for bar, value in zip(
            bars,
            estimated
        ):

            label = label_map.get(
                bar.side
            )

            if label is None:
                raise ValueError(
                    "バー位置を判定できませんでした。"
                    f"side={bar.side!r}"
                )

            distribution[label] = value

        return distribution


    # ======================================================
    # Estimate
    # ======================================================

    def estimate(
        self,
        bars: List[BarData],
        total_notes: int
    ) -> EstimateResult:
        """
        推定処理
        """

        if config.DEBUG_MODE:

            print("=" * 60)
            print("Estimate")
            print("=" * 60)

            print(f"Bars : {len(bars)}")

            for bar in bars:

                print(
                    f"x={bar.x} "
                    f"h={bar.height} "
                    f"{bar.side}"
                )

        result = self.create_result(
            bars,
            total_notes
        )

        distribution = self.create_distribution(
            bars,
            result.estimated_notes
        )

        result.distribution = distribution

        # Amazing+
        result.amazing_plus = distribution.get(
            "AMAZING+",
            0
        )

        # Amazing Slow
        result.amazing_slow = distribution.get(
            "AMAZING(SLOW)",
            0
        )

        # Amazing Fast
        result.amazing_fast = distribution.get(
            "AMAZING(FAST)",
            0
        )

        # Perfect Slow
        result.perfect_slow = distribution.get(
            "PERFECT(SLOW)",
            0
        )

        # Perfect Fast
        result.perfect_fast = distribution.get(
            "PERFECT(FAST)",
            0
        )

        # Amazing (Slow + Fast)
        result.amazing = (
            result.amazing_slow
            + result.amazing_fast
        )
        
        # Perfect (Slow + Fast)
        result.perfect = (
            result.perfect_slow
            + result.perfect_fast
        )

        # Slow Total
        result.slow = (
            result.amazing_slow
            + result.perfect_slow
        )

        # Fast Total
        result.fast = (
            result.amazing_fast
            + result.perfect_fast
        )

        # --------------------------------------------------
        # Balance Availability
        # --------------------------------------------------
        # BalanceはSLOW / FAST両側のバーを
        # 実際に検出できた場合のみ評価する。
        #
        # 値が0かどうかではなく、
        # バーが存在したかどうかで判定する。

        detected_sides = {
            bar.side
            for bar in bars
        }

        result.balance_available = (
            "SLOW" in detected_sides
            and "FAST" in detected_sides
        )

        # 推定精度（Version 1.0では仮に100%）
        result.estimated_accuracy = 100.0

        return result
    

# ======================================================
# Utility
# ======================================================

_estimator = Estimate()


def estimate(
    bars: List[BarData],
    total_notes: int
) -> EstimateResult:
    """
    Estimate簡易呼び出し
    """
    return _estimator.estimate(
        bars,
        total_notes
    )