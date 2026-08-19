"""
detector.py
Version : 1.0 Final Edition

Tap Timing Graph Detector

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from typing import List

import os

import cv2
import numpy as np

from models import BarData
import config


# ==========================================================
# Detector
# ==========================================================

class Detector:
    """
    タップタイミング棒検出器
    """

    def __init__(self):

        # HSV Lower
        self.lower = np.array(
            config.ORANGE_LOWER,
            dtype=np.uint8
        )

        # HSV Upper
        self.upper = np.array(
            config.ORANGE_UPPER,
            dtype=np.uint8
        )

        self.kernel = np.ones(
            (
                config.MORPH_KERNEL,
                config.MORPH_KERNEL
            ),
            np.uint8
        )

    # ======================================================
    # HSV
    # ======================================================

    def hsv_mask(
        self,
        image: np.ndarray
    ) -> np.ndarray:
        """
        オレンジ色抽出
        """

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        mask = cv2.inRange(
            hsv,
            self.lower,
            self.upper
        )

        return mask

    # ======================================================
    # Morphology
    # ======================================================

    def morphology(
        self,
        mask: np.ndarray
    ) -> np.ndarray:
        """
        ノイズ除去
        """

        if config.MORPH_ITER_CLOSE > 0:

            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_CLOSE,
                self.kernel,
                iterations=config.MORPH_ITER_CLOSE
            )

        return mask

    # ======================================================
    # Binary
    # ======================================================

    def preprocess(
        self,
        image: np.ndarray
    ) -> np.ndarray:
        """
        前処理
        """

        mask = self.hsv_mask(image)

        mask = self.morphology(mask)

        mask = self.apply_graph_roi(mask)

        if config.SAVE_DEBUG_IMAGE:

            os.makedirs(
                config.DEBUG_DIR,
                exist_ok=True
            )

            success, buffer = cv2.imencode(
                ".png",
                mask
            )

            if success:

                buffer.tofile(
                    os.path.join(
                        config.DEBUG_DIR,
                        "debug_mask.png"
                    )
                )
        
        return mask
    
    # ======================================================
    # Graph ROI
    # ======================================================

    def apply_graph_roi(
        self,
        mask: np.ndarray
    ) -> np.ndarray:
        """
        グラフ領域だけ残す
        """

        h, w = mask.shape

        roi = np.zeros_like(mask)

        left = int(
            config.GRAPH_MASK_LEFT * w
        )

        top = int(
            config.GRAPH_MASK_TOP * h
        )

        right = int(
            config.GRAPH_MASK_RIGHT * w
        ) 

        bottom = int(
            config.GRAPH_MASK_BOTTOM * h
        )

        roi[
            top:bottom,
            left:right
        ] = 255

        return cv2.bitwise_and(
            mask,
            roi
        )

    # ======================================================
    # Center
    # ======================================================

    def center_x(
        self,
        image: np.ndarray
    ) -> int:
        """
        グラフ中心
        """

        h, w = image.shape[:2]

        return w // 2
    # ======================================================
    # Contours
    # ======================================================

    def find_contours(
        self,
        mask: np.ndarray
    ) -> list[np.ndarray]:
        """
        棒グラフ候補の輪郭を取得
        """

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        return contours


    # ======================================================
    # Filter
    # ======================================================

    def filter_contours(
        self,
        contours: list[np.ndarray],
        image: np.ndarray
    ) -> list[np.ndarray]:
        """
        棒以外の輪郭を除外
        """

        graph_height = image.shape[0]

        results = []

        for contour in contours:

            x, y, w, h = cv2.boundingRect(contour)

            if y < graph_height * 0.25:
                continue

            #
            # FASTバーを除外
            #
            if y > graph_height * 0.71:
                continue

            area = cv2.contourArea(contour)

            if area < config.MIN_BAR_AREA:
                continue

            if w < config.MIN_BAR_WIDTH:
                continue

            if w > config.MAX_BAR_WIDTH:
                continue

            if h < config.MIN_BAR_HEIGHT:
                continue


            results.append(contour)

        return results
    
    # ======================================================
    # Recover Short Bar
    # ======================================================

    def recover_short_bar(
        self,
        all_contours: list[np.ndarray],
        filtered_contours: list[np.ndarray],
        image: np.ndarray
    ) -> list[np.ndarray]:
        """
        通常フィルターで2本だけ検出された場合、
        高さ不足だけで除外された短いバーを救済する。

        既存2本と幅・位置・間隔が整合する候補だけを採用する。
        """

        # 2本検出時のみ救済を試す
        if len(filtered_contours) != 2:
            return filtered_contours

        graph_height, graph_width = image.shape[:2]

        # 現在採用されている2本
        accepted = sorted(
            filtered_contours,
            key=lambda c: cv2.boundingRect(c)[0]
        )

        accepted_ids = {
            id(contour)
            for contour in accepted
        }

        # 既存2本の情報
        accepted_rects = [
            cv2.boundingRect(contour)
            for contour in accepted
        ]

        accepted_centers = [
            x + w / 2
            for x, y, w, h in accepted_rects
        ]

        accepted_widths = [
            w
            for x, y, w, h in accepted_rects
        ]

        mean_width = sum(accepted_widths) / len(accepted_widths)

        candidates = []

        for contour in all_contours:

            # すでに採用済みなら除外
            if id(contour) in accepted_ids:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)

            # 通常ROI条件は維持
            if y < graph_height * 0.25:
                continue

            if y > graph_height * 0.71:
                continue

            # 面積条件は維持
            if area < config.MIN_BAR_AREA:
                continue

            # 幅条件も維持
            if w < config.MIN_BAR_WIDTH:
                continue

            if w > config.MAX_BAR_WIDTH:
                continue

            # 通常条件を満たすものは救済対象ではない
            if h >= config.MIN_BAR_HEIGHT:
                continue

            # 救済対象は高さ3px以上
            if h < 3:
                continue

            # 既存バーと幅が大きく異なる候補は除外
            width_ratio = w / mean_width

            if not 0.75 <= width_ratio <= 1.25:
                continue

            candidate_center = x + w / 2

            # 既存2本と合わせて3本にする
            centers = sorted(
                accepted_centers + [candidate_center]
            )

            gap1 = centers[1] - centers[0]
            gap2 = centers[2] - centers[1]

            # 同一点付近は除外
            if gap1 <= 0 or gap2 <= 0:
                continue

            # 左右間隔の一致度
            gap_ratio = min(gap1, gap2) / max(gap1, gap2)

            # 3本がほぼ等間隔であること
            if gap_ratio < 0.80:
                continue

            # グラフ中央付近に3本セットが存在すること
            middle_center = centers[1]
            graph_center = graph_width / 2

            center_error = abs(
                middle_center - graph_center
            ) / graph_width

            if center_error > 0.08:
                continue

            candidates.append(
                (
                    gap_ratio,
                    contour
                )
            )

        # 条件を満たす候補がなければそのまま
        if not candidates:
            return filtered_contours

        # 最も等間隔な候補を採用
        candidates.sort(
            key=lambda item: item[0],
            reverse=True
        )

        recovered = accepted + [
            candidates[0][1]
        ]

        recovered.sort(
            key=lambda c: cv2.boundingRect(c)[0]
        )

        return recovered

    # ======================================================
    # BarData
    # ======================================================

    def create_bar_data(
        self,
        contour: np.ndarray,
        index: int,
        center_x: int
    ) -> BarData:
        """
        輪郭からBarData生成
        """

        x, y, w, h = cv2.boundingRect(contour)

        bar_center = x + w / 2

        distance = abs(bar_center - center_x)

        side = ""

        return BarData(

            index=index,

            x=x,

            y=y,

            width=w,

            height=h,

            side=side,

            distance=distance,

            color="orange"
        )
    
    # ======================================================
    # Bar Position Classification
    # ======================================================

    def classify_bar_side(
        self,
        bar: BarData,
        image: np.ndarray
    ) -> str:
        """
        グラフ中央からの位置に基づいて
        バーを SLOW / CENTER / FAST に分類する。

        Version 1.3:
        CENTER判定にはグラフ幅に対する
        正規化距離を使用する。
        """

        graph_width = image.shape[1]

        if graph_width <= 0:
            raise ValueError(
                "グラフ幅が不正です。"
            )

        graph_center = self.center_x(
            image
        )

        bar_center = (
            bar.x
            + bar.width / 2.0
        )

        offset = (
            bar_center
            - graph_center
        )

        distance_ratio = (
            abs(offset)
            / graph_width
        )

        if (
            distance_ratio
            <= config.BAR_CENTER_THRESHOLD_RATIO
        ):
            return "CENTER"

        if offset < 0:
            return "SLOW"

        return "FAST"


    # ======================================================
    # Detect Bars
    # ======================================================

    def detect_bars(
        self,
        image: np.ndarray
    ) -> List[BarData]:
        """
        棒グラフ検出
        """

        mask = self.preprocess(image)

        raw_contours = self.find_contours(mask)

        contours = self.filter_contours(
            raw_contours,
            image
        )

        contours = self.recover_short_bar(
            raw_contours,
            contours,
            image
        )

        center = self.center_x(image)

        bars: List[BarData] = []

        for i, contour in enumerate(contours):

            bar = self.create_bar_data(

                contour,

                i,

                center

            )

            bars.append(bar)

        bars.sort(
            key=lambda b: b.x
        )

        if len(bars) == 3:

            bars[0].side = "SLOW"
            bars[1].side = "CENTER"
            bars[2].side = "FAST"

        elif len(bars) == 2:

            for bar in bars:

                bar.side = self.classify_bar_side(
                    bar,
                    image
                )

        elif len(bars) == 1:

            bars[0].side = self.classify_bar_side(
                bars[0],
                image
            )

        for i, bar in enumerate(bars):

            bar.index = i

        return bars
    # ======================================================
    # Debug Draw
    # ======================================================

    def draw_debug(
        self,
        image: np.ndarray,
        bars: List[BarData]
    ) -> np.ndarray:
        """
        デバッグ描画
        """

        debug = image.copy()

        center = self.center_x(image)

        # 中心線
        cv2.line(
            debug,
            (center, 0),
            (center, image.shape[0]),
            config.CENTER_LINE_COLOR,
            config.CENTER_LINE_WIDTH
        )

                # ==================================================
        # Bar Bounding Boxes
        # ==================================================

        for bar in bars:

            # BBox
            cv2.rectangle(
                debug,
                (bar.x, bar.y),
                (
                    bar.x + bar.width,
                    bar.y + bar.height
                ),
                config.BAR_BOX_COLOR,
                config.BAR_BOX_THICKNESS
            )

            # BBoxには番号だけ表示
            number_text = str(bar.index + 1)

            text_x = bar.x
            text_y = max(12, bar.y - 5)

            # 黒縁
            cv2.putText(
                debug,
                number_text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.40,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

            # 白文字
            cv2.putText(
                debug,
                number_text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.40,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        # ==================================================
        # Bar Information
        # ==================================================

        info_x = 8
        info_y = 60
        info_line_height = 18

        for i, bar in enumerate(bars):

            label = (
                f"#{bar.index + 1} "
                f"{bar.side} "
                f"H:{bar.height}px"
            )

            position = (
                info_x,
                info_y + i * info_line_height
            )

            # 黒縁
            cv2.putText(
                debug,
                label,
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

            # 白文字
            cv2.putText(
                debug,
                label,
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        return debug


    # ======================================================
    # Main Detect
    # ======================================================

    def detect(
        self,
        image: np.ndarray
    ) -> List[BarData]:
        """
        タップタイミング棒検出
        """

        return self.detect_bars(
            image
        )
    # ======================================================
    # Debug Save
    # ======================================================

    def save_debug_image(
        self,
        image: np.ndarray,
        bars: List[BarData],
        filename: str = "detector_debug.png"
    ) -> None:
        """
        デバッグ画像保存
        """

        if not config.SAVE_DEBUG_IMAGE:
            return

        os.makedirs(
            config.DEBUG_DIR,
            exist_ok=True
        )

        debug = self.draw_debug(
            image,
            bars
        )

        path = os.path.join(
            config.DEBUG_DIR,
            filename
        )

        success, buffer = cv2.imencode(
            ".png",
            debug
        )

        if not success:

            raise RuntimeError(
                "Failed to encode debug image."
            )

        buffer.tofile(path)


# ==========================================================
# Utility
# ==========================================================

def load_image(
    image_path: str
) -> np.ndarray:
    """
    日本語パス対応画像読込
    """

    data = np.fromfile(
        image_path,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        data,
        cv2.IMREAD_COLOR
    )

    if image is None:

        raise FileNotFoundError(
            f"Image not found : {image_path}"
        )

    return image

_detector = Detector()

def detect(
    image: np.ndarray
) -> List[BarData]:
    """
    Detector簡易呼び出し
    """

    bars = _detector.detect(image)

    _detector.save_debug_image(
        image,
        bars
    )

    return bars       
# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """
    Detector単体テスト
    """

    try:

        image_path = os.path.join(
            config.OUTPUT_DIR,
            config.GRAPH_FILENAME
        )

        image = load_image(
            image_path
        )

        if image is None:

            raise FileNotFoundError(
                f"Image not found : {image_path}"
            )

        bars = detect(
            image
        )

        print("=" * 60)
        print("Detector Test")
        print("=" * 60)

        print(
            f"Graph Image : {image.shape}"
        )

        print(
            f"Detected Bars : {len(bars)}"
        )

        print()

        for bar in bars:

            print(
                f"[{bar.index:02d}] "
                f"x={bar.x:4d} "
                f"y={bar.y:4d} "
                f"w={bar.width:2d} "
                f"h={bar.height:3d} "
                f"{bar.side:5s} "
                f"distance={bar.distance:.1f}"
            )

        print()

        print(
            f"Debug Image : "
            f"{config.DEBUG_DIR}"
        )

        print("=" * 60)

    except Exception as error:

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