import streamlit as st
from data_clean import load_and_clean_data
from analysis_plot import calc_metrics, plot_stock_chart

st.header("📈 股價追蹤與波動提醒工具")

# 讀資料（A 成員產出）
df = load_and_clean_data()

# 使用者輸入股票代碼
stock_id = st.text_input(
    "請輸入股票代碼",
    value="0050"
)

# 自動補成 4 位數，避免 50 → 0050
stock_id = stock_id.strip().zfill(4)


# ===== 查詢與顯示結果 =====
if stock_id:
    df_stock = df[df["stock_id"] == stock_id]

    # 查不到股票
    if df_stock.empty:
        st.warning("查無此股票代碼，請重新輸入。")

    else:
        # 計算指標 + 取近 7 天資料（B 成員產出）
        summary, df_7 = calc_metrics(df_stock)

        # 顯示 7 天摘要
        st.write(summary)


        # ===== 波動提醒邏輯 =====
        threshold = 5  # 設定漲跌門檻（%）

        # 計算近 7 天單日漲跌幅
        start = df_7.iloc[0]["close"]
        end = df_7.iloc[-1]["close"]

        total_change = (end - start) / start * 100   # 7 天累積漲跌幅

        if total_change >= threshold:
            st.error(f" 提醒：近 7 天累積上漲 {total_change:.2f}%（超過 {threshold}%）")

        elif total_change <= -threshold:
            st.success(f" 提醒：近 7 天累積下跌 {total_change:.2f}%（超過 {threshold}%）")

        else:
            st.caption(" 近 7 天累積漲跌幅尚未超過提醒門檻")


        # ===== 繪製圖表（B 成員函式） =====
        fig = plot_stock_chart(df_7, stock_id)
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{stock_id}")
