# 3.2.7-dev — 2026-11-10

## OVERALL PACHINKO

- 「初当たり抽選」を「初当たり回転数」に変更。
- ルーレット停止ボタンの文言から「抽選結果は変わりません」を削除。
- 白点滅保留の説明を削除。
- スペック欄の保留信頼度の下に獲得期待出玉（約9,976 NOTES）を追加。
- 確定した21段階RANKボーダーの横に、初当たり1万回のシミュレーション人数・割合を追加。
- RUSH大当たり時、消化済み保留以外の未消化保留を次のSTへ引き継ぐよう変更。
- 初当たり獲得NOTESの数字を300=青、1,500=金、3,000/4,500=虹に統一。
- リザルトカード円グラフに割合ラベルを追加。小さい区分は引き出し線付きで表示。
- 結果画像を画面内にプレビュー表示。iPhone/iPadでは画像長押しで写真保存を試せるようにし、PCではPNGダウンロードを維持。
- PLAY RESULT見出しと画面内プレビューのQR位置を少し下へ調整。保存用カード画像のQR位置は維持。

## Verification

- Python syntax compilation: passed.
- Unit tests: 22 passed.
- Embedded JavaScript syntax: passed.
- iOS Safari / mobile browser visual and touch testing: not available in build environment; user-side verification required.
