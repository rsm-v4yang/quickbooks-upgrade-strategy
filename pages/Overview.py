import streamlit as st
import textwrap  # <- 新增這行

st.set_page_config(
    page_title="Intuit QuickBooks Upgrade Strategy",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------- Premium card + warm background style ----------
st.markdown(
    textwrap.dedent("""
    <style>
      :root{
        /* ===== Color System ===== */
        --bg: #F4F1EA;
        --panel: #FFFFFF;
        --panel-2: #F7F5F0;
        --text: #121417;
        --muted: rgba(18,20,23,.68);
        --primary: #1F2937;
        --primary-2: #111827;
        --accent: #F4C84A;
        --accent-2: #EFBF3B;
        --border: rgba(17,24,39,.10);
        --shadow: 0 10px 30px rgba(17,24,39,.10);
        --shadow-soft: 0 6px 18px rgba(17,24,39,.08);
        --radius: 18px;
        --radius-sm: 14px;
      }
      html, body, [data-testid="stAppViewContainer"]{
        background: var(--bg) !important;
        color: var(--text);
        font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
      }
      .block-container{
        max-width: 1120px;
        padding-top: 2.2rem;
        padding-bottom: 3.0rem;
      }
      [data-testid="stSidebar"]{
        background: rgba(255,255,255,.70);
        backdrop-filter: blur(8px);
        border-right: 1px solid var(--border);
      }
      [data-testid="stSidebar"] .block-container{ padding-top: 1.4rem; }
      h1{ font-size: 2.1rem; letter-spacing: -0.03em; margin: 0; color: var(--primary-2); }
      h2{ font-size: 1.35rem; margin-top: 1.3rem; color: var(--primary-2); }
      h3{ font-size: 1.1rem; margin-top: 1.0rem; color: var(--primary); }
      p, li{ font-size: 1.0rem; line-height: 1.7; color: rgba(18,20,23,.84); }
      .card{ background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow-soft); padding: 1.25rem 1.35rem; }
      .card-title{ font-weight: 650; color: var(--primary-2); font-size: 0.95rem; letter-spacing: -0.01em; margin-bottom: .45rem; }
      .subtle{ color: var(--muted); font-size: 0.95rem; line-height: 1.55; }
      .header{ padding: 1.35rem 1.45rem; border-radius: 24px; background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.82)); border: 1px solid rgba(17,24,39,.10); box-shadow: var(--shadow); }
      .pill{ display:inline-flex; align-items:center; gap:.5rem; padding:.42rem .7rem; border-radius: 999px; background: rgba(244,200,74,.22); border: 1px solid rgba(244,200,74,.40); color: rgba(17,24,39,.85); font-size:.85rem; font-weight: 600; }
      .kpi{ padding: 1rem 1.1rem; }
      .kpi .num{ font-size: 1.55rem; font-weight: 800; letter-spacing: -0.03em; color: var(--primary-2); margin-top: .15rem; }
      .kpi .delta{ font-size: .9rem; color: rgba(17,24,39,.70); }
      .dot{ width:10px; height:10px; border-radius:50%; background: var(--accent); display:inline-block; box-shadow: 0 0 0 6px rgba(244,200,74,.20); }
      .hr{ height: 1px; background: rgba(17,24,39,.10); border: 0; margin: 1.25rem 0; }
      [data-testid="stDataFrame"]{ border: 1px solid var(--border); border-radius: var(--radius-sm); overflow: hidden; box-shadow: var(--shadow-soft); background: var(--panel); }
      [data-testid="stVerticalBlock"] > div:first-child { padding-top: 0rem; }
    </style>
    """).strip(),
    unsafe_allow_html=True,
)

# Header block (use dedent as well)
st.markdown(
    textwrap.dedent("""
    <div class="header">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
        <div>
          <div class="pill"><span class="dot"></span> Strategy Report</div>
          <div style="height:.55rem"></div>
          <h1>Case 03: Intuit QuickBooks Upgrade Strategy</h1>
          <div class="subtle">Next-Gen Targeting Intelligence for Direct Marketing Optimization</div>
          <div class="subtle" style="margin-top:.35rem; font-size:.88rem;">
            <b>Group 45</b> | Team: Jing Yin, FanCheng Xia, Vivian Yang
          </div>
        </div>
        <div style="display:flex; gap:.6rem; align-items:center;">
          <div class="pill" style="background: rgba(31,41,55,0.10); border-color: rgba(31,41,55,0.18);">Primary: Deep Slate</div>
          <div class="pill">Accent: Warm Yellow</div>
        </div>
      </div>
    </div>
    <hr class="hr"/>
    """).strip(),
    unsafe_allow_html=True,
)
# ===== Executive Summary card =====
# ===== Executive Summary card (REVISED) =====
st.markdown(
    """
    <div class="card">
      <h3 style="margin-top:0;">1. Executive Summary</h3>

      <p>
        We built a <b>model-driven targeting strategy</b> for Intuit’s <b>Wave-2 direct mailing campaign</b>
        to promote the QuickBooks v3.0 upgrade. Instead of mailing everyone, we score each customer’s
        likelihood of responding and <b>mail only when the expected profit is positive</b>.
      </p>

      <p>
        Because Wave-2 is expected to have <b>~50% lower response</b> than Wave-1, we apply a conservative adjustment
        before making decisions. We estimate profit using the course assumptions:
        <b>$60 margin per responder</b> and <b>$1.41 cost per mail</b>.
      </p>

      <p>
        Our best-performing model (<b>Neural Network / MLP</b>) recommends mailing to the top <b>15.5%</b> of remaining non-responders.
        When scaled to the full eligible population, this approach is projected to generate
        <b>over $475,000</b> in incremental profit.
      </p>

      <div class="subtle" style="margin-top:.45rem;">
        <b>Decision rule:</b> Mail a customer only if <b>Expected Profit = 60 × (Adjusted Response Probability) − 1.41 &gt; 0</b>.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ===== Business Problem & Objective card (REVISED) =====
st.markdown(
    """
    <div class="card" style="margin-top:1.2rem;">
      <h3 style="margin-top:0;">2. Business Problem & Objective</h3>

      <p><b>Business Problem:</b><br/>
        After the Wave-1 campaign, Intuit still has <b>763,334 non-responding customers</b> who may upgrade to QuickBooks v3.0.
        Wave-2 is an opportunity to convert these customers, but mailing has a direct cost.
      </p>

      <p><b>Key Challenge:</b><br/>
        Each Wave-2 mail piece costs <b>$1.41</b>, and the Wave-2 response rate is expected to be about <b>50% lower</b> than Wave-1.
        A blanket mailing strategy would therefore include many customers with <b>negative expected returns</b>.
      </p>

      <p><b>Objective:</b><br/>
        Build a classification model that identifies customers to mail in Wave-2. We mail only when:
        <b>Expected Profit = 60 × (Adjusted Response Probability) − 1.41 &gt; 0</b>.
        This ensures each mailed customer has <b>positive expected incremental profit</b>, and total campaign profit is maximized.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)
