import streamlit as st
import textwrap

st.set_page_config(
    page_title="Strategic Recommendations",
    page_icon="🧭",
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
        <div class="tag">🏁 Section 8</div>
        <div style="height:.45rem"></div>
        <h1>Strategic Recommendations: Maximizing Wave-2 ROI</h1>
        <div class="subtle">Turning model performance into a capital-efficient Wave-2 execution plan.</div>
      </div>
    </div>
    <hr class="hr"/>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Optional metrics (kept consistent with your style)
# ----------------------------
TEST_SET_N = 22500
FULL_POOL_N = 118000

TARGET_DEPTH = 0.4180888888888889
RECOMMENDED_MAILS_TEST = 9407
PEAK_PROFIT_TEST = 18042.79399152022

MAIL_COST = 1.41
PROJECTED_MAILS_FULL = int(round(FULL_POOL_N * TARGET_DEPTH))
SAVINGS_FULL = (FULL_POOL_N - PROJECTED_MAILS_FULL) * MAIL_COST

m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
m1.metric("Test set size", f"{TEST_SET_N:,}")
m2.metric("Target depth", f"{TARGET_DEPTH * 100:.1f}%")
m3.metric("Recommended mails", f"{RECOMMENDED_MAILS_TEST:,}")
m4.metric("Peak profit (test)", f"${PEAK_PROFIT_TEST:,.0f}")

st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)

# ===========================
# Executive Summary (top) + Implementation notes (expandable)
# ===========================
st.markdown(
    f"""
    <div class="card" id="exec-summary-top">
      <div class="card-title">✅ <div>Executive Summary</div></div>
      <ul>
        <li><b>Deploy MLP (Neural Network):</b> Best at concentrating the most profitable responders at the top of the list.</li>
        <li><b>Stop at the profit peak:</b> Mail only the top <b>{TARGET_DEPTH * 100:.1f}%</b> of customers (≈ <b>{RECOMMENDED_MAILS_TEST:,}</b> in the test set).</li>
        <li><b>Scale efficiently:</b> Apply the same threshold to <b>{FULL_POOL_N:,}</b> eligible customers (≈ <b>{PROJECTED_MAILS_FULL:,}</b> mailings).</li>
        <li><b>Business outcome:</b> Maintain high ROI while avoiding low-probability spend (≈ <b>${SAVINGS_FULL:,.0f}</b> savings vs full-pool blast).</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Implementation notes", expanded=False):
    st.markdown(
        f"""
        **How to operationalize this on Wave-2:**
        1) Score customers with the MLP model and rank them by expected profit.
        2) Select the top **{TARGET_DEPTH * 100:.1f}%** as the mailing cohort.
        3) Treat the remainder as **do-not-mail** to prevent negative incremental ROI.

        **Why the cutoff is defensible:** after the peak, incremental expected profit drops below mailing cost,
        creating diminishing returns and eventually reducing total campaign profitability.
        """
    )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)

# ===========================
# Main content (Recommendations)
# ===========================
info_card(
    "1. Immediate Deployment: The Neural Network Model",
    f"""
    <b>Recommendation:</b> Use the <b>Multi-Layer Perceptron (MLP)</b> model to select the Wave-2 mailing list.<br><br>
    <b>Why:</b> Our analysis shows the MLP is markedly better at “identifying the needle in the haystack.”
    By capturing complex, non-linear customer behaviors, it generated <b>${PEAK_PROFIT_TEST:,.0f}</b> profit in the test set—<b>more than double</b>
    the Logistic Regression baseline. This is not about maximizing response volume; it is about maximizing <b>profit per mailed customer</b>.
    """,
    icon="🚀",
)

info_card(
    "2. Optimal Targeting Depth (The 15.5% Rule)",
    f"""
    <b>Recommendation:</b> Set the mailing cutoff at the <b>{TARGET_DEPTH * 100:.1f}% depth</b> (top-tier prospects).<br><br>
    <b>The logic:</b> In the test group of <b>{TEST_SET_N:,}</b>, this corresponds to <b>{RECOMMENDED_MAILS_TEST:,}</b> recommended mailings.<br><br>
    <b>Why we stop here:</b> Beyond this point, we see <b>diminishing returns</b>—the expected incremental revenue falls below the mailing cost (e.g., <code>$1.41</code>),
    meaning additional mailings start to reduce total profit. Stopping at the peak ensures <b>no budget is wasted</b> on low-probability prospects.
    """,
    icon="🎯",
)

info_card(
    "3. Full-Scale Rollout Strategy",
    f"""
    <b>Recommendation:</b> Apply the <b>{TARGET_DEPTH * 100:.1f}% threshold</b> to the entire eligible Wave-2 universe of <b>{FULL_POOL_N:,}</b> businesses.<br><br>
    <b>Projected scale:</b> Target approximately <b>{PROJECTED_MAILS_FULL:,}</b> high-value leads.<br><br>
    <b>Business impact:</b> This focused plan captures the majority of potential upgrades while avoiding low-yield mailings—saving
    <b>over ${SAVINGS_FULL:,.0f}</b> in unnecessary mailing and operational costs compared to a full-pool blast.
    """,
    icon="📦",
)

info_card(
    "4. Future Roadmap: Data-Driven Personalization",
    """
    <b>Leverage key drivers:</b> The strongest predictors of an upgrade are <b>Recency</b> (how recently a customer purchased)
    and <b>Ecosystem lock-in</b> (owning Intuit tax products).<br><br>
    <b>Next steps:</b> Future campaigns should test <b>product bundling</b> and personalized messaging for customers who own tax products
    but have not upgraded their QuickBooks version. This can increase response rate and potentially lower the breakeven threshold,
    further improving ROI.
    """,
    icon="🧠",
)

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)

# ===========================
# Executive Takeaway (Boss quote)
# ===========================
st.markdown(
    f"""
    <div class="card">
      <div class="card-title">🧾 <div>Executive Takeaway</div></div>
      <div class="subtle" style="font-size:1.0rem; line-height:1.7; color: rgba(18,20,23,.84);">
        “By shifting from a traditional mailing approach to an AI-driven targeting strategy, we achieve a peak profit of
        <b>${PEAK_PROFIT_TEST:,.0f}</b> in the test phase alone. Scaling this to the full <b>{FULL_POOL_N:,}</b> pool by targeting only the most
        profitable <b>{TARGET_DEPTH * 100:.1f}%</b> ensures we maximize revenue while maintaining the highest possible marketing efficiency.”
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Section 6 — Strategic Recommendations")
