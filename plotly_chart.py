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