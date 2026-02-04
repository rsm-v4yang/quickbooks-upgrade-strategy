import streamlit as st
import textwrap

# Must be the first Streamlit command
st.set_page_config(page_title="Neural Network (MLP)", page_icon="🧠", layout="wide")


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
st.title("Neural Network (MLP)")

# ===========================
# Metrics
# ===========================
MLP_ARCH = "(64, 32, 16)"
MLP_LIFT_TOP10 = 3.74
MLP_TEST_PROFIT = 14718
WAVE2_LEADS = 118000

m1, m2, m3, m4 = st.columns(4)
m1.metric("Architecture", MLP_ARCH)
m2.metric("Top-Decile Lift (Top 10%)", f"{MLP_LIFT_TOP10:.2f}")
m3.metric("Expected Profit (Test)", f"${MLP_TEST_PROFIT:,.0f}")
m4.metric("Wave-2 Target Leads", f"{WAVE2_LEADS:,.0f}")

st.divider()

left, right = st.columns([1.7, 1])

with left:
    # ===========================
    # 4.1 Architecture & Hyper-parameters
    # ===========================
    st.subheader("Architecture & Hyper-parameters")

    info_card(
        "Overview",
        """
        To capture complex interactions between customer variables that a linear model might miss,
        we implemented a Multi-Layer Perceptron (MLP).
        """,
        icon="🧩",
    )

    info_card(
        "Model Structure",
        f"""
        The MLP uses a deep architecture with three hidden layers: {MLP_ARCH}.
        This tapering structure allows the model to learn broad patterns in the first layer
        and progressively condense them into specific upgrade signals in the final layer.
        """,
        icon="🏗️",
    )

    info_card(
        "Activation Functions",
        """
        ReLU activation was used for the hidden layers to prevent vanishing gradients.
        A sigmoid activation function was used in the output layer to generate probabilities
        between 0 and 1.
        """,
        icon="⚡",
    )

    info_card(
        "Optimization",
        """
        The model was trained using the Adam optimizer with a maximum of 500 iterations
        to ensure convergence on the training loss.
        """,
        icon="🧪",
    )

    # ===========================
    # 4.2 Why the Neural Network Outperformed
    # ===========================
    st.subheader("Why the Neural Network Outperformed")

    info_card(
        "Non-Linear Relationships",
        """
        The primary advantage of the MLP in this case was its ability to handle non-linear
        relationships between customer variables.
        """,
        icon="🧠",
    )

    info_card(
        "Interaction Effects",
        """
        For example, the effect of total dollars spent on upgrade probability may change
        significantly depending on whether the business flag is equal to 1 or 0.
        The neural network automatically captures these interaction effects without the
        need for manual feature engineering.
        """,
        icon="🔁",
    )

    info_card(
        "Top-Decile Concentration",
        f"""
        The MLP achieved a lift of {MLP_LIFT_TOP10:.2f} in the top 10 percent of customers.
        In direct mail campaigns, a top-heavy ranking is critical because it concentrates
        budget on the most likely responders at the beginning of the mailing list.
        """,
        icon="🎯",
    )

    # ===========================
    # 4.3 Performance vs. Complexity Trade-off
    # ===========================
    st.subheader("Performance vs. Complexity Trade-off")

    info_card(
        "Profitability",
        f"""
        Although the neural network operates as a black-box model compared to logistic regression,
        its performance was evaluated using the Expected Profit metric on the test set.
        The MLP generated approximately ${MLP_TEST_PROFIT:,.0f} in total expected profit,
        outperforming the more conservative baseline logistic regression model.
        """,
        icon="⚖️",
    )

    info_card(
        "Stability",
        """
        StandardScaler was applied to numeric features such as dollars and last to prevent
        large-scale monetary variables from dominating gradients.
        This resulted in improved training stability and better generalization performance.
        """,
        icon="🧯",
    )

    # ===========================
    # 4.4 Strategic Implementation
    # ===========================
    st.subheader("Strategic Implementation")

    info_card(
        "Wave-2 Mailing Strategy",
        """
        The final Wave-2 mailing list was generated by passing all non-respondents through
        the trained MLP pipeline.
        """,
        icon="📬",
    )

    st.markdown(
        """
        <ol style="line-height: 1.8; font-size: 1.02rem;">
          <li><b>Probabilistic Scoring:</b> Every customer received a predicted upgrade probability score from the MLP.</li>
          <li><b>Economic Filter:</b> A 50 percent response decay and a $1.41 mailing cost threshold were applied.</li>
          <li><b>Outcome:</b> This precision-based filtering strategy allowed Intuit to ignore the long tail of
              unprofitable customers and focus on the 118,000 leads with the highest expected return on investment.</li>
        </ol>
        """,
        unsafe_allow_html=True,
    )

    st.success(
        f"Final Wave-2 targeting focuses on {WAVE2_LEADS:,.0f} leads with the highest ROI potential."
    )

with right:
    st.subheader("Executive Summary")

    st.markdown(
        """
        - Captures non-linear relationships and interaction effects
        - Produces strong top-decile concentration for direct mail targeting
        - Performance validated using Expected Profit on the test set
        """
    )

    with st.expander("Model Settings", expanded=False):
        st.markdown(
            f"""
            - Architecture: {MLP_ARCH}
            - Hidden activation: ReLU
            - Output activation: Sigmoid
            - Optimizer: Adam
            - Max iterations: 500
            - Scaling: StandardScaler
            """
        )

st.divider()
st.caption("Neural Network (MLP)")
