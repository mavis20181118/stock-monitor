import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 🟢 中文字型設定（必須放在繪圖前）
matplotlib.rcParams["font.sans-serif"] = [
    "Microsoft JhengHei",
    "Noto Sans CJK TC",
    "PingFang TC",
    "Arial Unicode MS",
]
matplotlib.rcParams["axes.unicode_minus"] = False

# B 模組：計算波動與指標
def calc_metrics(df_stock):
    """
    df_stock：單一股票資料（由 C 篩選後傳入）
    需要欄位：date, stock_id, close
    """

    # 只取最近 7 天
    df_7 = df_stock.tail(7).copy()

    # 計算每日漲跌百分比
    df_7["pct"] = df_7["close"].pct_change()

    # 近 7 天總漲跌幅
    start = df_7["close"].iloc[0]
    end = df_7["close"].iloc[-1]
    change_7d = (end - start) / start * 100

    # 最大單日波動
    max_vol = df_7["pct"].abs().max() * 100

    # 給 C 的摘要文字
    summary = (
        f"近 7 天漲跌幅：{change_7d:.2f}%　"
        f"最大單日波動：{max_vol:.2f}%"
    )


    return summary, df_7

