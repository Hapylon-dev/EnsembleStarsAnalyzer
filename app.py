"""
app.py
Version : Version 1.3

Ensemble Stars!! Music
Tap Timing Analyzer
"""

from __future__ import annotations

from pathlib import Path
import re
import os
import tempfile
import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

sys.path.append(str(Path(__file__).parent / "src"))

import config

from analyzer import analyze
from score import score
from result_card import create_result_card
from share import create_tweet_url

# ==========================================================
# Release Validation Settings
# ==========================================================

MAX_MUSIC_LENGTH = 80
MAX_UPLOAD_SIZE_MB = 20
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Ensemble Stars!! Music Tap Timing Analyzer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================================
# Device Detection
# ==========================================================

if config.DEBUG_MODE:
    debug_inner_width = streamlit_js_eval(
        js_expressions="window.innerWidth",
        key="debug_inner_width"
    )

    debug_client_width = streamlit_js_eval(
        js_expressions="document.documentElement.clientWidth",
        key="debug_client_width"
    )

    debug_screen_width = streamlit_js_eval(
        js_expressions="screen.width",
        key="debug_screen_width"
    )

    st.sidebar.write("JS Width Debug")
    st.sidebar.write(f"innerWidth : {debug_inner_width}")
    st.sidebar.write(f"clientWidth : {debug_client_width}")
    st.sidebar.write(f"screen.width : {debug_screen_width}")

def get_device_type():
    """
    画面幅からデバイス種別を判定
    """

    width = streamlit_js_eval(
        js_expressions="window.innerWidth",
        key="device_width"
    )

    # 初回描画時は取得できないことがある
    if width is None:
        width = 1200

    is_mobile = width < 768
    is_tablet = 768 <= width < 1200
    is_pc = width >= 1200

    return {
        "width": width,
        "is_mobile": is_mobile,
        "is_tablet": is_tablet,
        "is_pc": is_pc,
    }


DEVICE = get_device_type()

SCREEN_WIDTH = DEVICE["width"]

IS_MOBILE = DEVICE["is_mobile"]

IS_TABLET = DEVICE["is_tablet"]

IS_PC = DEVICE["is_pc"]

# ==========================================================
# Debug
# ==========================================================


if config.DEBUG_MODE:

    with st.sidebar:

        st.caption("Device")

        st.write(f"Width : {SCREEN_WIDTH}")

        if IS_PC:
            st.success("PC")

        elif IS_TABLET:
            st.info("Tablet")

        else:
            st.warning("Mobile")

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* ==========================================================
   Main Content Width
   ========================================================== */

[data-testid="stMainBlockContainer"] {
    max-width: 1600px;
    margin-left: auto;
    margin-right: auto;
}


/* ==========================================================
   App Header
   ========================================================== */

.app-header {

    text-align: center;

    padding: 24px 20px;

    margin-bottom: 24px;

    border-radius: 22px;

    background:
        linear-gradient(
            180deg,
            #FCFAFF 0%,
            #F6F0FF 40%,
            #FFFFFF 100%
        );

    border: 1px solid #E7DBF8;

    box-shadow:
        0 6px 18px rgba(123,44,191,0.08),
        inset 0 1px 0 rgba(255,255,255,0.95);

    position: relative;

    overflow: hidden;

}
            
.app-header::marker {
    display: none;
}
            
.app-header::before {

    content: "";

    position: absolute;

    left: -10%;

    top: -45%;

    width: 120%;

    height: 70%;

    background: linear-gradient(

        180deg,

        rgba(255,255,255,0.85),

        rgba(255,255,255,0.25),

        rgba(255,255,255,0.0)

    );

    transform: rotate(-4deg);

    pointer-events: none;

}
        
