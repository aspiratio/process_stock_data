# process_stock_data

## 処理内容

- （必須）SBI ネオモバイル証券のポートフォリオページから、株の情報をスクレイピングする
  - 証券コード
  - 銘柄名
  - 保有数量
  - 平均取得単価
  - 現在値
  - 1株あたりの配当金
- （必須）証券コードと業種を紐づける
  - https://www.jpx.co.jp/markets/statistics-equities/misc/01.html から入手した東証上場銘柄一覧を元に紐付けを行う
  - 可能なら https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls を直接参照したい
- （必須）高配当株ポートフォリオ スプレッドシートを編集する
