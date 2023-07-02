#!/usr/bin/env python
# coding: utf-8

import config

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def update_sheet(df_own_stock):
    # スプレッドシートに書き込めるようにリスト形式に変換する
    list_own_stock = df_own_stock.values.tolist()

    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    # 認証情報設定
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "keys/credentials.json", scope
    )

    # OAuth2の資格情報を使用してGoogle APIにログイン
    gc = gspread.authorize(credentials)

    # 共有設定したスプレッドシートを開く
    spreadsheet = gc.open_by_key(config.SPREADSHEET_KEY)

    # シート名を指定してシートを開く
    worksheet = spreadsheet.worksheet(config.SHEET_NAME)

    # シートの既存の値をクリアする（B列からJ列だけ上書きするため）
    worksheet.batch_clear(["B4:I300"])

    # シートのB4:J4からデータフレームの値を書き込む
    cell_range = f"B4:I{3 + len(list_own_stock)}"
    worksheet.update(cell_range, list_own_stock)
