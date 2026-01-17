import yfinance as yf
import pandas as pd


# 原版
#taiwan_2330 = yf.Ticker("2330.TW")
#stock_history_2y = taiwan_2330.history(period="2y")
#stock_history_1d_1m = taiwan_2330.history(period="1d", interval="1m")
#stock_history_1d = taiwan_2330.history(period="1d")

# 更新版
def fetch_stock_data(stock_id: str):
    ticker = yf.Ticker(f"{stock_id}.TW")
    stock_history_2y = ticker.history(period="2y") # 近兩年的股價資料
    stock_history_1d_1m = ticker.history(period="1d", interval="1m") #抓 今天每分鐘的股價
    stock_history_1d = ticker.history(period="1d") # 抓 今天收盤股價

    # 以下內縮
    one_year_ago = stock_history_2y.index[-1] - pd.DateOffset(years=1) # 計算一年前的日期
    one_month_ago = stock_history_2y.index[-1] - pd.DateOffset(months=1) # 計算一個月前的日期
    stock_history_1y = stock_history_2y.loc[stock_history_2y.index > one_year_ago] # 取出近一年的股價
    stock_history_1m = stock_history_2y.loc[stock_history_2y.index > one_month_ago] # 取出近一個月的股價

    data_for_line_chart = stock_history_2y[["Close"]].copy() # 每天收盤價
    data_for_line_chart["MA5"] = stock_history_2y[["Close"]].rolling(5).mean() # 計算五日均線
    data_for_line_chart["MA20"] = stock_history_2y[["Close"]].rolling(20).mean() # 計算二十日均線

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

    # warning
    start_1y = stock_history_1y["Close"].iloc[0]
    end_1y = stock_history_1y["Close"].iloc[-1]
    fluctuation_1y = (end_1y - start_1y) / start_1y
    if fluctuation_1y > 0.2:
        warning_1y = "一年上漲超過20%"
    elif fluctuation_1y < -0.2:
        warning_1y = "一年下跌超過20%"
    else:
        warning_1y = "無"

    start_1m = stock_history_1m["Close"].iloc[0]
    end_1m = stock_history_1m["Close"].iloc[-1]
    fluctuation_1m = (end_1m - start_1m) / start_1m
    if fluctuation_1m > 0.1:
        warning_1m = "單月上漲超過10%"
    elif fluctuation_1m < -0.1:
        warning_1m = "單月下跌超過10%"
    else:
        warning_1m = "無"

    #start_1d = stock_history_2d["Close"].iloc[0]
    #end_1d = stock_history_2d["Close"].iloc[-1]
    #fluctuation_1d = (end_1d - start_1d) / start_1d
    #if fluctuation_1d > 0.05:
        #warning_1d = "本日上漲超過5%"
    #elif fluctuation_1d < -0.05:
        #warning_1d = "本日下跌超過5%"
    #else:
        #warning_1d = "無"

    # 1d（用 開盤 vs 收盤 才合理）
    open_1d = stock_history_1d["Open"].iloc[-1]
    close_1d = stock_history_1d["Close"].iloc[-1]
    fluctuation_1d = (close_1d - open_1d) / open_1d

    if fluctuation_1d > 0.05:
        warning_1d = "本日上漲超過5%"
    elif fluctuation_1d < -0.05:
        warning_1d = "本日下跌超過5%"
    else:
        warning_1d = "無"


    # 測試用
    #print(one_year_ago)
    #print(one_month_ago)
    #print(stock_history_1y)
    #print(stock_history_1m)
    #print(data_for_line_chart.head())
    #print(data_for_line_chart["MA5"].head()) #看「前 5 筆」
    #print(data_for_line_chart["MA20"].tail()) #看「後 5 筆」

    #print(transaction_volume_1y,highest_price_1y,lowest_price_1y,data_line_chart_1y)
    #print(transaction_volume_1m,highest_price_1m,lowest_price_1m,data_line_chart_1m)
    #print(transaction_volume_1d,highest_price_1d,lowest_price_1d,data_line_chart_1d,open_price_1d)

    return {stock_history_1m,warning_1y,warning_1m,warning_1d}

# 測試選2330
#test = fetch_stock_data("2330")
#test.head() # 顯示前五筆資料