import os
import streamlit as st
import polars as pl
from plotnine import (
    ggplot,
    aes,
    geom_line,
    labs,
    theme_minimal,
    theme,
    geom_hline,
    geom_vline,
)

# ============================================================
# Model Output Visualization (Interactive Decision Tool)
# - Wrangling: POLARS (required)
# - Plotting: PLOTNINE (required)
# - pandas conversion: ONLY for plotnine rendering (acceptable)
# ============================================================

st.title("Model Output Visualization & Decision Tool")

# --- Minimal fallback card style (in case the main app doesn't inject it on this page) ---
st.markdown(
    """
    <style>
      .card{
        background: #FFFFFF;
        border: 1px solid rgba(17,24,39,.10);
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(17,24,39,.08);
        padding: 1.05rem 1.15rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar: scenario controls
# -----------------------------
st.sidebar.header("Scenario Controls")

MAIL_COST = st.sidebar.number_input(
    "Mail cost ($/piece)",
    value=1.41,
    step=0.01,
    format="%.2f",
    help="Course assumption default = $1.41 per mail piece.",
)

MARGIN_PER_RESPONDER = st.sidebar.number_input(
    "Margin per responder ($)",
    value=60.0,
    step=1.0,
    format="%.0f",
    help="Course assumption default = $60 net margin per responder (excluding mailing cost).",
)

WAVE2_RESPONSE_MULT = st.sidebar.slider(
    "Wave-2 response multiplier",
    min_value=0.10,
    max_value=1.00,
    value=0.50,
    step=0.05,
    help="Default = 0.50 (50% drop-off vs Wave-1). This scales predicted response probability.",
)

cutoff_rule = st.sidebar.radio(
    "Cutoff rule",
    options=[
        "Mail while Expected Profit > 0",
        "Mail until Peak Cumulative Profit",
        "Mail Top-N customers",
    ],
    index=0,
)

top_n = None
if cutoff_rule == "Mail Top-N customers":
    top_n = st.sidebar.slider(
        "Top N to mail", min_value=100, max_value=22500, value=3500, step=100
    )

show_cutoff_line = st.sidebar.checkbox("Show cutoff line on charts", value=True)

st.sidebar.divider()
st.sidebar.caption(
    "Defaults match the course-required assumptions. Adjust sliders for sensitivity analysis."
)

# -----------------------------
# Assumptions + formula
# -----------------------------
st.markdown(
    f"""
This page visualizes and **operationalizes** the Neural Network output into a Wave-2 mailing decision.

**Assumptions (editable in the sidebar):**
- Mailing cost = **${MAIL_COST:.2f}** per piece
- Margin per responder = **${MARGIN_PER_RESPONDER:.0f}** per responder (excluding mailing cost)
- Wave-2 response multiplier = **{WAVE2_RESPONSE_MULT:.2f}** (e.g., 0.50 means ~50% of Wave-1 response)

**Expected Profit per customer** is computed as:

> **EPᵢ = {MARGIN_PER_RESPONDER:.0f} × (p̂ᵢ × {WAVE2_RESPONSE_MULT:.2f}) − {MAIL_COST:.2f}**
"""
)
st.divider()


# -----------------------------
# Load NN results (polars)
# -----------------------------
@st.cache_data
def _load_raw_nn_results() -> pl.DataFrame:
    """
    Loads the NN results CSV using polars.
    Expected to live at: <project_root>/data/person2_nn_mailable_ranked.csv
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))  # app.py level
    csv_path = os.path.join(base_dir, "data", "person2_nn_mailable_ranked.csv")

    if not os.path.exists(csv_path):
        st.error(f"❌ File not found: {csv_path}")
        st.write("base_dir =", base_dir)
        data_dir = os.path.join(base_dir, "data")
        st.write(
            "Files in /data =",
            os.listdir(data_dir)
            if os.path.exists(data_dir)
            else "data/ folder not found",
        )
        st.stop()

    return pl.read_csv(csv_path)


