import streamlit as st
import textwrap

st.set_page_config(
    page_title="Targeting Strategy & Financial Impact",
    page_icon="💰",
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
# Key numbers (stars of the page)
# ----------------------------
RECOMMENDED_MAILS = 3489
PEAK_CUM_PROFIT = 14718
PROFIT_AT_CUTOFF = 14718

TEST_SET_SIZE = 22500
MAILING_DEPTH = RECOMMENDED_MAILS / TEST_SET_SIZE  # 15.5%

MAIL_COST = 1.41
MARGIN = 60
DECAY = 0.50
REWARD_WAVE2 = DECAY * MARGIN  # $30
BREAKEVEN = MAIL_COST / REWARD_WAVE2  # 4.7%

FULL_ELIGIBLE_POOL = 118000
FULL_RECOMMENDED = int(round(FULL_ELIGIBLE_POOL * MAILING_DEPTH))  # ~18,300

NOT_MAILED = FULL_ELIGIBLE_POOL - FULL_RECOMMENDED
AVOIDED_COST = NOT_MAILED * MAIL_COST  # should be > $140k


# ----------------------------
# Header + Metrics row
# ----------------------------
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
      <div>
        <div class="tag">💰 Section 6</div>
        <div style="height:.45rem"></div>
        <h1>Targeting Strategy &amp; Financial Impact: Precision at Scale</h1>
        <div class="subtle">
          The “stars” of this page are the exact cutoff and profit peak that prove the model is working:
          we mail the <b>3,489</b> customers that maximize profit at <b>$14,718</b>.
        </div>
      </div>
    </div>
    <hr class="hr"/>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
m1.metric("Recommended mails", f"{RECOMMENDED_MAILS:,}")
m2.metric("Peak cumulative profit", f"${PEAK_CUM_PROFIT:,.0f}")
m3.metric("Profit @ cutoff", f"${PROFIT_AT_CUTOFF:,.0f}")
m4.metric("Mailing depth", f"{MAILING_DEPTH * 100:.1f}%")

st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)

# ===========================
# Executive Summary + Implementation notes
# ===========================
st.markdown(
    f"""
    <div class="card" id="exec-summary-top">
      <div class="card-title">✅ <div>Executive Summary</div></div>
      <ul>
        <li><b>Proof the model works:</b> We don’t mail 15.5% randomly—we mail the exact <b>{RECOMMENDED_MAILS:,}</b> customers that maximize profit.</li>
        <li><b>Peak profit achieved:</b> Cumulative profit peaks at <b>${PEAK_CUM_PROFIT:,.0f}</b>, and we stop exactly at that point.</li>
        <li><b>Breakeven filter:</b> Any customer below <b>{BREAKEVEN * 100:.1f}%</b> purchase probability is automatically excluded.</li>
        <li><b>Rollout logic:</b> Scaling the same 15.5% strategy to <b>{FULL_ELIGIBLE_POOL:,}</b> yields ~<b>{FULL_RECOMMENDED:,}</b> targets while avoiding major wasted spend.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Implementation notes", expanded=False):
    st.markdown(
        f"""
        <div class="subtle">
          <b>Expected Profit rule:</b> (Probability of Buying × ${MARGIN}) − ${MAIL_COST}<br>
          <b>Wave-2 decay:</b> We conservatively adjust expected revenue by 50%, so reward becomes ${REWARD_WAVE2:.0f} per responder.<br>
          <b>Breakeven:</b> ${MAIL_COST:.2f} ÷ ${REWARD_WAVE2:.0f} = {BREAKEVEN * 100:.1f}%<br>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)

