import streamlit as st
import textwrap
import pandas as pd

# Must be the first Streamlit command
st.set_page_config(
    page_title="Modeling & Performance Analysis",
    page_icon="📊",
    layout="wide",
)


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
st.title("Modeling & Performance Analysis")

st.markdown(
    """
    The core of our analytical strategy was the comparison between a traditional statistical baseline
    and an advanced machine learning architecture. We evaluated a Logistic Regression model against
    a Multi-Layer Perceptron (MLP) Neural Network to determine the most effective targeting strategy
    for the Wave-2 campaign.
    """
)

st.divider()

# ===========================
# Key numbers (edit if needed)
# ===========================
ARCH = "(64, 32, 16)"
AUC_LR = 0.7470
AUC_MLP = 0.7418
LIFT_LR = 3.57
LIFT_MLP = 3.74
PROFIT_LR = 12940
PROFIT_MLP = 14718
MAIL_LR = 0.182
MAIL_MLP = 0.155
BREAKEVEN = 0.0235
FULL_POP = 763334
PROJ_INCREMENTAL = 475000  # user-provided projection

k1, k2, k3, k4 = st.columns(4)
k1.metric("Test AUC (LR)", f"{AUC_LR:.4f}")
k2.metric("Top-Decile Lift (MLP)", f"{LIFT_MLP:.2f}")
k3.metric("Projected Test Profit (MLP)", f"${PROFIT_MLP:,.0f}")
k4.metric("Targeted Mailing % (MLP)", f"{MAIL_MLP * 100:.1f}%")

st.divider()

left, right = st.columns([1.7, 1])

with left:
    # ===========================
    # 4.1 Comparative Framework
    # ===========================
    st.subheader("Comparative Framework")

    info_card(
        "Discriminatory Power (AUC)",
        """
        We used the Area Under the ROC Curve (AUC) to measure how well each model
        distinguishes between responders and non-responders across the population.
        """,
        icon="📈",
    )

    info_card(
        "Targeting Efficiency (Lift)",
        """
        Lift is critical in direct mail. It measures how much better the model performs
        at identifying responders in the top deciles compared to a random mailing.
        """,
        icon="🎯",
    )

    info_card(
        "Economic Optimization (Expected Profit)",
        f"""
        Expected Profit served as the decision metric. We adjusted predicted probabilities
        for Wave-2 response decay and applied campaign economics:

        Wave-2 probability adjustment:
        p_wave2 = p_wave1 × 0.5

        Breakeven response threshold:
        p* = 1.41 / 60 ≈ {BREAKEVEN * 100:.2f}%

        Expected profit logic (per customer):
        expected_profit = (p_wave2 × 60) − 1.41
        """,
        icon="💰",
    )

    # ===========================
    # 4.2 Model Performance Summary
    # ===========================
    st.subheader("Model Performance Summary")

    perf_df = pd.DataFrame(
        {
            "Metric": [
                "Architecture",
                "Test AUC",
                "Top-Decile Lift",
                "Projected Test Profit",
                "Targeted Mailing %",
            ],
            "Logistic Regression (Baseline)": [
                "Linear (Logit)",
                f"{AUC_LR:.4f}",
                f"{LIFT_LR:.2f}",
                f"${PROFIT_LR:,.0f}",
                f"{MAIL_LR * 100:.1f}%",
            ],
            "Neural Network (MLP)": [
                f"{ARCH} Layers",
                f"{AUC_MLP:.4f}",
                f"{LIFT_MLP:.2f}",
                f"${PROFIT_MLP:,.0f}",
                f"{MAIL_MLP * 100:.1f}%",
            ],
        }
    )

    st.dataframe(perf_df, use_container_width=True, hide_index=True)

    # ===========================
    # 4.3 Lift and Profitability Analysis
    # ===========================
    st.subheader("Lift and Profitability Analysis")

    info_card(
        "The Power of Lift",
        f"""
        While Logistic Regression showed a slightly higher overall AUC, the Neural Network
        demonstrated stronger top-heavy performance for campaign execution.
        The MLP achieved a top-decile lift of {LIFT_MLP:.2f}, indicating it is more efficient at clustering
        the highest-probability responders at the top of the ranked list and minimizing wasted spend.
        """,
        icon="🚀",
    )

    info_card(
        "Profit at Scale",
        f"""
        After applying the Wave-2 adjustment (p_wave2 = p_wave1 × 0.5), the Neural Network identified
        a more refined target segment of {MAIL_MLP * 100:.1f}% of the population.
        This leaner list produced higher total profit on the test set (${PROFIT_MLP:,.0f} vs ${PROFIT_LR:,.0f})
        because it more effectively excluded customers whose predicted response rate fell just below
        the breakeven threshold of {BREAKEVEN * 100:.2f}%.
        """,
        icon="📬",
    )

    # ===========================
    # 4.4 Justification for Selecting the Neural Network
    # ===========================
    st.subheader("Justification for Selecting the Neural Network")

    info_card(
        "Non-Linear Feature Mapping",
        f"""
        Unlike Logistic Regression, which assumes linear relationships, the Neural Network’s deep architecture
        ({ARCH}) captures complex interactions between geographic location (zip_bins), business status,
        and historical spending.
        """,
        icon="🧠",
    )

    info_card(
        "Precision in the Profit Zone",
        """
        The Neural Network’s higher lift in the top deciles concentrates the highest-propensity responders
        early in the ranked list. This improves ROI by capturing more upgrades in the first mailings,
        where returns are strongest.
        """,
        icon="🎯",
    )

    info_card(
        "Financial Impact",
        f"""
        When scaled to the full eligible population of {FULL_POP:,.0f} non-respondents, the Neural Network’s
        targeting precision is projected to generate incremental profit of over ${PROJ_INCREMENTAL:,.0f},
        outperforming the baseline by nearly 14 percent.
        """,
        icon="💵",
    )

with right:
    st.subheader("Executive Takeaways")

    st.markdown(
        f"""
        - AUC is necessary but not sufficient for direct-mail decisions
        - Lift reflects top-decile targeting quality, which drives mailing efficiency
        - Expected Profit provides the final business decision rule
        - MLP delivers higher profit with a leaner mailing depth ({MAIL_MLP * 100:.1f}% vs {MAIL_LR * 100:.1f}%)
        """
    )

    with st.expander("Numbers Used on This Page", expanded=False):
        st.markdown(
            f"""
            - Test set size: 22,500
            - AUC: LR {AUC_LR:.4f}, MLP {AUC_MLP:.4f}
            - Top-decile lift: LR {LIFT_LR:.2f}, MLP {LIFT_MLP:.2f}
            - Test profit: LR ${PROFIT_LR:,.0f}, MLP ${PROFIT_MLP:,.0f}
            - Mailing depth: LR {MAIL_LR * 100:.1f}%, MLP {MAIL_MLP * 100:.1f}%
            - Breakeven p*: {BREAKEVEN * 100:.2f}%
            - Full eligible population: {FULL_POP:,.0f}
            - Projected incremental profit: ${PROJ_INCREMENTAL:,.0f}
            """
        )

st.divider()
st.caption("Section 4 — Modeling & Performance Analysis")
