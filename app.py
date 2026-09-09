"""
app.py
あんさんぶるスターズ！！Music タップタイミング解析ツール

Ensemble Stars!! Music
Tap Timing Analyzer
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import os
import tempfile
import sys
import cv2

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

sys.path.append(str(Path(__file__).parent / "src"))

import config

from analyzer import analyze
from score import score
from result_card import create_result_card, generate_play_badge
from share import create_tweet_url
from ranking import load_ranking_base, calculate_ranking, build_rank_distribution

# ==========================================================
# Release Validation Settings
# ==========================================================

MAX_MUSIC_LENGTH = 50
MAX_UPLOAD_SIZE_MB = 20
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="あんさんぶるスターズ！！Music タップタイミング解析ツール",
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
:root {
    --app-bg: #eef0f3;
    --app-surface: #ffffff;
    --app-surface-2: #f7f8fa;
    --app-surface-3: #eceef2;
    --app-line: #d4d8df;
    --app-line-strong: #aeb5c0;
    --app-text: #2f3440;
    --app-muted: #68717e;
    --app-accent: #ff4d8d;
    --app-accent-2: #8b5cf6;
    --app-accent-3: #22d3ee;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main,
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {
    background: var(--app-bg) !important;
}
body, p, li, span, div, label { color: var(--app-text); }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color:#454c58 !important; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color:#66707d !important; }

[data-testid="stAppViewContainer"] {
    color: var(--app-text) !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1480px;
    margin: 0 auto;
    padding-top: 1.0rem;
    padding-bottom: 3rem;
}

/* ---------- Hero / visual direction ---------- */
.app-hero {
    position: relative;
    overflow: hidden;
    padding: 54px 46px 42px;
    margin: 0 0 30px;
    border-radius: 28px;
    color: #303640;
    background:
        radial-gradient(circle at 8% 18%, rgba(255,77,141,.28), transparent 28%),
        radial-gradient(circle at 90% 18%, rgba(139,92,246,.26), transparent 32%),
        linear-gradient(135deg, #e8eaf0 0%, #f7f8fa 48%, #e5e8ee 100%);
    border: 1px solid #2c2c38;
    box-shadow: 0 18px 46px rgba(45,52,64,.14);
}
.app-hero::before {
    content:"";
    position:absolute;
    inset:-40%;
    background: repeating-linear-gradient(115deg, transparent 0 24px, rgba(255,255,255,.035) 25px 26px);
    transform: rotate(-5deg);
    pointer-events:none;
}
.app-hero::after {
    content:"";
    position:absolute;
    width:280px; height:280px;
    right:-100px; bottom:-150px;
    border-radius:50%;
    border:1px solid rgba(255,255,255,.13);
    box-shadow: 0 0 0 30px rgba(255,255,255,.025), 0 0 0 60px rgba(255,255,255,.016);
}
.app-hero-inner { position:relative; z-index:2; max-width:980px; }
.app-kicker {
    display:inline-flex; align-items:center; gap:8px;
    padding:7px 12px; border-radius:999px;
    background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.12);
    font-size:12px; font-weight:900; letter-spacing:.10em;
    text-transform:uppercase;
}
.app-title { margin-top:18px; font-size:clamp(2rem,4vw,3.5rem); font-weight:950; line-height:1.02; letter-spacing:-.04em; color:#303640; }
.app-subtitle { margin-top:10px; font-size:clamp(1.05rem,2vw,1.55rem); font-weight:800; color:#5d4a92; letter-spacing:.02em; }
.app-fan-tool { margin-top:22px; font-size:15px; font-weight:850; color:#303640; }
.app-description { margin-top:9px; max-width:760px; font-size:14px; line-height:1.75; color:#68717e; }
.hero-rule { margin-top:28px; height:2px; width:100%; background:linear-gradient(90deg,#ff4d8d,#8b5cf6,#22d3ee,transparent); opacity:.9; }

/* ---------- Section headers ---------- */
.section-heading { display:flex; align-items:flex-end; justify-content:space-between; gap:18px; margin:32px 0 14px; }
.section-heading h2 { margin:0; font-size:clamp(1.35rem,2.3vw,1.9rem); color:#303640; font-weight:950; letter-spacing:-.025em; }
.section-heading p { margin:0; color:#66707d; font-size:13px; }

/* ---------- Generic surfaces ---------- */
.ui-card, .legal-box, .guide-tile {
    border:1px solid var(--app-line);
    border-radius:20px;
    background:linear-gradient(180deg,#17171f,#111118);
    box-shadow:0 10px 28px rgba(45,52,64,.10);
    color:var(--app-text);
}

/* ---------- Buttons ---------- */
div.stButton > button {
    min-height:52px !important; height:52px !important; max-height:52px !important;
    border-radius:14px !important; font-size:15px !important; font-weight:850 !important;
    background:#e7e9ee !important; color:#2f3440 !important;
    border:1px solid #5b6675 !important; box-shadow:0 7px 18px rgba(45,52,64,.12) !important;
    line-height:1 !important; padding:0 16px !important;
}
div.stButton > button:hover { transform:translateY(-1px); border-color:#bfc6d8 !important; }
div.stDownloadButton > button,
div[data-testid="stDownloadButton"] button,
div[data-testid="stLinkButton"] a {
    min-height:52px !important; height:52px !important; max-height:52px !important;
    border-radius:14px !important;
    font-size:15px !important;
    font-weight:850 !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    box-sizing:border-box !important;
}
div.stDownloadButton > button,
div[data-testid="stDownloadButton"] button {
    background:linear-gradient(135deg,#7c3aed,#a855f7) !important;
    color:#3b424d !important;
    border:1px solid rgba(45,52,64,.08) !important;
}
div.stLinkButton > a,
div[data-testid="stLinkButton"] a {
    background:#e7e9ee !important; color:#3b424d !important; border:1px solid #5b6675 !important;
    text-decoration:none !important;
}
div.stDownloadButton > button:hover,
div.stLinkButton > a:hover,
div[data-testid="stLinkButton"] a:hover { transform:translateY(-1px); }

/* ---------- Inputs ---------- */
[data-testid="stFileUploaderDropzone"], [data-baseweb="select"] > div, input, textarea {
    border-radius:13px !important;
}
[data-testid="stFileUploaderDropzone"] { border:1px dashed #aeb6c2 !important; background:#f7f8fa !important; }
[data-testid="stFileUploaderDropzone"] * { color:#454c58 !important; }
input, textarea, [data-baseweb="select"] > div, [data-testid="stNumberInput"] input {
    background:#ffffff !important; color:#2f3440 !important; border-color:#b7bec8 !important;
}
input::placeholder, textarea::placeholder {
    color:#7b8490 !important;
    -webkit-text-fill-color:#7b8490 !important;
    opacity:1 !important;
}
[data-testid="stNumberInput"] button { background:#e5e8ed !important; color:#2f3440 !important; border-color:#b7bec8 !important; }
[data-testid="stWidgetLabel"] label, label, .stTextInput label, .stSelectbox label { color:#2f3440 !important; }
.stAlert, [data-testid="stAlert"] * { color:#454c58 !important; }

/* ---------- Ranking ---------- */
.ranking-shell {
    overflow:hidden; border-radius:24px; padding:1px;
    background:linear-gradient(135deg,#ff4d8d,#8b5cf6,#22d3ee);
    box-shadow:0 16px 40px rgba(45,52,64,.12);
}
.ranking-inner { background:#ffffff; border-radius:23px; padding:24px; color:#303640; }
.ranking-hero-row { display:flex; justify-content:space-between; align-items:center; gap:18px; }
.ranking-eyebrow { color:#6954a8; font-size:12px; font-weight:950; letter-spacing:.12em; text-transform:uppercase; }
.ranking-title { margin-top:5px; font-size:26px; font-weight:950; letter-spacing:-.025em; }
.ranking-meta { margin-top:5px; color:#66707d; font-size:13px; }
.ranking-stat {
    min-width:150px; padding:14px 16px; border-radius:16px;
    background:linear-gradient(135deg,rgba(139,92,246,.22),rgba(34,211,238,.08));
    border:1px solid rgba(45,52,64,.08); text-align:center;
}
.ranking-stat .num { font-size:25px; font-weight:950; color:#303640; }
.ranking-stat .label { margin-top:2px; font-size:11px; color:#6954a8; }
.ranking-table-wrap { overflow-x:auto; -webkit-overflow-scrolling:touch; margin-top:18px; border-radius:16px; border:1px solid rgba(45,52,64,.12); }
.ranking-table { width:100%; border-collapse:collapse; min-width:760px; font-size:13px; background:#ffffff; }
.ranking-table th { padding:12px 13px; text-align:left; color:#6954a8; background:#f1f3f6; font-weight:850; white-space:nowrap; }
.ranking-table td { padding:11px 13px; border-top:1px solid rgba(45,52,64,.10); color:#424954; white-space:nowrap; }
.ranking-table tr:nth-child(even) td { background:rgba(45,52,64,.035); }
.ranking-table tr.me td { background:linear-gradient(90deg,rgba(139,92,246,.16),rgba(255,77,141,.08)); color:#2f3440; font-weight:900; }
.rank-pos { font-weight:950; color:#303640; }
.rank-top { color:#67e8f9; font-weight:850; }
.rank-badge { display:inline-block; min-width:42px; padding:3px 8px; border-radius:999px; background:rgba(45,52,64,.08); text-align:center; font-weight:900; }

/* ---------- Guide / policy ---------- */
.guide-grid { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:10px; margin-top:14px; }
.guide-tile { padding:16px; min-height:132px; }
.guide-tile .icon { font-size:22px; }
.guide-tile .title { margin-top:7px; font-weight:900; color:#353b46; }
.guide-tile .desc { margin-top:5px; font-size:12px; line-height:1.55; color:#66707d; }
.legal-box { padding:20px; line-height:1.8; }
.legal-box h4 { margin:0 0 10px; color:#5d4a92; }

hr { margin:2rem 0; border-color:#d7dbe1 !important; }

/* Streamlit containers / alerts */
[data-testid="stAlert"] { background:#ffffff !important; color:#424954 !important; border-color:#d2d6dd !important; }
[data-testid="stExpander"] { background:#ffffff !important; border:1px solid #d5d9e0 !important; border-radius:16px !important; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p { color:#353b46 !important; }

/* ---------- Responsive ---------- */
@media (max-width: 1200px) {
    .guide-grid { grid-template-columns:repeat(3,minmax(0,1fr)); }
}
@media (max-width: 900px) {
    .app-hero { padding:38px 30px 32px; }
    .guide-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media (max-width: 767px) {
    [data-testid="stMainBlockContainer"] { padding-left:.8rem; padding-right:.8rem; padding-top:.6rem; }
    .app-hero { padding:28px 20px 24px; border-radius:22px; margin-bottom:18px; }
    .app-title { font-size:28px; }
    .app-subtitle { font-size:19px; }
    .app-fan-tool { font-size:14px; margin-top:16px; }
    .app-description { font-size:13px; }
    .section-heading { display:block; }
    .section-heading p { margin-top:5px; }
    .guide-grid { grid-template-columns:1fr; }
    .ranking-inner { padding:18px; }
    .ranking-hero-row { align-items:flex-start; flex-direction:column; }
    .ranking-stat { width:100%; min-width:0; }
    div.stButton > button { min-height:52px !important; height:52px !important; font-size:16px !important; }
}

/* ---------- Final readability pass ---------- */

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
    background:#eef0f3 !important;
    color:#2f3440 !important;
}

[data-testid="stMainBlockContainer"] {
    color:#2f3440 !important;
}

[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] * {
    color:#3b424d !important;
}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color:#68717e !important;
}

[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] *,
label {
    color:#3a414c !important;
}


/* ==========================================================
   通常入力欄
   ========================================================== */

input,
textarea,
[data-testid="stNumberInput"] input {
    background:#fbfbfc !important;
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
    border-color:#9fa8b5 !important;
}

input::placeholder,
textarea::placeholder {
    color:#7b8490 !important;
    -webkit-text-fill-color:#7b8490 !important;
    opacity:1 !important;
}

/* ==========================================================
   難易度・レベル
   選択中の表示
   白文字 + 黒縁
   ========================================================== */

[data-testid="stSelectbox"] [data-baseweb="select"] {
    background:#fbfbfc !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background:#fbfbfc !important;
    color:#ffffff !important;
    border-color:#9fa8b5 !important;
}

/* Selectbox内部の表示文字 */
[data-testid="stSelectbox"] [data-baseweb="select"] > div > div {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    text-shadow:
        -1px -1px 0 #111111,
         1px -1px 0 #111111,
        -1px  1px 0 #111111,
         1px  1px 0 #111111 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div > div * {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    text-shadow:
        -1px -1px 0 #111111,
         1px -1px 0 #111111,
        -1px  1px 0 #111111,
         1px  1px 0 #111111 !important;
}


/* Selectbox内部の入力要素 */
[data-testid="stSelectbox"] [data-baseweb="select"] input {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

/* ==========================================================
   ファイルアップロード
   ========================================================== */

[data-testid="stFileUploaderDropzone"] {
    background:#f1f3f6 !important;
    border-color:#9fa8b5 !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color:#555e6b !important;
}


/* ==========================================================
   Number Input
   ========================================================== */

[data-testid="stNumberInput"] input {
    background:#fbfbfc !important;
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
    border-color:#9fa8b5 !important;
}

[data-testid="stNumberInput"] button {
    background:#e4e7ec !important;
    color:#3d4550 !important;
    border-color:#b7bec8 !important;
}

[data-testid="stNumberInput"] button * {
    color:#3d4550 !important;
}


/* ==========================================================
   Expander
   ========================================================== */

[data-testid="stExpander"] {
    background:#ffffff !important;
    border-color:#d1d5dc !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color:#343b46 !important;
}


/* ==========================================================
   Alert
   ========================================================== */

.stAlert,
[data-testid="stAlert"] {
    background:#f7f8fa !important;
    color:#454c58 !important;
}

.stAlert *,
[data-testid="stAlert"] * {
    color:#454c58 !important;
}


/* ==========================================================
   Cards
   ========================================================== */

.ui-card,
.legal-box,
.guide-tile {
    background:#f9fafb !important;
    color:#3b424d !important;
    border-color:#d2d6dd !important;
}

.guide-tile .title,
.legal-box h4 {
    color:#4b3c79 !important;
}

.guide-tile .desc {
    color:#69727f !important;
}


/* ==========================================================
   Ranking
   ========================================================== */

.ranking-inner {
    background:#ffffff !important;
    color:#303640 !important;
}

.ranking-table th {
    background:#eef0f4 !important;
    color:#55477d !important;
}

.ranking-table td {
    background:#ffffff !important;
    color:#414955 !important;
    border-top-color:#e0e3e8 !important;
}

.ranking-table tr:nth-child(even) td {
    background:#f8f9fb !important;
}

.ranking-table tr.me td {
    background:#eee8fb !important;
    color:#343a45 !important;
}

.rank-pos {
    color:#303640 !important;
}

.rank-top {
    color:#2f7d8c !important;
}

.rank-badge {
    background:#eceef2 !important;
    color:#3d4550 !important;
}


/* ==========================================================
   Header / Hero
   ========================================================== */

.section-heading h2,
.app-title {
    color:#2d333d !important;
}

.app-subtitle,
.app-fan-tool {
    color:#51427e !important;
}

.app-description,
.section-heading p {
    color:#66707d !important;
}

.app-kicker {
    background:#f0f1f5 !important;
    border-color:#d3d7de !important;
    color:#5a6270 !important;
}

.app-hero {
    color:#303640 !important;
    border-color:#d2d6dd !important;
}

.app-hero::before {
    background:
        repeating-linear-gradient(
            115deg,
            transparent 0 24px,
            rgba(70,78,92,.035) 25px 26px
        );
}


/* ==========================================================
   通常ボタン
   前のページ / 次のページ
   紫背景 + 白文字
   ========================================================== */

div.stButton > button {
    background:#6650a4 !important;
    color:#ffffff !important;
    border-color:#4f3d82 !important;
}

div.stButton > button *,
div.stButton > button p,
div.stButton > button span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

div.stButton > button:hover {
    background:#55418d !important;
    color:#ffffff !important;
    border-color:#43336f !important;
}

div.stButton > button:hover *,
div.stButton > button:hover p,
div.stButton > button:hover span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ==========================================================
   解析開始
   赤背景 + 白文字 + 黒縁
   ========================================================== */

div.stButton > button[kind="primary"] {
    background:#d92d3f !important;
    color:#ffffff !important;
    border-color:#b51f30 !important;
    box-shadow:0 8px 20px rgba(181,31,48,.20) !important;
}

div.stButton > button[kind="primary"] *,
div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    text-shadow:
        -1px -1px 0 #111111,
         1px -1px 0 #111111,
        -1px  1px 0 #111111,
         1px  1px 0 #111111 !important;
}

div.stButton > button[kind="primary"]:hover {
    background:#b51f30 !important;
    color:#ffffff !important;
}

div.stButton > button[kind="primary"]:hover *,
div.stButton > button[kind="primary"]:hover p,
div.stButton > button[kind="primary"]:hover span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ==========================================================
   リザルトカード 保存
   紫背景 + 白文字
   ========================================================== */

div[data-testid="stDownloadButton"] button {
    background:linear-gradient(135deg,#6d4cc2,#805ad5) !important;
    color:#ffffff !important;
    border-color:#5a3fa5 !important;
}

div[data-testid="stDownloadButton"] button *,
div[data-testid="stDownloadButton"] button p,
div[data-testid="stDownloadButton"] button span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    text-shadow:
        -1px -1px 0 #111111,
         1px -1px 0 #111111,
        -1px  1px 0 #111111,
         1px  1px 0 #111111 !important;
}

div[data-testid="stDownloadButton"] button:hover {
    background:linear-gradient(135deg,#5a3fa5,#6d4cc2) !important;
    color:#ffffff !important;
}

div[data-testid="stDownloadButton"] button:hover *,
div[data-testid="stDownloadButton"] button:hover p,
div[data-testid="stDownloadButton"] button:hover span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ==========================================================
   X 結果を共有
   黒背景 + 白文字
   ========================================================== */

div[data-testid="stLinkButton"] a {
    background:#111111 !important;
    color:#ffffff !important;
    border-color:#111111 !important;
}

div[data-testid="stLinkButton"] a *,
div[data-testid="stLinkButton"] a p,
div[data-testid="stLinkButton"] a span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    text-shadow:
        -1px -1px 0 #000000,
         1px -1px 0 #000000,
        -1px  1px 0 #000000,
         1px  1px 0 #000000 !important;
}

div[data-testid="stLinkButton"] a:hover {
    background:#000000 !important;
    color:#ffffff !important;
    border-color:#000000 !important;
}

div[data-testid="stLinkButton"] a:hover *,
div[data-testid="stLinkButton"] a:hover p,
div[data-testid="stLinkButton"] a:hover span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ==========================================================
   保存・共有ボタンの高さ統一
   ========================================================== */

div[data-testid="stDownloadButton"],
div[data-testid="stLinkButton"] {
    margin-top:0 !important;
}

div[data-testid="stDownloadButton"] button,
div[data-testid="stLinkButton"] a {
    min-height:52px !important;
    height:52px !important;
    max-height:52px !important;
    box-sizing:border-box !important;
}


/* ==========================================================
   Ranking page form
   ========================================================== */

.ranking-page-form input {
    text-align:center !important;
    font-weight:800 !important;
}


/* ==========================================================
   Legacy inline input / notice blocks
   ========================================================== */

[style*="background:#15151c"],
[style*="background:#111118"],
[style*="background:#18161a"] {
    background:#f9fafb !important;
    color:#3b424d !important;
}

[style*="color:#f4f4f5"],
[style*="color:#e4e4e7"],
[style*="color:#d8d0ff"],
[style*="color:white"] {
    color:#3b424d !important;
}

/* ----------------------------------------------------------
   保存・共有ボタンの高さを統一
   ---------------------------------------------------------- */
div[data-testid="stDownloadButton"],
div[data-testid="stLinkButton"] {
    margin-top:0 !important;
}

div[data-testid="stDownloadButton"] button,
div[data-testid="stLinkButton"] a {
    min-height:52px !important;
    height:52px !important;
    max-height:52px !important;
    box-sizing:border-box !important;
}


/* ----------------------------------------------------------
   通常ボタン
   前のページ / 次のページ
   ---------------------------------------------------------- */
div.stButton > button {
    background:#5d4a92 !important;
    color:#ffffff !important;
    border-color:#4b3c79 !important;
}

div.stButton > button *,
div.stButton > button p,
div.stButton > button span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

div.stButton > button:hover {
    background:#4b3c79 !important;
    color:#ffffff !important;
}

div.stButton > button:hover *,
div.stButton > button:hover p,
div.stButton > button:hover span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ----------------------------------------------------------
   ランキング「このページを表示」
   ---------------------------------------------------------- */
div[data-testid="stFormSubmitButton"] button {
    background:#5d4a92 !important;
    color:#ffffff !important;
    border-color:#4b3c79 !important;
    font-weight:900 !important;
}

div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stFormSubmitButton"] button p,
div[data-testid="stFormSubmitButton"] button span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background:#4b3c79 !important;
    color:#ffffff !important;
}

div[data-testid="stFormSubmitButton"] button:hover *,
div[data-testid="stFormSubmitButton"] button:hover p,
div[data-testid="stFormSubmitButton"] button:hover span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ==========================================================
   解析開始ボタン
   赤背景 + 白文字 + 黒縁
   ========================================================== */

div.stButton > button[kind="primary"] {
    background:#d92d3f !important;
    color:#ffffff !important;
    border-color:#b51f30 !important;
    box-shadow:0 8px 20px rgba(181,31,48,.20) !important;
}

div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span,
div.stButton > button[kind="primary"] div {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    text-shadow:
        -1px -1px 0 #111111,
         1px -1px 0 #111111,
        -1px  1px 0 #111111,
         1px  1px 0 #111111 !important;
}

div.stButton > button[kind="primary"]:hover {
    background:#b51f30 !important;
    color:#ffffff !important;
}


/* ==========================================================
   通常ボタン
   ランキングページ移動など
   ========================================================== */

div.stButton > button {
    background:#6650a4 !important;
    color:#ffffff !important;
    border-color:#4f3d82 !important;
}

div.stButton > button p,
div.stButton > button span,
div.stButton > button div {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

div.stButton > button:hover {
    background:#55418d !important;
    color:#ffffff !important;
}

div.stButton > button:hover p,
div.stButton > button:hover span,
div.stButton > button:hover div {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}


/* ==========================================================
   Ranking page form
   ========================================================== */

.ranking-page-form input {
    text-align:center !important;
    font-weight:800 !important;
}

div[data-testid="stFormSubmitButton"] button {
    background:#6650a4 !important;
    color:#ffffff !important;
    border-color:#4f3d82 !important;
    font-weight:900 !important;
}

div[data-testid="stFormSubmitButton"] button p,
div[data-testid="stFormSubmitButton"] button span,
div[data-testid="stFormSubmitButton"] button div {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background:#55418d !important;
    color:#ffffff !important;
}

/* ==========================================================
   難易度・レベル Selectbox
   選択中の値：通常の黒文字
   ========================================================== */

/* Selectbox本体 */
div[data-testid="stSelectbox"]
div[data-baseweb="select"] {
    color:#303640 !important;
}

/* 選択中の値 */
div[data-testid="stSelectbox"]
div[data-baseweb="select"] div[role="combobox"] {
    background:#fbfbfc !important;
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
}

/* 選択中の文字を入れている内部要素 */
div[data-testid="stSelectbox"]
div[data-baseweb="select"] div[role="combobox"] > div,
div[data-testid="stSelectbox"]
div[data-baseweb="select"] div[role="combobox"] > div > div,
div[data-testid="stSelectbox"]
div[data-baseweb="select"] div[role="combobox"] span,
div[data-testid="stSelectbox"]
div[data-baseweb="select"] div[role="combobox"] p {
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
    -webkit-text-stroke:0 !important;
    text-shadow:none !important;
}

/* Selectbox内のinput */
div[data-testid="stSelectbox"]
div[data-baseweb="select"] input {
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
    background:transparent !important;
}

/* Selectboxの矢印 */
div[data-testid="stSelectbox"]
div[data-baseweb="select"] svg {
    color:#303640 !important;
    fill:#303640 !important;
    stroke:#303640 !important;
}

/* ==========================================================
   Selectbox 候補一覧
   ライトモード：白背景 + 濃色文字
   ダークモード：暗色背景 + 白文字
   ========================================================== */

/* ライトモード */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"],
[role="listbox"],
[role="option"] {
    background:#ffffff !important;
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
    text-shadow:none !important;
}

[data-baseweb="popover"] [role="option"] *,
[role="listbox"] [role="option"] * {
    color:#303640 !important;
    -webkit-text-fill-color:#303640 !important;
    text-shadow:none !important;
}

[data-baseweb="popover"] [role="option"]:hover,
[role="listbox"] [role="option"]:hover {
    background:#eef0f4 !important;
    color:#20252d !important;
}

[data-baseweb="popover"] [role="option"]:hover *,
[role="listbox"] [role="option"]:hover * {
    color:#20252d !important;
    -webkit-text-fill-color:#20252d !important;
}

/* ダークモード：スマートフォン等のシステム設定に対応 */
@media (prefers-color-scheme: dark) {
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] [role="option"],
    [role="listbox"],
    [role="option"] {
        background:#1f232b !important;
        color:#f4f4f5 !important;
        -webkit-text-fill-color:#f4f4f5 !important;
        text-shadow:none !important;
    }

    [data-baseweb="popover"] [role="option"] *,
    [role="listbox"] [role="option"] * {
        color:#f4f4f5 !important;
        -webkit-text-fill-color:#f4f4f5 !important;
        text-shadow:none !important;
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [role="listbox"] [role="option"]:hover {
        background:#343a46 !important;
        color:#ffffff !important;
    }

    [data-baseweb="popover"] [role="option"]:hover *,
    [role="listbox"] [role="option"]:hover * {
        color:#ffffff !important;
        -webkit-text-fill-color:#ffffff !important;
    }
}

/* Ranking title list */
.ranking-title-box {
    border:1px solid #d2d6dd;
    border-radius:18px;
    background:#ffffff;
    padding:16px;
    box-shadow:0 8px 24px rgba(45,52,64,.08);
}

.ranking-title-placeholder {
    min-height:110px;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    color:#68717e;
    background:#f7f8fa;
    border:1px dashed #aeb6c2;
    border-radius:14px;
    padding:18px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# Header
# ==========================================================

st.markdown(
    f"""
