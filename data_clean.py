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

    try:
        stock_history_2y = ticker.history(period="2y")
        stock_history_1d = ticker.history(period="1d")
        stock_history_1d_1m = ticker.history(period="1d", interval="1m")
    except Exception:
        return {}

    if stock_history_2y.empty:
        return {}

    #stock_history_2y = ticker.history(period="2y")

    # 改成內縮
    one_year_ago = stock_history_2y.index[-1] - pd.DateOffset(years=1) 
    one_month_ago = stock_history_2y.index[-1] - pd.DateOffset(months=1)
    stock_history_1y = stock_history_2y.loc[stock_history_2y.index > one_year_ago]
    stock_history_1m = stock_history_2y.loc[stock_history_2y.index > one_month_ago]

    data_for_line_chart = stock_history_2y[["Close"]].copy()
    data_for_line_chart["MA5"] = stock_history_2y[["Close"]].rolling(5).mean()
    data_for_line_chart["MA20"] = stock_history_2y[["Close"]].rolling(20).mean()

    # 1y
    # 原版
    #transaction_volume_1y = sum(stock_history_1y["Volume"]) # 當年交易量
    #highest_price_1y = max(stock_history_1y["Close"]) # 當年最高價
    #lowest_price_1y = min(stock_history_1y["Close"]) # 當年最低價
    #data_line_chart_1y = data_for_line_chart.loc[data_for_line_chart.index > one_year_ago].copy()

    # 更新版
    summary_1y = {
        "transaction_volume": sum(stock_history_1y.get("Volume")),
        "highest_price": max(stock_history_1y.get("Close")),
        "lowest_price": min(stock_history_1y.get("Close")),
        "line_chart": data_for_line_chart.loc[data_for_line_chart.index > one_year_ago].copy()
            if not stock_history_1y.empty else pd.DataFrame()
    }

    # 測試
    #print(summary_1y)

    # 1m
    # 原版
    #transaction_volume_1m = sum(stock_history_1m["Volume"]) # 當月交易量
    #highest_price_1m = max(stock_history_1m["Close"]) # 當月最高價
    #lowest_price_1m = min(stock_history_1m["Close"]) # 當月最低價
    #data_line_chart_1m = data_for_line_chart.loc[data_for_line_chart.index > one_month_ago].copy()

    # 更新版
    summary_1m = {
        "transaction_volume": sum(stock_history_1m.get("Volume")),
        "highest_price": max(stock_history_1m.get("Close")),
        "lowest_price": min(stock_history_1m.get("Close")),
        "line_chart": data_for_line_chart.loc[data_for_line_chart.index > one_month_ago].copy() 
            if not stock_history_1m.empty else pd.DataFrame()
    }
    
    # 測試
    #print(summary_1m)

    # 1d
    # 原版
    #transaction_volume_1d = stock_history_1d["Volume"].iloc[-1] # 當日交易量
    #highest_price_1d = stock_history_1d["High"].iloc[-1] # 當日最高價
    #lowest_price_1d = stock_history_1d["Low"].iloc[-1] # 當日最低價
    #close_price_1d = stock_history_1d["Close"].iloc[-1] # 當日收盤價
    #open_price_1d = stock_history_1d["Open"].iloc[-1] # 當日開盤價
    #data_line_chart_1d = stock_history_1d_1m[["Close"]].copy()

    # 更新版
    if stock_history_1d.empty:
        summary_1d = {
            "transaction_volume": None,
            "open": None,
            "close": None,
            "high": None,
            "low": None,
            "line_chart": pd.DataFrame()
        }
    else:
        summary_1d = {
            "transaction_volume": stock_history_1d["Volume"].iloc[-1],
            "open": stock_history_1d["Open"].iloc[-1],
            "close": stock_history_1d["Close"].iloc[-1],
            "high": stock_history_1d["High"].iloc[-1],
            "low": stock_history_1d["Low"].iloc[-1],
            "line_chart": (
                stock_history_1d_1m[["Close"]].copy()
                    if not stock_history_1d_1m.empty else pd.DataFrame()
            )
        }
    
    # 測試  
    #print(summary_1d)
    
    return summary_1y,summary_1m,summary_1d


# 測試選2330
#test = fetch_stock_data("2330")
#test.head() # 顯示前五筆資料