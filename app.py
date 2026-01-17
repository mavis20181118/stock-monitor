#這段無法做測試

import streamlit as st
# .py檔語法
from data_clean import fetch_stock_data
from plotly_chart import plot_month_price

st.set_page_config(page_title="股價追蹤工具", layout="wide")
st.title("📈 股價追蹤與波動提醒工具")

# 使用者輸入股票代碼
stock_id = st.text_input(
    "請輸入股票代碼",
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
            # ===== 波動提醒區 =====
            st.subheader("波動提醒")

            col1, col2, col3 = st.columns(3)

            with col1:
                if warning_1y != "無":
                    st.warning(f"一年：{warning_1y}")
                else:
                    st.success("一年：無明顯異常波動")

            with col2:
                if warning_1m != "無":
                    st.warning(f"單月：{warning_1m}")
                else:
                    st.success("單月：無明顯異常波動")

            with col3:
                if warning_1d != "無":
                    st.warning(f"本日：{warning_1d}")
                else:
                    st.success("本日：無明顯異常波動")

            # ===== 圖表區 =====
            st.subheader("近一個月股價走勢")

            fig = plot_month_price(data_1m, stock_id)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("資料讀取或圖表產生失敗，請稍後再試。")