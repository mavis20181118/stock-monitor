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
        threshold = 5  # 設定跌幅門檻（%）

        # 計算近 7 天「最大單日跌幅」
        drop_pct = df_7["close"].pct_change().min() * 100

        if drop_pct <= -threshold:
            st.error(f"近 7 天最大跌幅已達 {drop_pct:.2f}%（超過 {threshold}%）")
        else:
            st.info("目前波動仍在正常範圍內")


        # ===== 繪製圖表（B 成員函式） =====
        fig = plot_stock_chart(df_7, stock_id)
        st.plotly_chart(fig, use_container_width=True, key=f"chart_{stock_id}")
