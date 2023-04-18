import re


def extract_number(text):
    """
    文字列から数値部分のみを抽出するための関数
    """
    number = re.findall(r"[-+]?\d*\.\d+|\d+", text.replace(",", ""))[0]
    return number
