import streamlit as st
from data_clean import load_and_clean_data
from analysis_plot import calc_metrics, plot_stock_chart

st.title("📈 股價追蹤與波動提醒工具")

# 讀資料
df = load_and_clean_data()

# 股票代碼下拉選單
stock_list = df["stock_id"].unique()
stock_id = st.selectbox("請選擇股票代碼", stock_list)

# 篩選股票資料
df_stock = df[df["stock_id"] == stock_id]

# 指標計算
summary, df_7 = calc_metrics(df_stock)

# 顯示文字摘要
st.write("👉", summary)

# 繪製圖表（Plotly）
fig = plot_stock_chart(df_7, stock_id)
st.plotly_chart(fig, use_container_width=True)