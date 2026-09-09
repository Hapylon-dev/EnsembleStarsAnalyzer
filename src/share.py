"""
==========================================================
Ensemble Stars!! Music
Tap Timing Analyzer

X Share Utility
Version : 1.3

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
X_POST_SAFE_LIMIT = 250


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

def ranking_emoji(ranking_title: str | None) -> str:
    """ランキング称号名からX投稿用の対応絵文字だけを返す。"""
    mapping = {
        "レインボーランカー": "🌈",
        "ダイヤモンドランカー": "💎",
        "プラチナランカー": "🤍",
        "ゴールドランカー": "💛",
        "シルバーランカー": "🩶",
        "ブロンズランカー": "🤎",
        "パープルランカー": "🟣",
        "レッドランカー": "🔴",
        "オレンジランカー": "🟠",
        "グリーンランカー": "🟢",
        "ブルーランカー": "🔵",
        "ホワイトランカー": "⚪️",
    }
    return mapping.get(str(ranking_title).strip(), "")


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
    ranking_position: int | None = None,
    ranking_comparison_total: int | None = None,
    ranking_top_percent: float | None = None,
    ranking_title: str | None = None,
) -> str:
    """X投稿本文を生成する。"""

    # 曲名は日本語・英語・混在を区別せず、最大20文字を基本上限とする。
    # 投稿全体が250文字を超える場合のみ、さらに曲名を短縮する。
    music = shorten_music_name(str(music).strip(), 20)

    emoji = ranking_emoji(ranking_title)
    ranking_block = ""
    if (
        emoji
        and ranking_position is not None
        and ranking_comparison_total is not None
        and ranking_top_percent is not None
    ):
        ranking_block = (
            f"\n{emoji} {ranking_position}位 / "
            f"{ranking_comparison_total}件中\n"
            f"上位 {ranking_top_percent:.1f}%"
        )

    fixed_text = f"""🎵 {{music}}
{difficulty} / Lv.{level}

AMZ+ {amazing_plus} / AMZ {amazing}
FAST {fast} / SLOW {slow}

🏆 ACH {achievement:.3f}%

🎯 PRE {precision:.3f}%
⚖️ BAL {balance:.3f}%

⭐ OVR {overall_score:.3f}pt
Rank {rank}{ranking_block}

🔗 {WEB_APP_URL}

#あんスタMusic #タップタイミング解析"""

    text = fixed_text.format(music=music)

    if len(text) <= X_POST_SAFE_LIMIT:
        return text

    # 投稿全体が250文字を超えた場合だけ、曲名を必要な分だけ短縮する。
    # 日本語・英語・混在による文字種判定は行わない。
    text_without_music = fixed_text.format(music="")
    available_length = (
        X_POST_SAFE_LIMIT
        - len(text_without_music)
        - len("🎵 ")
    )

    # 曲名の上限20文字を超えない範囲で調整する。
    available_length = max(1, min(20, available_length))
    music_short = shorten_music_name(music, available_length)
    text = fixed_text.format(music=music_short)

    # 通常のケースではここで250文字以内になる。
    if len(text) <= X_POST_SAFE_LIMIT:
        return text

    # 想定外に固定部分が長くなった場合の最終安全処理。
    # 曲名を1文字まで縮めても250文字を超える場合は、
    # 投稿本文の固定部分自体が250文字を超えているため、
    # 曲名以外を削らず、その状態を返す。
    music_short = shorten_music_name(music, 1)
    return fixed_text.format(music=music_short)


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
    ranking_position: int | None = None,
    ranking_comparison_total: int | None = None,
    ranking_top_percent: float | None = None,
    ranking_title: str | None = None,
) -> str:
    """X投稿用URLを生成する。"""

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
        ranking_position=ranking_position,
        ranking_comparison_total=ranking_comparison_total,
        ranking_top_percent=ranking_top_percent,
        ranking_title=ranking_title,
    )

    return "https://twitter.com/intent/tweet?text=" + quote(text)

