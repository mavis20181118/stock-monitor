#這段無法做測試

import streamlit as st
# .py檔語法
from data_clean import fetch_stock_data
from plotly_chart import plot_month_price

st.set_page_config(page_title="股價追蹤工具", layout="wide")
st.title("📈 股價追蹤與波動提醒工具")

# 使用者輸入股票代碼
stock_id = st.text_input(
    "請輸入股票代碼（例如 2330）",
    value="2330"
).strip()

if stock_id:
    try:
        # A：抓取近一個月資料
        data_1m = fetch_stock_data(stock_id)

        # 若資料為空，避免 B 端出錯
        if data_1m.empty:
            st.warning("查無資料，請確認股票代碼是否正確。")

        else:
            # B：產生圖表
            fig = plot_month_price(data_1m, stock_id)

            # C：顯示圖表
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("資料讀取或圖表產生失敗，請稍後再試。")