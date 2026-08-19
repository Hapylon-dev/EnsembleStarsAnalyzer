"""
graph.py
Version : 2.1 Final Edition

Graph Region Extractor

Author : OpenAI + Hapylon
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

import config


# ==========================================================
# Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

YOLO_MODEL_PATH = (
    PROJECT_ROOT
    / config.YOLO_MODEL
)

_yolo_model: YOLO | None = None

OUTPUT_DIR = (
    PROJECT_ROOT
    / config.OUTPUT_DIR
)

OUTPUT_GRAPH = (
    OUTPUT_DIR
    / config.GRAPH_FILENAME
)

# ==========================================================
# YOLO Model
# ==========================================================

def get_yolo_model() -> YOLO:
    """
    YOLO graph detectorを取得する。

    モデルは初回呼び出し時のみロードし、
    以降は同じインスタンスを再利用する。
    """

    global _yolo_model

    if _yolo_model is not None:
        return _yolo_model

    if not YOLO_MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"YOLO model not found : {YOLO_MODEL_PATH}"
        )

    if config.DEBUG_MODE:
        print(
            f"Loading YOLO model : {YOLO_MODEL_PATH}"
        )

    _yolo_model = YOLO(
        str(YOLO_MODEL_PATH)
    )

    if config.DEBUG_MODE:
        print(
            "YOLO model loaded."
        )

    return _yolo_model

def detect_graph_bbox(
    image: np.ndarray
) -> tuple[int, int, int, int]:
    """
    YOLOでタップタイミンググラフ領域を検出する。

    Returns
    -------
    tuple[int, int, int, int]
        (x1, y1, x2, y2)

    Raises
    ------
    RuntimeError
        graphを検出できなかった場合。
    """

    if image is None or image.size == 0:
        raise ValueError(
            "Input image is empty."
        )

    model = get_yolo_model()

    results = model.predict(
        source=image,
        conf=config.YOLO_CONFIDENCE,
        iou=config.YOLO_IOU,
        device=config.YOLO_DEVICE,
        verbose=False,
    )

    if not results:
        raise RuntimeError(
            "YOLO prediction returned no results."
        )

    result = results[0]
    boxes = result.boxes

    if boxes is None or len(boxes) == 0:
        raise RuntimeError(
            "Graph was not detected by YOLO."
        )

    # confidenceが最も高いBBoxを採用
    best_index = int(
        boxes.conf.argmax().item()
    )

    confidence = float(
        boxes.conf[best_index].item()
    )

    x1, y1, x2, y2 = (
        boxes.xyxy[best_index]
        .cpu()
        .tolist()
    )

    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))

    if config.DEBUG_MODE:
        print(
            "YOLO graph detected : "
            f"confidence={confidence:.6f}, "
            f"bbox=({x1}, {y1}, {x2}, {y2})"
        )

    return x1, y1, x2, y2

def extract_graph_yolo(
    image: np.ndarray
) -> np.ndarray:
    """
    YOLOで検出したBBoxから
    タップタイミンググラフ領域を切り出す。
    """

    if image is None or image.size == 0:
        raise ValueError(
            "Input image is empty."
        )

    image_h, image_w = image.shape[:2]

    x1, y1, x2, y2 = detect_graph_bbox(image)

    # 画像範囲内に制限
    x1 = max(0, min(x1, image_w))
    x2 = max(0, min(x2, image_w))
    y1 = max(0, min(y1, image_h))
    y2 = max(0, min(y2, image_h))

    if x2 <= x1 or y2 <= y1:
        raise RuntimeError(
            "Invalid YOLO graph bounding box: "
            f"({x1}, {y1}, {x2}, {y2})"
        )

    graph_image = image[
        y1:y2,
        x1:x2
    ].copy()

    if graph_image.size == 0:
        raise RuntimeError(
            "YOLO graph crop is empty."
        )

    if config.DEBUG_MODE:
        print(
            "YOLO graph cropped : "
            f"{graph_image.shape[1]} x "
            f"{graph_image.shape[0]}"
        )

    return graph_image

# ==========================================================
# Utility
# ==========================================================

def load_image(
    image_path: Path
) -> np.ndarray:
    """
    日本語パス対応画像読込
    """

    data = np.fromfile(
        str(image_path),
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


def create_output_dir() -> None:
    """
    出力フォルダ作成
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ==========================================================
# Result Panel Detection
# ==========================================================

