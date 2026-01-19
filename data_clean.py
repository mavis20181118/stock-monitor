import yfinance as yf
import pandas as pd

def fetch_stock_data(stock_id: str):
    try:
        ticker = yf.Ticker(f"{stock_id}.TW")
        # 抓長資料 (近兩年，用來切分年/月)
        stock_history_2y = ticker.history(period="2y")
        # 抓短資料 (當日分K)
        stock_history_1d_1m = ticker.history(period="1d", interval="1m")
    except Exception as e:
        print(f"連線失敗: {e}")
        return None

    if stock_history_2y.empty:
        print("查無資料")
        return None

    # 切割時間
    one_year_ago = stock_history_2y.index[-1] - pd.DateOffset(years=1)
    one_month_ago = stock_history_2y.index[-1] - pd.DateOffset(months=1)

    stock_history_1y = stock_history_2y.loc[stock_history_2y.index > one_year_ago]
    stock_history_1m = stock_history_2y.loc[stock_history_2y.index > one_month_ago]

    # 回傳字典
    return {
        "data_1d_1m": stock_history_1d_1m,
        "data_1m": stock_history_1m,  # 當月資料
        "data_1y": stock_history_1y   # 當年資料
    }

# 測試選2330
#stock_id = "2330"
#result = fetch_stock_data_test(stock_id)
#print(result["data_1d_1m"])
#print(result["data_1m"])
#print(result["data_1y"])