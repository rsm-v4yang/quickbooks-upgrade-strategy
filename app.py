import streamlit as st
import textwrap

st.set_page_config(
    page_title="Intuit QuickBooks Upgrade Strategy",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------- Global CSS (keep here) ----------
st.markdown(
    textwrap.dedent("""
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
        -webkit-backdrop-filter: blur(8px);
        border-right: 1px solid var(--border);
      }
      [data-testid="stSidebar"] .block-container{ padding-top: 1.4rem; }
      h1{ font-size: 2.1rem; letter-spacing: -0.03em; margin: 0; color: var(--primary-2); }
      h2{ font-size: 1.35rem; margin-top: 1.3rem; color: var(--primary-2); }
      h3{ font-size: 1.1rem; margin-top: 1.0rem; color: var(--primary); }
      p, li{ font-size: 1.0rem; line-height: 1.7; color: rgba(18,20,23,.84); }
      .card{ background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); box-shadow: var(--shadow-soft); padding: 1.25rem 1.35rem; }
      .subtle{ color: var(--muted); font-size: 0.95rem; line-height: 1.55; }
      .header{ padding: 1.35rem 1.45rem; border-radius: 24px; background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.82)); border: 1px solid rgba(17,24,39,.10); box-shadow: var(--shadow); }
      .pill{ display:inline-flex; align-items:center; gap:.5rem; padding:.42rem .7rem; border-radius: 999px; background: rgba(244,200,74,.22); border: 1px solid rgba(244,200,74,.40); color: rgba(17,24,39,.85); font-size:.85rem; font-weight: 600; }
      .dot{ width:10px; height:10px; border-radius:50%; background: var(--accent); display:inline-block; box-shadow: 0 0 0 6px rgba(244,200,74,.20); }
      .hr{ height: 1px; background: rgba(17,24,39,.10); border: 0; margin: 1.25rem 0; }

      /* ========== Mobile Sidebar Fix (prevents blur/washed-out sidebar) ========== */
      @media (max-width: 768px) {
        /* Make sidebar solid (no blur) */
        [data-testid="stSidebar"]{
          background: #ffffff !important;
          backdrop-filter: none !important;
          -webkit-backdrop-filter: none !important;
        }

        /* Ensure sidebar text is readable */
        [data-testid="stSidebar"] *{
          color: #121417 !important;
          opacity: 1 !important;
          filter: none !important;
        }

        /* Avoid the app body being blurred/dimmed when sidebar opens */
        [data-testid="stAppViewContainer"]{
          filter: none !important;
        }

        /* Optional: make sidebar a bit narrower on phone */
        [data-testid="stSidebar"]{
          width: 85vw !important;
          max-width: 85vw !important;
        }
      }
    </style>
    """).strip(),
    unsafe_allow_html=True,
)

# ===========================
# Navigation (this controls the sidebar order)
# ===========================
pages = [
    st.Page("pages/Overview.py", title="Overview"),
    st.Page(
        "pages/Data Engineering & Feature Selection.py",
        title="Data Engineering & Feature Selection",
    ),
    st.Page("pages/Logistic Regression.py", title="Logistic Regression"),
    st.Page("pages/Neural Network(MLP).py", title="Neural Network (MLP)"),
    st.Page(
        "pages/Modeling & Performance Analysis.py",
        title="Modeling & Performance Analysis",
    ),
    st.Page(
        "pages/Targeting Strategy & Financial Impact.py",
        title="Targeting Strategy & Financial Impact",
    ),
    st.Page("pages/Model Output Visualization.py", title="Model Output Visualization"),
    st.Page("pages/Strategic Recommendations.py", title="Strategic Recommendations"),
]

pg = st.navigation(pages)
pg.run()
