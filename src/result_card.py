"""
result_card.py
Version : 1.3 Final

Ensemble Stars!! Music
Tap Timing Analyzer

Result Card Generator
"""

from __future__ import annotations

from pathlib import Path

from datetime import datetime
import math

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter

# ==========================================================
# Output
# ==========================================================

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

CARD_PATH = OUTPUT_DIR / "result_card.png"

# ==========================================================
# Ranking Assets
# ==========================================================

RANKING_TITLE_DIR = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "ranking_titles"
)

RANKING_TITLE_FILES = {
    "レインボーランカー": "rainbow.png",
    "ダイヤモンドランカー": "diamond.png",
    "プラチナランカー": "platinum.png",
    "ゴールドランカー": "gold.png",
    "シルバーランカー": "silver.png",
    "ブロンズランカー": "bronze.png",
    "パープルランカー": "purple.png",
    "レッドランカー": "red.png",
    "オレンジランカー": "orange.png",
    "グリーンランカー": "green.png",
    "ブルーランカー": "blue.png",
    "ホワイトランカー": "white.png",
}

# ==========================================================
# Ranking Plate Styles
# ==========================================================

RANKING_PLATE_STYLES = {
    # Rainbow / Prism
    "レインボーランカー": {
        "mode": "rainbow",
        "top": (255, 253, 255),
        "middle": (250, 248, 255),
        "bottom": (245, 242, 252),
        "line": (190, 160, 220),
        "highlight": (255, 255, 255),
        "crystal": (225, 205, 245),
        "accent": (248, 205, 225),
        "rainbow_colors": (
            (255, 205, 220),
            (255, 232, 190),
            (230, 245, 190),
            (190, 238, 220),
            (185, 225, 250),
            (215, 200, 248),
            (248, 205, 232),
        ),
    },

    # Diamond / Ice Crystal
    "ダイヤモンドランカー": {
        "mode": "gradient",
        "top": (255, 255, 255),
        "middle": (238, 249, 255),
        "bottom": (218, 237, 250),
        "line": (165, 205, 235),
        "highlight": (255, 255, 255),
        "crystal": (190, 225, 250),
        "accent": (210, 238, 255),
    },

    # Platinum / White Silver
    "プラチナランカー": {
        "mode": "gradient",
        "top": (255, 255, 255),
        "middle": (247, 249, 252),
        "bottom": (222, 228, 236),
        "line": (190, 202, 216),
        "highlight": (255, 255, 255),
        "crystal": (210, 218, 230),
        "accent": (232, 237, 244),
    },

    # Gold / Champagne
    "ゴールドランカー": {
        "mode": "gradient",
        "top": (255, 254, 246),
        "middle": (253, 244, 211),
        "bottom": (238, 211, 150),
        "line": (205, 160, 65),
        "highlight": (255, 255, 245),
        "crystal": (242, 211, 145),
        "accent": (255, 229, 170),
    },

    # Silver / Crystal
    "シルバーランカー": {
        "mode": "gradient",
        "top": (255, 255, 255),
        "middle": (247, 249, 252),
        "bottom": (232, 237, 243),
        "line": (200, 208, 220),
        "highlight": (255, 255, 255),
        "crystal": (218, 226, 237),
        "accent": (235, 241, 248),
    },

    # Bronze / Copper
    "ブロンズランカー": {
        "mode": "gradient",
        "top": (255, 250, 246),
        "middle": (249, 231, 211),
        "bottom": (229, 198, 165),
        "line": (185, 130, 85),
        "highlight": (255, 253, 248),
        "crystal": (230, 185, 145),
        "accent": (248, 210, 175),
    },

    # Purple / Amethyst
    "パープルランカー": {
        "mode": "gradient",
        "top": (255, 252, 255),
        "middle": (247, 237, 254),
        "bottom": (224, 205, 242),
        "line": (180, 140, 215),
        "highlight": (255, 255, 255),
        "crystal": (214, 185, 236),
        "accent": (238, 208, 248),
    },

    # Red / Ruby
    "レッドランカー": {
        "mode": "gradient",
        "top": (255, 250, 251),
        "middle": (252, 231, 235),
        "bottom": (239, 198, 207),
        "line": (205, 125, 142),
        "highlight": (255, 255, 255),
        "crystal": (241, 170, 184),
        "accent": (250, 208, 216),
    },

    # Orange / Amber
    "オレンジランカー": {
        "mode": "gradient",
        "top": (255, 253, 247),
        "middle": (253, 239, 211),
        "bottom": (239, 211, 164),
        "line": (210, 155, 65),
        "highlight": (255, 255, 248),
        "crystal": (244, 207, 140),
        "accent": (255, 226, 170),
    },

    # Green / Emerald
    "グリーンランカー": {
        "mode": "gradient",
        "top": (248, 255, 251),
        "middle": (228, 247, 235),
        "bottom": (193, 225, 207),
        "line": (105, 175, 130),
        "highlight": (255, 255, 255),
        "crystal": (165, 214, 185),
        "accent": (207, 237, 219),
    },

    # Blue / Sapphire
    "ブルーランカー": {
        "mode": "gradient",
        "top": (248, 253, 255),
        "middle": (226, 241, 253),
        "bottom": (194, 220, 243),
        "line": (110, 160, 210),
        "highlight": (255, 255, 255),
        "crystal": (165, 205, 238),
        "accent": (205, 231, 252),
    },

    # White / Pearl
    "ホワイトランカー": {
        "mode": "gradient",
        "top": (255, 255, 255),
        "middle": (252, 252, 253),
        "bottom": (238, 238, 243),
        "line": (208, 208, 218),
        "highlight": (255, 255, 255),
        "crystal": (228, 228, 237),
        "accent": (242, 242, 248),
    },
}

RANKING_RANK_ORDER = (
    "SSS+", "SSS", "SS+", "SS", "S+", "S",
    "AAA+", "AAA", "AA+", "AA", "A+", "A",
    "BBB", "BB", "B", "CCC", "CC", "C", "D", "E", "F",
)

RANKING_SECTION_HEIGHT = 300

# ==========================================================
# Card Size
# ==========================================================

CARD_WIDTH = 1080
CARD_HEIGHT = 1450


# ==========================================================
# Layout
# ==========================================================

CARD_MARGIN = 18

CONTENT_MARGIN = 20

SECTION_GAP = 8

FOOTER_TOP_GAP = 4

COLUMN_GAP = 20

CARD_RADIUS = 22

CARD_BORDER = 2

INNER_PADDING = 18

# ==========================================================
# Common Padding
# ==========================================================

RIGHT_PADDING = 20
LEFT_PADDING = 20


# ==========================================================
# Song Badge
# ==========================================================

DIFFICULTY_BADGE_WIDTH = 160

LEVEL_BADGE_GAP = 14

LEVEL_BADGE_MIN_WIDTH = 88

BADGE_HEIGHT = 36

BADGE_RADIUS = 22


# ==========================================================
# Pie Chart Layout
# ==========================================================

PIE_SIZE = 230

PIE_LIST_GAP = 8


# ==========================================================
# Content Area
# ==========================================================

CONTENT_LEFT = CARD_MARGIN + CONTENT_MARGIN

CONTENT_TOP = CARD_MARGIN + CONTENT_MARGIN

CONTENT_RIGHT = CARD_WIDTH - CARD_MARGIN - CONTENT_MARGIN
CONTENT_BOTTOM = CARD_HEIGHT - CARD_MARGIN - CONTENT_MARGIN


# ==========================================================
# Column
# ==========================================================

LEFT_WIDTH = 455

RIGHT_WIDTH = (
    CONTENT_RIGHT
    - CONTENT_LEFT
    - LEFT_WIDTH
    - COLUMN_GAP
)

LEFT_X = CONTENT_LEFT

RIGHT_X = (
    LEFT_X
    + LEFT_WIDTH
    + COLUMN_GAP
)


# ==========================================================
# Section Height
# ==========================================================

HEADER_HEIGHT = 88

SONG_HEIGHT = 140

MAIN_HEIGHT = 640

FASTSLOW_HEIGHT = 92

COMMENT_HEIGHT = 300

FOOTER_HEIGHT = 90

# ==========================================================
# Layout Engine
# ==========================================================

def layout_rect(
    left: int,
    top: int,
    width: int,
    height: int,
):
    """
    矩形生成
    """
    return (
        left,
        top,
        left + width,
        top + height,
    )


def next_top(
    rect,
    gap: int = SECTION_GAP,
):
    """
    次のセクション開始位置
    """
    return rect[3] + gap

# ==========================================================
# Rectangle
# ==========================================================

HEADER_RECT = layout_rect(
    CONTENT_LEFT,
    CONTENT_TOP,
    CONTENT_RIGHT - CONTENT_LEFT,
    HEADER_HEIGHT,
)

SONG_RECT = layout_rect(
    CONTENT_LEFT,
    next_top(HEADER_RECT),
    CONTENT_RIGHT - CONTENT_LEFT,
    SONG_HEIGHT,
)

LEFT_RECT = layout_rect(
    LEFT_X,
    next_top(SONG_RECT),
    LEFT_WIDTH,
    MAIN_HEIGHT,
)

RIGHT_RECT = layout_rect(
    RIGHT_X,
    next_top(SONG_RECT),
    RIGHT_WIDTH,
    MAIN_HEIGHT,
)

# ==========================================================
# Fixed Layout (1080 x 1450)
# ==========================================================

HEADER_RECT = layout_rect(
    CONTENT_LEFT,
    CONTENT_TOP,
    CONTENT_RIGHT - CONTENT_LEFT,
    HEADER_HEIGHT,
)

SONG_RECT = layout_rect(
    CONTENT_LEFT,
    next_top(HEADER_RECT),
    CONTENT_RIGHT - CONTENT_LEFT,
    SONG_HEIGHT,
)

LEFT_RECT = layout_rect(
    LEFT_X,
    next_top(SONG_RECT),
    LEFT_WIDTH,
    MAIN_HEIGHT,
)

RIGHT_RECT = layout_rect(
    RIGHT_X,
    next_top(SONG_RECT),
    RIGHT_WIDTH,
    MAIN_HEIGHT,
)

# ----------------------------------------------------------
# Main bottom
# ----------------------------------------------------------

MAIN_BOTTOM = max(
    LEFT_RECT[3],
    RIGHT_RECT[3],
)

# ----------------------------------------------------------
# Combined SLOW / FAST
# ----------------------------------------------------------

FASTSLOW_RECT = layout_rect(
    CONTENT_LEFT,
    MAIN_BOTTOM + SECTION_GAP + 8,
    CONTENT_RIGHT - CONTENT_LEFT,
    FASTSLOW_HEIGHT,
)

# ----------------------------------------------------------
# Lower cards
# 左：解析結果
# 右：ランキング
# ----------------------------------------------------------

LOWER_TOP = FASTSLOW_RECT[3] + SECTION_GAP

LOWER_LEFT_RECT = layout_rect(
    LEFT_X,
    LOWER_TOP,
    LEFT_WIDTH,
    COMMENT_HEIGHT,
)

LOWER_RIGHT_RECT = layout_rect(
    RIGHT_X,
    LOWER_TOP,
    RIGHT_WIDTH,
    RANKING_SECTION_HEIGHT,
)

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------

LOWER_BOTTOM = max(
    LOWER_LEFT_RECT[3],
    LOWER_RIGHT_RECT[3],
)

FOOTER_RECT = (
    CONTENT_LEFT,
    LOWER_BOTTOM + SECTION_GAP + FOOTER_TOP_GAP,
    CONTENT_RIGHT,
    LOWER_BOTTOM + SECTION_GAP + FOOTER_TOP_GAP + FOOTER_HEIGHT,
)

# ==========================================================
# Color
# ==========================================================

BACKGROUND = (
    248,
    248,
    250,
)

WHITE = (
    252,
    253,
    255,
)

TITLE = (
    110,
    60,
    180,
)

TEXT = (
    45,
    45,
    45,
)

SUBTEXT = (
    120,
    120,
    120,
)

LINE = (
    229,
    227,
    229,
)

SHADOW = (
    228,
    231,
    238,
)

RANK_COLOR = (
    249,
    168,
    37,
)

RESULT_TITLE = (
    88,
    54,
    170,
)

def get_rank_color(rank: str):
    """
    Overall Rank表示用メインカラー。

    SSS系 : 虹色描画用フォールバック
    SS系  : Gold
    S系   : Silver
    AAA系 : Bronze
    AA系  : Red
    A系   : Deep Red
    BBB/BB/B : Amber / Gold Yellow / Yellow
    CCC/CC/C : Blue系
    D/E/F : Gray系

    Overallの現行ランク体系に合わせ、旧 DDD / DD / EEE / EE
    および存在しない旧Plusランクは定義しない。
    """

    colors = {

        # ==================================================
        # SSS : Rainbow
        # ==================================================
        # draw_rank_text() では専用Rainbow描画を使用。
        # ここではフォールバック色としてGoldを指定。
        "SSS+": (255, 215, 0),
        "SSS":  (255, 215, 0),

        # ==================================================
        # SS : Gold
        # ==================================================
        "SS+": (255, 193, 7),
        "SS":  (255, 193, 7),

        # ==================================================
        # S : Silver
        # ==================================================
        "S+": (170, 185, 205),
        "S":  (170, 185, 205),

        # ==================================================
        # AAA : Bronze
        # ==================================================
        "AAA+": (205, 127, 50),
        "AAA":  (205, 127, 50),

        # ==================================================
        # AA : Red
        # ==================================================
        "AA+": (239, 83, 80),
        "AA":  (239, 83, 80),

        # ==================================================
        # A : Deep Red
        # ==================================================
        "A+": (229, 57, 53),
        "A":  (229, 57, 53),

        # ==================================================
        # BBB : Amber
        # ==================================================
        "BBB": (230, 150, 35),

        # ==================================================
        # BB : Gold Yellow
        # ==================================================
        "BB": (245, 190, 45),

        # ==================================================
        # B : Yellow
        # ==================================================
        "B": (255, 224, 102),

        # ==================================================
        # CCC : Deep Blue
        # ==================================================
        "CCC": (45, 90, 170),

        # ==================================================
        # CC : Blue
        # ==================================================
        "CC": (55, 110, 205),

        # ==================================================
        # C : Light Blue
        # ==================================================
        "C": (66, 133, 244),

        # ==================================================
        # D : Light Gray
        # ==================================================
        "D": (145, 145, 145),

        # ==================================================
        # E : Dark Charcoal
        # ==================================================
        "E": (95, 95, 100),

        # ==================================================
        # F
        # ==================================================
        "F": (65, 65, 70),
    }

    return colors.get(
        rank,
        TITLE,
    )