.app-header::after {

    content: "";

    position: absolute;

    inset: 0;

    pointer-events: none;

    background-image:

        radial-gradient(circle, rgba(255,255,255,0.90) 0 1px, transparent 2px),

        radial-gradient(circle, rgba(255,245,210,0.75) 0 1.5px, transparent 2.5px),

        radial-gradient(circle, rgba(230,220,255,0.80) 0 1px, transparent 2px);

    background-size:

        180px 180px,

        240px 240px,

        210px 210px;

    background-position:

        28px 24px,

        145px 70px,

        290px 36px;

    opacity: 0.45;

}
            
.app-header .header-divider {

    position: absolute;

    left: 5%;

    right: 5%;

    bottom: 0;

    height: 3px;

    border-radius: 999px;

    background: linear-gradient(
        90deg,
        rgba(180,150,255,0.00),
        rgba(180,150,255,0.55),
        rgba(255,255,255,0.90),
        rgba(180,150,255,0.55),
        rgba(180,150,255,0.00)
    );

}

.app-title {

    font-size: 40px;

    font-weight: 800;

    color: #7B2CBF;

    line-height: 1.1;

    text-shadow:
        0 1px 0 rgba(255,255,255,0.95),
        0 2px 6px rgba(123,44,191,0.15);

    position: relative;

    z-index: 2;

}

.app-subtitle {

    font-size: 28px;

    font-weight: 700;

    color: #666A85;

    margin-top: 5px;

    letter-spacing: 0.5px;
            
    position: relative;

    z-index: 2;

}

.app-fan-tool {
    margin-top: 18px;
    font-size: 18px;
    font-weight: 700;
    color: #444444;
}

.app-description {
    margin-top: 12px;
    font-size: 15px;
    color: #666666;
    line-height: 1.6;
}


/* ==========================================================
   Headings
   ========================================================== */

h1 {
    color: #7B2CBF;
    font-weight: 800;
}

h2,
h3 {
    color: #6A0DAD;
}


/* ==========================================================
   Button
   ========================================================== */

div.stButton > button {

    min-height:56px;

    font-size:18px;

    font-weight:700;

    box-shadow:
        0 6px 14px rgba(123,44,191,.18);

}

div.stButton > button:hover {

    transform:translateY(-2px);

    box-shadow:
        0 10px 22px rgba(123,44,191,.28);

}

/* ==========================================================
   Progress Bar
========================================================== */

.stProgress > div {

    border-radius: 12px;
    overflow: hidden;

}

.stProgress > div > div > div > div {

    background: #7A3CF0;

}

/* ==========================================================
   Download Button
========================================================== */

div.stDownloadButton > button{

    min-height:52px;

    border-radius:14px;

    font-size:16px;

    font-weight:700;

    background:#7A3CF0;

    color:white;

    border:none;

    box-shadow:
        0 6px 14px rgba(123,44,191,.18);

    transition:all .18s ease;

}

div.stDownloadButton > button:hover{

    background:#6A2EE0;

    transform:translateY(-2px);

    box-shadow:
        0 10px 22px rgba(123,44,191,.28);

}

/* ==========================================================
   Link Button
========================================================== */

div.stLinkButton > a{

    min-height:52px;

    border-radius:14px;

    font-size:16px;

    font-weight:700;

    background:#242424;

    color:white;

    border:none;

    box-shadow:
        0 6px 14px rgba(0,0,0,.18);

}

div.stLinkButton > a:hover{

    background:#111111;

    transform:translateY(-2px);

}

/* ==========================================================
   Streamlit Components
   ========================================================== */

details {
    border-radius: 10px;
}

[data-testid="stMetric"] {
    border: 1px solid #DDDDDD;
    border-radius: 10px;
    padding: 8px;
}

[data-testid="stInfo"] {
    border-radius: 10px;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

[data-testid="stTextInput"] {
    padding-top: 6px;
}

[data-testid="stNumberInput"] {
    padding-top: 6px;
}

[data-testid="stSelectbox"] {
    padding-top: 6px;
}

[data-testid="stFileUploader"] {
    padding-top: 6px;
}

hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}


/* ==========================================================
   Tablet Responsive
   768px - 1199px
   ========================================================== */

