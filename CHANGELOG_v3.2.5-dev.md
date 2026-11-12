# Version 3.2.5-dev — 2026-11-10

## OVERALL PACHINKO
- Moved START/HOLD controls directly below the draw display; empty hold row collapses on normal play.
- Moved specs, payout distributions, play guide, and RANK thresholds into in-page collapsible sections.
- Added iOS/Safari audio-context unlock on the first user gesture, volume slider, normal-mode drum-roll ticks, jackpot cues, and weighted RUSH payout roulette presentation.
- Prevented text selection and iOS callout while long-pressing HOLD.
- RUSH payout roulette outcome is randomly selected before the animation; the stop-animation control does not alter payout odds.
- Added brief white flash as a hold-arrival pre-alert; the actual hold color and its probability are unchanged.
- Clarified initial hit probability (~1/35), RUSH hit probability (1/73), and rounded continuation rate (~81%). Blue hold trust is displayed as ~0.5%.
- Matched payout chart segment/legend colors to the payout tiers and colored total/RUSH-earned NOTES independently from RANK.
- Removed highest COMBO from stats/result presentation; retained only RUSH jackpot count.
- Updated 21 rank thresholds and unified rank colors across PACHINKO and Tap Timing Analyzer result displays.

## Verification
- Python compileall: passed.
- Unit tests: 19 passed.
- JavaScript syntax check: run separately during packaging.
- Actual iPhone/Safari audio and touch behavior still require user-device confirmation; browser autoplay restrictions and device mute settings remain outside app control.

## 3.2.6-dev (2026-11-10)
- OVERALL PACHINKO RANK thresholds updated to the 1,000,000-trial unimodal-distribution proposal: F starts at 300 NOTES; all 21 ranks have unique lower bounds from 300 through 55,200+.
- The live result card was rebuilt around the supplied 4:3 reference layout: total NOTES and RANK, ranking status, initial-hit information, RUSH information, payout pie/legend, play date, app URL, and QR code.
- The downloaded PNG result card now uses the same 1600×1200 (4:3) panel composition and includes the payout pie chart and all five payout categories.
- The rank manual table and README rank thresholds were synchronized with the new boundaries.
- Tap timing score logic and fixed baseline data were not changed.