<div class="app-hero">
  <div class="app-hero-inner">
    <div class="app-kicker">✦ TAP TIMING ANALYZER</div>
    <div class="app-title">Ensemble Stars!! Music</div>
    <div class="app-subtitle">Tap Timing Analyzer</div>
    <div class="app-fan-tool">あんさんぶるスターズ！！Music 非公式ファンツール</div>
    <div class="app-description">
      タップタイミング棒グラフを解析し、判定分布・精密度・安定度・総合評価などを
      独自アルゴリズムで推定します。
    </div>
    <div class="hero-rule"></div>
  </div>
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


def _ranking_value(row, key, default=""):
    """ランキングCSV由来の値を安全に取得する。"""
    value = row.get(key, default) if isinstance(row, dict) else default
    return default if value is None else value


def _safe_float(value, default=None):
    """ランキング表示用。N/A・空欄・不正値を安全に扱う。"""
    if value is None:
        return default
    if isinstance(value, str) and value.strip().upper() in {"", "N/A", "NA", "NONE", "NULL"}:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _format_ranking_table(rows, current_position=None):
    """ランキング一覧をレスポンシブHTMLテーブルへ変換する。"""
    html = [
        '<div class="ranking-table-wrap"><table class="ranking-table">',
        '<thead><tr><th>順位</th><th>Overall</th><th>Rank</th><th>Precision</th><th>Balance</th><th>プレイ傾向</th></tr></thead><tbody>'
    ]

    for row in rows:
        try:
            position = int(_ranking_value(row, "ranking_position", 0))
        except (TypeError, ValueError):
            position = 0

        overall_value = _safe_float(_ranking_value(row, "overall_score", 0), 0.0)
        precision_value = _safe_float(_ranking_value(row, "precision", 0), 0.0)
        balance_value = _safe_float(_ranking_value(row, "balance", None), None)

        overall = f"{overall_value:.3f}" if overall_value is not None else "N/A"
        precision = f"{precision_value:.3f}" if precision_value is not None else "N/A"
        balance = f"{balance_value:.3f}" if balance_value is not None else "N/A"

        rank = str(_ranking_value(row, "rank", "-"))
        tendency = str(_ranking_value(row, "play_tendency", "N/A"))
        is_me = bool(row.get("is_current_user", False))
        classes = ' class="me"' if is_me else ''
        position_label = f"{position}位" + (" ★あなた" if is_me else "")
        html.append(
            f'<tr{classes}>'
            f'<td class="rank-pos">{position_label}</td>'
            f'<td class="rank-top">{overall}</td>'
            f'<td><span class="rank-badge">{rank}</span></td>'
            f'<td>{precision}</td>'
            f'<td>{balance}</td>'
            f'<td>{tendency}</td>'
            '</tr>'
        )

    html.append('</tbody></table></div>')
    return "".join(html)


