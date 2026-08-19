"""
==========================================================
Ensemble Stars!! Music
Tap Timing Analyzer

X Share Utility
Version : 1.2

Author : OpenAI + Hapylon
==========================================================
"""

from __future__ import annotations

from urllib.parse import quote


# ==========================================================
# Web App URL
# ==========================================================

WEB_APP_URL = "https://ensemble-stars-analyzer.streamlit.app/"


# ==========================================================
# X Post Settings
# ==========================================================

X_POST_LIMIT = 280

# Xの仕様変更等に備えて少し余裕を持たせる
X_POST_SAFE_LIMIT = 270


# ==========================================================
# Music Name
# ==========================================================

def shorten_music_name(
    music: str,
    max_length: int,
) -> str:
    """
    曲名を指定文字数以内に短縮する。

    長すぎる場合は末尾を「…」にする。
    """

    music = str(music).strip()

    if len(music) <= max_length:
        return music

    if max_length <= 1:
        return "…"[:max_length]

    return music[:max_length - 1] + "…"


# ==========================================================
# Build Tweet Text
# ==========================================================

def build_tweet_text(
    music: str,
    difficulty: str,
    level: str,
    amazing_plus: int,
    amazing: int,
    fast: int,
    slow: int,
    achievement: float,
    precision: float,
    balance: float,
    overall_score: float,
    rank: str,
) -> str:
    """
    X投稿本文を生成する。

    投稿全体がXの文字数制限を超えないように、
    曲名を必要に応じて自動短縮する。
    """

    music = str(music).strip()

    # ------------------------------------------------------
    # 固定部分を先に作成
    # ------------------------------------------------------

    fixed_text = f"""🎵 {{music}}
{difficulty} / Lv.{level}

AMZ+ {amazing_plus} / AMZ {amazing}
FAST {fast} / SLOW {slow}

🏆 Achievement {achievement:.3f}%
🎯 Precision {precision:.3f}% / Balance {balance:.3f}%
⭐ Overall {overall_score:.1f}pt / Rank {rank}

🔗 {WEB_APP_URL}

#あんスタMusic #TapTimingAnalyzer"""

    # ------------------------------------------------------
    # まず曲名をそのまま使用
    # ------------------------------------------------------

    text = fixed_text.format(
        music=music,
    )

    if len(text) <= X_POST_SAFE_LIMIT:
        return text

    # ------------------------------------------------------
    # 文字数超過時だけ曲名を短縮
    # ------------------------------------------------------

    # 曲名以外の文字数
    text_without_music = fixed_text.format(
        music="",
    )

    available_length = (
        X_POST_SAFE_LIMIT
        - len(text_without_music)
    )

    # 「🎵 」の分を考慮
    available_length -= len("🎵 ")

    if available_length < 2:
        available_length = 2

    music_short = shorten_music_name(
        music,
        available_length,
    )

    text = fixed_text.format(
        music=music_short,
    )

    # ------------------------------------------------------
    # 念のため最終チェック
    # ------------------------------------------------------

    if len(text) <= X_POST_LIMIT:
        return text

    # ------------------------------------------------------
    # 想定外のケース
    # ------------------------------------------------------

    # 曲名をさらに短縮して安全側へ寄せる
    music_short = shorten_music_name(
        music,
        max(1, available_length - 10),
    )

    return fixed_text.format(
        music=music_short,
    )


# ==========================================================
# X Share URL
# ==========================================================

def create_tweet_url(
    music: str,
    difficulty: str,
    level: str,
    amazing_plus: int,
    amazing: int,
    fast: int,
    slow: int,
    achievement: float,
    precision: float,
    balance: float,
    overall_score: float,
    rank: str,
) -> str:
    """
    X（旧Twitter）投稿用URLを生成する。

    解析結果の主要指標とWebアプリURLを含める。
    """

    text = build_tweet_text(
        music=music,
        difficulty=difficulty,
        level=level,
        amazing_plus=amazing_plus,
        amazing=amazing,
        fast=fast,
        slow=slow,
        achievement=achievement,
        precision=precision,
        balance=balance,
        overall_score=overall_score,
        rank=rank,
    )

    return (
        "https://twitter.com/intent/tweet?text="
        + quote(text)
    )