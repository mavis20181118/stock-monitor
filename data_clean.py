import pandas as pd

# 民國年 → 西元年，例如 114/12/31 → 2025-12-31
def convert_roc_to_ad(roc):
    y, m, d = roc.split("/")      # "114", "12", "31"
    y = int(y) + 1911             # 114 + 1911 = 2025
    return f"{y}-{m}-{d}"         # "2025-12-31"


# 讀取 ＆ 整理股價資料
def load_and_clean_data(file_path="sample_data.csv"):

    # 讀檔，強制把 stock_id 視為字串（避免 0050 被變成 50）
    df = pd.read_csv(file_path, dtype={"stock_id": str})

    # 日期：民國 → 西元 → datetime
    df["date"] = df["date"].apply(convert_roc_to_ad)
    df["date"] = pd.to_datetime(df["date"])

    # 股票代碼補齊 4 碼
    df["stock_id"] = df["stock_id"].astype(str).str.zfill(4)

    # 收盤價轉數字，移除不合法資料
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna()

    # 依日期排序，確保時間順序正確
    df = df.sort_values(["stock_id", "date"])

    return df