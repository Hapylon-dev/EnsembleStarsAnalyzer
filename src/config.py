"""
config.py
Version : 1.2 Final

Global Configuration
"""

from dataclasses import dataclass

# ==========================================================
# Application
# ==========================================================

APP_NAME = "Ensemble Stars!! Music Judgement Analyzer"
VERSION = "1.3 Final"

DEBUG_MODE = False

# ==========================================================
# YOLO Graph Detector
# Version 1.3
# ==========================================================

# False : Version 1.2 固定比率によるグラフ領域切り出し
# True  : Version 1.3 YOLOによるグラフ領域検出
USE_YOLO = True

# Version 1.3 正式学習済みモデル
YOLO_MODEL = "weights/graph_detector_v13.pt"

# 推論設定
YOLO_CONFIDENCE = 0.50
YOLO_IOU = 0.45

# 推論デバイス
# None : Ultralyticsの自動選択に任せる
YOLO_DEVICE = None

# ==========================================================
# Tesseract
# ==========================================================
# ==========================================================
# Output
# ==========================================================

OUTPUT_DIR = "output"
DEBUG_DIR = "debug"

GRAPH_FILENAME = "graph.png"

SAVE_DEBUG_IMAGE = False
# ==========================================================
# Image Processing
# ==========================================================

RESIZE_SCALE = 2.0
THRESHOLD = 0

# ==========================================================
# Detector
# ==========================================================

ORANGE_LOWER = (5, 80, 120)
ORANGE_UPPER = (35, 255, 255)

MORPH_KERNEL = 3
MORPH_ITER_OPEN = 1
MORPH_ITER_CLOSE = 0

MIN_BAR_AREA = 30
MIN_BAR_WIDTH = 2
MIN_BAR_HEIGHT = 4
MAX_BAR_WIDTH = 40

# ==========================================================
# Bar Position Classification
# ==========================================================

# グラフ中央からこの割合以内のバーをCENTERと判定する。
#
# Version 1.3 external_test:
# CENTER max = 1.016%
# SIDE min   = 8.079%
#
# 境界は両分布の空白領域内に設定。
BAR_CENTER_THRESHOLD_RATIO = 0.04

CENTER_LINE_WIDTH = 2
CENTER_LINE_COLOR = (255, 0, 0)

BAR_BOX_COLOR = (0, 255, 0)
BAR_BOX_THICKNESS = 1

# ==========================================================
# Graph Resolution Validation
# YOLOで切り出したグラフ領域の最低解像度
# ==========================================================

MIN_GRAPH_WIDTH = 200
MIN_GRAPH_HEIGHT = 160

# ==========================================================
# Detector ROI
# グラフ画像内で棒が存在する範囲
# （graph.png に対する割合）
# ==========================================================

GRAPH_MASK_LEFT = 0.00
GRAPH_MASK_TOP = 0.00
GRAPH_MASK_RIGHT = 0.94
GRAPH_MASK_BOTTOM = 0.84

# ==========================================================
# Region
#
# left, top, right, bottom
# 画像サイズに対する割合
# ==========================================================

REGIONS = {

    "jacket": (
        0.025,
        0.055,
        0.155,
        0.230
    ),

    "title": (
        0.165,
        0.060,
        0.640,
        0.120
    ),

    "difficulty": (
        0.170,
        0.125,
        0.270,
        0.165
    ),

    "level": (
        0.275,
        0.125,
        0.330,
        0.165
    ),

    "rank": (
        0.450,
        0.200,
        0.630,
        0.390
    ),

    "challenge_rate": (
        0.150,
        0.255,
        0.345,
        0.315
    ),

    "judge": (
        0.120,
        0.435,
        0.235,
        0.695
    ),

        "result_panel": (
        0.02,
        0.12,
        0.73,
        0.93
    ),

    "graph_panel": (
        0.54,
        0.52,
        0.90,
        0.89
    ),

    "notes": (
        0.455,
        0.765,
        0.595,
        0.825
    )
}

# ==========================================================
# Region Class
# ==========================================================

@dataclass(frozen=True)
class Region:

    left: float
    top: float
    right: float
    bottom: float

# ==========================================================
# Utility
# ==========================================================

def get_region(name: str) -> Region:

    if name not in REGIONS:
        raise KeyError(f"Region '{name}' not found.")

    left, top, right, bottom = REGIONS[name]

    return Region(
        left,
        top,
        right,
        bottom
    )