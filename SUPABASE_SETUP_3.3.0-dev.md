# Supabase setup — EnsembleStarsAnalyzer 3.3.0-dev

## 1. Create a project
1. Open https://supabase.com/dashboard and create a new project.
2. Choose a project name (for example `ensemble-stars-analyzer`).
3. Choose the Tokyo region when available.
4. Save the database password securely.

## 2. Create the leaderboard schema
1. Open the project.
2. Open **SQL Editor** → **New query**.
3. Copy the complete contents of `supabase/pachinko_schema.sql`.
4. Run the SQL.
5. In **Table Editor**, confirm that `public.pachinko_results` exists.
6. In **Database → Functions**, confirm that `get_pachinko_rank_for_score` and `get_pachinko_leaderboard` exist.

This script is for a new project. It creates a table with nullable `initial_overall`, RLS policies, and two RPC functions. Pity Time records must have `initial_type = 'PITY TIME'`, `initial_spins = 150`, `initial_payout_notes = 6000`, and `initial_overall = NULL`.

## 3. Configure Streamlit secrets

For local execution, create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
SUPABASE_PUBLISHABLE_KEY = "sb_publishable_..."
```

For Streamlit Community Cloud, enter the same TOML values in the app's **Settings → Secrets** page.

The app accepts `SUPABASE_ANON_KEY` as a legacy fallback, but new projects should use `SUPABASE_PUBLISHABLE_KEY`. The new `sb_publishable_...` key is sent in the `apikey` header only; the app does not send it as a Bearer JWT. For a legacy `anon` JWT key, the app also sends `Authorization: Bearer ...`.

**Never use `service_role` or `sb_secret` keys in the browser or in the Streamlit secrets consumed by the browser game. The app detects and blocks the new `sb_secret_` format and legacy JWTs with the `service_role` role.** The publishable/anon key is public by design; database access must be controlled by RLS.

## 4. Test the connection

1. Start the app.
2. Open **OVERALL PACHINKO**.
3. Complete one game.
4. Confirm the result card shows a ranking position.
5. Open the Supabase Table Editor and confirm a new row exists.
6. Confirm normal games store a numeric `initial_overall`.
7. Confirm a Pity Time game stores SQL `NULL` in `initial_overall`, `PITY TIME` in `initial_type`, and `150` in `initial_spins`.
8. Refresh the app and confirm the saved row appears in the shared leaderboard.

## 5. Ranking semantics

- Ranking order: `total_notes DESC`.
- Equal `total_notes` share the same rank.
- Competition ranking is used: `1, 2, 2, 4`.
- The app fetches one page through `get_pachinko_leaderboard`.
- The result rank is calculated by `get_pachinko_rank_for_score`.

## 6. Security limitation

The public leaderboard currently allows anonymous INSERT and SELECT so users can submit and view shared results without accounts. This does not prove that a submitted score was earned by the game client. Anyone with the public app can potentially submit fabricated rows or automate requests. If anti-cheat or abuse resistance is required, move writes behind a Supabase Edge Function or another trusted server that validates signed game results and rate limits submissions.
