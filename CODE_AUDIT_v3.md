# 3.0移行時コード監査

確認日：2026-11-07  
対象：2.0 Final（v2～v7統合・Rank/SlowFast調整版）

## 確認できた改善点

| 対象 | 確認内容 | 対応 |
|---|---|---|
| `app.py` → `src/result_card.py` | 旧実装の既定出力先 `output/result_card.png` をWebアプリの各セッションが共有していた | Webアプリから呼ぶ際は解析ごとに一意な一時PNGパスを渡すよう変更。成功・例外時の後処理も追加 |
| 日時処理 | `datetime.now()` とUTC+9固定指定が混在 | `Asia/Tokyo` に統一 |
| `src/validator.py` | `ValidationResult` の必須フィールドを渡さず、dataclassに存在しない `valid` 属性を設定していた | 実際のdataclassフィールドに合わせて修正。呼び出し元が指定した場合のみチャレンジレート閾値を判定 |
| テスト | 計算・境界値の自動回帰テストが不足 | unittestベースの9テストを追加 |
| `src/utils.py` | 現行 `src/score.py` と異なる旧スコア式が残存。プロジェクト内の参照は検出されなかった | 互換性を考慮してファイルは残置。今後の整理対象として記録 |

## 追加で確認したい箇所

- `app.py` は約2,740行で、画面描画・入力・解析呼び出し・ランキング・共有が同じファイルに存在する。機能単位で段階的に分割する。
- `src/result_card.py` は約6,129行。現行デザインを維持したまま、描画領域ごとの関数・モジュールへ分割する余地がある。
- `src/crop.py` と `src/cropper.py` は役割の重複がないか、呼び出し元を追跡してから統合可否を判断する。
- `app.py.pre_rank_slowfast` と `src/result_card.py.pre_rank_slowfast` はバックアップ用途のため、実行パッケージから分離できる。
- `requirements.txt` は現行環境でのインストール・起動確認が未実施。依存バージョンを安易に変更せず、デプロイ環境で検証する。
- Streamlit Cloud上のブラウザ実機テストおよび複数セッションの負荷テストは未実施。

## この監査で変更していないもの

- YOLOモデルと検出閾値
- 棒グラフ検出・判定推定ロジック
- AMAZING+ / AMAZINGの達成率ウェイト
- Precision / Balance / Overallの計算とランク境界
- ランキング基準CSV（1,799件）
- リザルトカードのデザイン・寸法
- READMEに掲載された従来画面のスクリーンショット

## ローカル確認結果

- `python -m compileall -q app.py ranking.py src tests`：PASS
- `python -m unittest discover -s tests -v`：9 tests PASS
- Streamlit / streamlit-js-eval / ultralytics：この作業環境に未導入のためWebアプリ起動・YOLO推論は未確認。
