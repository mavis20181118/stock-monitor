import plotly.express as px
import pandas as pd

def plot_month_price(data_1m: pd.DataFrame, stock_id: str):
    fig = px.line(
        data_1m,
        y="Close",
        title=f"{stock_id} 近一個月收盤價走勢",
        labels={
            "index": "日期",
            "Close": "價格"
        }
    )

    return fig