import streamlit as st
import textwrap

# ============================================================
# Global App Config
# ============================================================
st.set_page_config(
    page_title="Intuit QuickBooks Upgrade Strategy",
    layout="wide",  # ✅ desktop keeps wide
    initial_sidebar_state="collapsed",  # ✅ mobile starts collapsed
)

# ============================================================
# CSS: only "safe" anti-overflow (no sidebar hacking)
# ============================================================
st.markdown(
    textwrap.dedent("""
    <style>
      html, body{
        overflow-x: hidden !important;
        max-width: 100% !important;
      }

      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      section.main{
        overflow-x: hidden !important;
        max-width: 100% !important;
      }

      /* Force wrapping so long strings never create horizontal pan on mobile */
      [data-testid="stMarkdownContainer"],
      [data-testid="stMarkdownContainer"] *{
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
      }

      img, video, canvas, svg, iframe{
        max-width: 100% !important;
        height: auto !important;
      }

      table{
        display: block !important;
        width: 100% !important;
        overflow-x: auto !important;
      }

      pre, code{
        white-space: pre-wrap !important;
        word-break: break-word !important;
      }

      /* Mobile: prevent iOS sideways drag */
      @media (max-width: 768px){
        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        section.main{
          overscroll-behavior-x: none !important;
          touch-action: pan-y !important;
        }

        .block-container{
          padding-left: 1rem !important;
          padding-right: 1rem !important;
        }
      }
    </style>
    """).strip(),
    unsafe_allow_html=True,
)

# ============================================================
# Pages definition (single source of truth)
# ============================================================
PAGES = [
    ("Overview", "pages/Overview.py"),
    (
        "Data Engineering & Feature Selection",
        "pages/Data Engineering & Feature Selection.py",
    ),
    ("Logistic Regression", "pages/Logistic Regression.py"),
    ("Neural Network (MLP)", "pages/Neural Network(MLP).py"),
    ("Modeling & Performance Analysis", "pages/Modeling & Performance Analysis.py"),
    (
        "Targeting Strategy & Financial Impact",
        "pages/Targeting Strategy & Financial Impact.py",
    ),
    ("Model Output Visualization", "pages/Model Output Visualization.py"),
    ("Strategic Recommendations", "pages/Strategic Recommendations.py"),
]

# Build Streamlit nav pages
nav_pages = [st.Page(path, title=title) for title, path in PAGES]
pg = st.navigation(nav_pages)  # ✅ keeps normal sidebar navigation on desktop

# ============================================================
# Mobile-friendly top nav (does NOT replace sidebar; it just lets phone users jump)
# ============================================================
# We don't try to "switch" pg (no such API). We use session_state + rerun.
page_titles = [t for t, _ in PAGES]

# initialize
if "mobile_page" not in st.session_state:
    st.session_state.mobile_page = page_titles[0]

# Show dropdown at top (works on desktop too, but mainly for mobile)
st.markdown("### Navigate")
choice = st.selectbox(
    "",
    page_titles,
    index=page_titles.index(st.session_state.mobile_page),
)

# If user changes dropdown, store and rerun. Then sidebar nav can follow on its own.
if choice != st.session_state.mobile_page:
    st.session_state.mobile_page = choice
    st.rerun()

# ============================================================
# Run the app navigation
# ============================================================
pg.run()