@media (min-width: 768px) and (max-width: 1199px) {

    .app-title {
        font-size: 34px;
    }

    .app-subtitle {
        font-size: 24px;
    }

    .app-fan-tool {
        font-size: 17px;
    }
}


/* ==========================================================
   Mobile Responsive
   767px以下
   ========================================================== */

@media (max-width: 767px) {

    [data-testid="stMainBlockContainer"] {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1 {
        font-size: 1.8rem;
    }

    h2 {
        font-size: 1.5rem;
    }

    h3 {
        font-size: 1.25rem;
    }

    div.stButton > button {
        min-height: 52px;
        font-size: 16px;
        border-radius: 12px;
    }

    hr {
        margin-top: 1.4rem;
        margin-bottom: 1.4rem;
    }

    .app-header {
        padding-top: 6px;
        padding-bottom: 10px;
    }

    .app-title {
        font-size: 28px;
        line-height: 1.2;
    }

    .app-subtitle {
        font-size: 21px;
        margin-top: 6px;
    }

    .app-fan-tool {
        margin-top: 14px;
        font-size: 16px;
    }

    .app-description {
        margin-top: 10px;
        font-size: 14px;
        line-height: 1.6;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# Header
# ==========================================================

st.markdown(
    f"""
<div class="app-header">
<div class="app-title">✨ Ensemble Stars!! Music ✨</div>
<div class="app-subtitle">Tap Timing Analyzer</div>
<div class="app-fan-tool">あんさんぶるスターズ！！Music 非公式ファンツール</div>
<div class="app-description">
タップタイミング棒グラフ（3本以下）を解析し、<br>
判定分布を独自アルゴリズムで推定します。
</div>
<div class="header-divider"></div>
</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# Layout Utility
# ==========================================================

# ==========================================================
# Input Layout
# ==========================================================

INPUT_LEFT_RATIO = 1.15
INPUT_RIGHT_RATIO = 1.0


def create_input_columns():
    """
    入力画面レイアウト
    """

    left, right = st.columns(
        [INPUT_LEFT_RATIO, INPUT_RIGHT_RATIO],
        vertical_alignment="top",
    )

    return left, right

def create_result_columns():
    """
    Result表示レイアウト
    """

    image_col, result_col = st.columns(
        [1.05, 1.15],
        vertical_alignment="top",
    )

    return image_col, result_col

def create_share_columns():
    """
    共有ボタンレイアウト
    """

    if IS_PC:
        return st.columns(2)

    return (
        st.container(),
        st.container(),
    )

st.divider()

# ==========================================================
# Input Area
# ==========================================================

st.markdown("""
<div style="padding:18px;
border-radius:12px;
border:2px solid #8E44AD;
background-color:#F7F3FF;">

<h3 style="color:#7D3C98;margin-top:0;">
解析可能な画像
</h3>

✅ 新UI（2025年4月29日以降）<br>

✅ スクリーンショット<br>

✅ 編集・加工していない高解像度の画像<br>

✅ タップタイミンググラフを表示<br>

✅ 棒グラフ3本以下（中央を含む）<br>

✅ MISS = 0（総ノーツ = 最高判定）<br>

✅ PERFECT COMBO（内部 ALL AMAZING）または ALL AMAZING<br><br>

<b style="color:#C0392B;">
※条件を満たさない画像では
正しい解析結果が得られない場合があります。
</b>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# Input Card
# ==========================================================

st.markdown("""
<div style="
border:1px solid #E2D8F5;
border-radius:12px;
padding:24px;
background:#FFFFFF;
">
<h3 style="margin-top:0;color:#7B2CBF;">
⚙️ 解析設定
</h3>

<p style="
margin-top:6px;
color:#666666;
font-size:15px;
">

楽曲情報・難易度・レベル・
総ノーツ数を入力してください。

</p>
</div>
""", unsafe_allow_html=True)

upload_col, info_col = create_input_columns()

# ----------------------------------------------------------
# Upload
# ----------------------------------------------------------

with upload_col:

    st.markdown("### 🖼️ リザルト画像")

    st.caption(
        "解析するリザルト画面のスクリーンショットを選択してください。"
    )

    st.info(
        "📷 PNG・JPG・JPEG形式のスクリーンショットに対応しています。"
    )

    uploaded_file = st.file_uploader(
        "リザルト画像",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
    )

# ----------------------------------------------------------
# Song Information
# ----------------------------------------------------------
with info_col:

    st.markdown("### 🎼 楽曲情報")

    st.caption(
        "リザルト画面に表示されている内容を入力してください。"
    )

    music = st.text_input(
        "🎵 楽曲名",
        placeholder="例：BRAND NEW STARS!!",
        max_chars=MAX_MUSIC_LENGTH,
        help=f"最大{MAX_MUSIC_LENGTH}文字まで入力できます。"
    )

    difficulty = st.selectbox(
        "🎼 難易度",

        [

            "Easy",

            "Normal",

            "Hard",

            "Expert",

            "Special"

        ],

        index=3

    )

    # ==========================================================
    # Level List
    # ==========================================================

    LEVEL_LIST = {
        "Easy": [
            "5", "6", "7", "8", "9", "10"
        ],

        "Normal": [
            "11", "12", "13", "14", "15", "16", "17"
        ],

        "Hard": [
            "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"
        ],

        "Expert": [
            "23",
            "24",
            "25",
            "26", "26+",
            "27", "27+",
            "28", "28+",
            "29", "29+",
            "30", "30+",
        ],

        "Special": [
            "26", "26+",
            "27", "27+",
            "28", "28+",
            "29", "29+",
            "30", "30+",
            "31", "31+",
            "♪", "♪♪", "♪♪♪", "♪♪♪♪", "♪♪♪♪♪", "♪♪♪♪♪♪",
        ],
    }

    level_list = LEVEL_LIST[difficulty]

    level = st.selectbox(
        "⭐ レベル",
        level_list,
    )

    difficulty_name = difficulty.upper()

    if difficulty == "Easy":
        background_style = "background:#2F8FE8;"

    elif difficulty == "Normal":
        background_style = "background:#FDD835; color:#222;"

    elif difficulty == "Hard":
        background_style = "background:#EB4036;"

    elif difficulty == "Special":
        background_style = (
            "background:#FF4F9E;"
            "border:2px solid #C63E79;"
        )

    else:

        background_style = (
            "background: linear-gradient("
            "90deg,"
            "#FFE6A8 0%,"
            "#FFF9E8 10%,"
            "#D8F7B0 22%,"
            "#9CF0D5 36%,"
            "#B8E5FF 50%,"
            "#C7D6FF 64%,"
            "#E1C6FF 78%,"
            "#FFD0E7 90%,"
            "#FFF0F8 100%"
            ");"
            "border:2px solid #2D4A5F;"
            "box-shadow:"
            "0 0 8px rgba(255,255,255,.9) inset,"
            "0 0 10px rgba(0,0,0,.18);"
        )
    
    st.markdown(
        f"""
    <div style="
    padding:10px 12px;
    margin-top:10px;
    border-radius:12px;
    {background_style}
    color:white;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,.25);
    border:2px solid rgba(255,255,255,.25);
    ">

    <div style="
    font-size:26px;
    text-shadow:1px 1px 2px black;
    font-weight:700;
    letter-spacing:1px;
    ">
    {difficulty_name}
    </div>

    <div style="
    margin-top:4px;
    text-align:center;
    ">

    <div style="
    margin-top:5px;
    font-size:16px;
    font-weight:700;
    color:#27486A;
    text-shadow:0 1px 2px rgba(255,255,255,.95);
    ">
    Lv. {level}
    </div>

    </div>

    </div>
    """,
        unsafe_allow_html=True,
    )


    st.markdown("#### 🔢 総ノーツ数")

    total_notes = st.number_input(
        "総ノーツ数",
        min_value=1,
        value=1,
        step=1,
        help=(
            "ライブの総ノーツ数を入力してください。\n\n"
            "ゲームのリザルト画面に表示される総ノーツ数を入力してください。\n"
            "誤った値では正しい解析結果になりません。"
        )
    )

    st.divider()

# ==========================================================
# Analyze
# ==========================================================
st.markdown("""
<div style="
padding:12px 16px;
border-radius:12px;
background:#F6F1FF;
border:1px solid #DCCAF7;
margin-bottom:10px;
">

<b style="color:#6A2EB8;">
ℹ 解析の流れ
</b>

<div style="margin-top:6px; color:#555; line-height:1.7;">

・タップタイミング棒グラフ解析<br>
・判定分布の推定<br>
・Result Card生成

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
padding:12px 16px;
border-radius:12px;
background:#FFF8E5;
border:1px solid #FFD56A;
margin-bottom:18px;
">

<b style="color:#C67C00;">
⚠ 解析可能な画像をご確認ください
</b>

<div style="margin-top:6px;color:#666;">
条件を満たさない画像では
正しい解析結果が得られない場合があります。
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("## ▶ タップタイミング解析")

st.caption(
    "スクリーンショットから判定分布を推定し、Result Card を生成します。"
)

st.write("")

analyze_button = st.button(
    "▶ 解析開始",
    type="primary",
    width="stretch"
)

if analyze_button:

    # ==========================================================
    # Input Validation
    # ==========================================================

    errors = []

    if not music.strip():
        errors.append("🎵 楽曲名")

    if uploaded_file is None:
        errors.append("📷 リザルト画像")

    if errors:

        st.error(
            "以下の項目を入力してください。"
        )

        for item in errors:
            st.markdown(f"- {item}")

        st.stop()

    if uploaded_file.size > MAX_UPLOAD_SIZE_BYTES:
        st.error(
            "❌ 画像ファイルのサイズが大きすぎます。"
        )
        st.info(
            f"アップロードできる画像は最大{MAX_UPLOAD_SIZE_MB}MBです。"
            "より小さい画像を使用してください。"
        )
        st.stop()

    if total_notes == 1:

        st.warning(
            "⚠️ 総ノーツ数が初期値のままです。入力内容を確認してください。"
        )

    suffix = Path(
        uploaded_file.name
    ).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(
            uploaded_file.getbuffer()
        )

        image_path = temp_file.name

    try:

        # ==========================================================
        # Progress UI
        # ==========================================================

        progress_container = st.container()

        with progress_container:

            progress_title = st.empty()
            progress_bar = st.progress(0)
            progress_status = st.empty()

        progress_title.markdown("""
        ### 🔄 タップタイミング解析中

        Result Card を生成しています。
        処理には数秒かかる場合があります。
        """)

        progress_status.markdown("""
        **現在の処理**

        ⏳ リザルト画像読込

        ⬜ 棒グラフ解析

        ⬜ 判定推定

        ⬜ Result Card生成
        """)

        progress_bar.progress(10)

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ⏳ 棒グラフ解析

        ⬜ 判定推定

        ⬜ Result Card生成
        """)

        progress_bar.progress(35)

        estimate_result = analyze(
            image_path=image_path,
            total_notes=total_notes,
        )

        graph_image = Path(config.OUTPUT_DIR) / config.GRAPH_FILENAME

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ✅ 棒グラフ解析

        ⏳ 判定推定

        ⬜ Result Card生成
        """)

        progress_bar.progress(65)

        analysis_score = score(
            estimate_result,
            total_notes=total_notes,
        )

        achievement = analysis_score.achievement

        if config.DEBUG_MODE:
            st.write("=== DEBUG: EstimateResult ===")
            st.write("total_notes:", total_notes)
            st.write("distribution:", estimate_result.distribution)
            st.write("amazing_plus:", estimate_result.amazing_plus)
            st.write("amazing:", estimate_result.amazing)
            st.write("perfect:", estimate_result.perfect)
            st.write("fast:", estimate_result.fast)
            st.write("slow:", estimate_result.slow)

            st.write("=== DEBUG: AnalysisScore ===")
            st.write("achievement:", analysis_score.achievement)
            st.write("precision:", analysis_score.precision)
            st.write("balance:", analysis_score.balance)
            st.write("overall_score:", analysis_score.overall_score)
            st.write("rank:", analysis_score.rank)

            amazing = 0
            perfect = 0

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ✅ 棒グラフ解析

        ✅ 判定推定

        ⏳ Result Card生成
        """)

        progress_bar.progress(90)

        # ==========================================================
        # Calculate Result Values
        # ==========================================================

        amazing_plus = estimate_result.distribution.get(
            "AMAZING+",
            0
        )

        amazing = (
            estimate_result.fast
            + estimate_result.slow
        )

        # ==========================================================
        # Result Card
        # ==========================================================

        card_path = create_result_card(

            music=music,

            difficulty=difficulty,

            level=level,

            amazing_plus=amazing_plus,

            amazing=amazing,

            perfect=0,

            great=0,

            good=0,

            bad=0,

            miss=0,

            total_notes=total_notes,

            fast=estimate_result.fast,

            slow=estimate_result.slow,

            slow_available=(
                "AMAZING(SLOW)" in estimate_result.distribution
                or "PERFECT(SLOW)" in estimate_result.distribution
            ),

            fast_available=(
                "AMAZING(FAST)" in estimate_result.distribution
                or "PERFECT(FAST)" in estimate_result.distribution
            ),

            achievement=analysis_score.achievement,

            precision=analysis_score.precision,

            precision_grade=analysis_score.precision_grade,

            balance=analysis_score.balance,

            balance_grade=analysis_score.balance_grade,

            balance_available=analysis_score.balance_available,

            overall_score=analysis_score.overall_score,

            rank=analysis_score.rank

        )

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ✅ 棒グラフ解析

        ✅ 判定推定

        ✅ Result Card生成
        """)

        progress_bar.progress(100)

        progress_container.empty()

        st.success(
            "✅ 解析が正常に完了しました。"
        )

        tweet_url = create_tweet_url(

            music=music,

            difficulty=difficulty,

            level=level,

            amazing_plus=amazing_plus,

            amazing=amazing,

            fast=estimate_result.fast,

            slow=estimate_result.slow,

            achievement=analysis_score.achievement,

            precision=analysis_score.precision,

            balance=analysis_score.balance,

            overall_score=analysis_score.overall_score,

            rank=analysis_score.rank

        )

    except ValueError as error:

        progress_container.empty()

        error_message = str(error)

        if "画像の解像度が低すぎるため" in error_message:

            st.error(
                "❌ 画像の解像度が低すぎます。"
            )

            st.warning(
                "タイミンググラフを正確に解析できないため、"
                "解析を中止しました。"
            )

            st.info(
                "より高解像度のリザルト画像を使用してください。"
            )

            if config.DEBUG_MODE:

                st.caption(error_message)

        elif "解析対象は1～3本ですが" in error_message:

            st.error(
                "❌ タップタイミンググラフを正しく解析できませんでした。"
            )

            st.warning(
                "解析対象となる1～3本のタイミングバーを"
                "正しく検出できなかったため、解析を中止しました。"
            )

            st.info(
                "タップタイミング棒グラフ全体が"
                "はっきり表示されたリザルト画像を使用してください。"
            )

            if config.DEBUG_MODE:

                st.caption(error_message)

        else:

            if config.DEBUG_MODE:

                st.exception(error)

            else:

                st.error(
                    "❌ 解析中にエラーが発生しました。"
                )

                st.info(
                    "入力内容や画像をご確認のうえ、"
                    "もう一度解析してください。"
                )

        st.stop()

    except Exception as error:

        progress_container.empty()

        if config.DEBUG_MODE:

            st.exception(error)

        else:

            st.error(
                "❌ 解析中にエラーが発生しました。"
            )

            st.info(
                "入力内容や画像をご確認のうえ、"
                "もう一度解析してください。"
)

        st.stop()

    finally:
        # 解析用に作成した一時画像を必ず削除する
        if "image_path" in locals():
            try:
                os.remove(image_path)
            except FileNotFoundError:
                pass
            except OSError:
                if config.DEBUG_MODE:
                    st.caption("一時画像ファイルを削除できませんでした。")

    # ==========================================================
    # Result Card Preview
    # ==========================================================

    st.markdown("## 📊 解析結果")

    st.caption(
        "解析結果カードを生成しました。"
    )

    st.markdown("## 🖼️ Result Card")

    st.caption(
        "生成されたResult Cardです。クリックすると拡大表示できます。"
    )

    st.image(
        card_path,
        use_container_width=True,
    )
    
    st.markdown("## 💾 保存・共有")
    st.caption("Result Card を保存したり、𝕏 へ共有したりできます。")

    share_col1, share_col2 = st.columns(
        [1, 1],
        gap="medium",
    )

    with share_col1:

        st.markdown("#### 📥 Result Card 保存")

        st.caption(
            "Result CardをPNG形式で保存できます。"
        )

        # ----------------------------------------------------------
        # Download File Name
        # ----------------------------------------------------------

        safe_music_name = re.sub(
            r'[\\/:*?"<>|]',
            "_",
            music.strip(),
        )

        safe_music_name = safe_music_name.rstrip(" .")

        if not safe_music_name:
            safe_music_name = "Result"

        # ファイル名が極端に長くならないよう制限
        safe_music_name = safe_music_name[:80]

        download_file_name = (
            f"{safe_music_name}_ResultCard.png"
        )

        with open(card_path, "rb") as file:

            st.download_button(

                label="📥 Result Card を保存",

                data=file,

                file_name=download_file_name,

                mime="image/png",

                use_container_width=True,

            )
        
        st.caption(
            "※ 保存した画像はSNSなどで共有できます。"
        )

    with share_col2:

        st.markdown("#### 𝕏 結果を共有")

        st.caption(
            "Xへ解析結果を投稿できます。"
        )

        st.link_button(

            label="𝕏 結果を共有",

            url=tweet_url,

            use_container_width=True,

        )

    st.divider()

    # ----------------------------------------------------------
    # Result Image
    # ----------------------------------------------------------

    st.markdown("## 📷 解析画像")

    st.caption(
        "解析対象となったリザルト画像です。"
    )

    st.image(
        uploaded_file,
        use_container_width=True,
    )

    # ==========================================================
    # Developer Information
    # ==========================================================

    if config.DEBUG_MODE:

        with st.expander(
            "🛠️ Developer Information",
            expanded=False,
        ):

            st.caption(
                "開発・デバッグ用の情報です。通常は確認する必要はありません。"
            )

            dev_col1, dev_col2 = st.columns(2)

            with dev_col1:

                st.metric(
                    "推定ノーツ合計",
                    sum(estimate_result.estimated_notes)
                )

                st.metric(
                    "推定精度",
                    f"{estimate_result.estimated_accuracy:.2f}%"
                )

            with dev_col2:

                st.metric(
                    "FAST",
                    estimate_result.fast
                )

                st.metric(
                    "SLOW",
                    estimate_result.slow
                )

            st.write("")

            st.markdown("#### 判定分布")

            distribution_df = pd.DataFrame({

                "判定": list(estimate_result.distribution.keys()),

                "推定数": list(estimate_result.distribution.values())

            })

            st.table(distribution_df)

    # ==========================================================
    # Graph
    # ==========================================================


    st.divider()

    with st.expander(
        "📈 解析に使用した棒グラフ",
        expanded=False
    ):

        st.markdown("""
        <div style="
        border:1px solid #DDDDDD;
        border-radius:12px;
        padding:20px;
        background:#FCFCFC;
        ">
        <h3 style="
        margin-top:0;
        color:#7B2CBF;
        ">
        解析に使用した棒グラフ
        </h3>

        <p style="
        color:#666666;
        margin-top:-5px;
        ">
        解析に使用した棒グラフです。<br>
        正しく検出されていることをご確認ください。
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.image(
            graph_image,
            use_container_width=True,
        )

        st.success(
            "✓ この棒グラフを使用して解析しました。"
        )

        st.caption(
            "現在は棒グラフ3本以下（中央を含む）の画像を解析対象としています。"
        )

    # ==========================================================
    # Information
    # ==========================================================

    st.divider()

    with st.expander(
        "ℹ️ この解析について",
        expanded=False
    ):

        st.markdown("""
        <div style="
        border:1px solid #DDDDDD;
        border-radius:12px;
        padding:22px;
        background:#FCFCFC;
        ">

        <h3 style="
        margin-top:0;
        color:#7B2CBF;
        ">
        解析について
        </h3>

        <p>

        本ツールはタップタイミング棒グラフ（3本以下）から
        独自アルゴリズムによって判定分布を推定しています。

        </p>

        <p>

        表示される
        <b>AMAZING+ ～ MISS</b>
        は推定値です。

        ゲーム内部で実際に使用されている
        判定・評価・計算方法を
        再現したものではありません。

        </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        <div style="
        border:1px solid #FFCC80;
        border-radius:12px;
        padding:20px;
        background:#FFF8E1;
        ">

        <h3 style="margin-top:0;color:#E65100;">

        解析可能な画像

        </h3>

        <ul>

        <li>新UI（2025年4月29日以降）</li>

        <li>スクリーンショット</li>

        <li>画像編集をしていない高解像度のもの</li>

        <li>タップタイミングを表示</li>

        <li>棒グラフ3本以下（中央を含む）</li>

        <li>MISS = 0（総ノーツ = 最高判定）</li>

        <li>PERFECT COMBO（内部 ALL AMAZING）または ALL AMAZING</li>

        </ul>

        <b>

        条件を満たさない画像では、
        正しい解析結果が得られない場合があります。

        </b>

        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="
    padding:18px;
    background:#F5F5F5;
    border-radius:12px;
    font-size:14px;
    color:#555555;
    ">

    <b>
    ⚠️ 免責事項
    </b>

    <br><br>

    当Webアプリは、株式会社Happy Elementsのゲームブランドである
                
    カカリアスタジオが配信・運営する
                
    スマートフォン向けアイドル育成リズムゲーム

    「あんさんぶるスターズ！！Music」

    の非公式ファンツールです。

    本ツールはHappy Elements株式会社とは関係ありません。

    <br><br>

    「あんさんぶるスターズ！！」

    「あんさんぶるスターズ！！Music」

    に関する名称・画像・ロゴ・キャラクター等の権利は、
    それぞれの権利者に帰属します。

    <br><br>

    本ツールは
    ゲームデータを改変・抽出するものではなく、

    ユーザー自身が取得した
    リザルト画像を解析することのみを目的としています。

    <br><br>

    解析結果は
    独自アルゴリズムによる推定値であり、

    ゲーム内部で実際に使用されている
    判定値・計算方法を示すものではありません。

    <br><br>

    本ツールの利用によって生じた
    いかなる損害についても、
    開発者は一切責任を負いません。

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div style="
    text-align:center;
    padding:20px 10px;
    color:#666666;
    font-size:14px;
    ">

    <div style="
    font-size:20px;
    font-weight:700;
    color:#7B2CBF;
    margin-bottom:14  px;
    ">

    Ensemble Stars!! Music Tap Timing Analyzer

    </div>

    <div style="
    margin-bottom:6px;
    ">

    Unofficial Fan Tool

    </div>

    <div style="
    font-size:13px;
    color:#999999;
    ">

    Developed by Hapylon with ChatGPT

    </div>

    </div>
    """, unsafe_allow_html=True)