# Changelog — 3.3.3-dev

Date: 2026-11-11

## Branding
- App title uses ensemble-stars-analyzer; the analysis page is described as あんさんぶるスターズ！！Music タップタイミング解析Webアプリ.
- Subtitle: Tap Timing Analysis & Mini Games.
- Deployment URL and database identifiers remain unchanged.

## Completed RUSH presentation layer
- Added a RUSH-specific presentation selector, available at RUSH entry and changeable during active RUSH:
  - STANDARD: balanced hold, foreshadowing, and result presentation.
  - SHADOW VISITOR: hold-arrival atmosphere followed by a darkened screen, red-eye motif, approach cue, and sudden reveal after a confirmed hit.
  - IMPACT: impact flash and screen shake for selected hold-arrival cues, with a strong confirmed-hit reveal.
  - ONE PUSH: after a hit has already been determined, the player can press PUSH to reveal it; automatic reveal follows after 4.5 seconds if not pressed.
- Added hold-arrival foreshadowing. It is a presentation cue only and does not promise a hit.
- Added escalating screen treatment at 1–3, 4–7, 8–11, and 12+ consecutive RUSH hits.
- Added visible chain count to the RUSH screen and jackpot message.
- Added payout-tier-specific reveal glow for 300 / 1,500 / 3,000 / 4,500 / 6,000 NOTES, without changing the payout distribution.
- All RUSH presentation modes are independent of hit determination, payout selection, ST decrement, and hold outcome.

## Responsive result card
- Saved PNG card height now expands based on achievement and date-line content.
- QR placement follows the dynamic footer position.
- Achievement labels and date text wrap into additional lines rather than being clipped.

## Preserved mechanics
- Normal hit probability, RUSH hit probability, ST120, hold color weights, hold upgrade 1/50, Pity Time (150 consecutive misses / +6000 NOTES), RUSH payout weights, rank thresholds, and simulation data are unchanged.
- Visual random values for the normal spin animation use Web Crypto and do not consume the gameplay Math.random stream.
- Supabase schema, RPC, and registration payload are unchanged.
- Public ranking displays only rank, total NOTES, RANK, RUSH chain count, and play date/time.
- X share weighted-length limit remains 220 characters.

## Design note
- The RUSH presentation uses original OVERALL PACHINKO visual language. It is inspired by general suspense and one-shot announcement design patterns, not a reproduction of copyrighted characters, artwork, dialogue, music, or screen layouts.


## Final polish — normal-time presentation

- Added three dedicated normal-time presentation modes: STANDARD, FORESHADOW, and QUICK.
- Added a staged normal-spin presentation: hold arrival / subtle foreshadowing / chance reach / final development / result reveal.
- Added distinct visual language for tease, reach, hot development, and final moment.
- Presentation tier is selected with `visualRandom()` only. It does not consume game draw RNG, change the selected OVERALL result, alter the 1/34.6 hit rate, modify initial payout, or change Pity Time at 150 consecutive misses.
- Normal-time mode selector is hidden during RUSH; the RUSH selector remains available during RUSH.
- Added regression tests for the three normal modes, isolated visual RNG, and staged visual states.

## User-test revision — 2026-11-12

- Removed the SIMPLE / BALANCE / PREMIUM selector and fixed the presentation quality to PREMIUM.
- Removed short explanatory narration from normal-spin stages; normal-time cues now rely on screen treatment and sound.
- Updated the three normal-time mode descriptions to the requested wording.
- Added a Pity Time countdown from 50 spins remaining, with stronger treatment in the final 10 spins. Trigger condition remains 150 consecutive misses.
- Reworked SHADOW VISITOR, IMPACT, and ONE PUSH so the cue (including its foreshadowing) can occur before the result is revealed, on either a hit or a miss.
- Calibrated hit and miss cue-selection paths so that each dedicated cue has 40% conditional hit confidence; the cue does not change the 1/73 RUSH hit probability.
- Added initial cue-frequency settings by hold color: blue 1.2%, green 7%, red 8%, gold 10%; rainbow holds are excluded because they are already guaranteed hits.
- Added original Web Audio synthesized win cues for SHADOW VISITOR, IMPACT, and ONE PUSH. Long dedicated sounds are played only on hits.
- Intensified remaining-ST screen treatment.
- Removed achievement titles from the result card and moved play date into a dedicated footer with a visible lower border. PNG layout now reserves a fixed, adequate date area.
- Added `docs/OVERALL_PACHINKO演出マニュアル.md`. The cue rates are marked as initial calibration values pending browser/device play testing.
- Added regression checks for 40% conditional cue confidence and fixed PREMIUM presentation.

