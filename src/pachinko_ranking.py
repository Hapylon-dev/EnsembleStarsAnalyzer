"""Supabase RPC client for the public OVERALL PACHINKO leaderboard."""
from __future__ import annotations

from typing import Any

import requests

from supabase_keys import is_elevated_supabase_key


def _headers(api_key: str) -> dict[str, str]:
    if is_elevated_supabase_key(api_key):
        raise ValueError("Supabase secret/service_role keys must never be used by the public leaderboard client")
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
    }
    # New sb_publishable keys are opaque API keys, not JWTs. Only legacy anon
    # JWT keys belong in Authorization: Bearer.
    if not api_key.startswith("sb_publishable_"):
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def fetch_page(
    url: str,
    anon_key: str,
    page: int,
    page_size: int = 50,
    timeout: float = 15,
) -> tuple[list[dict[str, Any]] | None, int, str | None]:
    """Fetch a leaderboard page using one database RPC call."""
    if not url or not anon_key:
        return None, 0, "Supabaseのランキング保存設定がありません。"
    if is_elevated_supabase_key(anon_key):
        return None, 0, "Supabase Secret/service_role keyは公開ランキングに使用できません。Publishable keyを設定してください。"
    try:
        page = max(1, int(page))
        page_size = max(1, min(int(page_size), 100))
        response = requests.post(
            url.rstrip("/") + "/rest/v1/rpc/get_pachinko_leaderboard",
            headers=_headers(anon_key),
            json={"p_limit": page_size, "p_offset": (page - 1) * page_size},
            timeout=timeout,
        )
        response.raise_for_status()
        rows = response.json()
        if not isinstance(rows, list):
            raise ValueError("ランキングAPIの応答形式が正しくありません")
        if rows:
            total = int(rows[0]["total_count"])
        else:
            count_response = requests.head(
                url.rstrip("/") + "/rest/v1/pachinko_results",
                headers={**_headers(anon_key), "Prefer": "count=exact", "Range": "0-0"},
                params={"select": "id"},
                timeout=timeout,
            )
            count_response.raise_for_status()
            content_range = count_response.headers.get("Content-Range", "")
            total = int(content_range.rsplit("/", 1)[1]) if "/" in content_range and content_range.rsplit("/", 1)[1].isdigit() else 0
        return rows, total, None
    except requests.RequestException as exc:
        detail = getattr(getattr(exc, "response", None), "text", "")
        return None, 0, f"ランキングを取得できませんでした：{detail[:180] or str(exc)}"
    except (ValueError, KeyError, TypeError) as exc:
        return None, 0, f"ランキングの応答を解析できませんでした：{exc}"