def find_result_panel(
    image: np.ndarray
) -> tuple[int, int, int, int]:
    """
    リザルトパネル検出
    """

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    lower = np.array(
        [0, 0, 150],
        dtype=np.uint8
    )

    upper = np.array(
        [180, 70, 255],
        dtype=np.uint8
    )

    mask = cv2.inRange(
        hsv,
        lower,
        upper
    )

    kernel = np.ones(
        (9, 9),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    best = None
    best_score = -1

    image_h, image_w = image.shape[:2]

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 50000:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        aspect = w / h

        if not (0.6 <= aspect <= 2.5):
            continue

        area_score = area

        center_x = x + w / 2
        center_y = y + h / 2

        position_score = 0

        if center_x < image_w * 0.65:
            position_score += 50000

        if center_y < image_h * 0.75:
            position_score += 50000

        score = area_score + position_score

        print(
            f"candidate "
            f"area={area:.0f} "
            f"aspect={aspect:.2f} "
            f"score={score:.0f}"
        )

        if score > best_score:

            best_score = score

            best = (
                x,
                y,
                w,
                h
            )

    if best is None:

        raise RuntimeError(
            "Result panel not found."
        )

    print(
        f"Selected Panel : {best}"
    )

    return best
# ==========================================================
# Result Panel Crop
# ==========================================================

def crop_result_panel(
    image: np.ndarray
) -> np.ndarray:
    """
    リザルトパネル切り抜き
    """

    x, y, w, h = find_result_panel(
        image
    )

    margin_x = int(w * 0.01)
    margin_y = int(h * 0.01)

    left = max(
        0,
        x - margin_x
    )

    top = max(
        0,
        y - margin_y
    )

    right = min(
        image.shape[1],
        x + w + margin_x
    )

    bottom = min(
        image.shape[0],
        y + h + margin_y
    )

    panel = image[
        top:bottom,
        left:right
    ]

    if panel.size == 0:

        raise RuntimeError(
            "Result panel is empty."
        )

    print(
        f"Result Panel : {panel.shape}"
    )

    return panel


# ==========================================================
# Graph Extraction
# ==========================================================

# ==========================================================
# Utility
# ==========================================================

def clip_rect(
    left: int,
    top: int,
    right: int,
    bottom: int,
    width: int,
    height: int
):
    """
    画像範囲内へ補正
    """

    left = max(0, left)
    top = max(0, top)

    right = min(width, right)
    bottom = min(height, bottom)

    return (
        left,
        top,
        right,
        bottom
    )


def crop_rect(
    image: np.ndarray,
    left: int,
    top: int,
    right: int,
    bottom: int
):
    """
    矩形切り出し
    """

    h, w = image.shape[:2]

    left, top, right, bottom = clip_rect(
        left,
        top,
        right,
        bottom,
        w,
        h
    )

    return image[
        top:bottom,
        left:right
    ]

def extract_graph(
    panel: np.ndarray
) -> np.ndarray:
    """
    Tap Timing Graph Extraction
    Version 3.0
    """

    panel_h, panel_w = panel.shape[:2]

    create_output_dir()

    panel_h, panel_w = panel.shape[:2]

    left = int(panel_w * 0.05)
    right = int(panel_w * 0.50)

    top = int(panel_h * 0.44)
    bottom = int(panel_h * 0.86)

    graph = panel[
        top:bottom,
        left:right
    ]

    success, buffer = cv2.imencode(
        ".png",
        graph
    )

    if success and config.DEBUG_MODE:

        buffer.tofile(
            str(
                OUTPUT_DIR /
                "debug_graph.png"
            )
        )

    print()
    print("=" * 40)
    print("Graph Extraction Result")
    print("=" * 40)
    print(f"Panel : {panel.shape}")
    print(f"Graph : {graph.shape}")
    print(
        f"Rect  : ({left}, {top}, {right-left}, {bottom-top})"
    )
    print("=" * 40)
    print()

    return graph
# ==========================================================
# Save Graph
# ==========================================================

def save_graph(
    graph: np.ndarray
) -> None:
    """
    graph.png 保存
    """

    create_output_dir()
    # 公開版では解析途中の画像をディスクへ保存しない。
    # graph_image は呼び出し元へNumPy配列として返し、メモリ上で後続解析する。
    return None

# ==========================================================
# Create Graph
# ==========================================================

def create_graph(
    image_path: str
) -> np.ndarray:
    """
    リザルト画像からタップタイミンググラフを抽出し、
    graph画像を返す。

    Version 1.3:
    USE_YOLO=True の場合はYOLOでグラフ領域を検出する。
    USE_YOLO=False の場合は従来方式を使用する。
    """

    image = load_image(
        Path(image_path)
    )

    # --------------------------------------------------
    # YOLO Graph Detection
    # --------------------------------------------------

    if config.USE_YOLO:

        graph_image = extract_graph_yolo(
            image
        )

    # --------------------------------------------------
    # Legacy Graph Extraction
    # --------------------------------------------------

    else:

        panel = crop_result_panel(
            image
        )

        graph_image = extract_graph(
            panel
        )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    save_graph(
        graph_image
    )

    return graph_image

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

        # ----------------------------------------------
        # Create Graph
        # ----------------------------------------------

        image_path = input(
            "Image Path : "
        )

        graph_image = create_graph(
            image_path
        )

        print(
            f"Graph Image : {graph_image.shape}"
        )
        print()

        print(
            "Graph extraction completed."
        )

        print(
            f"Input  : {image_path}"
        )

        print(
            f"Output : {OUTPUT_GRAPH}"
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