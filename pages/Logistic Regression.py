import streamlit as st
import textwrap

st.set_page_config(
    page_title="Logistic Regression",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Shared style (match Section 2 visual language) ---
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


# ----------------------------
# Header + Metrics row
# ----------------------------
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
      <div>
        <div class="tag">🧱 Section 3</div>
        <div style="height:.45rem"></div>
        <h1>Logistic Regression: The Strategic Baseline</h1>
        <div class="subtle">A concise explanation for Product Managers with analytical rigor preserved.</div>
      </div>
    </div>
    <hr class="hr"/>
    """,
    unsafe_allow_html=True,
)

# Optionally show metrics (kept from original page)
AUC = 0.747
BREAKEVEN_PROB = 0.0235

m1, m2, _ = st.columns([1, 1, 2])
m1.metric("AUC", f"{AUC:.3f}")
m2.metric("Breakeven Probability", f"{BREAKEVEN_PROB * 100:.2f}%")

st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)

# ===========================
# Executive Summary (top) + Implementation notes (expandable)
# ===========================
st.markdown(
    """
    <div class="card" id="exec-summary-top">
      <div class="card-title">✅ <div>Executive Summary</div></div>
      <ul>
        <li><b>Transparent baseline:</b> Logistic Regression explains drivers and supports business interpretation</li>
        <li><b>Conservative planning:</b> 50% Wave-2 decay gives realistic financial forecasts</li>
        <li><b>Actionable signals:</b> Recency, spend, product ownership, and geography guide targeting</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Implementation notes", expanded=False):
    st.markdown(
        """
        If desired, we can include coefficient tables, odds ratios, and simple uplift slices
        for the recommended mailing cohort.

        These outputs make it straightforward to translate model insights into campaign rules
        and operational targeting logic.
        """
    )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)

# ===========================
# Main content (model description)
# ===========================
info_card(
    "1. Model Overview: Establishing a Baseline",
    """
    Before deploying complex machine learning algorithms, we established a <b>Logistic Regression</b> model. Think of this as our "foundation".<br><br>
    <b>Why we use it:</b> While complex models (like Neural Networks) are great at prediction, they can be "black boxes." Logistic Regression provides <b>transparency</b>.<br><br>
    <b>The Benefit:</b> It doesn't just tell us <i>who</i> will buy; it tells us <i>why</i> they are buying by identifying the specific customer attributes that drive the decision.
    """,
    icon="🔍",
)

info_card(
    "2. Realistic Financial Planning (The Wave-2 Adjustment)",
    """
    We trained our model on data from the first mailing (Wave-1), but we know that response rates typically drop in follow-up campaigns.<br><br>
    <b>The Adjustment:</b> We applied a <b>50% decay factor</b> to our predictions.<br><br>
    <b>The Business Logic:</b> Instead of being overly optimistic, we intentionally lowered our success probability estimates. This provides a <b>conservative financial forecast</b>, ensuring we only spend budget on customers who are likely to generate a profit even in a tougher market environment.
    """,
    icon="🔁",
)

info_card(
    "3. Key Business Drivers: What Predicts a Sale?",
    """
    Our analysis identified several behaviors that signal a customer is ready to upgrade. Below are the primary drivers identified as both statistically and economically meaningful:<br><br>
    <b>• Recency Matters (Time since last order):</b> Customers who purchased recently are much more likely to upgrade. The longer the gap since their last interaction, the lower their likelihood of buying.<br><br>
    <b>• High Value Customers (Historical Spend):</b> There is a direct link between total historical spending and the likelihood to upgrade. Customers who have spent more in the past are safer bets for this campaign.<br><br>
    <b>• Ecosystem Lock-in (Tax Software Users):</b> Customers who already own Intuit's <b>tax products</b> show strong loyalty and "lock-in" to the ecosystem. They are significantly more likely to purchase the QuickBooks upgrade.<br><br>
    <b>• Location Trends (Geographic Indicators):</b> Where the business is located matters. We found clear regional variations (based on Zip Code bins) that impact response behavior.
    """,
    icon="📊",
)

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)
st.caption("Logistic Regression")
