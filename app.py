import streamlit as st
import textwrap

# ============================================================
# Global App Config (ONLY ONCE)
# ============================================================
st.set_page_config(
    page_title="Intuit QuickBooks Upgrade Strategy",
    layout="wide",
    initial_sidebar_state="collapsed",  # mobile-safe
)

# ============================================================
# Global CSS
# ============================================================
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
        font-family: ui-sans-serif, system-ui, -apple-system,
                     "Segoe UI", Roboto, Helvetica, Arial;
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

      [data-testid="stSidebar"] .block-container{
        padding-top: 1.4rem;
      }

      h1{ font-size: 2.1rem; letter-spacing: -0.03em; color: var(--primary-2); }
      h2{ font-size: 1.35rem; color: var(--primary-2); }
      h3{ font-size: 1.1rem; color: var(--primary); }

      p, li{
        font-size: 1.0rem;
        line-height: 1.7;
        color: rgba(18,20,23,.84);
      }

      .card{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow-soft);
        padding: 1.25rem 1.35rem;
      }

      .subtle{
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.55;
      }

      /* ===== General "safety" (prevents wide content from breaking layout) ===== */
      img, video, canvas, svg {
        max-width: 100% !important;
        height: auto !important;
      }

      iframe {
        max-width: 100% !important;
      }

      table {
        max-width: 100% !important;
      }

      pre, code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
      }

      /* ================= Mobile fixes (FINAL: kill horizontal pan) ================= */
      @media (max-width: 768px) {

        /* Make every container behave */
        * { box-sizing: border-box !important; }

        html, body{
          width: 100% !important;
          max-width: 100% !important;
          overflow-x: hidden !important;
          overscroll-behavior-x: none !important;
          touch-action: pan-y !important; /* key: allow vertical only */
        }

        /* Streamlit root containers (the usual overflow culprits) */
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main {
          width: 100% !important;
          max-width: 100% !important;
          overflow-x: hidden !important;
          overscroll-behavior-x: none !important;
          touch-action: pan-y !important;
        }

        /* Markdown/text: force wrapping so long words/strings never widen the page */
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] * {
          overflow-wrap: anywhere !important;
          word-break: break-word !important;
        }

        /* Sidebar overlay (can still open/close) */
        [data-testid="stSidebar"]{
          position: fixed !important;
          top: 0 !important;
          left: 0 !important;
          height: 100vh !important;
          width: 85vw !important;
          max-width: 85vw !important;
          z-index: 9999 !important;

          background: #ffffff !important;
          backdrop-filter: none !important;
          -webkit-backdrop-filter: none !important;

          /* IMPORTANT: do NOT force transform:none
             Streamlit uses transform to slide open/close */
          overflow-y: auto !important;
          box-shadow: 0 8px 30px rgba(17,24,39,.12) !important;
          border-right: 1px solid rgba(17,24,39,.06) !important;
        }

        [data-testid="stSidebar"] *{
          color: #121417 !important;
          opacity: 1 !important;
        }

        /* Mobile layout padding */
        .block-container{
          max-width: 100% !important;
          padding-left: 1rem !important;
          padding-right: 1rem !important;
        }

        /* Tables/iframes should not force page wide */
        table{
          display: block !important;
          width: 100% !important;
          max-width: 100% !important;
          overflow-x: auto !important;
        }

        iframe, img, video, canvas, svg{
          max-width: 100% !important;
          height: auto !important;
        }
      }
    </style>
    """).strip(),
    unsafe_allow_html=True,
)

# ============================================================
# Navigation
# ============================================================
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
