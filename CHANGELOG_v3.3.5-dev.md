# Changelog — 3.3.5-dev

Date: 2026-11-13

## OVERALL PACHINKO
- 特図2：時短にALL 6,000 NOTES（100%）の円グラフを追加。
- 時短131回転の大当たり期待度（約97.9％）を表示。
- 遊タイム発動条件を通常時150回転連続未当選に設定。
- 1回の通常区間で遊タイムに到達する確率、時短スルー確率もマニュアルへ記載。

## Simulation
- `theoretical_pity_percentage` の欠落による表示エラーを修正。
- 100万件シミュレーションのRANK分布チャートがエラーで中断されないように修正。
- 150回転条件で100万件シミュレーションを再生成。

## Validation
- Full unittest suite: 70 passed.
