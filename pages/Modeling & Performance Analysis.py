import streamlit as st
import textwrap

st.set_page_config(
    page_title="Modeling & Performance Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Shared style (match your Section 2 / Section 3 visual language) ---
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

      /* Make the expander content look more like a card when opened */
      .stExpander > button {
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
      }
    </style>
    """
    ).strip(),
    unsafe_allow_html=True,
)


def info_card(title: str, body_html: str, icon: str = "📌"):
    body_html = textwrap.dedent(body_html).strip()
    st.markdown(
        f"""
        <div class="card">
          <div class="card-title">{icon} <div>{title}</div></div>
          <div>{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------
# Numbers (UPDATED)
# ----------------------------
AUC_LR = 0.7470
BREAKEVEN_PROB = 0.0235

PROFIT_LR = 7129.78
PROFIT_MLP = 14718
LIFT_MLP = 3.74

# User correction
MAIL_LR = 0.289  # 28.9%
MAIL_MLP = 0.155  # 15.5%


# ----------------------------
# Header + Metrics row (match your template)
# ----------------------------
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
      <div>
        <div class="tag">🥊 Section 5</div>
        <div style="height:.45rem"></div>
        <h1>Modeling &amp; Performance Analysis: The Showdown</h1>
        <div class="subtle">
          We didn’t rely on just one method. We set up a competition between a standard industry baseline
          and an advanced AI model to see which one actually drives more revenue.
        </div>
      </div>
    </div>
    <hr class="hr"/>
    """,
    unsafe_allow_html=True,
)

# Metrics row (keep same visual behavior as your LR page)
m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
m1.metric("AUC (LR)", f"{AUC_LR:.4f}")
m2.metric("Top-Decile Lift (MLP)", f"{LIFT_MLP:.2f}")
m3.metric("Profit (LR)", f"${PROFIT_LR:,.2f}")
m4.metric("Profit (MLP)", f"~${PROFIT_MLP:,.0f}")

st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)

# ===========================
# Executive Summary (top) + Implementation notes (expandable)
# ===========================
st.markdown(
    f"""
    <div class="card" id="exec-summary-top">
      <div class="card-title">✅ <div>Executive Summary</div></div>
      <ul>
        <li><b>Baseline vs Challenger:</b> Logistic Regression provides a reliable benchmark; MLP tests whether advanced patterns drive more revenue.</li>
        <li><b>Profit verdict:</b> LR delivers <b>${PROFIT_LR:,.2f}</b>, while MLP delivers <b>~${PROFIT_MLP:,.0f}</b> — a clear <b>profit multiplier</b>.</li>
        <li><b>Why MLP wins:</b> Top-decile concentration (Lift <b>{LIFT_MLP:.2f}</b>) creates precision targeting that drives the profit gap.</li>
        <li><b>Diminishing returns:</b> Mailing deeper doesn’t guarantee profit; we stop when stamp cost (<b>$1.41</b>) exceeds expected return.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Implementation notes", expanded=False):
    st.markdown(
        f"""
        <div class="subtle">
          <b>Wave-2 adjustment:</b> p_wave2 = p_wave1 × 0.5<br>
          <b>Breakeven threshold:</b> p* = 1.41 / 60 ≈ {(BREAKEVEN_PROB * 100):.2f}%<br>
          <b>Mailing depth:</b> LR {(MAIL_LR * 100):.1f}% vs MLP {(MAIL_MLP * 100):.1f}%<br>
          <b>Expected profit per customer:</b> (p_wave2 × 60) − 1.41
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)

# ===========================
# Main content (YOUR exact showdown text, structured)
# ===========================
info_card(
    "1. The Head-to-Head Strategy",
    """
    We didn't rely on just one method. We set up a competition between a standard industry baseline and an advanced AI model to see which one actually drives more revenue.

    <ul>
      <li><b>The Baseline:</b> Logistic Regression (Standard statistical modeling).</li>
      <li><b>The Challenger:</b> Neural Network / MLP (Advanced pattern recognition).</li>
    </ul>
    """,
    icon="🥊",
)

info_card(
    "2. The Verdict: Profitability (The Bottom Line)",
    f"""
    This is the most critical finding for the Product Manager. While the Logistic Regression model is "good," the Neural Network is a <b>profit multiplier</b>.

    <ul>
      <li>
        <b>Logistic Regression Profit:</b> <b>${PROFIT_LR:,.2f}</b><br>
        <i>Performance:</i> It identifies a profitable group, but it misses subtler patterns, leaving money on the table.
      </li>
      <li style="margin-top:.65rem;">
        <b>Neural Network Profit:</b> <b>~${PROFIT_MLP:,.0f}</b><br>
        <i>Performance:</i> By capturing complex customer behaviors, the Neural Network <b>doubles</b> the expected profit compared to the baseline.
      </li>
    </ul>
    """,
    icon="💰",
)

info_card(
    "3. Why the Difference? (Understanding the Metrics)",
    f"""
    To understand <i>why</i> the Neural Network won, we look at two key metrics:

    <ul>
      <li>
        <b>Discrimination (AUC):</b><br>
        <i>What it is:</i> A general measure of how well the model separates "buyers" from "non-buyers."<br>
        <i>Result:</i> The Logistic Regression had a decent score (AUC <b>{AUC_LR:.4f}</b>), proving it <i>works</i>. However, accuracy alone doesn't guarantee the highest profit.
      </li>

      <li style="margin-top:.75rem;">
        <b>Efficiency (Lift):</b><br>
        <i>What it is:</i> How good is the model at putting the absolute best customers at the very top of the list?<br>
        <i>Result:</i> The Neural Network achieved a <b>Top-Decile Lift of {LIFT_MLP:.2f}</b>.
        This means when we target the top 10% of our list, we are nearly <b>4× more likely</b> to find a buyer than if we mailed randomly.
        This "precision targeting" is what drives the massive profit gap.
      </li>
    </ul>
    """,
    icon="📈",
)

info_card(
    '4. The "Diminishing Returns" Reality (From your Data)',
    """
    Your analysis of the Logistic Regression mailing depths (5% to 100%) reveals a crucial business lesson:
    <b>More volume does not mean more profit.</b>

    <ul>
      <li>As shown in your data, mailing 100% of the list actually leads to a <b>loss</b> (-$1,751).</li>
      <li>The models allow us to stop mailing exactly when the cost of the stamp (<b>$1.41</b>) outweighs the expected return, ensuring every dollar spent is an <b>investment</b>, not an expense.</li>
    </ul>
    """,
    icon="📉",
)

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)
st.caption("Section 4 — Modeling & Performance Analysis")
