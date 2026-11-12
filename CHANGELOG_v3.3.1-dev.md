# Changelog — 3.3.1-dev

Date: 2026-11-11

## OVERALL PACHINKO
- Updated the normal + Pity Time five-outcome specification display to 26.6%, 55.1%, 15.2%, 1.9%, and 1.2%.
- Updated displayed normal jackpot probability to approximately 1/35.
- Color-coded the RUSH payout table to match its pie chart.
- Added hold-color hit-rate and appearance-rate table, using the rates defined by the existing game probability constants.
- Corrected the Pity Time display line to `+ 6,000 NOTES`.
- Added an X weighted-character-length guard (280 maximum); optional detail lines are removed and the final text is shortened if needed.
- Updated expected payout figures to integer display values: 1,465 / 1,521 / 8,511 / 10,032 NOTES.
- Updated displayed RUSH continuation to approximately 81% and Pity Time activation odds to approximately 1/81.
- Removed the in-game Pity Time sample/test button; the actual Pity Time game logic and payout remain unchanged.
- Removed the HTML result-panel QR image; the QR code remains on the saved result-card image.
- Added RUSH remaining-ST phase labels and presentation transitions.
- Added in-play achievement notifications and result-card/X-share achievement summaries.
- Added SIMPLE / BALANCE / PREMIUM effect modes. These alter presentation timing/effects only.
- Reordered the 1M simulation histogram from F (left) to SSS+ (right); removed the detail table and download controls from this section.

## Compatibility
- No changes to pachinko draw probabilities, payout distributions, RUSH hit probability, Pity Time trigger, random selection order, Supabase schema, ranking RPC, or ranking payload.
- The uploaded 3.3.0-dev achievement/effect specification is implemented within `src/pachinko_ui.py` where possible.