def get_rank_card_colors(rank: str):
    """
    Rankカード用の背景色・枠線色を返す。

    Rank文字を主役にするため、
    背景へのRank色の反映はごく薄くする。
    """

    # ==================================================
    # SSS : Champagne Gold
    # ==================================================
    if rank.startswith("SSS"):
        return (
            (255, 247, 220),
            (235, 198, 110),
        )

    # ==================================================
    # SS : Pale Gold
    # ==================================================
    elif rank.startswith("SS"):
        return (
            (255, 246, 220),
            (228, 200, 135),
        )

    # ==================================================
    # S : Platinum
    # ==================================================
    elif rank.startswith("S"):
        return (
            (250, 252, 255),
            (198, 208, 220),
        )

    # ==================================================
    # AAA : Bronze
    # ==================================================
    elif rank.startswith("AAA"):
        return (
            (248, 241, 232),
            (205, 167, 118),
        )

    # ==================================================
    # Others
    # ==================================================
    else:
        return (
            (255, 250, 235),
            (235, 220, 170),
        )

def draw_rainbow_rank_text(
    draw: ImageDraw.ImageDraw,
    *,
    rank: str,
    center_x: int,
    center_y: int,
):
    """
    Version 1.3 Final

    SSS / SSS+ 専用Rank描画。

    ・文字内部：高彩度Rainbow
    ・Rainbow：約1.8周期
    ・外縁：Gold
    ・外側：Gold Glow
    ・SSS+ は SSS より強い装飾
    """

    # ------------------------------------------------------
    # Text Bounding Box
    # ------------------------------------------------------

    bbox = draw.textbbox(
        (0, 0),
        rank,
        font=RANK_FONT,
        stroke_width=0,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 16

    layer_width = text_width + padding * 2
    layer_height = text_height + padding * 2

    # ------------------------------------------------------
    # Text Mask
    # ------------------------------------------------------

    mask = Image.new(
        "L",
        (layer_width, layer_height),
        0,
    )

    mask_draw = ImageDraw.Draw(mask)

    text_x = padding - bbox[0]
    text_y = padding - bbox[1]

    mask_draw.text(
        (text_x, text_y),
        rank,
        fill=255,
        font=RANK_FONT,
    )

    # ------------------------------------------------------
    # Rainbow Gradient
    # ------------------------------------------------------

    rainbow = Image.new(
        "RGB",
        (layer_width, layer_height),
    )

    rainbow_pixels = rainbow.load()

    # 最初のRedを最後にも置き、
    # 虹を自然にループさせる
    rainbow_colors = [
        (255, 55, 70),     # Red
        (255, 135, 35),    # Orange
        (255, 220, 45),    # Yellow
        (70, 210, 95),     # Green
        (45, 200, 220),    # Cyan
        (65, 125, 255),    # Blue
        (135, 80, 255),    # Violet
        (235, 70, 220),    # Magenta
        (255, 55, 70),     # Red
    ]

    color_segments = len(rainbow_colors) - 1

    # 文字幅の中で虹を約1.8周させる
    rainbow_cycles = 1.8

    for x in range(layer_width):

        normalized = (
            x / max(1, layer_width - 1)
        )

        cycle_position = (
            normalized * rainbow_cycles
        ) % 1.0

        position = (
            cycle_position
            * color_segments
        )

        index = min(
            int(position),
            color_segments - 1,
        )

        fraction = position - index

        color1 = rainbow_colors[index]
        color2 = rainbow_colors[index + 1]

        color = tuple(
            int(
                color1[i]
                + (
                    color2[i]
                    - color1[i]
                )
                * fraction
            )
            for i in range(3)
        )

        for y in range(layer_height):
            rainbow_pixels[x, y] = color

    # ------------------------------------------------------
    # Position
    # ------------------------------------------------------

    layer_left = (
        center_x
        - layer_width // 2
    )

    layer_top = (
        center_y
        - layer_height // 2
    )

    # ------------------------------------------------------
    # Decoration Strength
    # ------------------------------------------------------

    is_plus = rank == "SSS+"

    glow_width = 9 if is_plus else 7
    outer_width = 5 if is_plus else 4

    # ------------------------------------------------------
    # Gold Glow
    # ------------------------------------------------------

    draw.text(
        (
            center_x,
            center_y,
        ),
        rank,
        fill=(255, 225, 100),
        font=RANK_FONT,
        anchor="mm",
        stroke_width=glow_width,
        stroke_fill=(255, 220, 90),
    )

    # ------------------------------------------------------
    # Dark Gold Outer Edge
    # ------------------------------------------------------

    draw.text(
        (
            center_x,
            center_y,
        ),
        rank,
        fill=(255, 255, 255),
        font=RANK_FONT,
        anchor="mm",
        stroke_width=outer_width,
        stroke_fill=(175, 105, 0),
    )

    # ------------------------------------------------------
    # Bright Gold Inner Edge
    # ------------------------------------------------------

    draw.text(
        (
            center_x,
            center_y,
        ),
        rank,
        fill=(255, 255, 255),
        font=RANK_FONT,
        anchor="mm",
        stroke_width=2,
        stroke_fill=(255, 225, 90),
    )

    # ------------------------------------------------------
    # Rainbow Main
    # ------------------------------------------------------

    draw._image.paste(
        rainbow,
        (
            layer_left,
            layer_top,
        ),
        mask,
    )

def draw_rank_text(
    draw: ImageDraw.ImageDraw,
    *,
    rank: str,
    center_x: int,
    center_y: int,
):
    """
    Rank文字を多重縁取りで描画する。

    SSS系の虹色描画は別Phaseで追加する。
    """

    main_color = get_rank_color(rank)

    # ------------------------------------------------------
    # SSS / SSS+ Rainbow
    # ------------------------------------------------------

    if rank in ("SSS", "SSS+"):

        draw_rainbow_rank_text(
            draw,
            rank=rank,
            center_x=center_x,
            center_y=center_y,
        )

        return

    # ------------------------------------------------------
    # Rank group
    # ------------------------------------------------------

    if rank.startswith("SSS"):

        outer_color = (255, 170, 0)
        glow_color = (255, 225, 120)
        inner_color = (255, 255, 230)

    elif rank.startswith("SS"):

        outer_color = (150, 95, 0)
        glow_color = (255, 220, 100)
        inner_color = (255, 248, 210)

    elif rank.startswith("S"):

        outer_color = (90, 100, 115)
        glow_color = (220, 230, 240)
        inner_color = (250, 250, 255)

    elif rank.startswith("AAA"):

        # Bronze
        outer_color = (115, 65, 20)
        glow_color = (235, 185, 125)
        inner_color = (255, 238, 215)

    elif rank.startswith("AA"):

        # Red
        outer_color = (135, 35, 35)
        glow_color = (255, 175, 175)
        inner_color = (255, 235, 235)

    elif rank.startswith("A"):

        # Deep Red
        outer_color = (120, 25, 25)
        glow_color = (245, 155, 155)
        inner_color = (255, 225, 225)

    elif rank.startswith("B"):

        outer_color = (150, 105, 0)
        glow_color = (255, 230, 130)
        inner_color = (255, 250, 220)

    elif rank.startswith("C"):

        outer_color = (25, 70, 150)
        glow_color = (170, 205, 255)
        inner_color = (235, 245, 255)

    elif rank.startswith("D"):

        outer_color = (80, 80, 80)
        glow_color = (205, 205, 205)
        inner_color = (240, 240, 240)

    else:

        outer_color = (55, 55, 55)
        glow_color = (175, 175, 175)
        inner_color = (225, 225, 225)

    position = (
        center_x,
        center_y,
    )

    # ------------------------------------------------------
    # Outer glow
    # ------------------------------------------------------

    draw.text(
        position,
        rank,
        fill=glow_color,
        font=RANK_FONT,
        anchor="mm",
        stroke_width=7,
        stroke_fill=glow_color,
    )

    # ------------------------------------------------------
    # Dark outer edge
    # ------------------------------------------------------

    draw.text(
        position,
        rank,
        fill=main_color,
        font=RANK_FONT,
        anchor="mm",
        stroke_width=4,
        stroke_fill=outer_color,
    )

    # ------------------------------------------------------
    # Bright inner edge
    # ------------------------------------------------------

    draw.text(
        position,
        rank,
        fill=main_color,
        font=RANK_FONT,
        anchor="mm",
        stroke_width=1,
        stroke_fill=inner_color,
    )

    # ------------------------------------------------------
    # Main
    # ------------------------------------------------------

    draw.text(
        position,
        rank,
        fill=main_color,
        font=RANK_FONT,
        anchor="mm",
    )


def draw_expert_badge(
    draw: ImageDraw.ImageDraw,
    badge_rect,
):
    """
    Version 1.3 Final

    Expert専用 Difficulty Badge

    ・全面虹グラデーション
    ・左側ダークグラデーション
    ・白ハイライト
    ・控えめ三角パターン
    ・文字が読みやすい中央帯
    ・濃紺フレーム
    """

    x1, y1, x2, y2 = badge_rect

    width = x2 - x1
    height = y2 - y1

    # ---------------------------------------------
    # Base Image
    # ---------------------------------------------

    badge = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    badge_draw = ImageDraw.Draw(badge)

    # ---------------------------------------------
    # Rainbow Colors
    # ---------------------------------------------

    rainbow = [

        (255, 205, 220),   # Red
        (255, 232, 180),   # Orange
        (255, 252, 225),   # Yellow
        (205, 248, 190),   # Green
        (185, 245, 245),   # Cyan
        (185, 220, 255),   # Blue
        (220, 205, 255),   # Violet
        (255, 220, 240),   # Pink

    ]

    # ---------------------------------------------
    # Rainbow Gradient
    # ---------------------------------------------

    for px in range(width):

        t = px / max(1, width - 1)

        pos = t * (len(rainbow) - 1)

        index = int(pos)

        if index >= len(rainbow) - 1:
            color = rainbow[-1]

        else:

            frac = pos - index

            c1 = rainbow[index]
            c2 = rainbow[index + 1]

            color = tuple(
                int(
                    c1[i]
                    + (c2[i] - c1[i]) * frac
                )
                for i in range(3)
            )

        badge_draw.line(
            (
                px,
                0,
                px,
                height,
            ),
            fill=color,
        )

    # ---------------------------------------------
    # White Highlight
    # ---------------------------------------------

    highlight = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    hdraw = ImageDraw.Draw(highlight)

    for py in range(height // 2):

        for px in range(width):

            vertical = 1 - py / (height / 2)
            horizontal = 1 - px / width

            alpha = int(
                60
                * vertical
                * (0.7 + horizontal * 0.3)
            )

            hdraw.point(
                (px, py),
                fill=(
                    255,
                    255,
                    255,
                    alpha,
                ),
            )

    badge.alpha_composite(highlight)

    # ---------------------------------------------
    # Triangle Pattern
    # ---------------------------------------------

    pattern = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    pdraw = ImageDraw.Draw(pattern)

    spacing = 22

    size = 7

    for yy in range(8, height, spacing):

        offset = 0

        if (yy // spacing) % 2:
            offset = spacing // 2

        for xx in range(offset, width, spacing):

            pdraw.polygon(

                [

                    (xx, yy),

                    (xx + size, yy + size),

                    (xx - size, yy + size),

                ],

                fill=(
                    255,
                    255,
                    255,
                    22,
                ),

            )

    badge.alpha_composite(pattern)

    # ---------------------------------------------
    # Center Gloss
    # ---------------------------------------------

    center = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    cdraw = ImageDraw.Draw(center)

    band_top = height // 2 - 7
    band_bottom = height // 2 + 7

    cdraw.rounded_rectangle(

        (
            10,
            band_top,
            width - 10,
            band_bottom,
        ),

        radius=10,

        fill=(
            255,
            255,
            255,
            38,
        ),

    )

    badge.alpha_composite(center)

    # ---------------------------------------------
    # Rounded Mask
    # ---------------------------------------------

    mask = Image.new(
        "L",
        (width, height),
        0,
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.rounded_rectangle(
        (
            0,
            0,
            width - 1,
            height - 1,
        ),
        radius=BADGE_RADIUS,
        fill=255,
    )

    # ---------------------------------------------
    # Border
    # ---------------------------------------------

    border = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    bdraw = ImageDraw.Draw(border)

    # 内側ハイライト
    bdraw.rounded_rectangle(
        (
            2,
            2,
            width - 3,
            height - 3,
        ),
        radius=max(1, BADGE_RADIUS - 2),
        outline=(255, 255, 255, 35),
        width=1,
    )

    badge.alpha_composite(border)

    # ---------------------------------------------
    # Paste
    # ---------------------------------------------

    draw._image.paste(
        badge,
        (
            x1,
            y1,
        ),
        mask,
    )

# ==========================================================
# Judge Color
# ==========================================================

JUDGE_COLOR = {

    "AMAZING+": (123, 77, 255),

    "AMAZING": (255, 95, 162),

    "PERFECT": (255, 102, 204),

    "GREAT": (255, 64, 129),

    "GOOD": (255, 152, 0),

    "BAD": (25, 118, 210),

    "MISS": (56, 142, 60),

}


# ==========================================================
# Comment Color
# ==========================================================

COMMENT_BACKGROUND = (
    252,
    252,
    255,
)

COMMENT_BORDER = (
    225,
    225,
    235,
)

COMMENT_TITLE = TITLE


# ==========================================================
# Version
# ==========================================================

APP_NAME = "Ensemble Stars!! Music"

APP_SUBTITLE = "Tap Timing Analyzer"

VERSION = "Version 1.3 Final"

COPYRIGHT = "Developed by Hapylon × ChatGPT"

# ==========================================================
# Font
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FONT_DIR = PROJECT_ROOT / "fonts"

DEFAULT_FONT = "NotoSansJP-Regular.otf"
DEFAULT_BOLD_FONT = "NotoSansJP-Bold.otf"

FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


# ==========================================================
# Font Loader
# ==========================================================

def load_font(
    size: int,
    *,
    bold: bool = False,
):
    """
    共通フォント取得
    （内部では get_font() を利用）
    """

    key = ("bold" if bold else "regular", size)

    if key in FONT_CACHE:
        return FONT_CACHE[key]

    font = get_font(
        size,
        bold=bold,
    )

    FONT_CACHE[key] = font

    return font

# ==========================================================
# Font Size
# ==========================================================

TITLE_FONT_SIZE = 50

SUBTITLE_FONT_SIZE = 22

SECTION_FONT_SIZE = 24

TEXT_FONT_SIZE = 20

SMALL_FONT_SIZE = 16

VALUE_FONT_SIZE = 24

LARGE_VALUE_FONT_SIZE = 42

RANK_FONT_SIZE = 72

FOOTER_FONT_SIZE = 16

COMMENT_FONT_SIZE = 16

# ==========================================================
# Font Utility
# ==========================================================

def get_font(
    size: int,
    bold: bool = False,
):
    """
    日本語対応フォント取得
    """

    if bold:
        candidates = [
            FONT_DIR / DEFAULT_BOLD_FONT,
            Path("C:/Windows/Fonts/meiryob.ttc"),
            Path("C:/Windows/Fonts/YuGothB.ttc"),
            Path("C:/Windows/Fonts/msgothic.ttc"),
        ]
    else:
        candidates = [
            FONT_DIR / DEFAULT_FONT,
            Path("C:/Windows/Fonts/meiryo.ttc"),
            Path("C:/Windows/Fonts/YuGothR.ttc"),
            Path("C:/Windows/Fonts/msgothic.ttc"),
        ]

    for path in candidates:
        try:
            return ImageFont.truetype(
                str(path),
                size,
            )
        except OSError:
            continue

    return ImageFont.load_default()

def clear_font_cache():
    """
    フォントキャッシュ初期化
    """

    FONT_CACHE.clear()

# ==========================================================
# Font Instance
# ==========================================================

TITLE_FONT = load_font(
    TITLE_FONT_SIZE,
    bold=True,
)

SUBTITLE_FONT = load_font(
    SUBTITLE_FONT_SIZE,
)

SECTION_FONT = load_font(
    SECTION_FONT_SIZE,
    bold=True,
)

TEXT_FONT = load_font(
    TEXT_FONT_SIZE,
)

DIFFICULTY_FONT = load_font(
    23,
    bold=True,
)

SMALL_FONT = load_font(
    SMALL_FONT_SIZE,
)

RESULT_TITLE_FONT = load_font(
    34,
    bold=True,
)

# ==========================================================
# Pie Chart Font
# ==========================================================

PIE_NAME_FONT = load_font(
    15,
    bold=True,
)

PIE_VALUE_FONT = load_font(
    18,
    bold=True,
)

PIE_PERCENT_FONT = load_font(
    14,
)

VALUE_FONT = load_font(
    VALUE_FONT_SIZE,
    bold=True,
)

STAR_FONT = load_font(
    21,
    bold=True,
)

LARGE_VALUE_FONT = load_font(
    LARGE_VALUE_FONT_SIZE,
    bold=True,
)

RANK_FONT = load_font(
    RANK_FONT_SIZE,
    bold=True,
)

FOOTER_FONT = load_font(
    FOOTER_FONT_SIZE,
)

COMMENT_FONT = load_font(
    COMMENT_FONT_SIZE,
)

ACHIEVEMENT_VALUE_FONT = load_font(
    46,
    bold=True,
)

# ==========================================================
# Rating Icon Font
# ==========================================================

RATING_ICON_FONT = load_font(
    22,
    bold=True,
)

# ==========================================================
# Rating Layout
# ==========================================================

RATING_LEFT = 18
RATING_ICON_OFFSET = 0

RATING_TITLE_Y = 10
RATING_SUBTITLE_Y = 11
RATING_DESC_Y = 36
RATING_VALUE_Y = 49
RATING_ICON_Y = 76

RATING_PRECISION_SUBTITLE_X = 128
RATING_BALANCE_SUBTITLE_X = 118

# ==========================================================
# Comment Layout
# ==========================================================

COMMENT_LEFT_PADDING = 30

COMMENT_PLAY_STYLE_LABEL_TOP = 12

COMMENT_BADGE_TOP = 96

COMMENT_BADGE_HEIGHT = 52

COMMENT_BADGE_TEXT_Y = 22

COMMENT_COMMENT_LABEL_TOP = 124

COMMENT_TEXT_TOP = 186

COMMENT_BOTTOM_PADDING = 20

# ==========================================================
# Text Utility
# ==========================================================

def text_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
) -> tuple[int, int]:
    """
    文字列サイズ取得
    """

    if not text:
        return (0, 0)

    left, top, right, bottom = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return (
        right - left,
        bottom - top,
    )


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    start_size: int,
    min_size: int = 16,
    *,
    bold: bool = False,
):
    """
    指定幅に収まるフォントを返す
    """

    size = start_size

    while size >= min_size:

        font = get_font(
            size,
            bold=bold,
        )

        width, _ = text_size(
            draw,
            text,
            font,
        )

        if width <= max_width:
            return font

        size -= 1

    return get_font(
        min_size,
        bold=bold,
    )

# ==========================================================
# Wrap Text
# ==========================================================

def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
    max_width: int,
):
    """
    横幅で自動改行

    Version 1.3 Final
    日本語の簡易禁則処理に対応。
    句読点や閉じ括弧などが行頭に単独で来ることを防ぐ。
    """

    if not text:
        return [""]

    # 行頭に置かない文字
    prohibited_line_start = set(
        "、。，．！？!?"
        ")]}）］｝】〕〉》」』】"
        "ぁぃぅぇぉっゃゅょゎ"
        "ァィゥェォッャュョヮ"
        "ー"
    )

    lines = []
    current = ""

    for ch in text:

        # 明示的な改行を維持
        if ch == "\n":

            lines.append(current)
            current = ""
            continue

        candidate = current + ch

        width, _ = text_size(
            draw,
            candidate,
            font,
        )

        if width <= max_width:
            current = candidate
            continue

        # --------------------------------------------------
        # Japanese Kinsoku Processing
        # --------------------------------------------------

        # ch が句読点などの場合、
        # ch だけを次行に送らず現在行へ残す。
        if (
            ch in prohibited_line_start
            and current
        ):
            current += ch
            lines.append(current)
            current = ""
            continue

        # 通常の折り返し
        if current:
            lines.append(current)

        current = ch

    if current:
        lines.append(current)

    return lines

# ==========================================================
# Decorative Star
# ==========================================================

def draw_four_point_star(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    outer: int = 18,
    inner: int = 5,
    fill=TITLE,
):
    """
    フォントに依存しない四芒星を描画する。

    Unicodeの ✦ / ✧ は環境によって
    □ と表示されるため、Pillowの図形として描画する。
    """

    points = [
        (cx, cy - outer),
        (cx + inner, cy - inner),
        (cx + outer, cy),
        (cx + inner, cy + inner),
        (cx, cy + outer),
        (cx - inner, cy + inner),
        (cx - outer, cy),
        (cx - inner, cy - inner),
    ]

    draw.polygon(
        points,
        fill=fill,
    )

# ==========================================================
# Center Text
# ==========================================================

def draw_center_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font,
    color,
):
    """
    横中央描画
    """

    width, _ = text_size(
        draw,
        text,
        font,
    )

    x = (CARD_WIDTH - width) // 2

    draw.text(
        (
            x,
            y,
        ),
        text,
        fill=color,
        font=font,
    )