def _compute_profit_table(df_raw: pl.DataFrame) -> pl.DataFrame:
    """
    Ensures expected_profit_nn exists using the current sidebar assumptions,
    then ranks by expected profit and computes cumulative profit.
    """
    df = df_raw

    prob_candidates = [
        "pred_prob_nn",
        "predicted_prob_nn",
        "p_hat_nn",
        "p_hat",
        "pred_prob",
        "predicted_prob",
        "prob",
        "proba",
        "response_prob",
        "nn_prob",
        "nn_proba",
    ]
    prob_col = next((c for c in prob_candidates if c in df.columns), None)

    # If expected_profit_nn doesn't exist, compute it from a probability column.
    if "expected_profit_nn" not in df.columns:
        if prob_col is None:
            st.error(
                "❌ Could not find 'expected_profit_nn' OR any recognized probability column to compute it.\n\n"
                "Please ensure your CSV includes either:\n"
                "- expected_profit_nn, OR\n"
                "- a predicted probability column (e.g., pred_prob_nn / predicted_prob / prob)."
            )
            st.write("Columns found:", df.columns)
            st.stop()

        df = df.with_columns(
            (
                pl.lit(MARGIN_PER_RESPONDER)
                * (pl.col(prob_col).cast(pl.Float64) * pl.lit(WAVE2_RESPONSE_MULT))
                - pl.lit(MAIL_COST)
            ).alias("expected_profit_nn")
        )
    else:
        # Even if expected_profit_nn exists, recompute it when a prob column exists
        # so sidebar controls truly update results.
        if prob_col is not None:
            df = df.with_columns(
                (
                    pl.lit(MARGIN_PER_RESPONDER)
                    * (pl.col(prob_col).cast(pl.Float64) * pl.lit(WAVE2_RESPONSE_MULT))
                    - pl.lit(MAIL_COST)
                ).alias("expected_profit_nn")
            )

    df = (
        df.sort("expected_profit_nn", descending=True)
        .with_row_index(name="rank", offset=1)
        .with_columns(pl.col("expected_profit_nn").cum_sum().alias("cumulative_profit"))
    )
    return df


df_raw = _load_raw_nn_results()
df_pl = _compute_profit_table(df_raw)
df = df_pl.to_pandas()  # plotnine expects pandas

# -----------------------------
# Determine cutoffs / KPIs
# -----------------------------
# First non-positive EP rank (profit>0 rule)
profit_cutoff_rank = None
if (df["expected_profit_nn"] <= 0).any():
    profit_cutoff_rank = int(df.loc[df["expected_profit_nn"] <= 0, "rank"].iloc[0])
else:
    profit_cutoff_rank = int(df["rank"].max())

# Peak cumulative profit rule
peak_idx = int(df["cumulative_profit"].idxmax())
peak_rank = int(df.loc[peak_idx, "rank"])
peak_profit = float(df.loc[peak_idx, "cumulative_profit"])

# Choose active cutoff
if cutoff_rule == "Mail while Expected Profit > 0":
    cutoff_rank = profit_cutoff_rank
elif cutoff_rule == "Mail until Peak Cumulative Profit":
    cutoff_rank = peak_rank
else:
    cutoff_rank = int(top_n)

# Profit at chosen cutoff
profit_at_cutoff = float(df.loc[df["rank"] == cutoff_rank, "cumulative_profit"].iloc[0])

# Human-readable label for cutoff method (short + won't overflow)
cutoff_method_label = {
    "Mail while Expected Profit > 0": "Expected Profit > 0",
    "Mail until Peak Cumulative Profit": "Peak cumulative profit",
    "Mail Top-N customers": f"Top-N (N={top_n:,})" if top_n is not None else "Top-N",
}.get(cutoff_rule, cutoff_rule)

# -----------------------------
# Plot 1: EP by rank
# -----------------------------
st.markdown("### Plot 1: Expected Profit by Customer Rank (Neural Network)")

# -----------------------------
# KPI row (decision at a glance) — FIXED
# -----------------------------
k1, k2, k3, k4 = st.columns([1.15, 1.7, 1.15, 1.15])

k1.metric("Recommended mails", f"{cutoff_rank:,}")
k3.metric("Peak cumulative profit", f"${peak_profit:,.0f}")
k4.metric("Profit @ cutoff", f"${profit_at_cutoff:,.0f}")

