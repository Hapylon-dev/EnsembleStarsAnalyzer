"""
models.py
Version : 1.0 Final Edition

Data Models

Author : OpenAI + Hapylon
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

import numpy as np


# ==========================================================
# Validation
# ==========================================================

@dataclass(slots=True)
class ValidationResult:
    """
    リザルト画面判定結果
    """

    is_target: bool

    challenge_rate_ok: bool

    judge_ok: bool

    challenge_rate_text: str = ""

    judge_values: Dict[str, str] = field(default_factory=dict)

    message: str = ""


# ==========================================================
# Bar
# ==========================================================

@dataclass(slots=True)
class BarData:
    """
    タップタイミング棒1本分
    """

    index: int

    x: int

    y: int

    width: int

    height: int

    side: str           # FAST / SLOW

    distance: float     # 中心線からの距離(px)

    color: str = "orange"


# ==========================================================
# Graph Analysis
# ==========================================================

@dataclass(slots=True)
class AnalysisData:
    """
    graph.py の最終出力
    """

    # Validation
    validation: ValidationResult

    # 画像
    jacket_image: Optional[np.ndarray] = None

    title_image: Optional[np.ndarray] = None

    difficulty_image: Optional[np.ndarray] = None

    level_image: Optional[np.ndarray] = None

    rank_image: Optional[np.ndarray] = None

    graph_image: Optional[np.ndarray] = None

    notes_image: Optional[np.ndarray] = None

    # OCR
    challenge_rate: float = 0.0

    perfect: int = 0

    great: int = 0

    good: int = 0

    bad: int = 0

    miss: int = 0

    # グラフ
    bars: List[BarData] = field(default_factory=list)

    center_x: int = 0

    image_width: int = 0

    image_height: int = 0


# ==========================================================
# Estimate
# ==========================================================

@dataclass(slots=True)
class EstimateResult:
    """
    estimate.py 出力
    """

    # 最大棒高さ(px)
    max_height: int = 0

    # 各棒の高さ比率
    height_ratio: List[float] = field(default_factory=list)

    # 棒ごとの推定ノーツ数
    estimated_notes: List[int] = field(default_factory=list)

    # 判定別推定結果
    distribution: Dict[str, int] = field(default_factory=dict)

    # 集計
    amazing_plus: int = 0

    amazing: int = 0

    perfect: int = 0

    # 詳細内訳
    amazing_slow: int = 0

    amazing_fast: int = 0

    perfect_slow: int = 0

    perfect_fast: int = 0

    # 集計
    fast: int = 0

    slow: int = 0

    # Balance評価可否
    # SLOW / FAST の両側バーを検出できた場合のみ True
    balance_available: bool = False

    # 推定精度
    estimated_accuracy: float = 0.0


# ==========================================================
# Score
# ==========================================================

@dataclass(slots=True)
class ScoreResult:
    """
    score.py 出力
    """

    achievement: float = 0.0

    precision: float = 0.0

    precision_grade: str = ""

    balance: float = 0.0

    balance_grade: str = ""

    # Balance評価可否
    balance_available: bool = False

    overall_score: float = 0.0

    rank: str = ""

# ==========================================================
# Render
# ==========================================================

@dataclass(slots=True)
class RenderData:
    """
    renderer.py 入力
    """

    analysis: AnalysisData

    estimate: EstimateResult

    score: ScoreResult

    output_image: Optional[np.ndarray] = None