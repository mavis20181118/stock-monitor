import yfinance as yf
import pandas as pd


def fetch_stock_data(stock_id: str):
    """
    抓取台股資料並產生波動提醒
    回傳：
    {
        data_1m: DataFrame,
        warning_1y: str,
        warning_1m: str,
        warning_1d: str
    }
    """

    # ===== 抓資料 =====
    ticker = yf.Ticker(f"{stock_id}.TW")

    stock_history_2y = ticker.history(period="2y")          # 近兩年（日）
    stock_history_1d = ticker.history(period="1d")          # 今日（日）
    stock_history_1d_1m = ticker.history(period="1d", interval="1m")  # 今日（分）

    # ===== 防呆：完全沒資料 =====
    if stock_history_2y.empty:
        return {
            "data_1m": pd.DataFrame(),
            "warning_1y": "無",
            "warning_1m": "無",
            "warning_1d": "無"
        }

    # ===== 切時間區間 =====
    one_year_ago = stock_history_2y.index[-1] - pd.DateOffset(years=1)
    one_month_ago = stock_history_2y.index[-1] - pd.DateOffset(months=1)

    stock_history_1y = stock_history_2y.loc[stock_history_2y.index > one_year_ago]
    stock_history_1m = stock_history_2y.loc[stock_history_2y.index > one_month_ago]

    # ===== 波動提醒 =====

    # --- 1 年 ---
    start_1y = stock_history_1y["Close"].iloc[0]
    end_1y = stock_history_1y["Close"].iloc[-1]
    fluctuation_1y = (end_1y - start_1y) / start_1y

    if fluctuation_1y > 0.2:
        warning_1y = "一年上漲超過20%"
    elif fluctuation_1y < -0.2:
        warning_1y = "一年下跌超過20%"
    else:
        warning_1y = "無"

    # --- 1 個月 ---
    start_1m = stock_history_1m["Close"].iloc[0]
    end_1m = stock_history_1m["Close"].iloc[-1]
    fluctuation_1m = (end_1m - start_1m) / start_1m

    if fluctuation_1m > 0.1:
        warning_1m = "單月上漲超過10%"
    elif fluctuation_1m < -0.1:
        warning_1m = "單月下跌超過10%"
    else:
        warning_1m = "無"

    # --- 單日（用開盤 vs 收盤） ---
    if not stock_history_1d.empty:
        open_1d = stock_history_1d["Open"].iloc[-1]
        close_1d = stock_history_1d["Close"].iloc[-1]
        fluctuation_1d = (close_1d - open_1d) / open_1d

        if fluctuation_1d > 0.05:
            warning_1d = "本日上漲超過5%"
        elif fluctuation_1d < -0.05:
            warning_1d = "本日下跌超過5%"
        else:
            warning_1d = "無"
    else:
        warning_1d = "無"

    # ===== 回傳給 app.py =====
    return {
        "data_1m": stock_history_1m,
        "warning_1y": warning_1y,
        "warning_1m": warning_1m,
        "warning_1d": warning_1d
    }