# ==========================================================
# Right Text
# ==========================================================

def draw_right_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    font,
    color=TEXT,
):
    """
    右寄せ描画
    """

    draw.text(
        (
            x,
            y,
        ),
        text,
        fill=color,
        font=font,
        anchor="ra",
    )


def draw_left_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    font,
    color=TEXT,
):
    """
    左寄せ描画
    """

    draw.text(
        (
            x,
            y,
        ),
        text,
        fill=color,
        font=font,
    )

# ==========================================================
# Multiline Utility
# ==========================================================

def draw_multiline_text(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    x: int,
    y: int,
    font,
    color=TEXT,
    line_spacing: int = 10,
    max_bottom=None,
):
    """
    複数行描画
    """

    current_y = y

    for line in lines:

        _, height = text_size(
            draw,
            line,
            font,
        )

        if (
            max_bottom is not None
            and current_y + height > max_bottom
        ):
            break

        draw.text(
            (
                x,
                current_y,
            ),
            line,
            fill=color,
            font=font,
        )

        current_y += height + line_spacing

    return current_y

# ==========================================================
# Card Utility
# ==========================================================

def draw_card(
    draw: ImageDraw.ImageDraw,
    rect,
    *,
    fill=(251,252,254),
    outline=(204,208,220),
    radius=CARD_RADIUS,
    width=CARD_BORDER,
):
    """
    共通カード描画
    """

    draw.rounded_rectangle(
        rect,
        radius=radius,
        fill=fill,
        outline=outline,
        width=width,
    )

    # ------------------------------------------------------
    # Top Highlight Gradient
    # ------------------------------------------------------

    x1, y1, x2, y2 = rect

    for i in range(24):

        alpha = int(18 * (1 - i / 24))

        draw.line(
            (
                x1 + radius,
                y1 + i,
                x2 - radius,
                y1 + i,
            ),
            fill=(
                255 - alpha,
                255 - alpha,
                255,
            ),
            width=1,
        )

    x1, y1, x2, y2 = rect

    # ------------------------------------------------------
    # Glass Highlight
    # ------------------------------------------------------

    draw.arc(

        (

            x1 + 2,

            y1 + 2,

            x2 - 2,

            y2 - 2,

        ),

        start=180,

        end=360,

        fill=(255,255,255),

        width=1,

    )

    draw.line(

        (

            x1 + 18,

            y1 + 2,

            x2 - 18,

            y1 + 2,

        ),

        fill=(255,255,255),

    )

    draw.line(

        (

            x1 + 28,

            y1 + 3,

            x2 - 28,

            y1 + 3,

        ),

        fill=(250,250,252),

    )

    # ------------------------------------------------------
    # Top Highlight
    # ------------------------------------------------------

    x1, y1, x2, y2 = rect

    draw.line(

        (

            x1 + 18,

            y1 + 1,

            x2 - 18,

            y1 + 1,

        ),

        fill=(255,255,255),

        width=1,

    )

    draw.line(

        (

            x1 + 26,

            y1 + 2,

            x2 - 26,

            y1 + 2,

        ),

        fill=(252,252,252),

        width=1,

    )

    draw.line(

    (
    x1 + 18,
    y1 + 4,
    x2 - 18,
    y1 + 4,
    ),

    fill=(255,255,255),

    width=2,
    )

    draw.line(

    (
    x1 + 22,
    y1 + 6,
    x2 - 22,
    y1 + 6,
    ),

    fill=(248,248,250),

    width=1,
    )

    draw.arc(

        (
            x1+1,
            y1+1,
            x2-1,
            y2-1,
        ),

        180,

        270,

        fill=(255,255,255),

        width=2,

    )

    draw.arc(

        (
            x1+2,
            y1+2,
            x2-2,
            y2-2,
        ),

        270,

        360,

        fill=(252,252,255),

        width=1,

    )

def draw_card_shadow(
    draw: ImageDraw.ImageDraw,
    rect,
):
    """
    カード影
    """

    x1, y1, x2, y2 = rect

    shadow = Image.new(
        "RGBA",
        (
            x2-x1+20,
            y2-y1+20,
        ),
        (0,0,0,0),
    )

    sdraw = ImageDraw.Draw(shadow)

    sdraw.rounded_rectangle(

        (
            8,
            8,
            x2-x1+8,
            y2-y1+8,
        ),

        radius=CARD_RADIUS,

        fill=(145,155,175,42),

    )

    shadow = shadow.filter(
        ImageFilter.GaussianBlur(18)
    )

    draw._image.alpha_composite(
        shadow,
        (
            x1-6,
            y1-2,
        ),
    )


def draw_card_with_shadow(
    draw: ImageDraw.ImageDraw,
    rect,
):
    """
    影付きカード
    """

    draw_card_shadow(
        draw,
        rect,
    )

    draw_card(
        draw,
        rect,
    )

# ==========================================================
# Card Geometry
# ==========================================================

def card_inner_rect(
    rect,
    padding: int = INNER_PADDING,
):
    """
    カード内側矩形
    """

    x1, y1, x2, y2 = rect

    return (
        x1 + padding,
        y1 + padding,
        x2 - padding,
        y2 - padding,
    )


def card_width(rect):

    return rect[2] - rect[0]


def card_height(rect):

    return rect[3] - rect[1]


def card_content_top(
    rect,
):
    """
    タイトル下開始位置
    """

    return rect[1] + 70

# ==========================================================
# Card Header
# ==========================================================

