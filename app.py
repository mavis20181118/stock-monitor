import streamlit as st
from data_clean import fetch_stock_data
from plotly_chart import plot_trend_with_volume


# ===== Streamlit 基本設定 =====
st.set_page_config(
    page_title="股價追蹤與波動提醒工具",
    layout="wide"
)

st.title("📈 股價追蹤與波動提醒工具")

# ===== 使用者輸入 =====
stock_id = st.text_input("請輸入股票代碼", value="2330").strip()

# ===== 輔助函式：計算漲跌幅並顯示 =====
# 這段就是依照你提供的語法邏輯改寫的通用函式
def check_volatility(df, threshold, time_label, col_name="Close"):
    if df.empty:
        st.caption(f"{time_label}：無資料")
        return

    # 取得第一筆與最後一筆資料
    start_price = df.iloc[0]["Open"] if time_label == "當日" else df.iloc[0][col_name]
    end_price = df.iloc[-1][col_name]
    
    # 計算漲跌幅 (%)
    change_pct = (end_price - start_price) / start_price * 100

    # 顯示數據
    st.metric(label=f"{time_label}漲跌幅", value=f"{change_pct:.2f}%")

    # 依照你的語法邏輯判斷 (紅漲綠跌)
    if change_pct >= threshold:
        st.error(f"{time_label}累積上漲 {change_pct:.2f}%（超過 {threshold}%）")
    elif change_pct <= -threshold:
        st.success(f"{time_label}累積下跌 {change_pct:.2f}%（超過 {threshold}%）")
    else:
        st.caption(f"{time_label}波動平穩 (未超過 {threshold}%)")

# ===== 主流程 =====
if stock_id:
    try:
        # 1. 抓資料
        result = fetch_stock_data(stock_id)
        
        # 2. 解包資料
        data_1d_1m = result["data_1d_1m"]  # 當日
        data_1m = result["data_1m"]        # 當月
        data_1y = result["data_1y"]        # 當年
        
        # ===== 防呆：沒資料 =====
        if data_1m.empty:
            st.warning("查無資料，請確認代碼或目前非交易時間。")
        else:
            st.markdown("---")
            st.subheader("波動提醒警示 (紅=漲 / 綠=跌)")
            
            # 建立三欄
            col1, col2, col3 = st.columns(5)

            # --- 第一欄：當日 (門檻設 3%) ---
            with col1:
                check_volatility(data_1d_1m, threshold=5, time_label="當日")

            # --- 第二欄：近一月 (門檻設 10%) ---
            with col2:
                check_volatility(data_1m, threshold=10, time_label="近一月")

            # --- 第三欄：近一年 (門檻設 20%) ---
            with col3:
                check_volatility(data_1y, threshold=20, time_label="近一年")

            st.markdown("---")

            # ===== 4. 股價走勢圖 (分頁顯示) =====
            st.subheader(f"{stock_id} 股價走勢圖")
            
            tab1, tab2, tab3 = st.tabs(["🕒 當日走勢", "近一個月", "近一年"])

            with tab1:
                if not data_1d_1m.empty:
                    fig_day = plot_trend_with_volume(data_1d_1m, stock_id, "當日")
                    st.plotly_chart(fig_day, use_container_width=True)
                else:
                    st.info("無當日盤中資料")

            with tab2:
                if not data_1m.empty:
                    fig_month = plot_trend_with_volume(data_1m, stock_id, "近一個月")
                    st.plotly_chart(fig_month, use_container_width=True)

            with tab3:
                if not data_1y.empty:
                    fig_year = plot_trend_with_volume(data_1y, stock_id, "近一年")
                    st.plotly_chart(fig_year, use_container_width=True)

    except Exception as e:
        st.error(f"發生錯誤: {e}")