# process_stock_data

## 処理内容

- SBI ネオモバイル証券のポートフォリオページから、株の情報をスクレイピングする
  - 証券コード
  - 銘柄名
  - 保有数量
  - 平均取得単価
  - 現在値
- みんかぶの配当ページをスクレイピング
  - 1 株あたりの配当金
- 日本取引所グループ（https://www.jpx.co.jp/markets/statistics-equities/misc/01.html）が公開している「東証上場銘柄一覧」から下記情報を入手
  可能なら https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls を直接参照したい
  - 市場
  - 業種
- 高配当株ポートフォリオ スプレッドシートを編集する
