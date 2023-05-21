#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import requests


def get_stock_list():
    stock_list_url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    response = requests.get(stock_list_url)
    return pd.read_excel(response.content)
