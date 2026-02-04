import streamlit as st
import textwrap

# ============================================================
# Global App Config (FINAL, STABLE)
# ============================================================
st.set_page_config(
    page_title="Intuit QuickBooks Upgrade Strategy",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# Global CSS (NO custom background, NO sidebar hacks)
# ============================================================
st.markdown(
    textwrap.dedent("""
    <style>
      /* Force consistent light background everywhere */
      html, body,
      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      section.main {
        background: #ffffff !important;
        color: #121417 !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
      }

      /* Prevent iOS horizontal drag */
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

      /* Safe wrapping */
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
    </style>
    """),
    unsafe_allow_html=True,
)

# ============================================================
# Navigation (OFFICIAL Streamlit only)
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
