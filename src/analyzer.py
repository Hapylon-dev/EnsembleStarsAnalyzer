"""
analyzer.py
Version : 1.0 Final Edition

Tap Timing Analyzer

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np

import config
import graph

from detector import Detector
from estimate import Estimate
from models import EstimateResult


# ==========================================================
# Analyzer
# ==========================================================

class Analyzer:
    """
    タップタイミング解析
    """

    def __init__(self):

        self.detector = Detector()

        self.estimator = Estimate()

    # ======================================================
    # Graph Resolution Validation
    # ======================================================

    def validate_graph_resolution(
        self,
        graph_image: np.ndarray
    ) -> None:
        """
        YOLOで切り出したグラフ領域が、
        解析に必要な最低解像度を満たしているか確認する。
        """

        if graph_image is None or graph_image.size == 0:
            raise ValueError(
                "グラフ画像を取得できませんでした。"
            )

        graph_height, graph_width = graph_image.shape[:2]

        if (
            graph_width < config.MIN_GRAPH_WIDTH
            or graph_height < config.MIN_GRAPH_HEIGHT
        ):
            raise ValueError(
                "画像の解像度が低すぎるため、"
                "タイミンググラフを正確に解析できません。"
                "より高解像度のリザルト画像を使用してください。 "
                f"(検出グラフ: {graph_width}x{graph_height}, "
                f"必要最低: {config.MIN_GRAPH_WIDTH}x"
                f"{config.MIN_GRAPH_HEIGHT})"
            )

    # ======================================================
    # Analyze
    # ======================================================

    def analyze(
        self,
        image_path: str,
        total_notes: int,
        return_graph: bool = False,
    ) -> EstimateResult | tuple[EstimateResult, np.ndarray]:
   
        """
        タップタイミング解析
        """

        # --------------------------------------------------
        # Graph Extraction
        # --------------------------------------------------

        graph_image = graph.create_graph(
            image_path
        )

        # --------------------------------------------------
        # Graph Resolution Validation
        # --------------------------------------------------

        self.validate_graph_resolution(
            graph_image
        )

        # --------------------------------------------------
        # Detect
        # --------------------------------------------------

        bars = self.detector.detect(
            graph_image
        )

        # --------------------------------------------------
        # Bar Count Validation
        # --------------------------------------------------

        bar_count = len(bars)

        if not 1 <= bar_count <= 3:
            raise ValueError(
                "タップタイミングバーを正しく検出できませんでした。"
                f"解析対象は1～3本ですが、"
                f"{bar_count}本検出されました。"
                "別のリザルト画像を使用してください。"
            )

        if config.DEBUG_MODE:

            print()
            print("=== Analyzer DEBUG ===")
            print("image_path :", image_path)
            print("graph shape:", graph_image.shape)
            print("bars       :", len(bars))

            for i, bar in enumerate(bars):
                print(
                    f"[{i}] "
                    f"x={bar.x}, y={bar.y}, "
                    f"w={bar.width}, h={bar.height}, "
                    f"side={bar.side}"
                )

            print("======================")
            print()

        self.detector.save_debug_image(
            graph_image,
            bars
        )

        # --------------------------------------------------
        # Estimate
        # --------------------------------------------------

        result = self.estimator.estimate(
            bars,
            total_notes
        )

        if return_graph:
            return result, graph_image

        return result


# ==========================================================
# Utility
# ==========================================================

_analyzer = Analyzer()


def analyze(
    image_path: str,
    total_notes: int,
    return_graph: bool = False,
):
    """
    Analyzer簡易呼び出し
    """

    return _analyzer.analyze(
        image_path,
        total_notes,
        return_graph,
    )

# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    メイン処理
    """

    try:

        print("=" * 60)
        print(
            f"{config.APP_NAME} "
            f"Version {config.VERSION}"
        )
        print("=" * 60)

        print()

        total_notes = int(
            input(
                "Total Notes : "
            )
        )

        image_path = input(
            "Image Path : "
        )

        print()

        result = analyze(
            image_path,
            total_notes,
        )

        print("=" * 60)
        print("Estimate Result")
        print("=" * 60)

        print(
            f"Max Height      : "
            f"{result.max_height}"
        )

        print(
            f"Height Ratio    : "
            f"{result.height_ratio}"
        )

        print(
            f"Estimated Notes : "
            f"{result.estimated_notes}"
        )

        print()

        print("Distribution")

        if len(result.distribution) == 0:

            print("  No data")

        else:

            for label, value in result.distribution.items():

                print(
                    f"  {label:<18}"
                    f"{value}"
                )

        print()

        print(
            f"Slow Total          : "
            f"{result.slow}"
        )

        print(
            f"Fast Total          : "
            f"{result.fast}"
        )

        print(
            f"Estimated Accuracy  : "
            f"{result.estimated_accuracy:.1f}%"
        )

        print("=" * 60)
    except Exception as error:

        print()

        print("=" * 60)
        print("[ERROR]")
        print(type(error).__name__)
        print(error)
        print("=" * 60)

        raise


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()