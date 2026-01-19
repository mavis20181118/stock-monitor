import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_trend_with_volume(data, stock_id, title_suffix):
    if data is None or data.empty:
        return None

    # 1. 建立雙層圖表
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,          
        vertical_spacing=0.05,      
        row_heights=[0.7, 0.3],     
        subplot_titles=(f"股價", "成交量")
    )

    # 2. 上圖：股價 (折線)
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Close"], 
        name="收盤價", mode="lines", 
        line=dict(color="#1f77b4", width=2)
    ), row=1, col=1)

    # 3. 下圖：成交量 (長條)
    fig.add_trace(go.Bar(
        x=data.index, y=data["Volume"], 
        name="成交量", marker_color="#ff7f0e"
    ), row=2, col=1)
    
    # 預設設定 (讓標籤旋轉 -45 度避免重疊)
    xaxis_config = dict(
        tickangle=-45,
        rangeslider=dict(visible=False), # 隱藏下方滑桿以節省空間
        showgrid=True,
        gridcolor='rgba(128,128,128,0.2)', # 淡灰色網格
    )

    # (A) 針對「近一個月」：顯示詳細日期 (例如 01/05)
    if "月" in title_suffix:
        xaxis_config.update(dict(
            tickformat="%m/%d",     # 格式：月/日
            dtick=86400000.0 * 1,   # 刻度：強制每 1 天顯示一次 (避免太擠或太疏)
        ))
    
    # (B) 針對「近一年」：顯示月份 (例如 2025/03)
    elif "年" in title_suffix:
        xaxis_config.update(dict(
            tickformat="%Y/%m",     # 格式：年/月
            dtick="M1"              # 刻度：強制每一個月顯示一次
        ))

    # (C) 針對「當日」：顯示時間 (例如 09:30)
    elif "日" in title_suffix:
        xaxis_config.update(dict(
            tickformat="%H:%M",     # 格式：時:分
        ))

    # 套用 X 軸設定
    fig.update_xaxes(**xaxis_config)

    # 4. 其他版面設定
    fig.update_layout(
        height=550, 
        title_text=f"{stock_id} {title_suffix}走勢圖",
        showlegend=False,
        hovermode="x unified",  # 讓滑鼠游標能同時顯示上下圖的數值
        margin=dict(l=50, r=50, t=80, b=80) # 調整邊界避免文字被切到
    )
    
    return fig

# 測試
#stock_id = "2330"
#result = fetch_stock_data_test(stock_id)

#if result:
    data_day = result["data_1d_1m"]
    data_month = result["data_1m"]
    data_year = result["data_1y"]

    # 1. 當日走勢
    if not data_day.empty:
        fig1 = plot_trend_with_volume(data_day, stock_id, "當日")
        fig1.show()
    else:
        print("無當日盤中資料 (可能未開盤)")

    # 2. 當月走勢 (這就是你要加的)
    if not data_month.empty:
        fig2 = plot_trend_with_volume(data_month, stock_id, "近一個月")
        fig2.show()
    else:
        print("無當月資料")

    # 3. 當年走勢
    if not data_year.empty:
        fig3 = plot_trend_with_volume(data_year, stock_id, "近一年")
        fig3.show()
    else:
        print("無當年資料")