import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ 建議：在 multipage 專案裡，set_page_config 只放 app.py
# 如果你 app.py 已經有 set_page_config，這裡就不要再放，避免怪問題
# st.set_page_config(
#     page_title="Model Output Visualization",
#     page_icon="📉",
#     layout="wide",
# )

# ===========================
# Page Title
# ===========================
st.title("Model Output Visualization")

st.markdown(
    """
    To validate the profit-based Wave-2 mailing decision, we visualize the output of the
    final Neural Network model. Rather than introducing new evaluation metrics, these plots
    provide an intuitive check that the model’s ranking behavior aligns with economic logic
    under the case assumptions.
    """
)

st.divider()


# ===========================
# Load NN results
# ===========================
@st.cache_data
def load_nn_results():
    # 專案根目錄（app.py 那層）
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # ✅ 你的 CSV 在 data 資料夾
    csv_path = os.path.join(BASE_DIR, "data", "person2_nn_mailable_ranked.csv")

    # 如果找不到，直接把資訊印出來方便你 debug（找到後可刪）
    if not os.path.exists(csv_path):
        st.error(f"❌ File not found: {csv_path}")
        st.write("BASE_DIR =", BASE_DIR)
        data_dir = os.path.join(BASE_DIR, "data")
        st.write(
            "Files in /data =",
            os.listdir(data_dir)
            if os.path.exists(data_dir)
            else "data/ folder not found",
        )
        st.stop()

    df = pd.read_csv(csv_path)
    df = df.sort_values("expected_profit_nn", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    df["cumulative_profit"] = df["expected_profit_nn"].cumsum()
    return df


df = load_nn_results()

left, right = st.columns([1.7, 1])

with left:
    # ===========================
    # Plot 1
    # ===========================
    st.subheader("Plot 1: Expected Profit by Customer Rank")

    st.markdown(
        """
        This plot shows expected profit for customers ranked by the Neural Network model,
        from highest to lowest expected profit.
        """
    )

    fig1, ax1 = plt.subplots()
    ax1.plot(df["rank"], df["expected_profit_nn"])
    ax1.set_xlabel("Customer Rank (Highest Expected Profit First)")
    ax1.set_ylabel("Expected Profit ($)")
    ax1.set_title("Expected Profit by Customer Rank (Neural Network)")
    st.pyplot(fig1)

    st.markdown(
        """
        **Interpretation:**
        Customers ranked highest by the Neural Network generate the largest expected profit.
        As rank increases, expected profit declines steadily and eventually becomes negative.
        This pattern supports the Wave-2 decision rule of mailing only customers with positive
        expected profit, since mailing beyond this point would reduce overall profitability.
        """
    )

    # ===========================
    # Plot 2
    # ===========================
    st.subheader("Plot 2: Cumulative Expected Profit as More Customers Are Mailed")

    st.markdown(
        """
        This plot shows cumulative expected profit as customers are added in order of
        decreasing expected profit.
        """
    )

    fig2, ax2 = plt.subplots()
    ax2.plot(df["rank"], df["cumulative_profit"])
    ax2.set_xlabel("Number of Customers (Sorted by Expected Profit)")
    ax2.set_ylabel("Cumulative Expected Profit ($)")
    ax2.set_title("Cumulative Expected Profit as More Customers Are Mailed (NN)")
    st.pyplot(fig2)

    st.markdown(
        """
        **Interpretation:**
        Cumulative expected profit increases rapidly for the top-ranked customers,
        indicating that mailing to these customers generates positive incremental profit.
        As lower-ranked customers are included, the curve flattens and eventually declines
        once expected profits become negative. This provides a direct economic justification
        for using expected profit greater than zero as the cutoff for Wave-2 mailing.
        """
    )

with right:
    st.subheader("Why These Plots Matter")

    st.markdown(
        """
        - Confirms that the Neural Network ranking aligns with profit logic
        - Visually validates the Expected Profit > 0 decision rule
        - Demonstrates why a cutoff is necessary for maximizing total profit
        - Bridges model output with business execution decisions
        """
    )

st.divider()
st.caption("Section 12 — Model Output Visualization")