def draw_card_title(
    draw: ImageDraw.ImageDraw,
    rect,
    title: str,
    *,
    centered: bool = False,
):
    """
    カードタイトル
    """

    x1, y1, x2, _ = rect

    if centered:
        center_x = (x1 + x2) // 2

        draw.text(
            (
                center_x,
                y1 + 18,
            ),
            title,
            fill=TITLE,
            font=SECTION_FONT,
            anchor="ma",
        )
    else:
        draw.text(
            (
                x1 + 20,
                y1 + 18,
            ),
            title,
            fill=TITLE,
            font=SECTION_FONT,
        )


def draw_card_divider(
    draw: ImageDraw.ImageDraw,
    rect,
):
    """
    タイトル下区切り線
    """

    x1, y1, x2, _ = rect

    draw.line(
        (
            x1 + 18,
            y1 + 62,
            x2 - 18,
            y1 + 62,
        ),
        fill=LINE,
        width=2,
    )


def draw_card_header(
    draw: ImageDraw.ImageDraw,
    rect,
    title: str,
    *,
    centered: bool = False,
):
    """
    カードヘッダー
    """

    draw_card_title(
        draw,
        rect,
        title,
        centered=centered,
    )

    draw_card_divider(
        draw,
        rect,
    )

# ==========================================================
# Label Utility
# ==========================================================

def draw_label_value(
    draw: ImageDraw.ImageDraw,
    *,
    x: int,
    y: int,
    label: str,
    value: str,
):
    """
    ラベル＋値
    """

    draw.text(
        (
            x,
            y,
        ),
        label,
        fill=TITLE,
        font=TEXT_FONT,
    )

    draw_right_text(
        draw,
        value,
        x + 260,
        y,
        VALUE_FONT,
    )

# ==========================================================
# Grade Utility
# ==========================================================

GRADE_STAR = {

    # SSS / SS / S
    "SSS": "★★★★★★",
    "SS":  "★★★★★★",
    "S":   "★★★★★★",

    # AAA / AA / A
    "AAA": "★★★★★☆",
    "AA":  "★★★★★☆",
    "A":   "★★★★★☆",

    # BBB / BB / B
    "BBB": "★★★★☆☆",
    "BB":  "★★★★☆☆",
    "B":   "★★★★☆☆",

    # CCC / CC / C
    "CCC": "★★★☆☆☆",
    "CC":  "★★★☆☆☆",
    "C":   "★★★☆☆☆",

    # D
    "D":   "★★☆☆☆☆",

    # E
    "E":   "★☆☆☆☆☆",

    # F
    "F":   "☆☆☆☆☆☆",
}

GRADE_DIAMOND = {

    # SSS / SS / S
    "SSS": "◆◆◆◆◆◆",
    "SS":  "◆◆◆◆◆◆",
    "S":   "◆◆◆◆◆◆",

    # AAA / AA / A
    "AAA": "◆◆◆◆◆◇",
    "AA":  "◆◆◆◆◆◇",
    "A":   "◆◆◆◆◆◇",

    # BBB / BB / B
    "BBB": "◆◆◆◆◇◇",
    "BB":  "◆◆◆◆◇◇",
    "B":   "◆◆◆◆◇◇",

    # CCC / CC / C
    "CCC": "◆◆◆◇◇◇",
    "CC":  "◆◆◆◇◇◇",
    "C":   "◆◆◆◇◇◇",

    # D
    "D":   "◆◆◇◇◇◇",

    # E
    "E":   "◆◇◇◇◇◇",

    # F
    "F":   "◇◇◇◇◇◇",
}

def star_string(
    grade: str,
):
    """
    Precision用★
    """

    return GRADE_STAR.get(
        grade,
        "",
    )


def diamond_string(
    grade: str,
):
    """
    Balance用◆
    """

    return GRADE_DIAMOND.get(
        grade,
        "",
    )

def split_star_string(grade: str):
    """
    Precision評価を
    塗り★・空き☆へ分離
    """

    stars = GRADE_STAR.get(grade, "")

    filled = stars.count("★")

    return (
        "★" * filled,
        "☆" * (6 - filled),
    )

def split_diamond_string(grade: str):
    """
    Balance評価を
    塗り◆・空き◇へ分離
    """

    diamonds = GRADE_DIAMOND.get(grade, "")

    filled = diamonds.count("◆")

    return (
        "◆" * filled,
        "◇" * (6 - filled),
    )

# ==========================================================
# Canvas
# ==========================================================

def create_canvas():
    """
    Result Cardキャンバス生成
    """

    image = Image.new(
        "RGBA",
        (
            CARD_WIDTH,
            CARD_HEIGHT,
        ),
        BACKGROUND + (255,),
    )

    return image


def create_draw(
    image: Image.Image,
):
    """
    ImageDraw生成
    """

    return ImageDraw.Draw(image)

# ==========================================================
# Background
# ==========================================================

