import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def process_stock(stock_code, driver):
    print(f"{stock_code} start")
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


def append_dividend(df_own_stock):
    print("Minkabu scraping started...")

    stock_codes = df_own_stock["コード"].tolist()
    results = []

    try:
        # ヘッドレスモードのブラウザインスタンスを3つ生成する
        options = ChromeOptions()
        options.add_argument("--headless")  # ヘッドレスモードで起動（GUIを使用しない）
        service = ChromeService(
            ChromeDriverManager().install()
        )  # ドライバが古ければ新しいものをインストールする
        driver1 = webdriver.Chrome(service=service, options=options)
        driver2 = webdriver.Chrome(service=service, options=options)
        driver3 = webdriver.Chrome(service=service, options=options)
        driver4 = webdriver.Chrome(service=service, options=options)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 複数のインスタンスで並行して処理する
            futures = []
            for i, stock_code in enumerate(stock_codes):
                driver = (
                    driver1
                    if i % 4 == 0
                    else driver2
                    if i % 4 == 1
                    else driver3
                    if i % 4 == 2
                    else driver4
                )
                futures.append(executor.submit(process_stock, stock_code, driver))

            for future in concurrent.futures.as_completed(futures):
                stock_code, dividend = future.result()
                results.append((stock_code, dividend))

        # 結果を DataFrame に反映する
        for stock_code, dividend in results:
            index = df_own_stock[df_own_stock["コード"] == stock_code].index[0]
            df_own_stock.loc[index, "1株配当"] = dividend

    finally:
        # ブラウザを終了
        driver1.quit()
        driver2.quit()
        driver3.quit()
        driver4.quit()

    print("Minkabu scraping finished")

    return df_own_stock
