import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def process_stock(stock_code):
    print(f"{stock_code} start")

    options = ChromeOptions()
    options.add_argument("--headless")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 配当ページへアクセス
        url_dividend = f"https://minkabu.jp/stock/{stock_code}/dividend"
        driver.get(url_dividend)

        # 要素が表示されるまで待機する
        wait = WebDriverWait(driver, 10)
        try:
            dividend_elements = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "dividend-state__amount__integer")
                )
            )
            dividend_decimal_elements = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "dividend-state__amount__decimal")
                )
            )
        except TimeoutException:
            # 予想配当金がないものは0円として処理する
            print(f"{stock_code} skipped")
            return stock_code, 0

        # 1株配当金を取得する
        dividend_integer = dividend_elements[0].text.strip()
        dividend_decimal = dividend_decimal_elements[0].text.strip()
        dividend = float(dividend_integer + dividend_decimal)
        print(f"{stock_code} finish")
        return stock_code, dividend
    finally:
        driver.quit()


def append_dividend(df_own_stock):
    print("Minkabu scraping started...")

    stock_codes = df_own_stock["コード"].tolist()
    results = []

    try:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(process_stock, stock_code) for stock_code in stock_codes
            ]

            for future in concurrent.futures.as_completed(futures):
                stock_code, dividend = future.result()
                results.append((stock_code, dividend))

        # 結果を DataFrame に反映する
        for stock_code, dividend in results:
            index = df_own_stock[df_own_stock["コード"] == stock_code].index[0]
            df_own_stock.loc[index, "1株配当"] = dividend
    finally:
        print("Minkabu scraping finished")

    return df_own_stock