with k2:
    st.markdown(
        f"""
        <div class="card" style="padding:0.85rem 1rem; min-height:112px;">
          <div style="font-size:.85rem; color:rgba(18,20,23,.65); font-weight:600; margin-bottom:.35rem;">
            Cutoff method
          </div>
          <div style="font-size:1.0rem; font-weight:800; line-height:1.35; white-space:normal; word-break:break-word;">
            {cutoff_method_label}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

p1 = (
    ggplot(df, aes(x="rank", y="expected_profit_nn"))
    + geom_line()
    + geom_hline(yintercept=0)
    + (geom_vline(xintercept=cutoff_rank) if show_cutoff_line else 0)
    + labs(
        title="Expected Profit by Customer Rank (Neural Network)",
        x="Customer Rank (Highest Expected Profit First)",
        y="Expected Profit ($)",
    )
    + theme_minimal()
    + theme(figure_size=(10, 4))
)
st.pyplot(p1.draw(), clear_figure=True)

st.markdown(
    f"""
**Interpretation:**
Customers ranked highest by the Neural Network generate the largest expected profit.
As rank increases, expected profit declines and can turn negative.
Under the selected rule, the recommended cutoff is **rank {cutoff_rank:,}**.
"""
)

# -----------------------------
# Decision Summary card (full width)
# -----------------------------
st.markdown(
    f"""
<div class="card" style="margin-top:0.8rem;">
  <h3 style="margin-top:0;">Decision Summary</h3>
  <ul>
    <li><b>Decision rule:</b> Mail a customer only when the chosen cutoff criterion is satisfied.</li>
    <li><b>Current recommendation:</b> Mail the top <b>{cutoff_rank:,}</b> customers (highest expected profit first).</li>
    <li><b>Economic logic:</b> Expected Profit is computed as <b>{MARGIN_PER_RESPONDER:.0f} × (p̂ × {WAVE2_RESPONSE_MULT:.2f}) − {MAIL_COST:.2f}</b>.</li>
  </ul>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()

# -----------------------------
# Plot 2: Cumulative profit
# -----------------------------
st.markdown("### Plot 2: Cumulative Expected Profit as More Customers Are Mailed (NN)")

p2 = (
    ggplot(df, aes(x="rank", y="cumulative_profit"))
    + geom_line()
    + (geom_vline(xintercept=cutoff_rank) if show_cutoff_line else 0)
    + labs(
        title="Cumulative Expected Profit as More Customers Are Mailed (NN)",
        x="Number of Customers (Sorted by Expected Profit)",
        y="Cumulative Expected Profit ($)",
    )
    + theme_minimal()
    + theme(figure_size=(10, 4))
)
st.pyplot(p2.draw(), clear_figure=True)

st.markdown(
    """
**Interpretation:**
Cumulative expected profit rises quickly for top-ranked customers, meaning those mailings add positive incremental profit.
As lower-ranked customers are included, the curve can flatten and eventually decline once incremental expected profits turn negative.
This provides a direct economic justification for selecting a cutoff rather than mailing the entire test set.
"""
)

# -----------------------------
# Download Wave-2 mailing list (id, mailto_wave2)
# -----------------------------
st.divider()
st.markdown("### Export: Wave-2 Mailing List")

if "id" not in df_pl.columns:
    st.error(
        "❌ The results file does not contain an 'id' column required for Wave-2 output."
    )
    st.write("Columns found:", df_pl.columns)
else:
    wave2 = (
        df_pl.select(["id", "rank"])
        .with_columns((pl.col("rank") <= pl.lit(cutoff_rank)).alias("mailto_wave2"))
        .select(["id", "mailto_wave2"])
    )

    st.caption(
        "Output format: exactly two columns (`id`, `mailto_wave2`). Customers not mailed remain with `mailto_wave2 = False`."
    )

    st.download_button(
        "Download Wave-2 mailing list (CSV)",
        data=wave2.write_csv(),
        file_name="wave2_mailing_list.csv",
        mime="text/csv",
    )
