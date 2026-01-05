import pandas as pd
import plotly.express as px

# 計算 7 日漲跌幅與最大單日波動
def calc_metrics(df_stock):
    df_7 = df_stock.tail(7)

    start = df_7.iloc[0]["close"]
    end = df_7.iloc[-1]["close"]
    pct_change = (end - start) / start * 100

    df_7["daily_pct"] = df_7["close"].pct_change() * 100
    max_vol = df_7["daily_pct"].abs().max()

    summary = (
        f"{df_7.iloc[-1]['stock_id']} 近 7 天漲跌幅：{pct_change:.2f}%　"
        f"最大單日波動：{max_vol:.2f}%"
    )

    return summary, df_7


# 🔹 Plotly 畫圖（支援中文，不用字型設定）
def plot_stock_chart(df_7, stock_id):
    fig = px.line(
        df_7,
        x="date",
        y="close",
        markers=True,
        title=f"{stock_id} 近 7 天價格走勢"
    )

    fig.update_layout(
        xaxis_title="日期",
        yaxis_title="價格",
    )

    return fig