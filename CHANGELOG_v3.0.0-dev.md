# Changelog — 3.0.0-dev

日付：2026-11-07

## 安定性・保守性の初期整備
- カード画像の出力先を解析ごとの一意な一時ファイルに変更。
- カード一時ファイルを例外経路も含めてクリーンアップ。
- アプリおよびCSV記録のタイムゾーンを `Asia/Tokyo` に統一。
- `validator.py` を `ValidationResult` dataclassに適合させ、任意のチャレンジレート閾値を明示的に指定するAPIへ整理。
- スコア計算、ランク境界、バリデーション、ランキング基準件数の回帰テストを追加。
- 既存の解析モデル・スコア仕様・ランキング基準・カードデザインは維持。

## 未実施
- Webアプリ全体のUI刷新
- `app.py` の全面的なモジュール分割
- PERFECT判定の拡張
- ランキング基準データ2,000件化
- Streamlit Cloud上の実機E2Eテスト

## 3.1.0-dev Renewal Preview — 2026-11-07

- Added top-level tabs for Tap Timing Analyzer and OVERALL PACHINKO.
- Added browser-side pachinko mini-game with fixed 1,799-record sampling, RUSH/ST/hold loop, calibrated 1/99 conditional probability, payout distribution, result PNG and X sharing.
- Added first-visit three-step guidance and explicit estimated-value notice.
- Added five achievement badge artworks based on existing analysis outputs; score formulas remain unchanged.
- Added animated rank reveal and ranking summary/distribution details.
- Added result-card QR code and app URL.
- Added README and implementation notes.
- No analysis-history or account features added; ranking baseline remains read-only.
