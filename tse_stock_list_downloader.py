#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import requests


def get_tse_stock_df():
    stock_list_url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    response = requests.get(stock_list_url)
    return pd.read_excel(response.content)


def append_market_and_industries(df_own_stock):
    df_tse_stock = get_tse_stock_df()
    df_tse_stock["コード"] = df_tse_stock["コード"].astype(object)
    # 銘柄コードにマッチする市場と業種を一時的なデータフレームに追加する
    temp_merged_df = pd.merge(df_own_stock, df_tse_stock, on="コード", how="left")
    # 既存の"市場"列と"業種"列の値を上書きする
    df_own_stock["市場"] = temp_merged_df["市場・商品区分"]
    df_own_stock["業種"] = temp_merged_df["33業種区分"]
    return df_own_stock