def _build_ranking_page(ranking_base, ranking_result, page_number, page_size=50):
    """固定1,799件に現在結果を一時挿入して、1800件表示用のページを作る。"""
    base_rows = []
    current_position = int(ranking_result["ranking_position"])
    current_score = float(ranking_result["overall_score"]) if "overall_score" in ranking_result else None

    for row in ranking_base:
        item = dict(row)
        try:
            item["ranking_position"] = int(item.get("ranking_position", 0))
        except (TypeError, ValueError):
            continue
        item["is_current_user"] = False
        base_rows.append(item)

    base_rows.sort(key=lambda r: r["ranking_position"])

    # 現在ユーザーの行は保存せず、この画面の表示時だけ挿入する。
    current_row = {
        "ranking_position": current_position,
        "overall_score": current_score if current_score is not None else 0.0,
        "rank": ranking_result.get("rank", "-"),
        "precision": ranking_result.get("precision", 0.0),
        "balance": ranking_result.get("balance", None),
        "play_tendency": ranking_result.get("play_tendency", "N/A"),
        "is_current_user": True,
    }

    visible = []
    for row in base_rows:
        pos = row["ranking_position"]
        if pos >= current_position:
            row = dict(row)
            row["ranking_position"] = pos + 1
        visible.append(row)
    visible.insert(current_position - 1, current_row)

    total = len(visible)
    page_count = max(1, (total + page_size - 1) // page_size)
    page_number = max(1, min(page_number, page_count))
    start = (page_number - 1) * page_size
    end = min(start + page_size, total)
    return visible[start:end], page_count, total, current_position


def render_guide_and_policies():
    """解析前から確認できる利用ガイド・注意事項・権利・プライバシー情報。"""
    st.divider()
    st.markdown(
        """<div class="section-heading">
        <div><h2>📚 ご利用ガイド・ポリシー</h2><p>はじめに、使い方・注意事項・利用規約・プライバシー・公式ガイドラインをご確認ください。</p></div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="guide-grid">
        <a class="guide-tile" href="#guide-use" style="text-decoration:none;">
          <div class="icon">📖</div><div class="title">ご利用ガイド</div><div class="desc">使い方・入力項目・リザルトカード・ランキング・共有。</div>
        </a>
        <a class="guide-tile" href="#guide-notice" style="text-decoration:none;">
          <div class="icon">⚠️</div><div class="title">ご利用上の注意</div><div class="desc">対応画像・推定値・画像に含まれる情報をご確認ください。</div>
        </a>
        <a class="guide-tile" href="#guide-terms" style="text-decoration:none;">
          <div class="icon">📜</div><div class="title">利用規約</div><div class="desc">利用条件・禁止事項・サービス変更・権利関係など。</div>
        </a>
        <a class="guide-tile" href="#guide-privacy" style="text-decoration:none;">
          <div class="icon">🔒</div><div class="title">プライバシー</div><div class="desc">画像・入力情報・解析データの取り扱い。</div>
        </a>
        <a class="guide-tile" href="#guide-guideline" style="text-decoration:none;">
          <div class="icon">©️</div><div class="title">ガイドライン</div><div class="desc">非公式表示・権利関係・コンテンツ利用について。</div>
        </a>
        <a class="guide-tile" href="#guide-disclaimer" style="text-decoration:none;">
          <div class="icon">❗</div><div class="title">免責事項</div><div class="desc">推定値であることと正確性等の非保証について。</div>
        </a>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown('<div id="guide-use"></div>', unsafe_allow_html=True)
    with st.expander("📖 ご利用ガイド", expanded=False):
        st.markdown("""
### 1. このツールについて
『あんさんぶるスターズ！！Music』のリザルト画面に表示されるタップタイミング棒グラフを解析し、判定分布やタップタイミングの傾向を独自アルゴリズムで推定する非公式ファンツールです。Happy Elements 株式会社とは関係ありません。

### 2. 使い方
1. ゲームから撮影したリザルト画像を用意します。
2. 画像をアップロードします。
3. 楽曲名・難易度・レベル・総ノーツ数を入力します。
4. 「解析開始」を押します。
5. リザルトカード、総合評価ランキングを確認します。

### 3. 入力できる総ノーツ数
総ノーツ数は **20～2000** の範囲で入力してください。

### 4. 解析結果
達成率、精密度、安定度、総合評価、ランク、プレイ傾向などは本ツール独自の推定・評価です。ゲーム内部の正式な判定値ではありません。

### 5. ランキング
ランキングは固定された1,799件の基準データと今回の解析結果を比較して表示します。今回の解析結果は基準データへ保存・追加しません。

### 6. リザルトカード とX共有
リザルトカードは画像として保存できます。X共有では解析結果の共有を行います。投稿前に内容をご確認ください。
        """)

    st.markdown('<div id="guide-notice"></div>', unsafe_allow_html=True)
    with st.expander("⚠️ ご利用上の注意", expanded=False):
        st.markdown("""
### 対応画像について
- ゲームから直接撮影したスクリーンショットを推奨します。
- 画像編集・加工を行っていない、十分な解像度の画像を使用してください。
- タップタイミング棒グラフが明確に表示されている必要があります。
- 現在の解析対象は、Webアプリ画面に表示されている対応条件を満たすリザルト画像です。

### 解析結果について
画像から推定した結果であり、ゲーム内部の正式な判定・計算方法を再現するものではありません。画像の状態によっては正しく解析できない場合があります。

### 画像に含まれる情報
アップロード前に、個人情報が画像に含まれていないか確認してください。
        """)

    st.markdown('<div id="guide-terms"></div>', unsafe_allow_html=True)
    with st.expander("📜 利用規約", expanded=False):
        st.markdown("""
**制定日：2026年9月7日**

#### 第1条　本サービス
本サービスは、『あんさんぶるスターズ！！Music』のリザルト画像を解析し、タップタイミング等に関する情報を推定・可視化する非公式ファンツールです。本サービスはHappy Elements株式会社およびその関連会社等とは関係ありません。

#### 第2条　解析結果
本サービスの解析結果は推定値です。ゲーム公式の判定結果、スコア、評価等を保証するものではありません。

#### 第3条　利用者の責任
利用者は、本サービスへのアップロードが適切であると判断した画像を使用するものとします。第三者が公開した画像を使用する場合は、画像に個人情報等が含まれていないか確認し、第三者の権利や利用条件等に配慮してください。

#### 第4条　禁止事項
不正な目的での利用、サービスへ過度な負荷を与える行為、正常な動作を妨害する行為、不正アクセスを試みる行為、第三者の権利を侵害する行為、その他サービスの運営を妨げる行為を禁止します。

#### 第5条　サービスの変更・停止
メンテナンス、障害、仕様変更その他の事情により、サービスの内容を変更、または停止する場合があります。

#### 第6条　免責
本サービスは、解析結果の正確性、完全性、有用性等を保証するものではありません。サービスの利用または利用できなかったことによって生じた損害について、法令上許される範囲で責任を負わないものとします。

#### 第7条　権利
ゲームおよび関連する名称、画像、ロゴ、キャラクター等の権利は、それぞれの権利者に帰属します。本サービスはそれらの権利を取得するものではありません。

#### 第8条　規約の変更
本規約は、必要に応じて変更する場合があります。変更後の内容は、本Webアプリ上に掲載した時点から適用します。
        """)

    st.markdown('<div id="guide-privacy"></div>', unsafe_allow_html=True)
    with st.expander("🔒 プライバシーポリシー", expanded=False):
        st.markdown("""
**制定日：2026年9月7日**  
**最終更新日：2026年9月9日**

#### 1．取得する情報
本サービスでは、主に以下の情報を利用します。
- 利用者がアップロードしたリザルト画像
- 利用者が入力した楽曲名、難易度、レベル、総ノーツ数
- 本サービスが解析によって生成する解析結果

個人情報を入力する機能は設けていません。ただし、画像に個人情報が含まれている場合、その情報も処理対象となる可能性があります。

#### 2．利用目的
取得した情報は、リザルト画像の解析、タップタイミング・判定分布の推定、解析結果の算出、リザルトカードの生成を目的として利用します。

#### 3．アップロード画像・解析データの保持
アップロードされた画像は、解析および解析結果の表示のために一時的に取り扱います。解析結果を表示している間は、アプリのセッション内で画像データや解析結果が一時的に保持される場合があります。

本アプリには、アップロード画像や解析結果をユーザー履歴として継続的に保存したり、ランキング基準データへ自動的に追加したりする機能はありません。

解析処理のために作成した一時ファイルは、処理後に削除する処理を行います。

なお、ブラウザやホスティング基盤側で行われるログ・キャッシュその他の取り扱いについては、本アプリの実装だけで保証するものではありません。

#### 4．解析結果
解析結果は本サービス独自の推定値です。ゲーム内部の正式な判定・計算方法を取得または再現したものではありません。

#### 5．第三者への提供
本アプリには、利用者がアップロードした画像や入力情報を第三者へ提供・販売するための機能はありません。

ただし、Streamlit Community Cloud等のホスティング基盤、ブラウザその他の外部サービスが独自に取得・処理する情報については、本アプリの実装だけで保証するものではありません。

法令に基づく場合など、必要な場合を除き、開発者が利用者の情報を第三者へ提供することを目的とした運用は行いません。

#### 6．変更
サービス内容や利用環境の変更等に応じて、本ポリシーを変更する場合があります。変更した場合は本Webアプリ上で確認できるようにします。
        """)

    st.markdown('<div id="guide-guideline"></div>', unsafe_allow_html=True)
    with st.expander("©️ コンテンツ利用ガイドライン・権利について", expanded=False):
        st.markdown("""
本サービスは『あんさんぶるスターズ！！Music』の**非公式ファンツール**です。Happy Elements株式会社および公式・公認のサービスではありません。

Happy Elements株式会社のコンテンツ利用ガイドラインでは、非営利目的でのWebサイト利用について一定の利用が認められています。一方、公式・公認と誤認させる表示や、各タイトルの個別ガイドラインに反する利用は禁止されています。『あんさんぶるスターズ！！』にはタイトル固有のガイドラインがあり、内容が異なる場合はタイトル固有のガイドラインが優先されます。

本サービスでは、利用者が用意したリザルト画像を解析対象とし、ゲーム画像を素材として配布することを目的としていません。元画像をXへ自動投稿する機能も本サービスの共有機能には含めません。


**公式情報**  
- Happy Elements コンテンツ利用ガイドライン  
  https://www.happyelements.co.jp/contents-guideline/
- 『あんさんぶるスターズ！！』コンテンツ利用ガイドライン案内  
  https://ensemble-stars-music.zendesk.com/hc/ja/articles/39158218386201-%E3%82%B3%E3%83%B3%E3%83%86%E3%83%B3%E3%83%84%E5%88%A9%E7%94%A8%E3%82%AC%E3%82%A4%E3%83%89%E3%83%A9%E3%82%A4%E3%83%B3
        """)

    st.markdown('<div id="guide-disclaimer"></div>', unsafe_allow_html=True)
    with st.expander("❗ 免責事項", expanded=False):
        st.markdown("""
本Webアプリは、『あんさんぶるスターズ！！Music』の非公式ファンツールです。Happy Elements株式会社とは関係ありません。

本ツールはゲーム内部のデータを取得・改変するものではなく、利用者が用意したリザルト画像を独自の方法で解析し、推定値を表示するものです。

表示される判定分布、達成率、精密度、安定度、総合評価、ランク、ランキング等は、本ツール独自の解析・評価結果であり、ゲーム公式の判定値・評価・ランキングではありません。

解析結果の正確性、完全性、有用性を保証するものではありません。サービスの利用または利用できなかったことによって生じた損害について、法令上許される範囲で責任を負わないものとします。
        """)

with st.expander("❓ よくある質問", expanded=False):

    st.markdown("""
**Q. このツールは無料ですか？**  
はい。現在、無料で利用できます。会員登録も必要ありません。

**Q. スマートフォンでも解析できますか？**  
はい。スマートフォンからも利用できます。スマートフォンのブラウザからリザルト画像をアップロードして解析できます。

**Q. 解析できるリザルト画像には条件がありますか？**  
はい。新UI（2025年4月29日以降）のライブリザルト画面を使用してください。

画像は編集・加工していない高解像度のスクリーンショットで、タップタイミング棒グラフが明確に表示されている必要があります。

また、ライブチャレンジでは「ALL AMAZING（100.000%）」、ノーマルライブ・あんさんぶるライブ・ソロライブでは「PERFECT COMBO」が表示され、棒グラフが対応条件を満たしている必要があります。

詳しい条件は「解析可能な画像」をご確認ください。

**Q. なぜ総ノーツ数を入力する必要がありますか？**  
本ツールでは、リザルト画像のタップタイミング棒グラフから判定分布を推定しています。

棒グラフの割合を実際のノーツ数に換算するため、ゲームのリザルト画面に表示されている総ノーツ数を入力してください。

誤った総ノーツ数を入力すると、判定数や解析結果も正しくならない場合があります。

**Q. 解析結果はゲーム公式の数値ですか？**  
いいえ。本ツールがリザルト画像から独自に推定・算出した結果です。

ゲーム内部で使用されている判定・評価・計算方法を取得または再現したものではありません。そのため、ゲーム公式の数値として扱わないでください。

**Q. ランキングは公式ランキングですか？**  
いいえ。本ツール独自の基準データを使用したランキングです。ゲーム公式のランキングではありません。

**Q. ランキングに解析結果は保存されますか？**  
今回の解析結果を固定1,799件のランキング基準データへ保存・追加することはありません。画面上では1,800件目として一時的に表示します。

**Q. なぜ解析結果を新しいランキング記録として登録しないのですか？**  
ランキングの公平性を保つためです。解析結果を繰り返し登録できる仕組みにすると、一部の利用者による過度な登録などによってランキング分布が不自然に偏る可能性があります。そのため、今回の解析結果はランキング基準データへ新規登録せず、現在の解析結果として一時的に表示しています。

**Q. 1,799件のランキング基準データはどのように取得したのですか？**  
開発者本人が過去に記録したリザルトや、SNSのフォロワーから提供していただいたリザルトをもとに作成しています。

**Q. 解析画像に個人情報が写っていても大丈夫ですか？**  
個人情報が含まれる画像について、安全性を保証することはできません。

アップロード前に、個人を特定できる可能性のある情報が画像に含まれていないか確認してください。

個人情報が含まれている場合は、必要に応じて個人情報が写らない画像を使用してください。

**Q. アップロードした画像は保存されますか？**  
本アプリには、アップロード画像をユーザー履歴として継続的に保存する機能はありません。

一方、解析や解析結果の表示に必要な間は、アプリのセッション内で画像データが一時的に保持される場合があります。解析処理のために作成した一時ファイルは、処理後に削除する処理を行います。

なお、ブラウザやホスティング基盤側のログ・キャッシュ等については、本アプリの実装だけで保証するものではありません。

**Q. X共有すると、アップロードしたリザルト画像も投稿されますか？**  
いいえ。X共有では、解析結果をもとに作成した共有用の文章とWebアプリのURLを投稿します。

アップロードしたリザルト画像そのものをXへ自動投稿する機能はありません。

投稿前に、表示される内容を確認してから共有してください。

**Q. 解析結果が正しく表示されない場合はどうすればよいですか？**  
まず「解析可能な画像」の条件を確認してください。

条件を満たしている場合でも、画像の解像度や状態、入力した総ノーツ数などによって正しく解析できない場合があります。
""")


render_guide_and_policies()

st.divider()

# ==========================================================
# Input Area
# ==========================================================

st.markdown("""
<div style="
padding:18px;
border-radius:12px;
border:2px solid #8E44AD;
background:#f8f9fb;
color:#424954;
">

<h3 style="color:#353b46;margin-top:0;">
解析可能な画像
</h3>

<p><b>以下の条件を満たすライブリザルト画像を使用してください。</b></p>

<ul style="line-height:1.8;">
<li>新UI（2025年4月29日以降）のライブリザルト画面</li>
<li>ライブリザルトのスクリーンショット</li>
<li>編集・加工していない高解像度の画像</li>
<li>タップタイミング棒グラフが表示されている</li>
<li>棒グラフが中央1本＋左右各1本の合計3本以内に収まっている</li>
<li>ALL AMAZING（内部判定を含む）に相当する結果</li>
<li>MISSがなく、総ノーツ数と最高判定数が一致している</li>
</ul>

<p><b>ライブチャレンジ</b><br>
「ALL AMAZING（100.000%）」と表示されているリザルトが対象です。</p>

<p><b>ノーマルライブ・あんさんぶるライブ・ソロライブ</b><br>
「PERFECT COMBO」と表示され、棒グラフが中央1本＋左右各1本の合計3本以内に収まっているリザルトが対象です。これらのライブでは、画面上に「AMAZING」が最高判定として表示されないため、棒グラフから内部的なALL AMAZING相当かを判断します。</p>

<p><b>棒グラフについて</b><br>
棒グラフは中央に近いほど、より正確なタイミングでタップできています。中央の1本と、その左右1本ずつまでがAMAZING判定の範囲です。</p>

<p><b>MISSについて</b><br>
MISSはタップタイミング棒グラフには表示されないため、総ノーツ数と最高判定数が一致していることも確認してください。</p>

<b style="color:#C0392B;">
※条件を満たさない画像は解析対象外です。条件を満たしている場合でも、画像の状態や入力内容によって正しく解析できない場合があります。
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
background:#ffffff !important;
color:#424954 !important;
">

<h3 style="
margin-top:0;
color:#5d4a92 !important;
">
⚙️ 解析設定
</h3>

<p style="
margin-top:6px;
color:#66707d !important;
font-size:15px;
line-height:1.6;
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
        "📷 PNG・JPG・JPEG・WebP形式のスクリーンショットに対応しています。"
    )

    uploaded_file = st.file_uploader(
        "リザルト画像",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed",
    )

    # ----------------------------------------------------------
    # Ranking Titles
    # ----------------------------------------------------------

    ranking_title_image = (
        Path(__file__).resolve().parent
        / "assets"
        / "ranking_titles"
        / "ranking.png"
    )

    with st.expander("🏆 ランキング称号一覧", expanded=False):
        st.caption("ランキング順位に応じた称号一覧です。")

        if ranking_title_image.is_file():
            with open(ranking_title_image, "rb") as f:
                ranking_title_bytes = f.read()

            st.image(
                ranking_title_bytes,
                use_container_width=True,
            )
        else:
            st.warning(
                "ランキング称号一覧の画像を表示できませんでした。"
            )

# ----------------------------------------------------------
# Song Information
# ----------------------------------------------------------
with info_col:

    st.markdown("### 🎼 楽曲情報")

    st.caption(
        "リザルト画面（下の「解析対象となるリザルト画像」）に表示されている内容を入力してください。"
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
            "♪1", "♪2", "♪3", "♪4", "♪5", "♪6",
        ],
    }

    level_list = LEVEL_LIST[difficulty]

    level = st.selectbox(
        "⭐ レベル",
        level_list,
    )

    st.markdown("#### 🔢 総ノーツ数")

    total_notes = st.number_input(
        "総ノーツ数",
        min_value=20,
        max_value=2000,
        value=20,
        step=1,
        help=(
            "ライブの総ノーツ数を入力してください。\n\n"
            "ゲームのリザルト画面に表示される総ノーツ数を入力してください。\n"
            "20～2000の範囲で入力してください。\n"
            "誤った値では正しい解析結果になりません。"
        )
    )

    st.divider()

