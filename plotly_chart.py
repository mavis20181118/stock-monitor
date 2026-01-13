import plotly.express as px

def plot_month_price(data_1m, stock_id: str):
    fig = px.line(
        data_1m,
        x=data_1m.index,
        y="Close",
        title=f"{stock_id} 近一個月收盤價",
        labels={
            "index": "日期",
            "Close": "價格"
        }
    )

    return fig

# 測試用
#stock_id = "2330" # 測試用股票
#data_1m = fetch_stock_data(stock_id)  # 1_date_clean 端抓資料
#fig = plot_month_price(data_1m, stock_id)  # 畫圖
#fig.show()   # 直接顯示圖表（Notebook 專用）