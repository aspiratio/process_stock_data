#!/usr/bin/env python
# coding: utf-8


import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def append_dividend(driver, df_own_stock):
    # 各銘柄のみんかぶの配当ページから1株配当金を取得する

    for i, stock_code in enumerate(df_own_stock["コード"]):
        print(f"{stock_code} start")
        # 配当ページへアクセス
        url_dividend = f"https://minkabu.jp/stock/{stock_code}/dividend"
        driver.get(url_dividend)
        time.sleep(5)
        # 予想配当金がないものは0円として処理する
        list_element = driver.find_elements(
            By.CLASS_NAME, "dividend-state__amount__integer"
        )
        if list_element == []:
            df_own_stock.loc[i, "1株配当"] = 0
            print(f"{stock_code} skipped")
            continue
        # ページのhtmlを取得してパースする
        html = driver.page_source.encode("utf-8")
        parsed_html = BeautifulSoup(html, "html.parser")
        # 1株配当金を取得する
        dividend_integer = (
            parsed_html.find_all(class_="dividend-state__amount__integer")[0]
            .get_text()
            .strip()
        )  # 整数部分＋小数点
        dividend_decimal = (
            parsed_html.find_all(class_="dividend-state__amount__decimal")[0]
            .get_text()
            .strip()
        )  # 小数部分
        dividend = float(dividend_integer + dividend_decimal)
        df_own_stock.loc[i, "1株配当"] = dividend
        print(f"{stock_code} finish")

    return df_own_stock
