# Changelog — 3.3.2-dev

Date: 2026-11-11

## OVERALL PACHINKO

- Enabled SIMPLE / BALANCE / PREMIUM selection throughout an active game, including during RUSH.
- Kept the effect-mode selector available during RUSH so the player can change the presentation mode before or during a subsequent RUSH.
- Added an adjacent mode description and included the same explanations in the in-app rules guide.
- SIMPLE shortens presentation waits and suppresses decorative burst effects.
- BALANCE retains standard presentation timing and effects.
- PREMIUM lengthens presentation waits and emphasizes burst, screen, and jackpot visual effects.
- Added visual phase styling for CHANCE ZONE, HIGH CHANCE, COUNT DOWN, and FINAL CHANCE while preserving the existing ST thresholds.
- Reduced X share output to a maximum of 220 weighted characters, counting URLs as 23 characters and retaining the hashtag and app URL. Optional detail lines and then the achievement line are removed if needed.
- Kept achievement summaries on the result and saved result card.

## Compatibility / safety

- No edits to `src/pachinko.py`, payout constants, hold-color probabilities, random draw functions, Supabase schema, ranking RPC, or ranking payload.
- The mode selector only updates presentation state and CSS/timing behavior.
- Existing tests were updated to reflect the newly requested in-play mode selection and 220-character X-share limit.
