from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pachinko_ranking import fetch_page
from supabase_keys import is_elevated_supabase_key


class SupabaseRankingTests(unittest.TestCase):
    def test_fetch_page_uses_single_rpc_and_competition_rank(self):
        response = Mock()
        response.json.return_value = [{
            "rank": 3, "total_count": 120, "total_notes": 50400,
            "initial_overall": None, "initial_type": "PITY TIME",
            "initial_spins": 150, "rush_hits": 4, "rush_notes": 9000,
            "played_at": "2026-11-11T00:00:00+00:00",
        }]
        response.raise_for_status.return_value = None
        with patch("pachinko_ranking.requests.post", return_value=response) as post:
            rows, total, error = fetch_page("https://project.supabase.co", "sb_publishable_test", 2, 50)
        self.assertIsNone(error)
        self.assertEqual(total, 120)
        self.assertEqual(rows[0]["rank"], 3)
        self.assertIsNone(rows[0]["initial_overall"])
        args, kwargs = post.call_args
        self.assertEqual(kwargs["headers"]["apikey"], "sb_publishable_test")
        self.assertNotIn("Authorization", kwargs["headers"])
        self.assertEqual(args[0], "https://project.supabase.co/rest/v1/rpc/get_pachinko_leaderboard")
        self.assertEqual(kwargs["json"], {"p_limit": 50, "p_offset": 50})

    def test_legacy_anon_jwt_uses_bearer_header(self):
        response = Mock()
        response.json.return_value = []
        response.raise_for_status.return_value = None
        count_response = Mock()
        count_response.headers = {"Content-Range": "*/0"}
        count_response.raise_for_status.return_value = None
        with patch("pachinko_ranking.requests.post", return_value=response), patch(
            "pachinko_ranking.requests.head", return_value=count_response
        ) as head:
            rows, total, error = fetch_page("https://project.supabase.co", "eyJlegacyAnonJwt", 1, 50)
        self.assertIsNone(error)
        self.assertEqual(total, 0)
        self.assertEqual(rows, [])
        self.assertEqual(head.call_args.kwargs["headers"]["Authorization"], "Bearer eyJlegacyAnonJwt")

    def test_secret_key_is_rejected_by_public_client(self):
        rows, total, error = fetch_page("https://project.supabase.co", "sb_secret_do_not_use", 1, 50)
        self.assertIsNone(rows)
        self.assertEqual(total, 0)
        self.assertIn("Secret/service_role", error)

    def test_legacy_service_role_jwt_is_rejected(self):
        import base64
        payload = base64.urlsafe_b64encode(b'{"role":"service_role"}').decode().rstrip("=")
        key = "header." + payload + ".signature"
        self.assertTrue(is_elevated_supabase_key(key))
        rows, total, error = fetch_page("https://project.supabase.co", key, 1, 50)
        self.assertIsNone(rows)
        self.assertEqual(total, 0)
        self.assertIn("service_role", error)

    def test_sql_schema_allows_null_overall_only_for_pity_time(self):
        schema = (ROOT / "supabase" / "pachinko_schema.sql").read_text(encoding="utf-8")
        self.assertIn("initial_overall numeric(6,3),", schema)
        self.assertIn("initial_type = 'PITY TIME'", schema)
        self.assertIn("initial_overall is null", schema)
        self.assertIn("initial_overall is not null", schema)
        self.assertIn("pachinko_total_consistency", schema)
        self.assertIn("get_pachinko_rank_for_score", schema)
        self.assertIn("get_pachinko_leaderboard", schema)
        self.assertIn("enable row level security", schema.lower())


if __name__ == "__main__":
    unittest.main()
