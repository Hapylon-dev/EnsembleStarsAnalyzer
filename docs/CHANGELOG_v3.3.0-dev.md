# CHANGELOG — 3.3.0-dev

Release date: 2026-11-11

## OVERALL PACHINKO
- Added Pity Time after 150 consecutive normal misses.
- Pity Time awards 6,000 NOTES and enters RUSH.
- Pity Time results display `PITY TIME` and `--.---` for initial OVERALL.
- Updated RUSH payout weights to 300 / 1,500 / 3,000 / 4,500 / 6,000 NOTES = 20 / 50 / 15 / 10 / 5%.
- Corrected average RUSH payout to 2,010 NOTES.
- Updated theoretical EV values to include Pity Time.
- Updated all 21 RANK thresholds to the 3rd-edition final values.
- Centralized RANK thresholds, RUSH payout weights, hold color weights, and conditional hit rates for browser rendering.
- Rewrote in-game manual/specification values to match the 3rd-edition spec.

## Simulation
- Added deterministic 1,000,000-trial Monte Carlo simulation with seed 20261111.
- Added individual compressed CSV, summary JSON, and RANK histogram CSV.
- Added in-app simulation metrics, histogram, and CSV download.

## Supabase leaderboard
- Made `initial_overall` nullable for Pity Time.
- Added `initial_type`, `initial_spins`, `initial_payout_notes`, and `rush_notes`.
- Added RLS policies and RPC functions for efficient page retrieval and competition ranking.
- Added support for `SUPABASE_PUBLISHABLE_KEY` and legacy `SUPABASE_ANON_KEY`.
- Sends new opaque publishable keys only in the `apikey` header; legacy anon JWTs also use `Authorization: Bearer`.
- Refuses to embed a new `sb_secret_` key into the browser iframe.
- Changed leaderboard retrieval from per-row rank queries to a single RPC call.
- Added null-safe leaderboard and result-card display.

- Added a Pity Time demo control that runs the real activation display and opens a labeled sample result; demo records are explicitly excluded from Supabase registration and marked in X share text.

## Regression protection
- Preserved the existing tap timing analyzer, score calculations, ranking base CSV, assets, fonts, and result-card/share modules.
- Added Pity Time boundary, RANK boundary, simulation export, browser JavaScript, and Supabase schema/client tests.
