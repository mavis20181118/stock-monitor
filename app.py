import streamlit as st
import pandas as pd
from data_clean import fetch_stock_data
from plotly_chart import plot_trend_with_volume

# ===== 1. Streamlit 頁面設定 =====
st.set_page_config(
    page_title="股價追蹤與波動提醒工具",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("📈 股價追蹤與波動提醒工具")

# ===== 2. 定義波動提醒函式 (紅漲綠跌邏輯) =====
def check_volatility(df, threshold, time_label, col_name="Close"):
    """
    計算漲跌幅並顯示警示
    df: 資料 DataFrame
    threshold: 觸發提醒的百分比門檻 (例如 5, 10, 20)
    time_label: 顯示名稱 (例如 '當日', '近一月')
    col_name: 用來計算的欄位 (當日用 Open/Close, 其他用 Close)
    """
    if df.empty:
        st.caption(f"{time_label}：無資料")
        return

    # 取得第一筆與最後一筆資料
    # 當日走勢通常比較 Open vs 目前價；長線則比較第一天 Close vs 最後一天 Close
    if time_label == "當日":
        start_price = df.iloc[0]["Open"]
        end_price = df.iloc[-1]["Close"]
    else:
        start_price = df.iloc[0][col_name]
        end_price = df.iloc[-1][col_name]
    
    # 計算漲跌幅 (%)
    change_pct = (end_price - start_price) / start_price * 100

    # 顯示數據指標
    st.metric(label=f"{time_label}漲跌幅", value=f"{change_pct:.2f}%")

    # 依照門檻顯示提醒 (Streamlit: error=紅色/漲, success=綠色/跌)
    if change_pct >= threshold:
        st.error(f"{time_label}累積上漲 {change_pct:.2f}%（超過 {threshold}%）")
    elif change_pct <= -threshold:
        st.success(f"{time_label}累積下跌 {change_pct:.2f}%（超過 {threshold}%）")
    else:
        st.caption(f"{time_label}波動平穩 (未超過 {threshold}%)")


# ===== 3. 使用者輸入區 =====
stock_id = st.text_input("請輸入股票代碼", value="0050").strip()

# ===== 4. 主程式邏輯 =====
if stock_id:
    try:
        # --- A. 抓取資料 ---
        with st.spinner(f"正在抓取 {stock_id} 資料中..."):
            result = fetch_stock_data(stock_id)

        # --- B. 檢查回傳結果 ---
        # 如果 result 是 None 或資料異常，顯示錯誤
        if not result or result["data_1m"].empty:
            st.warning("查無資料，請確認股票代碼是否正確。")
        else:
            # --- C. 解包資料 (使用 Key 取值，避免 ValueError) ---
            data_1d_1m = result["data_1d_1m"]  # 當日 (分K)
            data_1m = result["data_1m"]        # 近一月 (日K)
            data_1y = result["data_1y"]        # 近一年 (日K)
            
            st.markdown("---")

            # --- D. 波動提醒區塊 (三欄版面) ---
            st.markdown("**波動提醒警示**")
            col1, col2, col3 = st.columns(3)

            # 1. 當日 (門檻 3%)
            with col1:
                check_volatility(data_1d_1m, threshold=3, time_label="當日")
            
            # 2. 近一月 (門檻 10%)
            with col2:
                check_volatility(data_1m, threshold=10, time_label="近一月")
            
            # 3. 近一年 (門檻 20%)
            with col3:
                check_volatility(data_1y, threshold=20, time_label="近一年")

            st.markdown("---")

            # --- E. 股價走勢圖 (分頁籤顯示) ---
            st.markdown("**股價走勢圖**")
            
            # 建立三個分頁
            tab1, tab2, tab3 = st.tabs(["當日", "近一月", "近一年"])

            # 分頁 1: 當日
            with tab1:
                if not data_1d_1m.empty:
                    fig_day = plot_trend_with_volume(data_1d_1m, stock_id, "當日")
                    st.plotly_chart(fig_day, use_container_width=True)
                else:
                    st.info("查無當日盤中資料 (可能為開盤前或休市)")

            # 分頁 2: 近一個月
            with tab2:
                if not data_1m.empty:
                    fig_month = plot_trend_with_volume(data_1m, stock_id, "近一個月")
                    st.plotly_chart(fig_month, use_container_width=True)
                else:
                    st.warning("查無當月資料")

            # 分頁 3: 近一年
            with tab3:
                if not data_1y.empty:
                    fig_year = plot_trend_with_volume(data_1y, stock_id, "近一年")
                    st.plotly_chart(fig_year, use_container_width=True)
                else:
                    st.warning("查無當年資料")

    except Exception as e:
        # --- F. 錯誤處理 ---
        st.error(f"發生未預期的錯誤: {e}")