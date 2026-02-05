import streamlit as st
import textwrap

st.set_page_config(
    page_title="Data Engineering & Feature Selection",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Keep style unified with Overview (but no big hero header) ---
st.markdown(
    textwrap.dedent(
        """
    <style>
      :root{
        --bg: #F4F1EA;
        --panel: #FFFFFF;
        --panel-2: #F7F5F0;
        --text: #121417;
        --muted: rgba(18,20,23,.68);
        --primary: #1F2937;
        --primary-2: #111827;
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

      h1{ font-size: 1.85rem; letter-spacing: -0.03em; margin: 0; color: var(--primary-2); }
      h2{ font-size: 1.25rem; margin-top: 1.25rem; color: var(--primary-2); }
      h3{ font-size: 1.05rem; margin-top: 0.9rem; color: var(--primary); }
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
        color: var(--primary-2);
        font-size: 0.98rem;
        letter-spacing: -0.01em;
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
# Page content (your revised copy) — now Section 2
# ----------------------------
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
      <div>
        <div class="tag">🗂️ Section 2</div>
        <div style="height:.55rem"></div>
        <h1>Data Engineering & Feature Selection: Building a Strong Foundation</h1>
        <div class="subtle">Professional terminology + plain English, optimized for both Data Science and Product stakeholders.</div>
      </div>
    </div>
    <hr class="hr"/>
    """,
    unsafe_allow_html=True,
)

# Overview card
info_card(
    "Overview",
    """
    We didn't just feed raw data into the computer; we built a rigorous process to clean and organize it.
    Because the performance of advanced models (like Neural Networks) depends entirely on the quality of the input,
    we transformed the raw customer data into a format that allows our model to easily spot complex patterns.
    """,
    icon="🧭",
)

left, right = st.columns([1.7, 1])

with left:
    info_card(
        "1. Ensuring Logical Consistency (Saving Money)",
        """
        <b>The Action:</b> We automatically identified and removed customers who had already responded to the first campaign (Wave-1).<br><br>
        <b>The Business Value:</b> This prevents “double-dipping.” We ensure we aren't wasting the marketing budget on people who have already upgraded.
        """,
        icon="💸",
    )

    info_card(
        "2. Smart Handling of Missing Numbers (Median Imputation)",
        """
        <b>The Action:</b> For missing numerical data—such as <code>numords</code> (number of orders) or <code>dollars</code> (total spend)—
        we filled in the blanks using the <i>median</i> value rather than the <i>average</i>.<br><br>
        <b>The “Why”:</b> Averages can be skewed by a few “whales” (customers who spend huge amounts).
        Using the median ensures our model learns from the behavior of the <i>typical</i> small business owner,
        rather than being confused by extreme outliers.
        """,
        icon="🧮",
    )

    info_card(
        "3. Preserving Customer Records (Categorical Handling)",
        """
        <b>The Action:</b> When demographic information (like <code>sex</code>) was missing, we didn't delete the customer.
        Instead, we created a specific category called <b>“Unknown”</b>.<br><br>
        <b>The Benefit:</b> This keeps our dataset large and complete. It also allows the model to analyze whether the very act of
        <i>not</i> providing information is, in itself, a predictor of whether they will buy.
        """,
        icon="🧾",
    )

    info_card(
        "4. High-Performance Tools",
        """
        <b>The Tech:</b> We utilized the <code>polars</code> library for data manipulation.
        This ensures that our data processing is fast, consistent, and capable of handling complex logical checks
        across all 75,000 records without error.
        """,
        icon="⚙️",
    )

with right:
    info_card(
        "Quick Summary",
        """
        <ul>
          <li><b>Spend less:</b> exclude Wave-1 responders from Wave-2 targeting</li>
          <li><b>Learn better:</b> median imputation avoids outlier distortion</li>
          <li><b>Keep signal:</b> “Unknown” preserves records + captures missingness patterns</li>
          <li><b>Run fast:</b> polars supports scalable processing at 75k rows</li>
        </ul>
        """,
        icon="✅",
    )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)
st.caption("Section 2 — Data Engineering & Feature Selection")
