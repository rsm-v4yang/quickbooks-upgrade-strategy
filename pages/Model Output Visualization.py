import os
import streamlit as st
import textwrap
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
    element_text,
)

st.set_page_config(
    page_title="Model Output Visualization (NN)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Shared style (match Section 2/3 visual language) ---
st.markdown(
    textwrap.dedent(
        """
    <style>
      :root{
        --bg: #F4F1EA;
        --panel: #FFFFFF;
        --text: #121417;
        --muted: rgba(18,20,23,.68);
        --primary: #1F2937;
        --accent: #F4C84A;
        --border: rgba(17,24,39,.10);
        --shadow-soft: 0 6px 18px rgba(17,24,39,.08);
        --radius: 18px;
      }

      html, body, [data-testid="stAppViewContainer"]{
        background: var(--bg) !important;
        color: var(--text);
        font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
      }

      .block-container{
        max-width: 1120px;
        padding-top: 1.7rem;
        padding-bottom: 2.8rem;
      }

      [data-testid="stSidebar"]{
        background: rgba(255,255,255,.70);
        backdrop-filter: blur(8px);
        border-right: 1px solid var(--border);
      }

      h1{ font-size: 1.85rem; letter-spacing: -0.03em; margin: 0; color: var(--primary); }
      p, li{ font-size: 1.0rem; line-height: 1.7; color: rgba(18,20,23,.84); }

      .card{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow-soft);
        padding: 1.15rem 1.25rem;
        margin-bottom: .9rem;
      }

      .card-title{
        font-weight: 800;
        color: var(--primary);
        font-size: 0.98rem;
        margin-bottom: .45rem;
        display:flex;
        gap:.55rem;
        align-items:flex-start;
      }

      .tag{
        display:inline-flex;
        align-items:center;
        gap:.5rem;
        padding:.35rem .65rem;
        border-radius: 999px;
        background: rgba(244,200,74,.22);
        border: 1px solid rgba(244,200,74,.40);
        color: rgba(17,24,39,.85);
        font-size:.82rem;
        font-weight: 700;
      }

      .subtle{
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.55;
      }

      .hr{
        height: 1px;
        background: rgba(17,24,39,.10);
        border: 0;
        margin: 1.15rem 0;
      }

      code{
        background: rgba(17,24,39,.06);
        padding: .12rem .35rem;
        border-radius: .45rem;
        border: 1px solid rgba(17,24,39,.08);
        font-size: .92em;
      }

      .stExpander > button {
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
      }
    </style>
    """
    ).strip(),
    unsafe_allow_html=True,
)


def info_card(title: str, body_md: str, icon: str = "📌"):
    body_md = textwrap.dedent(body_md).strip()
    st.markdown(
        f"""
        <div class="card">
          <div class="card-title">{icon} <div>{title}</div></div>
          <div>{body_md}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Course defaults (Report mode)
# ============================================================
COURSE_MAIL_COST = 1.41
COURSE_MARGIN = 60.0
COURSE_MULT = 0.50
COURSE_RULE = "Mail while Expected Profit > 0"


# ============================================================
# Sidebar controls
# ============================================================
st.sidebar.header("Controls")

mode = st.sidebar.radio(
    "Mode",
    ["Report (course defaults)", "Sensitivity (interactive)"],
    index=0,
    help="Report mode locks course-default assumptions so slide/submission numbers stay consistent.",
)
lock = mode == "Report (course defaults)"

st.sidebar.subheader("Data")
uploaded_csv = st.sidebar.file_uploader(
    "Upload NN results CSV (optional)",
    type=["csv"],
    help="If uploaded, this file is used instead of data/person2_nn_mailable_ranked.csv",
)

st.sidebar.divider()
st.sidebar.subheader("Assumptions")

MAIL_COST = st.sidebar.number_input(
    "Mail cost ($/piece)",
    value=COURSE_MAIL_COST,
    step=0.01,
    format="%.2f",
    disabled=lock,
    key="mail_cost",
)
MARGIN_PER_RESPONDER = st.sidebar.number_input(
    "Margin per responder ($)",
    value=COURSE_MARGIN,
    step=1.0,
    format="%.0f",
    disabled=lock,
    key="margin",
)
WAVE2_RESPONSE_MULT = st.sidebar.slider(
    "Wave-2 response multiplier",
    min_value=0.10,
    max_value=1.00,
    value=COURSE_MULT,
    step=0.05,
    disabled=lock,
    key="mult",
)

st.sidebar.subheader("Cutoff rule")
cutoff_rule = st.sidebar.radio(
    "Cutoff rule",
    options=[
        "Mail while Expected Profit > 0",
        "Mail until Peak Cumulative Profit",
        "Mail Top-N customers",
    ],
    index=0,
    disabled=lock,
)

top_n = None
if cutoff_rule == "Mail Top-N customers":
    top_n = st.sidebar.slider(
        "Top N to mail", min_value=100, max_value=22500, value=3500, step=100
    )

show_cutoff_line = st.sidebar.checkbox("Show cutoff line on charts", value=True)

# Force report defaults if locked
if lock:
    MAIL_COST = COURSE_MAIL_COST
    MARGIN_PER_RESPONDER = COURSE_MARGIN
    WAVE2_RESPONSE_MULT = COURSE_MULT
    cutoff_rule = COURSE_RULE

# Helper banner (this is the thing you問的藍色提示)
if lock:
    st.info(
        "Report mode uses course-default assumptions for consistent slide/submission numbers. "
        "Switch to Sensitivity mode to explore how the recommendation changes under different assumptions."
    )


# ============================================================
# Header
# ============================================================
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
      <div>
        <div class="tag">📈 Section 7</div>
        <div style="height:.45rem"></div>
        <h1>Model Output Visualization (Neural Network)</h1>
        <div class="subtle">Turning NN scores into a profit-based Wave-2 mailing decision.</div>
      </div>
    </div>
    <hr class="hr"/>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Load CSV (polars)
# ============================================================
@st.cache_data
def load_nn_results(uploaded_bytes: bytes | None) -> pl.DataFrame:
    if uploaded_bytes is not None:
        return pl.read_csv(uploaded_bytes)

    base_dir = os.path.dirname(os.path.dirname(__file__))  # app.py level
    csv_path = os.path.join(base_dir, "data", "person2_nn_mailable_ranked.csv")

    if not os.path.exists(csv_path):
        st.error(f"File not found: {csv_path}")
        st.stop()

    return pl.read_csv(csv_path)


def compute_profit_table(df_raw: pl.DataFrame, lock_report: bool) -> pl.DataFrame:
    """
    - Report mode (lock_report=True): prefer CSV expected_profit_nn if present (consistency).
    - Sensitivity mode: recompute expected_profit_nn from probability if possible (so charts move).
    """
    df = df_raw

    # Find a probability column (so we can recompute EP in Sensitivity mode)
    prob_candidates = [
        "p_wave2_nn",
        "p_wave2",
        "pred_prob_wave2_nn",
        "pred_prob_nn",
        "predicted_prob_nn",
        "prob",
        "proba",
    ]
    prob_col = next((c for c in prob_candidates if c in df.columns), None)

    if lock_report:
        # Keep slide/submission consistent
        if "expected_profit_nn" in df.columns:
            df = df.with_columns(pl.col("expected_profit_nn").cast(pl.Float64))
        else:
            # If file doesn't have EP, compute once using defaults
            if prob_col is None:
                st.error(
                    "Report mode requires either 'expected_profit_nn' or a probability column."
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
        # Sensitivity mode: recompute EP so the chart updates when sliders change
        if prob_col is None:
            # Can't move without probability; fall back but warn
            if "expected_profit_nn" not in df.columns:
                st.error("Sensitivity mode needs a probability column to recompute EP.")
                st.write("Columns found:", df.columns)
                st.stop()
            st.warning(
                "No probability column found, so expected_profit_nn cannot be recomputed. "
                "Charts will not respond to assumption changes unless your CSV includes p̂ (probability)."
            )
            df = df.with_columns(pl.col("expected_profit_nn").cast(pl.Float64))
        else:
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


df_raw = load_nn_results(uploaded_csv.getvalue() if uploaded_csv else None)
df_pl = compute_profit_table(df_raw, lock_report=lock)
df = df_pl.to_pandas()


# ============================================================
# Cutoff + KPIs
# ============================================================
# EP>0 cutoff should EXCLUDE first non-positive row
if (df["expected_profit_nn"] <= 0).any():
    first_nonpos_rank = int(df.loc[df["expected_profit_nn"] <= 0, "rank"].iloc[0])
    profit_cutoff_rank = max(1, first_nonpos_rank - 1)
else:
    profit_cutoff_rank = int(df["rank"].max())

peak_idx = int(df["cumulative_profit"].idxmax())
peak_rank = int(df.loc[peak_idx, "rank"])
peak_profit = float(df.loc[peak_idx, "cumulative_profit"])

if cutoff_rule == "Mail while Expected Profit > 0":
    cutoff_rank = profit_cutoff_rank
elif cutoff_rule == "Mail until Peak Cumulative Profit":
    cutoff_rank = peak_rank
else:
    cutoff_rank = int(top_n)

profit_at_cutoff = float(df.loc[df["rank"] == cutoff_rank, "cumulative_profit"].iloc[0])

m1, m2, m3 = st.columns([1, 1, 1])
m1.metric("Recommended mails", f"{cutoff_rank:,}")
m2.metric("Profit @ cutoff", f"${profit_at_cutoff:,.0f}")
m3.metric("Peak cumulative profit", f"${peak_profit:,.0f}")

st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)


# ============================================================
# Explanation cards
# ============================================================
info_card(
    "1. What these charts show",
    f"""
    We rank customers by expected profit and visualize:
    <ul>
      <li><b>Expected Profit by rank</b>: incremental profit per additional customer mailed.</li>
      <li><b>Cumulative Expected Profit</b>: total profit as mailing depth increases.</li>
    </ul>
    Expected Profit:
    <br><br>
    <code>EP = {MARGIN_PER_RESPONDER:.0f} × (p̂ × {WAVE2_RESPONSE_MULT:.2f}) − {MAIL_COST:.2f}</code>
    """,
    icon="📌",
)

info_card(
    "2. Interpreting the profit peak (the “sweet spot”)",
    f"""
    The cumulative curve rises fast for top-ranked customers and then flattens.
    The <b>peak</b> is the depth that maximizes total profit.
    <br><br>
    <b>Peak at:</b> rank <b>{peak_rank:,}</b>, cumulative profit <b>${peak_profit:,.0f}</b>.
    """,
    icon="🏔️",
)

info_card(
    "3. Wave-2 decision rule",
    f"""
    Selected rule: <b>{cutoff_rule}</b>.
    <br><br>
    Recommended mailing depth: <b>{cutoff_rank:,}</b>.
    Profit at cutoff: <b>${profit_at_cutoff:,.0f}</b>.
    """,
    icon="🧭",
)

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)


# ============================================================
# Charts (smaller + centered column so it doesn't stretch)
# ============================================================
st.markdown("### Plot 1: Expected Profit by Rank")

left, mid, right = st.columns([1, 2, 1])  # put chart in middle column (narrower)
with mid:
    p1 = (
        ggplot(df, aes(x="rank", y="expected_profit_nn"))
        + geom_line()
        + geom_hline(yintercept=0)
        + (geom_vline(xintercept=cutoff_rank) if show_cutoff_line else 0)
        + labs(
            title="Expected Profit by Customer Rank (NN)",
            x="Rank (higher EP first)",
            y="Expected Profit ($)",
        )
        + theme_minimal()
        + theme(
            figure_size=(3.6, 3.1),  # ✅ smaller
            text=element_text(size=8),  # ✅ smaller font
        )
    )
    st.pyplot(p1.draw(), clear_figure=True, use_container_width=False)

st.markdown("### Plot 2: Cumulative Expected Profit")

left2, mid2, right2 = st.columns([1, 2, 1])
with mid2:
    p2 = (
        ggplot(df, aes(x="rank", y="cumulative_profit"))
        + geom_line()
        + (geom_vline(xintercept=cutoff_rank) if show_cutoff_line else 0)
        + labs(
            title="Cumulative Expected Profit vs Mailing Depth (NN)",
            x="Customers mailed (by EP rank)",
            y="Cumulative Expected Profit ($)",
        )
        + theme_minimal()
        + theme(
            figure_size=(3.6, 3.1),  # ✅ smaller
            text=element_text(size=8),  # ✅ smaller font
        )
    )
    st.pyplot(p2.draw(), clear_figure=True, use_container_width=False)

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)


# ============================================================
# Export
# ============================================================
st.markdown("### Export: Wave-2 Mailing List")

if "id" not in df_pl.columns:
    st.error("The results file must contain an 'id' column.")
    st.write("Columns found:", df_pl.columns)
    st.stop()

wave2 = (
    df_pl.select(["id", "rank"])
    .with_columns((pl.col("rank") <= pl.lit(cutoff_rank)).alias("mailto_wave2"))
    .select(["id", "mailto_wave2"])
)

st.caption("Output format: exactly two columns (`id`, `mailto_wave2`).")

st.download_button(
    "Download Wave-2 mailing list (CSV)",
    data=wave2.write_csv(),
    file_name="wave2_mailing_list.csv",
    mime="text/csv",
)
