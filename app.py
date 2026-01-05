import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rcParams

from data_clean import load_and_clean_data
from analysis_plot import calc_metrics


# ===== 字型設定（避免中文變方框） =====
rcParams["font.sans-serif"] = [
    "Microsoft JhengHei",      # Windows
    "Taipei Sans TC Beta",     # macOS
    "Noto Sans CJK TC"         # Linux
]
rcParams["axes.unicode_minus"] = False


# ===== A：讀取整理後資料 =====
df = load_and_clean_data()

st.title("📈 股價追蹤與波動提醒工具")


# ===== C：使用者選股票 =====
stock_list = df["stock_id"].unique()
stock_id = st.selectbox("請選擇股票代碼", stock_list)

df_stock = df[df["stock_id"] == stock_id]


# ===== B：計算 7 天指標 =====
summary, df_7 = calc_metrics(df_stock)

st.write(stock_id, summary)


# ===== 視覺化（避免日期重疊，改為 mm-dd） =====
df_7["date_str"] = df_7["date"].dt.strftime("%m-%d")

fig, ax = plt.subplots()

ax.plot(df_7["date_str"], df_7["close"], linewidth=2)
ax.scatter(df_7["date_str"], df_7["close"], s=40)

ax.set_title(f"{stock_id} 近 7 天價格走勢")
ax.set_xlabel("日期")
ax.set_ylabel("價格")

ax.grid(alpha=0.3)
ax.xaxis.set_major_locator(plt.MaxNLocator(5))

st.pyplot(fig)