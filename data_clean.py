import yfinance as yf
import pandas as pd

# 修改前
#taiwan_2330 = yf.Ticker("2330.TW")
#stock_history_2y = taiwan_2330.history(period="2y")
#stock_history_1d_1m = taiwan_2330.history(period="1d", interval="1m")
#stock_history_1d = taiwan_2330.history(period="1d")

# 修改後
def fetch_stock_data(stock_id: str):
    ticker = yf.Ticker(f"{stock_id}.TW")
    stock_history_2y = ticker.history(period="2y")

    # 以下改成內縮
    one_year_ago = stock_history_2y.index[-1] - pd.DateOffset(years=1) 
    one_month_ago = stock_history_2y.index[-1] - pd.DateOffset(months=1)
    stock_history_1y = stock_history_2y.loc[stock_history_2y.index > one_year_ago]
    stock_history_1m = stock_history_2y.loc[stock_history_2y.index > one_month_ago]

    data_for_line_chart = stock_history_2y[["Close"]].copy()
    data_for_line_chart["MA5"] = stock_history_2y[["Close"]].rolling(5).mean()
    data_for_line_chart["MA20"] = stock_history_2y[["Close"]].rolling(20).mean()

    # 1y
    transaction_volume_1y = sum(stock_history_1y["Volume"]) # 當年交易量
    highest_price_1y = max(stock_history_1y["Close"]) # 當年最高價
    lowest_price_1y = min(stock_history_1y["Close"]) # 當年最低價
    data_line_chart_1y = data_for_line_chart.loc[data_for_line_chart.index > one_year_ago].copy()

    # 1m
    transaction_volume_1m = sum(stock_history_1m["Volume"]) # 當月交易量
    highest_price_1m = max(stock_history_1m["Close"]) # 當月最高價
    lowest_price_1m = min(stock_history_1m["Close"]) # 當月最低價
    data_line_chart_1m = data_for_line_chart.loc[data_for_line_chart.index > one_month_ago].copy()

    # 1d
    transaction_volume_1d = stock_history_1d["Volume"].iloc[-1] # 當日交易量
    highest_price_1d = stock_history_1d["High"].iloc[-1] # 當日最高價
    lowest_price_1d = stock_history_1d["Low"].iloc[-1] # 當日最低價
    close_price_1d = stock_history_1d["Close"].iloc[-1] # 當日收盤價
    open_price_1d = stock_history_1d["Open"].iloc[-1] # 當日開盤價
    data_line_chart_1d = stock_history_1d_1m[["Close"]].copy()

    return stock_history_1m