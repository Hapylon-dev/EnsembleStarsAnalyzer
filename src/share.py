"""
==========================================================
Ensemble Stars!! Music
Tap Timing Analyzer

X Share Utility
Version : 1.1

Author : OpenAI + Hapylon
==========================================================
"""

from __future__ import annotations

from urllib.parse import quote


# ==========================================================
# Web App URL
# ==========================================================

# リリース後に正式なURLへ変更
WEB_APP_URL = "https://ここに正式なWebアプリURL"


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

    text = f"""🎵 {music}
{difficulty} / Lv.{level}

AMZ+ {amazing_plus} / AMZ {amazing}
FAST {fast} / SLOW {slow}

🏆 Achievement {achievement:.3f}%
🎯 Precision {precision:.3f}% / Balance {balance:.3f}%
⭐ Overall {overall_score:.1f}pt / Rank {rank}

🔗 Webアプリ
{WEB_APP_URL}

#あんスタMusic #TapTimingAnalyzer"""

    return (
        "https://twitter.com/intent/tweet?text="
        + quote(text)
    )