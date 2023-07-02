#!/usr/bin/env python
# coding: utf-8


import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from sbi_scraping import get_own_stock_df
from minkabu_scraping import append_dividend
from tse_stock_list_downloader import append_market_and_industries
from spread_sheet_update import update_sheet


# 通常のドライバ
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


try:
    # 証券会社のwebサイトから保有株情報を抽出する
    df_own_stock = get_own_stock_df(driver)
except Exception as e:
    print("Failed get_own_stock_df")
    print(str(e))
finally:
    driver.quit()


try:
    # 配当金額を抽出する（処理に時間がかかる）
    df_own_stock = append_dividend(df_own_stock)
    # このあとでエラーになった場合途中から再開できるよう、CSVに吐き出しておく
    df_own_stock.to_csv("own_stock.csv")
except Exception as e:
    print("Failed append_dividend")
    print(str(e))


try:
    # 吐き出しておいたCSVを読み込む
    df_own_stock = pd.read_csv("own_stock.csv", index_col=0)
except Exception as e:
    print("Failed read_csv")
    print(str(e))


try:
    # データフレームに市場と業種を入れる
    df_own_stock = append_market_and_industries(df_own_stock)
except Exception as e:
    print("Failed append_market_and_industries")
    print(str(e))


try:
    # 完成したデータフレームをスプレッドシートに書き込む
    update_sheet(df_own_stock)
except Exception as e:
    print("Failed update_sheet")
    print(str(e))
