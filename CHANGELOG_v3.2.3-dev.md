# 3.2.3-dev — 2026-11-09

- Reverse-calibrate the pre-upgrade hold distribution so the final color distribution remains exactly 90% / 9% / 0.9% / 0.09% / 0.01% after the 1/50 one-step upgrade.
- Recalculate blue hold trust to approximately 0.526%; the final weighted hit probability is 1/73.
- Count the initial jackpot together with RUSH jackpots in the result payout distribution, including the 4,500 NOTES category.
- Fix the RANK lookup used by the PNG card and apply the same color to SSS+ and SSS, as well as the other plus/non-plus rank pairs.
- Add the payout distribution pie chart and all payout counts to the 4:3 landscape PNG result card.
- Add the initial jackpot category to the result display and card.
- Update the README manual to match the latest game rules and thresholds; include the public manual URL.
- Preserve the tap-timing score implementation and fixed baseline data.
