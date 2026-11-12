"""Helpers for identifying Supabase API keys that must stay server-side."""
from __future__ import annotations

import base64
import json


def is_elevated_supabase_key(key: str) -> bool:
    """Return True for new secret keys and legacy service_role JWTs."""
    value = str(key or "").strip()
    if value.startswith("sb_secret_"):
        return True
    parts = value.split(".")
    if len(parts) != 3:
        return False
    try:
        payload = parts[1]
        payload += "=" * (-len(payload) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload.encode("ascii")))
        return claims.get("role") == "service_role"
    except (ValueError, UnicodeError, json.JSONDecodeError):
        return False