def draw_background(
    image: Image.Image,
    *,
    ranking_title: str | None = None,
):
    """
    背景描画
    """

    x1 = CARD_MARGIN
    y1 = CARD_MARGIN
    x2 = CARD_WIDTH - CARD_MARGIN
    y2 = CARD_HEIGHT - CARD_MARGIN

    width = x2 - x1
    height = y2 - y1

    plate = Image.new(
        "RGBA",
        (width, height),
    )

    plate_draw = ImageDraw.Draw(plate)

    style = RANKING_PLATE_STYLES.get(ranking_title)

    if style is None:
        style = {
            "top": (250, 250, 252),
            "middle": (255, 255, 255),
            "bottom": (248, 248, 251),
            "line": (225, 225, 230),
            "highlight": (255, 255, 255),
            "crystal": (235, 235, 240),
        }

    # ------------------------------------------------------
    # Ranking-specific plate base
    # ------------------------------------------------------

    if style.get("mode") == "rainbow":
        # Rainbow is a true multi-color prism gradient rather than
        # the normal three-stop vertical gradient used by other ranks.
        colors = style["rainbow_colors"]
        segments = len(colors) - 1

        for y in range(height):
            # Vertical prism flow with a slight horizontal phase shift.
            base_t = y / max(height - 1, 1)

            for x in range(width):
                phase = (x / max(width - 1, 1)) * 0.18
                position = ((base_t + phase) % 1.0) * segments
                index = min(int(position), segments - 1)
                fraction = position - index
                c1 = colors[index]
                c2 = colors[index + 1]

                color = tuple(
                    int(c1[i] + (c2[i] - c1[i]) * fraction)
                    for i in range(3)
                )
                plate_draw.point((x, y), fill=color)
    else:
        for y in range(height):
            t = y / max(height - 1, 1)

            if t < 0.5:
                ratio = t / 0.5
                start = style["top"]
                end = style["middle"]
            else:
                ratio = (t - 0.5) / 0.5
                start = style["middle"]
                end = style["bottom"]

            r = int(start[0] + (end[0] - start[0]) * ratio)
            g = int(start[1] + (end[1] - start[1]) * ratio)
            b = int(start[2] + (end[2] - start[2]) * ratio)

            plate_draw.line(
                (0, y, width, y),
                fill=(r, g, b),
            )

    mask = Image.new(
        "L",
        (width, height),
        0,
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.rounded_rectangle(

        (
            0,
            0,
            width,
            height,
        ),

        radius=34,

        fill=255,

    )

    image.paste(

        plate,

        (
            x1,
            y1,
        ),

        mask,

    )

    draw = ImageDraw.Draw(image)

    # ------------------------------------------------------
    # Ranking Plate Decoration
    # ------------------------------------------------------

    if ranking_title in RANKING_PLATE_STYLES:

        # Ranking-specific outer border
        draw.rounded_rectangle(
            (
                x1,
                y1,
                x2,
                y2,
            ),
            radius=34,
            outline=style["line"],
            width=2,
        )

        # Inner white highlight
        draw.rounded_rectangle(
            (
                x1 + 3,
                y1 + 3,
                x2 - 3,
                y2 - 3,
            ),
            radius=31,
            outline=style["highlight"],
            width=1,
        )

        # --------------------------------------------------
        # Subtle Crystal Facets
        # --------------------------------------------------

        crystal = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0),
        )

        crystal_draw = ImageDraw.Draw(crystal)

        crystal_draw.polygon(
            [
                (80, 80),
                (360, 20),
                (260, height - 80),
                (20, height - 220),
            ],
            fill=(*style["crystal"], 14),
        )

        crystal_draw.polygon(
            [
                (width - 40, 80),
                (width - 300, 20),
                (width - 420, height - 120),
                (width - 80, height - 260),
            ],
            fill=(*style["accent"], 12),
        )

        crystal_draw.polygon(
            [
                (width // 2 - 40, 0),
                (width // 2 + 100, 0),
                (width // 2 + 20, height),
                (width // 2 - 180, height),
            ],
            fill=(*style["highlight"], 7),
        )

        crystal_draw.line(
            (
                100,
                160,
                330,
                40,
            ),
            fill=(*style["highlight"], 35),
            width=2,
        )

        crystal_draw.line(
            (
                width - 100,
                height - 160,
                width - 330,
                height - 40,
            ),
            fill=(*style["highlight"], 30),
            width=2,
        )

        crystal = crystal.filter(
            ImageFilter.GaussianBlur(1)
        )

        image.paste(
            crystal,
            (
                x1,
                y1,
            ),
            crystal,
        )

    # ------------------------------------------------------
    # Hairline Texture
    # ------------------------------------------------------

    texture_color = style.get("accent", (242, 243, 246))

    for x in range(
        x1,
        x2,
        2,
    ):
        alpha = 0.10 + ((x - x1) % 6) * 0.015

        # Blend the ranking tint very lightly into the existing
        # hairline texture so the plate remains clean and readable.
        texture = tuple(
            int(255 * (1 - alpha) + channel * alpha)
            for channel in texture_color
        )

        draw.line(
            (x, y1, x, y2),
            fill=texture,
        )
    
    # ------------------------------------------------------
    # Soft Highlight
    # ------------------------------------------------------

    highlight = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    highlight_draw = ImageDraw.Draw(
        highlight,
    )

    highlight_draw.ellipse(
        (
            -260,
            -180,
            700,
            340,
        ),

        fill=(255, 255, 255, 38),

    )

    highlight = highlight.filter(
        ImageFilter.GaussianBlur(80)
    )

    image.paste(

        highlight,

        (
            x1,
            y1,
        ),

        highlight,

    )

    # ------------------------------------------------------
    # Diagonal Premium Highlight
    # ------------------------------------------------------

    shine = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0),
    )

    shine_draw = ImageDraw.Draw(shine)

    shine_draw.polygon(

        [

            (120, 0),

            (520, 0),

            (220, height),

            (-180, height),

        ],

        fill=(255,255,255,12),

    )

    shine = shine.filter(
        ImageFilter.GaussianBlur(70)
    )

    image.paste(

        shine,

        (x1,y1),

        shine,

    )

    reflection = Image.new(
        "RGBA",
        (width, height),
        (0,0,0,0),
    )

    rdraw = ImageDraw.Draw(reflection)

    rdraw.polygon(

        [

            (620,-80),

            (980,0),

            (820,height),

            (420,height),

        ],

        fill=(255,255,255,12),

    )

    reflection = reflection.filter(
        ImageFilter.GaussianBlur(110)
    )

    image.paste(
        reflection,
        (x1,y1),
        reflection,
    )

    reflection2 = Image.new(
        "RGBA",
        (width,height),
        (0,0,0,0),
    )

    r2 = ImageDraw.Draw(reflection2)

    r2.polygon(

        [

            (760,-80),

            (1080,40),

            (930,height),

            (600,height),

        ],

        fill=(255,255,255,10),

    )

    reflection2 = reflection2.filter(
        ImageFilter.GaussianBlur(120)
    )

    image.paste(
        reflection2,
        (x1,y1),
        reflection2,
    )

# ==========================================================
# Initialize Card
# ==========================================================

def create_card(
    *,
    ranking_title: str | None = None,
):
    """
    Result Card生成
    """

    image = create_canvas()

    draw_background(
        image,
        ranking_title=ranking_title,
    )

    draw = create_draw(
        image,
    )

    draw_header(
        draw,
    )

    return image, draw

# ==========================================================
# Header
# ==========================================================

def draw_header_card(
    draw: ImageDraw.ImageDraw,
):
    """
    Header専用カード
    Version 1.3 Final
    """

    draw_card_shadow(
        draw,
        HEADER_RECT,
    )

    draw_card(

        draw,

        HEADER_RECT,

        fill=(251, 249, 255),

        outline=(206, 194, 232),

    )

    x1, y1, _, _ = HEADER_RECT

    sparkles = [

        (90, 24, 3, (255,255,255)),
        (170,48,2,(255,247,205)),
        (305,28,3,(238,230,255)),
        (520,36,3,(255,255,255)),
        (670,22,2,(255,247,205)),
        (760,50,3,(235,228,255)),
        (705, 18, 2, (255,255,255)),

    ]

    # Gold Light

    draw.line(

        (
            x1+70,
            y1+12,
            HEADER_RECT[2]-70,
            y1+12,
        ),

        fill=(255,245,210),

        width=2,
    )

    for sx, sy, r, color in sparkles:

        draw.ellipse(

            (
                x1 + sx - r,
                y1 + sy - r,
                x1 + sx + r,
                y1 + sy + r,
            ),

            fill=color,

        )

def draw_header(
    draw: ImageDraw.ImageDraw,
):
    """
    Header Card
    Version 1.3 Final
    """

    draw_header_card(
        draw,
    )

    # ------------------------------------------------------
    # Title
    # ------------------------------------------------------

    title_text = APP_NAME

    # タイトルを少し上へ
    title_y = HEADER_RECT[1] + 1

    title_width, _ = text_size(
        draw,
        title_text,
        TITLE_FONT,
    )

    title_x = (
        CARD_WIDTH - title_width
    ) // 2

    # ------------------------------------------------------
    # Decorative Stars
    #
    # 元の
    #     ✦✧ Ensemble Stars!! Music ✧✦
    # をフォント非依存の図形で再現する。
    # ------------------------------------------------------

    star_y = title_y + 31

    # 大きい星
    large_outer = 15
    large_inner = 5

    # 小さい星
    small_outer = 8
    small_inner = 3

    # タイトルから星までの距離
    large_gap = 48
    small_gap = 22

    # 左側
    left_large_x = title_x - large_gap
    left_small_x = title_x - small_gap

    # 右側
    right_small_x = title_x + title_width + small_gap
    right_large_x = title_x + title_width + large_gap

    # ------------------------------------------------------
    # Star Shadow
    # ------------------------------------------------------

    star_shadow = (188, 188, 198)

    # Left large
    draw_four_point_star(
        draw,
        left_large_x + 2,
        star_y + 2,
        outer=large_outer,
        inner=large_inner,
        fill=star_shadow,
    )

    # Left small
    draw_four_point_star(
        draw,
        left_small_x + 2,
        star_y + 2,
        outer=small_outer,
        inner=small_inner,
        fill=star_shadow,
    )

    # Right small
    draw_four_point_star(
        draw,
        right_small_x + 2,
        star_y + 2,
        outer=small_outer,
        inner=small_inner,
        fill=star_shadow,
    )

    # Right large
    draw_four_point_star(
        draw,
        right_large_x + 2,
        star_y + 2,
        outer=large_outer,
        inner=large_inner,
        fill=star_shadow,
    )

    # ------------------------------------------------------
    # Main Stars
    # ------------------------------------------------------

    # Left large
    draw_four_point_star(
        draw,
        left_large_x,
        star_y,
        outer=large_outer,
        inner=large_inner,
        fill=TITLE,
    )

    # Left small
    draw_four_point_star(
        draw,
        left_small_x,
        star_y,
        outer=small_outer,
        inner=small_inner,
        fill=TITLE,
    )

    # Right small
    draw_four_point_star(
        draw,
        right_small_x,
        star_y,
        outer=small_outer,
        inner=small_inner,
        fill=TITLE,
    )

    # Right large
    draw_four_point_star(
        draw,
        right_large_x,
        star_y,
        outer=large_outer,
        inner=large_inner,
        fill=TITLE,
    )

    # ------------------------------------------------------
    # Title Shadow
    # ------------------------------------------------------

    draw.text(
        (
            title_x,
            title_y + 2,
        ),
        title_text,
        fill=(188, 188, 198),
        font=TITLE_FONT,
    )

    # ------------------------------------------------------
    # Title Main
    # ------------------------------------------------------

    draw.text(
        (
            title_x,
            title_y,
        ),
        title_text,
        fill=TITLE,
        font=TITLE_FONT,
    )

    # ------------------------------------------------------
    # Subtitle
    # ------------------------------------------------------

    draw_center_text(
        draw,
        APP_SUBTITLE,
        HEADER_RECT[1] + 52,
        SUBTITLE_FONT,
        (96, 98, 120),
    )

    # ------------------------------------------------------
    # Bottom Accent Line
    # ------------------------------------------------------

    x1, y1, x2, _ = HEADER_RECT

    draw.line(

        (
            x1 + 30,
            y1 + 82,
            x2 - 30,
            y1 + 82,
        ),

        fill=(205, 200, 236),

        width=2,

    )

    # ------------------------------------------------------
    # Header Top Highlight
    # ------------------------------------------------------

    x1, y1, x2, _ = HEADER_RECT

    draw.line(

        (

            x1 + 22,

            y1 + 2,

            x2 - 22,

            y1 + 2,

        ),

        fill=(255,255,255),

        width=1,

    )

    draw.line(

        (

            x1 + 30,

            y1 + 3,

            x2 - 30,

            y1 + 3,

        ),

        fill=(252,252,255),

        width=1,

    )

# ==========================================================
# Song Card
# ==========================================================

def draw_song_card(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    music: str,
    difficulty: str,
    level: str,
):
    """
    Song Card
    """

    draw_card_with_shadow(
        draw,
        SONG_RECT,
    )

    draw_card_header(
        draw,
        SONG_RECT,
        "楽曲情報",
    )

    inner = card_inner_rect(
        SONG_RECT,
    )

    x1, y1, x2, y2 = inner

    y = SONG_RECT[1] + 51

    # ------------------------------------------------------
    # Song Title
    # ------------------------------------------------------

    song_font = fit_text(
        draw,
        music,
        max_width=(x2 - x1) - 20,
        start_size=30,
        min_size=14,
        bold=True,
    )

    # 曲名は常に1行。幅に収まるまでフォントだけ縮小する。
    # wrap_text() は使用しない。
    draw.text(
        (
            x1,
            SONG_RECT[1] + 57,
        ),
        music,
        fill=TEXT,
        font=song_font,
    )

    badge_color = {

        "Easy": (30,136,229),      # 青

        "Normal": (253,216,53),    # 黄

        "Hard": (229,57,53),       # 赤

        "Expert": (229,57,53),            # 虹は別描画

        "Special": (255,95,162),   # 桃

    }.get(
        difficulty,
        TITLE,
    )

    badge_margin = 20

    # 楽曲名の下に固定配置し、タイトルと難易度バッジを重ねない。
    # 下端側へ少し移動し、短い楽曲名との間隔を確保する。
    badge_y = SONG_RECT[3] - BADGE_HEIGHT - 5

    # ------------------------------------------------------
    # Difficulty Badge
    # ------------------------------------------------------

    badge_rect = (
        x1,
        badge_y,
        x1 + DIFFICULTY_BADGE_WIDTH,
        badge_y + BADGE_HEIGHT,
    )

    if difficulty == "Expert":

        draw_expert_badge(
            draw,
            badge_rect,
        )

    else:

        draw.rounded_rectangle(
            badge_rect,
            radius=BADGE_RADIUS,
            fill=badge_color,
        )

    difficulty_text = difficulty.upper()

    if difficulty == "Expert":
        text_color = WHITE
        stroke_fill = (35, 35, 35)
        stroke_width = 2

    elif difficulty == "Special":
        text_color = WHITE
        stroke_fill = (35, 35, 35)
        stroke_width = 2

    else:
        text_color = WHITE
        stroke_fill = (45, 45, 45)
        stroke_width = 1

    draw.text(

        (

            x1 + DIFFICULTY_BADGE_WIDTH // 2,
            badge_y + BADGE_HEIGHT // 2,

        ),

        difficulty_text,

        fill=text_color,

        font=DIFFICULTY_FONT,

        anchor="mm",

        stroke_width=stroke_width,

        stroke_fill=stroke_fill,

    )

    # ------------------------------------------------------
    # Level Badge
    # ------------------------------------------------------

    level_text = f"Lv.{level}"

    text_width, _ = text_size(
        draw,
        level_text,
        TEXT_FONT,
    )

    badge_left = (
        x1
        + DIFFICULTY_BADGE_WIDTH
        + LEVEL_BADGE_GAP
    )

    badge_width = max(
        LEVEL_BADGE_MIN_WIDTH,
        text_width + 48,
    )

    draw.rounded_rectangle(

        (
            badge_left,
            badge_y,
            badge_left + badge_width,
            badge_y + BADGE_HEIGHT,
        ),

        radius=BADGE_RADIUS,

        fill=(245,245,245),

        outline=LINE,

    )

    draw.text(
        (
            badge_left + badge_width // 2,
            badge_y + BADGE_HEIGHT // 2,
        ),
        level_text,
        fill=TEXT,
        font=TEXT_FONT,
        anchor="mm",
    )

# ==========================================================
# Pie Chart
# ==========================================================

def draw_pie_chart(
    draw: ImageDraw.ImageDraw,
    rect,
    judges: dict,
):

    total = sum(judges.values())

    if total == 0:
        return

    start = -90

    for name, value in judges.items():

        if value <= 0:
            continue

        angle = value / total * 360

        draw.pieslice(

            rect,

            start,

            start + angle,

            fill=JUDGE_COLOR.get(
                name,
                LINE,
            ),

            outline=WHITE,

        )

        # ------------------------------
        # 円グラフ中央文字
        # ------------------------------

        percent = value / total * 100

        # 小さい扇形も少し表示しやすくする
        if angle >= 24:

            center_angle = math.radians(
                start + angle / 2
            )

            cx = (rect[0] + rect[2]) / 2
            cy = (rect[1] + rect[3]) / 2

            # 少し外側へ
            r = (rect[2] - rect[0]) * 0.25

            tx = cx + math.cos(center_angle) * r
            ty = cy + math.sin(center_angle) * r

            shadow = (0, 0, 0)

            # ------------------------------
            # 判定名
            # ------------------------------

            for dx, dy in [(1, 1)]:
                draw.text(
                    (tx + dx, ty - 28 + dy),
                    name,
                    fill=shadow,
                    font=PIE_NAME_FONT,
                    anchor="mm",
                )

            draw.text(
                (tx, ty - 28),
                name,
                fill=WHITE,
                font=PIE_NAME_FONT,
                anchor="mm",
            )

            # ------------------------------
            # 件数
            # ------------------------------

            for dx, dy in [(1, 1)]:
                draw.text(
                    (tx + dx, ty + dy),
                    f"{value:,}",
                    fill=shadow,
                    font=PIE_VALUE_FONT,
                    anchor="mm",
                )

            draw.text(
                (tx, ty),
                f"{value:,}",
                fill=WHITE,
                font=PIE_VALUE_FONT,
                anchor="mm",
            )

            # ------------------------------
            # 割合
            # ------------------------------

            for dx, dy in [(1, 1)]:
                draw.text(
                    (tx + dx, ty + 28 + dy),
                    f"{percent:.1f}%",
                    fill=shadow,
                    font=PIE_PERCENT_FONT,
                    anchor="mm",
                )

            draw.text(
                (tx, ty + 28),
                f"{percent:.1f}%",
                fill=WHITE,
                font=PIE_PERCENT_FONT,
                anchor="mm",
            )

        start += angle

# ==========================================================
# Judge List
# ==========================================================

def draw_judge_list(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    judges: dict[str, int],
):

    total = sum(judges.values())

    row_height = 34

    for name, value in judges.items():

        color = JUDGE_COLOR.get(name, TEXT)

        draw.rounded_rectangle(
            (
                x,
                y - 4,
                x + min(395, LEFT_WIDTH - 60),
                y +30,
            ),
            radius=10,
            fill=(252, 252, 252),
            outline=LINE,
        )

        draw.text(
            (x + 10, y),
            "●",
            fill=color,
            font=TEXT_FONT,
        )

        draw_left_text(
            draw,
            name,
            x + JUDGE_NAME_X,
            y,
            TEXT_FONT,
        )

        draw_right_text(
            draw,
            str(value),
            x + JUDGE_VALUE_X,
            y,
            TEXT_FONT,
        )

        percent = (
            value / total * 100
            if total
            else 0
        )

        draw_right_text(
            draw,
            f"{percent:.1f}%",
            x + JUDGE_PERCENT_X,
            y,
            SMALL_FONT,
            SUBTEXT,
        )

        y += row_height

# ==========================================================
# Judge List Layout
# ==========================================================

JUDGE_NAME_X = 35
JUDGE_VALUE_X = 300
JUDGE_PERCENT_X = 390

# ==========================================================
# Left Panel
# ==========================================================

def draw_left_panel(
    draw: ImageDraw.ImageDraw,
    judges: dict,
    total_notes: int,
):

    draw_card_with_shadow(
        draw,
        LEFT_RECT,
    )

    x1, y1, x2, y2 = card_inner_rect(
        LEFT_RECT,
    )

    # ------------------------------------------------------
    # Section Title
    # ------------------------------------------------------

    draw_left_text(
        draw,
        "判定内訳（推定）",
        x1,
        y1,
        SECTION_FONT,
        TITLE,
    )

    # ------------------------------------------------------
    # Pie Chart
    # ------------------------------------------------------

    pie_left = (x1 + x2 - PIE_SIZE) // 2

    pie_top = card_content_top(LEFT_RECT) + 2

    pie = (
        pie_left,
        pie_top,
        pie_left + PIE_SIZE,
        pie_top + PIE_SIZE,
    )

    draw_pie_chart(
        draw,
        pie,
        judges,
    )

    # ------------------------------------------------------
    # Judge List
    # ------------------------------------------------------

    draw_judge_list(
        draw,
        x1,
        pie[3] + PIE_LIST_GAP,
        judges,
    )

    # ------------------------------------------------------
    # Total Notes Card
    # ------------------------------------------------------

    notes_rect = (

        x1 + 2,

        y2 - 70,

        x2 - 22,

        y2 - 12,
    )

    draw.rounded_rectangle(

        notes_rect,

        radius=14,

        fill=(250, 251, 255),

        outline=(218, 221, 230),

        width=1,

    )

    # ------------------------------------------------------
    # Label
    # ------------------------------------------------------

    draw.text(

        (

            notes_rect[0] + 12,

            notes_rect[1] + 15,

        ),

        "Total Notes",

        fill=SUBTEXT,

        font=TEXT_FONT,

    )

    # ------------------------------------------------------
    # Value
    # ------------------------------------------------------

    value = f"{total_notes:,}"

    text_w, _ = text_size(
        draw,
        value,
        VALUE_FONT,
    )

    draw.text(

        (

            notes_rect[2] - text_w - 18,

            notes_rect[1] + 12,

        ),

        value,

        fill=SUBTEXT,

        font=VALUE_FONT,

    )

    return y2

# ==========================================================
# Comment Generator
# ==========================================================

def generate_comment(
    *,
    achievement: float,
    precision: float,
    balance: float,
    balance_available: bool,
    rank: str,
    fast: int,
    slow: int,
):
    """
    Version 1.3 Final
    解析コメント生成
    """

    comments = []

    # ----------------------------
    # Precision
    # ----------------------------

    if precision >= 84.0:
        comments.append(
            "タイミングのばらつきが非常に少なく、非常に精密なタップです。"
        )

    elif precision >= 78.0:
        comments.append(
            "タイミングのばらつきが少なく、高い精密度です。"
        )

    elif precision >= 70.0:
        comments.append(
            "タイミングのばらつきは比較的少なく、精密度は良好です。"
        )

    elif precision >= 64.0:
        comments.append(
            "タイミングのばらつきは比較的抑えられています。"
        )

    elif precision >= 56.0:
        comments.append(
            "タイミングにややばらつきがあります。"
        )

    else:
        comments.append(
            "タイミングのばらつきが大きいため、中央判定を意識すると改善につながります。"
        )

    # ----------------------------
    # Balance
    # ----------------------------

    if balance_available:

        if balance >= 97.0:
            comments.append(
                "SLOW/FASTの偏りが非常に少なく、非常に安定したタップです。"
            )

        elif balance >= 87.0:
            comments.append(
                "SLOW/FASTの偏りが少なく、安定したタップです。"
            )

        elif balance >= 71.0:
            comments.append(
                "SLOW/FASTの偏りは比較的小さく、バランスは良好です。"
            )

        elif balance >= 53.0:
                comments.append(
                    "タイミングのばらつきは比較的抑えられています。"
                )

        elif balance >= 37.0:
            comments.append(
                "SLOW/FASTにやや偏りがあります。"
            )

        elif balance >= 20.0:
            comments.append(
                "SLOW/FASTの偏りが見られます。"
            )

        elif balance >= 12.0:
            comments.append(
                "SLOW/FASTの偏りが大きく、タップタイミングが一方向に寄っています。"
            )

        else:
            comments.append(
                "SLOW/FASTの偏りが非常に大きく、タップタイミングが一方向へ強く寄っています。"
            )

    # ----------------------------
    # SLOW / FAST
    # ----------------------------

    timing_total = fast + slow

    if balance_available and timing_total > 0:

        fast_rate = fast / timing_total * 100.0
        slow_rate = slow / timing_total * 100.0

        timing_difference = fast_rate - slow_rate

        if timing_difference >= 15.0:
            comments.append(
                "FAST傾向が強いため、少し遅めを意識すると改善できます。"
            )

        elif timing_difference <= -15.0:
            comments.append(
                "SLOW傾向が強いため、少し早めを意識すると改善できます。"
            )

    return "\n".join(comments)

# ==========================================================
# Play Style Badge
# ==========================================================

def generate_play_badge(
    *,
    precision: float,
    balance: float,
    balance_available: bool,
    fast: int,
    slow: int,
    amazing_plus: int,
):
    """
    Version 1.3 Final

    プレイ傾向バッジ

    判定優先順位
    1. Precision Master
    2. Amazing Specialist
    3. Balanced Player
    4. Fast Type
    5. Slow Type
    6. All Round Player
    """

    # ======================================================
    # Availability
    # ======================================================

    if not balance_available:
        return (
            "N/A",
            (120, 125, 135),
            (248, 249, 251),
        )

    # ======================================================
    # Amazing+率
    # ======================================================

    # AMAZING+率の定義：
    #
    # AMAZING+
    # ÷
    # (AMAZING+ + AMAZING(SLOW) + AMAZING(FAST))
    # × 100
    #
    # FAST / SLOW は AMAZING の内訳であり、
    # AMAZING 本体とは別の判定値ではない。

    amazing_total = (
        amazing_plus
        + slow
        + fast
    )

    if amazing_total > 0:

        amazing_plus_rate = (
            amazing_plus
            / amazing_total
            * 100.0
        )

    else:

        amazing_plus_rate = 0.0

    # ------------------------------------------------------
    # FAST / SLOW 比率
    # ------------------------------------------------------

    timing_total = fast + slow

    if timing_total > 0:

        fast_rate = (
            fast
            / timing_total
            * 100.0
        )

        slow_rate = (
            slow
            / timing_total
            * 100.0
        )

    else:

        fast_rate = 0.0
        slow_rate = 0.0

    # FAST - SLOW の percentage point 差
    timing_difference = (
        fast_rate
        - slow_rate
    )

    # ======================================================
    # Precision Master
    # ======================================================

    if (
        balance_available
        and precision >= 80.0
        and balance >= 87.0
    ):
        return (
            "✦ Precision Master",
            (123, 77, 255),
            (247, 242, 255),
        )

    # ======================================================
    # Amazing Specialist
    # ======================================================

    if amazing_plus_rate >= 80.0:
        return (
            "★ Amazing Specialist",
            (255, 180, 0),
            (255, 249, 225),
        )

    # ======================================================
    # Balanced Player
    # ======================================================

    if (
        balance_available
        and balance >= 87.0
    ):
        return (
            "■ Balanced Player",
            (0, 170, 120),
            (240, 255, 248),
        )

    # ======================================================
    # Fast Type
    # ======================================================

    if (
        balance_available
        and balance < 71.0
        and timing_difference > 15.0
    ):
        return (
            "▲ Fast Type",
            (230, 60, 60),
            (255, 242, 242),
        )

    # ======================================================
    # Slow Type
    # ======================================================

    if (
        balance_available
        and balance < 71.0
        and timing_difference < -15.0
    ):
        return (
            "▼ Slow Type",
            (40, 120, 255),
            (240, 248, 255),
        )

    # ======================================================
    # All Round Player
    # ======================================================

    return (
        "◉ All Round Player",
        TITLE,
        (248, 248, 255),
    )

# ==========================================================
# Right Panel
# ==========================================================

def draw_right_panel(
    draw: ImageDraw.ImageDraw,
    *,
    achievement: float,
    precision: float,
    precision_grade: str,
    balance: float,
    balance_grade: str,
    balance_available: bool,
    overall_score: float,
    rank: str,
):
    """
    Right Information Panel
    """

    draw_card_with_shadow(
        draw,
        RIGHT_RECT,
    )

    x1, y1, x2, y2 = card_inner_rect(
        RIGHT_RECT,
    )

    y = card_content_top(
        RIGHT_RECT,
    )

    CARD_GAP = 8

    ACHIEVEMENT_H = 92

    RATING_H = 108

    SCORE_H = 92

    RANK_H = 110

    # ======================================================
    # Achievement
    # ======================================================

    card_height = ACHIEVEMENT_H

    draw.rounded_rectangle(
        (
            x1,
            y,
            x2,
            y + card_height,
        ),
        radius=18,
        fill=(244, 239, 255),
        outline=(218, 205, 255),
        width=2,
    )

    title_text = "Achievement"
    sub_text = "（達成率）"

    draw_left_text(
        draw,
        title_text,
        x1 + 20,
        y + 17,
        SECTION_FONT,
        TITLE,
    )

    title_width, _ = text_size(
        draw,
        title_text,
        SECTION_FONT,
    )

    draw_left_text(
        draw,
        sub_text,
        x1 + 24 + title_width,
        y + 18,
        SMALL_FONT,
        SUBTEXT,
    )

    value_color = TITLE if achievement >= 100 else TEXT

    value = f"{achievement:.3f} %"

    value_width, value_height = text_size(
        draw,
        value,
        ACHIEVEMENT_VALUE_FONT,
    )

    draw.text(
        (
            x1 + (x2 - x1 - value_width) / 2,
            y + 33,
        ),
        value,
        fill=value_color,
        font=ACHIEVEMENT_VALUE_FONT,
    )

    y += ACHIEVEMENT_H + CARD_GAP

    # ======================================================
    # Precision
    # ======================================================

    title_x = x1 + RATING_LEFT
    desc_x = title_x
    value_x = title_x
    icon_x = value_x + RATING_ICON_OFFSET

    precision_card_height = RATING_H

    draw.rounded_rectangle(
        (
            x1,
            y,
            x2,
            y + precision_card_height,
        ),
        radius=18,
        fill=(248, 251, 255),
        outline=(205, 223, 255),
        width=2,
    )

    draw_left_text(
        draw,
        "Precision",
        title_x,
        y + RATING_TITLE_Y,
        SECTION_FONT,
        (33, 92, 210),
    )

    title_width, _ = text_size(
        draw,
        "Precision",
        SECTION_FONT,
    )

    draw_left_text(
        draw,
        "（精密度）",
        title_x + title_width + 6,
        y + RATING_TITLE_Y + 2,
        SMALL_FONT,
        SUBTEXT,
    )

    draw_left_text(
        draw,
        "タイミングのばらつきの少なさ",
        desc_x,
        y + RATING_DESC_Y,
        SMALL_FONT,
        SUBTEXT,
    )

    draw_right_text(
        draw,
        precision_grade,
        x2 - 18,
        y + 17,
        LARGE_VALUE_FONT,
        (33, 92, 210),
    )

    draw_left_text(
        draw,
        f"{precision:.3f} %",
        value_x,
        y + RATING_VALUE_Y,
        VALUE_FONT,
    )

    filled, empty = split_star_string(
        precision_grade
    )

    draw_left_text(
        draw,
        filled,
        icon_x,
        y + RATING_ICON_Y - 4,
        RATING_ICON_FONT,
        (33, 92, 210),
    )

    filled_width, _ = text_size(
        draw,
        filled,
        RATING_ICON_FONT,
    )

    draw_left_text(
        draw,
        empty,
        icon_x + filled_width,
        y + RATING_ICON_Y - 4,
        RATING_ICON_FONT,
        (205, 212, 225),
    )

    y += RATING_H + CARD_GAP

    # ======================================================
    # Balance
    # ======================================================

    title_x = x1 + RATING_LEFT
    desc_x = title_x
    value_x = title_x
    icon_x = value_x + RATING_ICON_OFFSET

    balance_card_height = RATING_H

    draw.rounded_rectangle(
        (
            x1,
            y,
            x2,
            y + balance_card_height,
        ),
        radius=18,
        fill=(245, 255, 249),
        outline=(184, 231, 208),
        width=2,
    )

    draw_left_text(
        draw,
        "Balance",
        title_x,
        y + RATING_TITLE_Y,
        SECTION_FONT,
        (0, 150, 110),
    )

    title_width, _ = text_size(
        draw,
        "Balance",
        SECTION_FONT,
    )

    draw_left_text(
        draw,
        "（安定度）",
        title_x + title_width + 6,
        y + RATING_TITLE_Y + 2,
        SMALL_FONT,
        SUBTEXT,
    )

    draw_left_text(
        draw,
        "SLOW/FASTの偏りの少なさ",
        desc_x,
        y + RATING_DESC_Y,
        SMALL_FONT,
        SUBTEXT,
    )

    if balance_available:

        draw_right_text(
            draw,
            balance_grade,
            x2 - 18,
            y + 17,
            LARGE_VALUE_FONT,
            (0, 150, 110),
        )

        draw_left_text(
            draw,
            f"{balance:.3f} %",
            value_x,
            y + RATING_VALUE_Y,
            VALUE_FONT,
        )

        filled, empty = split_diamond_string(
            balance_grade
        )

        draw_left_text(
            draw,
            filled,
            icon_x,
            y + RATING_ICON_Y - 4,
            RATING_ICON_FONT,
            (0, 170, 120),
        )

        filled_width, _ = text_size(
            draw,
            filled,
            RATING_ICON_FONT,
        )

        draw_left_text(
            draw,
            empty,
            icon_x + filled_width,
            y + RATING_ICON_Y - 4,
            RATING_ICON_FONT,
            (205, 212, 225),
        )

    else:

        draw_right_text(
            draw,
            "N/A",
            x2 - 18,
            y + 16,
            LARGE_VALUE_FONT,
            (120, 125, 135),
        )

        draw_left_text(
            draw,
            "評価対象外",
            value_x,
            y + RATING_VALUE_Y,
            VALUE_FONT,
            (120, 125, 135),
        )

    y += RATING_H + CARD_GAP

    # ======================================================
    # Overall Score
    # ======================================================

    score_card_height = SCORE_H

    draw.rounded_rectangle(
        (
            x1,
            y,
            x2,
            y + score_card_height,
        ),
        radius=18,
        fill=(255, 250, 238),
        outline=(255, 210, 120),
        width=2,
    )

    title = "Overall Score"
    subtitle = "（総合評価）"

    draw_left_text(
        draw,
        title,
        x1 + 18,
        y + 15,
        SECTION_FONT,
        (235, 125, 0),
    )

    title_width, _ = text_size(
        draw,
        title,
        SECTION_FONT,
    )

    draw_left_text(
        draw,
        subtitle,
        x1 + 18 + title_width + 6,
        y + 16,
        SMALL_FONT,
        SUBTEXT,
    )

    score_text = f"{overall_score:.3f} pt"

    score_width, _ = text_size(
        draw,
        score_text,
        LARGE_VALUE_FONT,
    )

    draw.text(
        (
            x1 + (x2 - x1 - score_width) / 2,
            y + 34,
        ),
        score_text,
        fill=(245, 140, 0),
        font=LARGE_VALUE_FONT,
    )

    y += SCORE_H + CARD_GAP

    # ======================================================
    # Rank
    # ======================================================

    rank_card_height = RANK_H

    rank_background, rank_outline = get_rank_card_colors(
        rank
    )

    draw.rounded_rectangle(
        (
            x1,
            y,
            x2,
            y + rank_card_height,
        ),
        radius=18,
        fill=rank_background,
        outline=rank_outline,
        width=2,
    )
    
    # Rankタイトル
    draw.text(
        (
            x1 + 18,
            y + 12,
        ),
        "Rank",
        fill=get_rank_color(rank),
        font=SECTION_FONT,
    )

    # Rank文字
    draw_rank_text(
        draw,
        rank=rank,
        center_x=(x1 + x2) // 2,
        center_y=y + 62,
    )

    # Rankカードの一番下を返す
    return y + rank_card_height + 12

# ==========================================================
# Fast / Slow Card
# ==========================================================

def draw_fastslow_card(
    draw,
    *,
    fast,
    slow,
    slow_available,
    fast_available,
    total_notes,
    top,
):
    """SLOW / FASTを横一列の1カードとして描画する。"""
    if total_notes > 0:
        slow_rate = slow / total_notes * 100.0
        fast_rate = fast / total_notes * 100.0
    else:
        slow_rate = 0.0
        fast_rate = 0.0

    rect = (
        CONTENT_LEFT,
        top,
        CONTENT_RIGHT,
        top + FASTSLOW_HEIGHT,
    )

    draw_card_with_shadow(draw, rect)

    x1, y1, x2, y2 = card_inner_rect(rect)

    center_x = (x1 + x2) // 2

    draw.line(
        (
            center_x,
            y1 + 10,
            center_x,
            y2 - 10,
        ),
        fill=LINE,
        width=1,
    )

    slow_center = (x1 + center_x) // 2
    fast_center = (center_x + x2) // 2


    # ------------------------------------------------------
    # Labels
    # ------------------------------------------------------

    draw.text(
        (x1 + 18, y1 + 12),
        "SLOW",
        fill=(33, 150, 243),
        font=SECTION_FONT,
    )

    draw.text(
        (center_x + 18, y1 + 12),
        "FAST",
        fill=(229, 57, 53),
        font=SECTION_FONT,
    )


    # ------------------------------------------------------
    # SLOW
    # ------------------------------------------------------

    if slow_available:

        draw.text(
            (slow_center, y1 + 29),
            str(slow),
            fill=(33, 150, 243),
            font=LARGE_VALUE_FONT,
            anchor="mm",
        )

        draw.text(
            (slow_center, y1 + 55),
            f"{slow_rate:.1f}%",
            fill=SUBTEXT,
            font=SMALL_FONT,
            anchor="mm",
        )

    else:

        draw.text(
            (slow_center, y1 + 29),
            "N/A",
            fill=SUBTEXT,
            font=LARGE_VALUE_FONT,
            anchor="mm",
        )


    # ------------------------------------------------------
    # FAST
    # ------------------------------------------------------

    if fast_available:

        draw.text(
            (fast_center, y1 + 29),
            str(fast),
            fill=(229, 57, 53),
            font=LARGE_VALUE_FONT,
            anchor="mm",
        )

        draw.text(
            (fast_center, y1 + 55),
            f"{fast_rate:.1f}%",
            fill=SUBTEXT,
            font=SMALL_FONT,
            anchor="mm",
        )

    else:

        draw.text(
            (fast_center, y1 + 29),
            "N/A",
            fill=SUBTEXT,
            font=LARGE_VALUE_FONT,
            anchor="mm",
        )
    return rect[3]

# ==========================================================
# Comment Card
# ==========================================================

# ==========================================================
# Comment Layout Utility
# ==========================================================

def calculate_comment_layout(
    draw: ImageDraw.ImageDraw,
    comment: str,
):
    """
    コメントカードの必要高さと折り返し結果を計算する。

    コメントを実際に描画する前に必要なキャンバス高さを
    確定するために使用する。
    """

    # ------------------------------------------------------
    # Comment width
    # ------------------------------------------------------

    base_rect = (
        CONTENT_LEFT,
        0,
        CONTENT_RIGHT,
        COMMENT_HEIGHT,
    )

    base_x1, _, base_x2, _ = card_inner_rect(
        base_rect,
    )

    total_width = base_x2 - base_x1

    # 左側：バッジ・コメント
    left_width = int(total_width * 0.72)

    comment_width = left_width - 50

    # ------------------------------------------------------
    # Wrap
    # ------------------------------------------------------

    lines = wrap_text(
        draw,
        comment,
        COMMENT_FONT,
        comment_width,
    )

    if not lines:
        lines = [""]

    # ------------------------------------------------------
    # Text height
    # ------------------------------------------------------

    comment_line_spacing = 14

    comment_text_height = 0
    current_offset = 0

    for index, line in enumerate(lines):

        left, bbox_top, right, bbox_bottom = draw.textbbox(
            (0, 0),
            line,
            font=COMMENT_FONT,
        )

        # 実際に描画される文字の下端
        actual_bottom = (
            current_offset
            + bbox_bottom
        )

        comment_text_height = max(
            comment_text_height,
            actual_bottom,
        )

        # draw_multiline_text() と同じ進行
        line_height = bbox_bottom - bbox_top

        current_offset += line_height

        if index < len(lines) - 1:
            current_offset += comment_line_spacing

    # ------------------------------------------------------
    # Required height
    # ------------------------------------------------------

    content_offset = 70

    required_comment_height = (
        content_offset
        + COMMENT_TEXT_TOP
        + comment_text_height
        + COMMENT_BOTTOM_PADDING
    )

    dynamic_comment_height = max(
        COMMENT_HEIGHT,
        required_comment_height,
    )

    return dynamic_comment_height, lines

def draw_comment_card(
    draw: ImageDraw.ImageDraw,
    *,
    badge: str,
    badge_color,
    badge_fill,
    comment: str,
    top: int,
    visible: bool = True,
):
    """
    Version 1.3 Final

    Comment Card
    Dynamic Layout

    コメント全文を表示し、
    必要な場合のみカード高さを自動拡張する。
    """

    if not visible:
        return top

    # ------------------------------------------------------
    # Base Layout
    # ------------------------------------------------------

    base_rect = (
        CONTENT_LEFT,
        top,
        CONTENT_RIGHT,
        top + COMMENT_HEIGHT,
    )

    base_x1, _, base_x2, _ = card_inner_rect(
        base_rect,
    )

    total_width = base_x2 - base_x1

    # 左側：バッジ・コメント
    left_width = int(total_width * 0.72)

    # ------------------------------------------------------
    # Comment Layout
    # ------------------------------------------------------

    dynamic_comment_height, lines = calculate_comment_layout(
        draw,
        comment,
    )

    # ------------------------------------------------------
    # Rectangle
    # ------------------------------------------------------

    comment_rect = (
        CONTENT_LEFT,
        top,
        CONTENT_RIGHT,
        top + dynamic_comment_height,
    )

    draw_card_with_shadow(
        draw,
        comment_rect,
    )

    draw_card_header(
        draw,
        comment_rect,
        "解析結果",
        centered=True,
    )

    x1, y1, x2, y2 = card_inner_rect(
        comment_rect,
    )

    content_top = card_content_top(
        comment_rect,
    )

    # ------------------------------------------------------
    # Play Badge
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Play Style Label
    # ------------------------------------------------------

    draw.text(
        (
            x1 + COMMENT_LEFT_PADDING,
            content_top + COMMENT_PLAY_STYLE_LABEL_TOP,
        ),
        "プレイ傾向",
        fill=TITLE,
        font=SECTION_FONT,
    )

    if badge.startswith("✦ "):
        badge_label = "Precision Master"

        badge_text_width, _ = text_size(
            draw,
            badge_label,
            SECTION_FONT,
        )

        badge_width = (
            badge_text_width
            + 20
            + 22
        )
    else:
        badge_text_width, _ = text_size(
            draw,
            badge,
            SECTION_FONT,
        )

        badge_width = badge_text_width + 22

    badge_left = x1 + COMMENT_LEFT_PADDING

    badge_top = (
        content_top
        + COMMENT_BADGE_TOP
    )

    badge_center_x = (
        badge_left
        + badge_width // 2
    )

    draw.rounded_rectangle(
        (
            badge_left,
            badge_top,
            badge_left + badge_width,
            badge_top + COMMENT_BADGE_HEIGHT,
        ),
        radius=20,
        fill=badge_fill,
        outline=badge_color,
        width=2,
    )

    if badge.startswith("✦ "):
        # Precision Master
        badge_label = "Precision Master"

        label_width, label_height = text_size(
            draw,
            badge_label,
            TEXT_FONT,
        )

        star_size = 10
        star_gap = 6

        total_width = (
            star_size * 2
            + star_gap
            + label_width
        )

        start_x = (
            badge_center_x
            - total_width // 2
        )

        draw_four_point_star(
            draw,
            start_x + star_size,
            badge_top + COMMENT_BADGE_TEXT_Y,
            outer=star_size,
            inner=3,
            fill=badge_color,
        )

        draw.text(
            (
                start_x
                + star_size * 2
                + star_gap,
                badge_top + COMMENT_BADGE_TEXT_Y,
            ),
            badge_label,
            fill=badge_color,
            font=TEXT_FONT,
            anchor="lm",
        )

    else:
        draw.text(
            (
                badge_center_x,
                badge_top + COMMENT_BADGE_TEXT_Y,
            ),
            badge,
            fill=badge_color,
            font=TEXT_FONT,
            anchor="mm",
        )

    # ------------------------------------------------------
    # Comment
    # ------------------------------------------------------

    comment_line_spacing = 14

    draw.text(
        (
            x1 + COMMENT_LEFT_PADDING,
            content_top + COMMENT_COMMENT_LABEL_TOP,
        ),
        "解析コメント",
        fill=TITLE,
        font=SECTION_FONT,
    )

    comment_color = (
        SUBTEXT
        if "解析コメントはありません" in comment
        else TEXT
    )

    draw_multiline_text(
        draw,
        lines,
        x1 + COMMENT_LEFT_PADDING,
        content_top + COMMENT_TEXT_TOP,
        COMMENT_FONT,
        color=comment_color,
        line_spacing=comment_line_spacing,
        max_bottom=None,
    )

    return comment_rect[3]

# ==========================================================
# Analysis Result (lower-left card)
# ==========================================================

def draw_analysis_result_card(
    draw: ImageDraw.ImageDraw,
    *,
    badge: str,
    badge_color,
    badge_fill,
    comment: str,
    rect,
):
    """下段左側：プレイ傾向と解析コメントを1カードに整理する。"""
    draw_card_with_shadow(draw, rect)
    draw_card_header(draw, rect, "解析結果", centered=True)

    x1, y1, x2, y2 = card_inner_rect(rect)
    content_top = card_content_top(rect)
    divider_x = x1 + int((x2 - x1) * 0.40)

    draw.line((divider_x, content_top + 4, divider_x, y2 - 12), fill=LINE, width=1)

    left_center = (x1 + divider_x) // 2
    right_x = divider_x + 20

    draw.text((left_center, content_top + 34), "プレイ傾向", fill=TITLE, font=SECTION_FONT, anchor="ma")

    # Badge width / fontを左カラム内に確実に収める。
    is_precision_master = badge.startswith("✦ ")
    label = "Precision Master" if is_precision_master else badge

    max_badge_width = max(100, divider_x - x1 - 10)
    if is_precision_master:
        badge_font = fit_text(
            draw,
            label,
            max_width=max_badge_width - 42,
            start_size=15,
            min_size=12,
            bold=False,
        )
        label_w, _ = text_size(draw, label, badge_font)
        badge_w = min(max_badge_width, label_w + 42)
    else:
        badge_font = fit_text(
            draw,
            label,
            max_width=max_badge_width - 24,
            start_size=15,
            min_size=12,
            bold=False,
        )
        label_w, _ = text_size(draw, label, badge_font)
        badge_w = min(max_badge_width, label_w + 24)

    badge_w = max(100, badge_w)
    badge_h = 38
    badge_rect = (
        left_center - badge_w // 2,
        content_top + 76,
        left_center + badge_w // 2,
        content_top + 76 + badge_h,
    )
    draw.rounded_rectangle(badge_rect, radius=18, fill=badge_fill, outline=badge_color, width=2)

    badge_center_y = (badge_rect[1] + badge_rect[3]) // 2

    if is_precision_master:
        start_x = left_center - (label_w + 30) // 2
        draw_four_point_star(
            draw,
            start_x + 8,
            badge_center_y,
            outer=8,
            inner=2.5,
            fill=badge_color,
        )
        draw.text(
            (start_x + 20, badge_center_y),
            label,
            fill=badge_color,
            font=badge_font,
            anchor="lm",
        )
    else:
        draw.text(
            (left_center, badge_center_y),
            label,
            fill=badge_color,
            font=badge_font,
            anchor="mm",
        )

    draw.text((right_x, content_top + 34), "解析コメント", fill=TITLE, font=SECTION_FONT)

    # コメントは条件によって行数が増えるため、カード内に全文が収まる
    # フォントサイズと行間を自動調整する。内容を途中で切らない。
    comment_text_x = right_x
    comment_text_y = content_top + 68
    comment_max_width = max(170, x2 - right_x - 8)
    comment_max_bottom = y2 - 12

    comment_font = COMMENT_FONT
    comment_line_spacing = 6
    lines = [""]

    fitted = False
    for font_size in range(COMMENT_FONT_SIZE, 11, -1):
        candidate_font = get_font(font_size, bold=False)
        candidate_lines = wrap_text(
            draw,
            comment,
            candidate_font,
            comment_max_width,
        )
        if not candidate_lines:
            candidate_lines = [""]

        for spacing in range(6, 2, -1):
            total_height = 0
            for index, line in enumerate(candidate_lines):
                _, line_height = text_size(draw, line, candidate_font)
                total_height += line_height
                if index < len(candidate_lines) - 1:
                    total_height += spacing

            if comment_text_y + total_height <= comment_max_bottom:
                comment_font = candidate_font
                comment_line_spacing = spacing
                lines = candidate_lines
                fitted = True
                break

        if fitted:
            break

    # 通常は上の範囲で収まるが、極端に長いコメントでも最後まで表示できる
    # よう、最小フォントで再計算する。
    if not fitted:
        comment_font = get_font(11, bold=False)
        comment_line_spacing = 2
        lines = wrap_text(
            draw,
            comment,
            comment_font,
            comment_max_width,
        ) or [""]

    draw_multiline_text(
        draw,
        lines,
        comment_text_x,
        comment_text_y,
        comment_font,
        color=SUBTEXT if "解析コメントはありません" in comment else TEXT,
        line_spacing=comment_line_spacing,
        max_bottom=comment_max_bottom,
    )

    return rect[3]

# ==========================================================
# Ranking Result
# ==========================================================

def draw_ranking_result_card(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    *,
    ranking_position: int,
    comparison_total: int,
    ranking_top_percent: float,
    ranking_title: str,
    ranking_rank: str,
    rank_distribution: dict[str, int],
    analysis_date: str | None,
    top: int,
    rect,
):
    """
    総合評価ランキング結果カード。

    左側:
        ・あなたの称号
        ・ランキング称号画像
        ・順位
        ・上位○%

    右側:
        ・総合評価スコア分布
        ・本人位置マーカー
        ・本人より高得点側の範囲を強調

    「上位○%」は左側に1回だけ表示し、
    グラフ側には重複表示しない。
    """

    draw_card_with_shadow(draw, rect)
    draw_card_header(
        draw,
        rect,
        "総合評価ランキング結果",
        centered=True,
    )

    x1, y1, x2, y2 = card_inner_rect(rect)
    content_top = card_content_top(rect)

    # ------------------------------------------------------
    # Layout
    # ------------------------------------------------------
    divider_x = x1 + int((x2 - x1) * 0.40)

    left_center = (x1 + divider_x) // 2

    chart_left = divider_x + 12
    chart_right = x2 - 6

    draw.line(
        (
            divider_x,
            content_top + 4,
            divider_x,
            y2 - 12,
        ),
        fill=LINE,
        width=1,
    )

    # ------------------------------------------------------
    # Left : Ranking information
    # ------------------------------------------------------

    # ① タイトル
    title_y = content_top + 34

    draw.text(
        (left_center, title_y),
        "あなたの称号",
        fill=TITLE,
        font=SECTION_FONT,
        anchor="ma",
    )

    # ② ランキング称号画像
    filename = RANKING_TITLE_FILES.get(ranking_title)

    title_img_bottom = content_top + 104

    if filename:
        title_path = RANKING_TITLE_DIR / filename

        if title_path.exists():
            title_img = Image.open(title_path).convert("RGBA")

            max_w = max(
                120,
                divider_x - x1 - 16,
            )

            max_h = 58

            scale = min(
                max_w / title_img.width,
                max_h / title_img.height,
                1.0,
            )

            if scale < 1.0:
                title_img = title_img.resize(
                    (
                        max(1, int(title_img.width * scale)),
                        max(1, int(title_img.height * scale)),
                    ),
                    Image.Resampling.LANCZOS,
                )

            title_img_y = content_top + 70

            image.alpha_composite(
                title_img,
                (
                    left_center - title_img.width // 2,
                    title_img_y,
                ),
            )

            title_img_bottom = (
                title_img_y + title_img.height
            )

    # ③ 順位
    position_y = max(
        content_top + 106,
        title_img_bottom + 4,
    )

    draw.text(
        (left_center, position_y),
        f"{ranking_position:,}位 / {comparison_total:,}件中",
        fill=TEXT,
        font=TEXT_FONT,
        anchor="ma",
    )

    # ④ 上位○%はここだけ
    top_percent_y = position_y + 32

    draw.text(
        (left_center, top_percent_y),
        f"上位 {ranking_top_percent:.1f}%",
        fill=TITLE,
        font=TEXT_FONT,
        anchor="ma",
    )

    # ------------------------------------------------------
    # Right : Distribution graph
    # ------------------------------------------------------

    graph_title_y = content_top + 5

    draw.text(
        (
            (chart_left + chart_right) // 2,
            graph_title_y,
        ),
        "総合評価スコア分布（固定基準データ1,799件）",
        fill=SUBTEXT,
        font=load_font(12),
        anchor="ma",
    )

    chart_x1 = chart_left + 2
    chart_x2 = chart_right - 2

    # グラフ領域をカード内で十分に確保
    chart_top = content_top + 56
    chart_bottom = y2 - 55

    plot_top = chart_top + 8

    chart_h = max(
        30,
        chart_bottom - plot_top,
    )

    labels = RANKING_RANK_ORDER
    counts = [
        int(rank_distribution.get(label, 0))
        for label in labels
    ]

    n = len(labels)

    gap = 2

    bar_w = max(
        3,
        (
            chart_x2
            - chart_x1
            - gap * (n - 1)
        ) // n,
    )

    max_count = max(counts) if counts else 1

    # ------------------------------------------------------
    # Histogram background
    # ------------------------------------------------------

    # 半透明ではなく、グラフ領域そのものを不透明に塗る。
    draw.rectangle(
        (
            chart_x1,
            chart_top,
            chart_x2,
            chart_bottom,
        ),
        fill=(247, 244, 255),
        outline=(225, 220, 238),
        width=1,
    )

    # 固定基準データは必ず1,799件であることを検証。
    distribution_total = sum(counts)
    if distribution_total != 1799:
        raise ValueError(
            f"ランキング分布データ件数が不正です: {distribution_total}件（期待値1799件）"
        )

    # ------------------------------------------------------
    # 本人位置
    # ------------------------------------------------------

    # 順位そのものを横位置へ線形変換してはいけない。
    # このグラフは「Rank別の1,799件分布」なので、
    # 現在のRankに対応する棒の中央を本人位置とする。
    current_rank_index = (
        labels.index(ranking_rank)
        if ranking_rank in labels
        else None
    )

    marker_x = None
    if current_rank_index is not None:
        marker_x = (
            chart_x1
            + current_rank_index * (bar_w + gap)
            + bar_w // 2
        )

    # ------------------------------------------------------
    # Histogram
    # ------------------------------------------------------

    for i, (label, count) in enumerate(
        zip(labels, counts)
    ):
        x = chart_x1 + i * (bar_w + gap)

        if count > 0:
            bar_h = (
                count
                / max_count
                * chart_h
            )
        else:
            bar_h = 0

        bar_y = chart_bottom - int(bar_h)

        bar_color = (126, 82, 240) if i == current_rank_index else (175, 183, 198)

        draw.rectangle(
            (
                x,
                bar_y,
                x + bar_w,
                chart_bottom,
            ),
            fill=bar_color,
        )

        if bar_w >= 8:
            draw.text(
                (
                    x + bar_w // 2,
                    chart_bottom + 5,
                ),
                label,
                fill=SUBTEXT,
                font=load_font(7),
                anchor="ma",
            )

    # ------------------------------------------------------
    # 本人位置マーカー
    # ------------------------------------------------------

    if marker_x is not None:
        draw.line(
            (
                int(marker_x),
                plot_top - 2,
                int(marker_x),
                chart_bottom + 4,
            ),
            fill=TITLE,
            width=3,
        )

    # マーカーラベル
    # 棒グラフを隠さないよう、ラベルはプロット領域の上側に配置する。
    marker_label_y = chart_top - 15

    if marker_x is not None:
        marker_overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        marker_draw = ImageDraw.Draw(marker_overlay)

        marker_draw.rounded_rectangle(
            (
                int(marker_x) - 34,
                marker_label_y - 12,
                int(marker_x) + 34,
                marker_label_y + 12,
            ),
            radius=8,
            fill=(126, 82, 240),
        )

        marker_draw.text(
            (
                int(marker_x),
                marker_label_y,
            ),
            "あなた",
            fill=WHITE,
            font=load_font(13),
            anchor="mm",
        )

        image.alpha_composite(marker_overlay)


    # ------------------------------------------------------
    # 軸方向
    # ------------------------------------------------------

    axis_y = chart_bottom + 24

    draw.text(
        (chart_x1, axis_y),
        "（高）",
        fill=SUBTEXT,
        font=load_font(8),
        anchor="lm",
    )

    draw.text(
        (
            (chart_x1 + chart_x2) // 2,
            axis_y,
        ),
        "総合評価スコア",
        fill=SUBTEXT,
        font=load_font(9),
        anchor="mm",
    )

    draw.text(
        (chart_x2, axis_y),
        "（低）",
        fill=SUBTEXT,
        font=load_font(8),
        anchor="rm",
    )

    # ------------------------------------------------------
    # 解析日
    # ------------------------------------------------------

    date_text = analysis_date or ""

    if date_text:
        draw_right_text(
            draw,
            f"解析日：{date_text}",
            x2 - 4,
            y2 - 18,
            font=load_font(9),
            color=SUBTEXT,
        )

# ==========================================================
# Footer
# ==========================================================

def draw_footer(
    draw: ImageDraw.ImageDraw,
    *,
    top: int,
):
    """
    Version 1.3 Final

    Footer
    Dynamic Layout
    """

    footer_left = CONTENT_LEFT + 20
    footer_right = CONTENT_RIGHT


    # ------------------------------------------------------
    # Disclaimer
    # ------------------------------------------------------

    draw.text(
        (
            footer_left,
            top,
        ),
        "※ 判定内訳・各スコアは解析結果から推定した値です。",
        fill=(125,128,138),
        font=FOOTER_FONT,
    )

    draw.text(
        (
            footer_left,
            top + 22,
        ),
        "公式アプリが表示する値ではありません。",
        fill=(125,128,138),
        font=FOOTER_FONT,
    )

    draw.text(
        (
            footer_left,
            top + 44,
        ),
        "本ツールは非公式ファンメイドツールです。",
        fill=(125,128,138),
        font=FOOTER_FONT,
    )

    # ------------------------------------------------------
    # Credit
    # ------------------------------------------------------

    draw_right_text(
        draw,
        "Developed by Hapylon × ChatGPT",
        footer_right,
        top + 42,
        FOOTER_FONT,
        (120,125,138),
    )

    return top + FOOTER_HEIGHT

# ==========================================================
# Create Result Card
# ==========================================================

def create_result_card(
    *,
    music: str,
    difficulty: str,
    level: str,
    amazing_plus: int,
    amazing: int,
    perfect: int,
    great: int,
    good: int,
    bad: int,
    miss: int,
    total_notes: int,
    fast: int,
    slow: int,
    slow_available: bool,
    fast_available: bool,
    achievement: float,
    precision: float,
    precision_grade: str,
    balance: float,
    balance_grade: str,
    balance_available: bool,
    overall_score: float,
    rank: str,
    ranking_position: int | None = None,
    ranking_comparison_total: int | None = None,
    ranking_top_percent: float | None = None,
    ranking_title: str | None = None,
    ranking_rank: str | None = None,
    ranking_distribution: dict[str, int] | None = None,
    ranking_analysis_date: str | None = None,
    comment: str = "",
    show_comment: bool = True,
    save_path: Path | None = None,
):
    """1080x1450の固定レイアウトで総合解析結果カードを生成する。"""
    if save_path is None:
        save_path = CARD_PATH

    image, draw = create_card(
        ranking_title=ranking_title,
    )
    judges = {
        "AMAZING+": amazing_plus,
        "AMAZING": amazing,
        "PERFECT": perfect,
        "GREAT": great,
        "GOOD": good,
        "BAD": bad,
        "MISS": miss,
    }

    # ------------------------------------------------------
    # 1. Song Information
    # ------------------------------------------------------
    draw_song_card(
        image,
        draw,
        music=music,
        difficulty=difficulty,
        level=level,
    )

    # ------------------------------------------------------
    # 2. Main Panels
    # ------------------------------------------------------

    left_bottom = draw_left_panel(
        draw,
        judges,
        total_notes=total_notes,
    )

    right_bottom = draw_right_panel(
        draw,
        achievement=achievement,
        precision=precision,
        precision_grade=precision_grade,
        balance=balance,
        balance_grade=balance_grade,
        balance_available=balance_available,
        overall_score=overall_score,
        rank=rank,
    )

    panel_bottom = max(
        left_bottom,
        right_bottom,
    )

    # ------------------------------------------------------
    # 3. One combined SLOW / FAST card.
    # ------------------------------------------------------

    fastslow_top = panel_bottom + SECTION_GAP + 20

    fastslow_bottom = draw_fastslow_card(
        draw,
        fast=fast,
        slow=slow,
        slow_available=slow_available,
        fast_available=fast_available,
        total_notes=sum(judges.values()),
        top=fastslow_top,
    )

    # 4. Generate analysis text once.
    badge, badge_color, badge_fill = generate_play_badge(
        precision=precision,
        balance=balance,
        balance_available=balance_available,
        fast=fast,
        slow=slow,
        amazing_plus=judges.get("AMAZING+", 0),
    )
    if show_comment:
        comment = generate_comment(
            achievement=achievement,
            precision=precision,
            balance=balance,
            balance_available=balance_available,
            rank=rank,
            fast=fast,
            slow=slow,
        )
    else:
        comment = "解析コメントはありません。\n（コメント表示OFFまたは解析対象外）"

    # 5. Lower cards: independent left/right placement.
    draw_analysis_result_card(
        draw,
        badge=badge,
        badge_color=badge_color,
        badge_fill=badge_fill,
        comment=comment,
        rect=LOWER_LEFT_RECT,
    )

    ranking_enabled = (
        ranking_position is not None
        and ranking_comparison_total is not None
        and ranking_top_percent is not None
        and bool(ranking_title)
        and bool(ranking_rank)
        and ranking_distribution is not None
    )

    if ranking_enabled:
        draw_ranking_result_card(
            image,
            draw,
            ranking_position=ranking_position,
            comparison_total=ranking_comparison_total,
            ranking_top_percent=ranking_top_percent,
            ranking_title=ranking_title,
            ranking_rank=ranking_rank,
            rank_distribution=ranking_distribution,
            analysis_date=ranking_analysis_date,
            top=LOWER_RIGHT_RECT[1],
            rect=LOWER_RIGHT_RECT,
        )

    # 6. Footer is anchored to the bottom of the fixed 1450px canvas.
    draw_footer(draw, top=FOOTER_RECT[1])

    # Never leave stale/unused canvas below the designed layout.
    image = image.crop((0, 0, CARD_WIDTH, CARD_HEIGHT))

    save_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(save_path, optimize=True)
    return str(save_path)

# ==========================================================
# End of File
# ==========================================================