## User-test follow-up — 2026-11-12
- Removed wording that described the miss percentage after the 40% dedicated-event confidence; the UI now displays confidence only.
- RUSH ST is represented as 116 main spins plus up to 4 already-stored reserve holds (maximum 120 total opportunities). New holds are blocked after the 116th main spin.
- Slowed the final ten opportunities (main spins 111–116 plus up to four reserve holds) and added a dedicated jackpot celebration for hits in that window.
- Adjusted provisional dedicated-event trigger rates by hold color while retaining 40% conditional confidence.
- Added an eight-chapter beginner manual in the app and a standalone Markdown copy.

## 2026-11-12 UI/UX refinement (user playtest feedback)
- Added a live RANK panel showing the current RANK and NOTES required to reach the next tier, with a progress bar.
- Added cumulative RUSH consumed-spin counter to the live game HUD.
- Added original synthesized final-zone BGM from the final 10 ST spins (107th–116th) through up to 4 reserve holds; final-zone interval slowed to 1.9 seconds.
- Added dedicated jackpot celebration when a hit occurs during the final 10 ST spins or the reserve-hold phase.
- Kept the ST specification at 116 main spins + up to 4 already-stored reserve holds; no new holds can be added after the 116th ST spin.
- Removed chapter jump-navigation links from the beginner guide; all chapters remain native collapsible sections.
- Expanded the beginner glossary and FAQ; blue-hold hit confidence is displayed as approximately 0.5%.
- Updated the OVERALL PACHINKO tab description and set the browser page title to the repository/deployment name ensemble-stars-analyzer.
- Changed the mini-game and result-card title to OVERALL PACHINKO; removed RESULT CARD label, web-app URL and QR code from the result card.
- Preserved app URL in X share text; the removal applies only to result-card presentation.


## 2026-11-12 UI・演出調整（動作確認用）
- メインのヒーロー見出しを「TAP TIMING ANALYZER / あんさんぶるスターズ！！Music / タップタイミング解析」に復元。
- ミニゲーム内の図柄・HOLD・ST・連チャン・回転数表示を先に配置し、モード選択とRANK進捗を下側へ移動してスマートフォンの視線移動を改善。
- 現在のRANK文字色をリザルトカードのRANKカラーと同期。
- 初心者向けガイドのRUSH説明を「連チャン（継続）を狙う遊技状態」に修正。
- ONE PUSH大当たり時の虹色演出と専用音の開始タイミングを同期。
- SHADOW VISITORの赤い眼を大型化し、発光・赤い残光を強化。
- 残保留当選時はSTを再セットし、連チャン数・獲得NOTES・未消化保留を引き継ぐ仕様を確認。未消化保留の当否は消化時に抽選する。


## 2026-11-12 — Pachinko scope separation
- Replaced the OVERALL PACHINKO result-card online leaderboard panel with a top-percentile comparison based on the existing 1,000,000-trial total-NOTES distribution. Equal-score trials are included in the displayed upper-tail percentage.
- Removed the OVERALL PACHINKO online leaderboard section from the bottom of the page and removed its client-side Supabase registration/rank lookup.
- Updated the beginner guide wording and removed obsolete ranking comparison / blackout explanations.
- Kept the main Tap Timing Analysis ranking unchanged.
- No changes to pachinko draw probabilities, payouts, RUSH/ST behavior, RANK thresholds, or simulation data.

## 2026-11-12 — Application naming
- Replaced the visible LIVE SCORE LAB product name with ensemble-stars-analyzer in the local app page title, footer, README, build information, and relevant manuals.
- Descriptive references use あんさんぶるスターズ！！Music タップタイミング解析 or タップタイミング解析Webアプリ. The pachinko mini-game name remains OVERALL PACHINKO.