# ===========================
# Main content (your provided copy, formatted into cards)
# ===========================
info_card(
    "1. The Core Strategy: Profit Maximization Rule",
    f"""
    We moved beyond simple “response rates” to focus on the only metric that matters: <b>Net Profit</b>.
    We use a strict financial filter to ensure every marketing dollar is an investment, not an expense.
    <br><br>

    <ul>
      <li><b>The Decision Rule:</b> We only mail a customer if their <b>Expected Profit is greater than $0</b>.</li>
      <li><b>The Calculation:</b> For every customer, we calculate:<br>
        <code>(Probability of Buying × ${MARGIN}) − ${MAIL_COST} Mailing Cost</code>
      </li>
      <li><b>The Goal:</b> Find the “Sweet Spot” (the cutoff) where we stop mailing just before we start losing money on low-probability leads.</li>
    </ul>
    """,
    icon="💡",
)

info_card(
    "2. The Financial Threshold (Breakeven Analysis)",
    f"""
    To justify the <b>${MAIL_COST:.2f}</b> cost of a single mailer, a customer must meet a specific probability hurdle.
    <br><br>

    <ul>
      <li><b>The Cost:</b> ${MAIL_COST:.2f} per mailer.</li>
      <li><b>The Reward:</b> ${REWARD_WAVE2:.0f} expected revenue per responder (This is the ${MARGIN} margin adjusted for the 50% “Wave-2 decay”).</li>
      <li><b>The Breakeven Point:</b> <b>{BREAKEVEN * 100:.1f}%</b> (${MAIL_COST:.2f} ÷ ${REWARD_WAVE2:.0f}).</li>
      <li><b>Strategic Implication:</b> Our model identifies and automatically filters out any customer with a purchase probability below <b>{BREAKEVEN * 100:.1f}%</b>.</li>
    </ul>
    """,
    icon="🧮",
)

info_card(
    "3. Test Results: Proven Performance",
    f"""
    Before rolling out to the full database, we validated this strategy on our test group (the hold-out set).
    <br><br>

    <ul>
      <li><b>Recommended Mails:</b> <b>{RECOMMENDED_MAILS:,}</b> (the optimal number of high-priority leads).</li>
      <li><b>Mailing Depth:</b> <b>{MAILING_DEPTH * 100:.1f}%</b> (we only mail the top tier, saving costs on the remaining {(1 - MAILING_DEPTH) * 100:.1f}%).</li>
      <li><b>Peak Cumulative Profit:</b> <b>${PEAK_CUM_PROFIT:,.0f}</b> (the maximum profit achievable; mailing more would decrease this number).</li>
      <li><b>Profit @ Cutoff:</b> <b>${PROFIT_AT_CUTOFF:,.0f}</b> (confirming we stopped exactly at the most profitable point).</li>
    </ul>
    """,
    icon="🧾",
)

info_card(
    "4. Full-Scale Recommendation (Wave-2 Rollout)",
    f"""
    Applying this proven <b>{MAILING_DEPTH * 100:.1f}%</b> targeting logic to the entire eligible universe:
    <br><br>

    <ul>
      <li><b>Total Eligible Pool:</b> {FULL_ELIGIBLE_POOL:,} businesses.</li>
      <li><b>Recommended Target List:</b> <b>~{FULL_RECOMMENDED:,}</b> businesses (the top {MAILING_DEPTH * 100:.1f}%).</li>
      <li><b>Strategy:</b> By focusing our budget on these ~{FULL_RECOMMENDED:,} leads, we capture “peak profit” at scale while avoiding over <b>${AVOIDED_COST:,.0f}</b> in wasted mailing costs.</li>
    </ul>
    """,
    icon="🌍",
)

info_card(
    "Summary for Stakeholders",
    f"""
    Our targeting strategy ensures we don’t “over-mail.”
    By stopping at the <b>{RECOMMENDED_MAILS:,}</b> mark in our test ({MAILING_DEPTH * 100:.1f}% depth),
    we achieve the maximum profit of <b>${PEAK_CUM_PROFIT:,.0f}</b>.
    Scaling this {MAILING_DEPTH * 100:.1f}% approach to the full <b>{FULL_ELIGIBLE_POOL:,}</b> pool represents the most efficient use of Intuit’s marketing budget.
    """,
    icon="📣",
)

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)
st.caption("Targeting Strategy & Financial Impact")