# ==========================================================
# Uploaded Image Preview
# ==========================================================

if uploaded_file is not None:
    st.markdown("### 🖼️ 解析対象となるリザルト画像")
    st.caption("解析対象となるリザルト画像です。")
    st.image(uploaded_file.getvalue(), use_container_width=True)

# ==========================================================
# Analyze
# ==========================================================
st.markdown("""
<div style="
padding:12px 16px;
border-radius:12px;
background:#f8f9fb;
border:1px solid #3b3b4a;
margin-bottom:10px;
">

<b style="color:#5d4a92;">
ℹ 解析の流れ
</b>

<div style="margin-top:6px; color:#66707d; line-height:1.7;">

・タップタイミング棒グラフ解析<br>
・判定分布の推定<br>
・リザルトカード生成

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
padding:12px 16px;
border-radius:12px;
background:#fff7e8;
border:1px solid #5a4a2a;
margin-bottom:18px;
">

<b style="color:#7a4f00;">
⚠ 解析可能な画像をご確認ください
</b>

<div style="margin-top:6px;color:#66707d;">
条件を満たさない画像では
正しい解析結果が得られない場合があります。
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("## ▶ タップタイミング解析")

st.caption(
    "スクリーンショットから判定分布を推定し、リザルトカード を生成します。"
)

st.write("")

analyze_button = st.button(
    "▶ 解析開始",
    type="primary",
    width="stretch"
)

if analyze_button:

    st.session_state.pop("analysis_result", None)

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

        リザルトカードを生成しています。
        処理には時間がかかる場合があります。
        """)

        progress_status.markdown("""
        **現在の処理**

        ⏳ リザルト画像読込

        ⬜ 棒グラフ解析

        ⬜ 判定推定

        ⬜ リザルトカード生成
        """)

        progress_bar.progress(10)

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ⏳ 棒グラフ解析

        ⬜ 判定推定

        ⬜ リザルトカード生成
        """)

        progress_bar.progress(35)

        estimate_result, graph_image = analyze(
            image_path=image_path,
            total_notes=total_notes,
            return_graph=True,
        )

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ✅ 棒グラフ解析

        ⏳ 判定推定

        ⬜ リザルトカード生成
        """)

        progress_bar.progress(65)

        analysis_score = score(
            estimate_result,
            total_notes=total_notes,
        )

        # ==========================================================
        # Ranking Calculation
        # ==========================================================
        # 固定1,799件の基準データと比較するだけで、
        # 今回の解析結果はランキング基準データへ追加・保存しない。
        ranking_base = load_ranking_base()
        ranking_result = calculate_ranking(
            analysis_score.overall_score,
            ranking_base,
        )
        ranking_result = dict(ranking_result)
        # リザルトカード と同じ判定ロジックを共有する。
        play_tendency, _, _ = generate_play_badge(
            precision=analysis_score.precision,
            balance=analysis_score.balance,
            balance_available=analysis_score.balance_available,
            fast=estimate_result.fast,
            slow=estimate_result.slow,
            amazing_plus=estimate_result.amazing_plus,
        )

        ranking_result.update({
            "overall_score": analysis_score.overall_score,
            "rank": analysis_score.rank,
            "precision": analysis_score.precision,
            "balance": analysis_score.balance if analysis_score.balance_available else None,
            "play_tendency": play_tendency,
            "ranking_analysis_date": datetime.now().strftime("%Y年%m月%d日"),
        })
        ranking_distribution = build_rank_distribution(ranking_base)

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

        ⏳ リザルトカード生成
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
        # リザルトカード
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

            rank=analysis_score.rank,

            ranking_position=ranking_result["ranking_position"],
            ranking_comparison_total=ranking_result["comparison_total"],
            ranking_top_percent=ranking_result["ranking_top_percent"],
            ranking_title=ranking_result["ranking_title"],
            ranking_rank=analysis_score.rank,
            ranking_distribution=ranking_distribution,
            ranking_analysis_date=datetime.now().strftime("%Y年%m月%d日"),

        )

        # リザルトカードをメモリへ読み込む
        with open(card_path, "rb") as file:
            card_data = file.read()

        # リザルトカードの一時ファイルを削除
        try:
            os.remove(card_path)
        except FileNotFoundError:
            pass
        except OSError:
            if config.DEBUG_MODE:
                st.caption(
                    "リザルトカードの一時ファイルを削除できませんでした。"
                )

        progress_status.markdown("""
        **現在の処理**

        ✅ リザルト画像読込

        ✅ 棒グラフ解析

        ✅ 判定推定

        ✅ リザルトカード生成
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

            rank=analysis_score.rank,

            ranking_position=ranking_result["ranking_position"],

            ranking_comparison_total=ranking_result["comparison_total"],

            ranking_top_percent=ranking_result["ranking_top_percent"],

            ranking_title=ranking_result["ranking_title"]

        )

        # Streamlitのページ移動で再実行されても解析結果を保持する。
        st.session_state["analysis_result"] = {
            "music": music,
            "difficulty": difficulty,
            "level": level,
            "total_notes": total_notes,
            "card_data": card_data,
            "uploaded_image_bytes": uploaded_file.getvalue(),
            "graph_image": graph_image,
            "estimate_result": estimate_result,
            "analysis_score": analysis_score,
            "ranking_base": ranking_base,
            "ranking_result": ranking_result,
            "ranking_distribution": ranking_distribution,
            "tweet_url": tweet_url,
        }
        st.session_state["ranking_page"] = max(
            1,
            (int(ranking_result["ranking_position"]) + 49) // 50,
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


def render_analysis_results(result_payload):
    """解析成功後の表示。ページ移動によるStreamlit再実行後も再表示できる。"""
    music = result_payload["music"]
    difficulty = result_payload["difficulty"]
    level = result_payload["level"]
    total_notes = result_payload["total_notes"]
    card_data = result_payload["card_data"]
    uploaded_image_bytes = result_payload["uploaded_image_bytes"]
    graph_image = result_payload["graph_image"]
    estimate_result = result_payload["estimate_result"]
    analysis_score = result_payload["analysis_score"]
    ranking_base = result_payload["ranking_base"]
    ranking_result = result_payload["ranking_result"]
    ranking_distribution = result_payload["ranking_distribution"]
    tweet_url = result_payload["tweet_url"]

    # ==========================================================
    # リザルトカード Preview
    # ==========================================================

    st.markdown("## 📊 解析結果")

    st.caption(
        "解析結果カードを生成しました。"
    )

    st.markdown("## 🖼️ リザルトカード")

    st.caption(
        "生成されたリザルトカードです。クリックすると拡大表示できます。"
    )

    if card_data is not None:
        st.image(card_data, use_container_width=True)
    else:
        st.warning("リザルトカード画像を表示できませんでした。解析をもう一度実行してください。")

    st.markdown("## 💾 保存・共有")
    st.caption("リザルトカードを保存したり、𝕏 へ共有したりできます。")

    share_col1, share_col2 = st.columns(
        [1, 1],
        gap="medium",
    )

    with share_col1:

        st.markdown("#### 📥 リザルトカード保存")

        st.markdown(
            """
            <div style="
                height: 30px;
                display: flex;
                align-items: center;
                color: #747d89;
                font-size: 12px;
                line-height: 1.2;
            ">
                リザルトカードをPNG形式で保存できます。
            </div>
            """,
            unsafe_allow_html=True,
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

        st.download_button(
            label="📥 リザルトカードを保存",
            data=card_data,
            file_name=download_file_name,
            mime="image/png",
            width="stretch",
        )

        st.caption(
            "※ 保存した画像はSNSなどで共有できます。"
        )

    with share_col2:

        st.markdown("#### 𝕏 結果を共有")

        st.markdown(
            """
            <div style="
                height: 30px;
                display: flex;
                align-items: center;
                color: #747d89;
                font-size: 12px;
                line-height: 1.2;
            ">
                Xへ解析結果を投稿できます。
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.link_button(
            label="𝕏 結果を共有",
            url=tweet_url,
            width="stretch",
        )

    # ==========================================================
    # Ranking Browser
    # ==========================================================
    st.markdown(
        """<div class="section-heading">
        <div><h2>🏆 総合評価ランキング</h2><p>固定1,799件の基準データに、今回の解析結果を一時的に加えた1,800件表示です。</p></div>
        </div>""",
        unsafe_allow_html=True,
    )

    ranking_page_key = "ranking_page"
    ranking_page_count = 36
    ranking_total = 1800

    if ranking_page_key not in st.session_state:
        st.session_state[ranking_page_key] = max(1, (int(ranking_result["ranking_position"]) + 49) // 50)
    current_page = max(1, min(int(st.session_state[ranking_page_key]), ranking_page_count))
    st.session_state[ranking_page_key] = current_page

    nav1, nav2, nav3 = st.columns([1.0, 1.25, 1.0], vertical_alignment="bottom")
    with nav1:
        if st.button(
            "‹ 前のページ",
            key="ranking_prev",
            width="stretch",
            disabled=current_page <= 1,
        ):
            st.session_state[ranking_page_key] = current_page - 1
            st.rerun()

    with nav2:
        with st.form("ranking_page_form", clear_on_submit=False):
            requested_page = st.number_input(
                "ページ",
                min_value=1,
                max_value=ranking_page_count,
                value=current_page,
                step=1,
                format="%d",
                help="1～36を入力してEnter、または下のボタンで移動できます。",
            )
            submitted = st.form_submit_button(
                "このページを表示",
                width="stretch",
            )
            if submitted:
                st.session_state[ranking_page_key] = int(requested_page)
                st.rerun()

    with nav3:
        if st.button(
            "次のページ ›",
            key="ranking_next",
            width="stretch",
            disabled=current_page >= ranking_page_count,
        ):
            st.session_state[ranking_page_key] = current_page + 1
            st.rerun()

    st.caption(f"{current_page} / {ranking_page_count}ページ　・　50件 / ページ　・　全 {ranking_total:,}件")

    ranking_page_rows, ranking_page_count_actual, ranking_total_actual, _ = _build_ranking_page(
        ranking_base,
        ranking_result,
        int(st.session_state[ranking_page_key]),
        page_size=50,
    )

    st.markdown(
        f"""<div class="ranking-shell"><div class="ranking-inner">
        <div class="ranking-hero-row">
          <div><div class="ranking-eyebrow">総合評価ランキング</div>
          <div class="ranking-title">あなたの順位：{ranking_result["ranking_position"]}位 / {ranking_result["comparison_total"]:,}件中</div>
          <div class="ranking-meta">上位 {ranking_result["ranking_top_percent"]:.1f}% ・ 解析日 {ranking_result["ranking_analysis_date"]}</div></div>
          <div class="ranking-stat"><div class="num">{ranking_result["ranking_top_percent"]:.1f}%</div><div class="label">上位割合</div></div>
        </div>
        {_format_ranking_table(ranking_page_rows)}
        </div></div>""",
        unsafe_allow_html=True,
    )

    st.caption("※ 今回の解析結果はランキング基準データへ保存・追加されません。ランキング一覧の「★あなた」は現在の解析結果を一時表示したものです。")

    st.divider()

    # ==========================================================
    # 開発者向け情報
    # ==========================================================

    if config.DEBUG_MODE:

        with st.expander(
            "🛠️ 開発者向け情報",
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

        st.caption(
            "解析に使用したタップタイミング棒グラフです。"
        )

        if graph_image is not None:
            graph_image_rgb = cv2.cvtColor(
                graph_image,
                cv2.COLOR_BGR2RGB,
            )

            st.image(
                graph_image_rgb,
                use_container_width=True,
            )
        else:
            st.warning(
                "解析に使用した棒グラフを表示できませんでした。"
            )

    st.divider()

    st.markdown("""
    <div class="legal-box">
    <b>© 権利・非公式表示</b><br><br>
    本Webアプリは『あんさんぶるスターズ！！Music』を題材とした非公式ファンツールです。Happy Elements株式会社とは関係ありません。<br><br>
    ゲームに関する名称・画像・ロゴ・キャラクター等の権利は、それぞれの権利者に帰属します。<br><br>
    本アプリで使用されるゲーム関連コンテンツは、転載・再配布を目的としたものではありません。<br><br>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
    <div style="
    text-align:center;
    padding:20px 10px;
    color:#66707d;
    font-size:14px;
    ">

    <div style="
    font-size:20px;
    font-weight:700;
    color:#5d4a92;
    margin-bottom:14px;
    ">

    あんさんぶるスターズ！！Music タップタイミング解析ツール

    </div>

    <div style="
    margin-bottom:6px;
    ">

    非公式ファンツール

    </div>

    <div style="
    font-size:13px;
    color:#6d7682;
    ">

    Hapylon × ChatGPT による開発

    </div>

    </div>
    """, unsafe_allow_html=True)

if "analysis_result" in st.session_state:
    render_analysis_results(st.session_state["analysis_result"])
