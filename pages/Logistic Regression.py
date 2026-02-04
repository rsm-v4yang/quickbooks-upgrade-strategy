import streamlit as st
import textwrap

st.set_page_config(page_title="Logistic Regression", page_icon="📈", layout="wide")


def info_card(title: str, body_md: str, icon: str = "📌"):
    body_md = textwrap.dedent(body_md).strip()

    st.markdown(
        f"""
        <div style="
            padding: 1rem 1.2rem;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.04);
            margin-bottom: 0.9rem;
        ">
            <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.45rem;">
                {icon} {title}
            </div>
            <div style="line-height: 1.6; opacity: 0.95;">
                {body_md}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================
# Page Title
# ===========================
st.title("Logistic Regression")

# ===========================
# Metrics (edit if needed)
# ===========================
AUC = 0.747
BREAKEVEN_PROB = 0.0235

m1, m2 = st.columns(2)
m1.metric("AUC", f"{AUC:.3f}")
m2.metric("Breakeven Probability", f"{BREAKEVEN_PROB * 100:.2f}%")

st.divider()

left, right = st.columns([1.7, 1])

with left:
    # ===========================
    # 3.1 Methodology & Implementation
    # ===========================
    st.subheader("Methodology & Implementation")

    info_card(
        "Model Overview",
        """
        Logistic Regression serves as the interpretive baseline in this analysis,
        providing transparency into the relationship between customer attributes
        and upgrade likelihood.
        """,
        icon="🔍",
    )

    info_card(
        "Estimation Approach",
        """
        A binary logistic regression model was trained to estimate the probability
        of response in Wave-1. These probabilities were later adjusted to reflect
        expected response decay in Wave-2.
        """,
        icon="📐",
    )

    info_card(
        "Wave-2 Adjustment",
        """
        Predicted probabilities were scaled using the expected decay factor:
        p̂_wave2 = p̂_wave1 × 0.5.
        This adjustment provides a conservative estimate suitable for financial
        decision-making.
        """,
        icon="🔁",
    )

    # ===========================
    # 3.2 Business Drivers
    # ===========================
    st.subheader("Significant Predictors (Business Drivers)")

    info_card(
        "Key Predictors",
        """
        Several variables were statistically significant and economically meaningful:
        - Recency (last): longer time since last purchase reduces upgrade likelihood
        - Monetary value (dollars): higher historical spend increases upgrade propensity
        - Product ownership (owntaxprod): tax product users exhibit strong ecosystem lock-in
        - Geographic indicators (zip bins): regional variation in response behavior
        """,
        icon="📊",
    )

    # ===========================
    # 3.3 Performance Evaluation
    # ===========================
    st.subheader("Performance Evaluation")

    info_card(
        "Discrimination Performance",
        """
        The logistic regression model achieved an AUC of approximately 0.747,
        indicating solid separation between responders and non-responders.
        """,
        icon="📈",
    )

    info_card(
        "Model Limitation",
        """
        A key limitation of logistic regression is its linear log-odds assumption.
        Interaction effects (e.g., dollars × recency) are not captured automatically,
        motivating the use of a neural network for non-linear optimization.
        """,
        icon="⚠️",
    )

    # ===========================
    # 3.4 Financial Application
    # ===========================
    st.subheader("Financial Application")

    info_card(
        "Breakeven Analysis",
        """
        Campaign economics imply a breakeven response probability of 2.35 percent,
        based on a mailing cost of $1.41 and a gross margin of $60 per sale.
        """,
        icon="💰",
    )

    info_card(
        "Decision Rule",
        """
        Customers with adjusted Wave-2 probabilities exceeding the breakeven threshold
        were classified as profitable under the logistic baseline, providing a
        conservative floor for expected incremental profit.
        """,
        icon="✅",
    )

with right:
    st.subheader("Executive Summary")

    st.markdown(
        """
        - Provides transparent and interpretable baseline
        - Identifies key business drivers of upgrade behavior
        - Establishes conservative profitability threshold
        - Motivates advanced modeling with neural networks
        """
    )

    with st.expander("Reproducibility Notes", expanded=False):
        st.markdown(
            """
            Model estimation and diagnostics (coefficients, p-values, VIFs)
            were generated using pyrsm and are documented in intuit.ipynb.
            """
        )

st.divider()
st.caption("Logistic Regression")
