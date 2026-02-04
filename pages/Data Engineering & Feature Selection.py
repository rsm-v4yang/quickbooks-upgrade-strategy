import streamlit as st
import textwrap

# Must be the first Streamlit command
st.set_page_config(
    page_title="Data Engineering & Feature Selection", page_icon="🧱", layout="wide"
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
st.title("Data Engineering & Feature Selection")

st.markdown(
    """
    The predictive performance of the Neural Network (NN) is critically dependent on the quality,
    consistency, and representation of the input features. To support non-linear pattern recognition
    and robust generalization, we implemented a rigorous data engineering pipeline that transforms
    the raw intuit75k dataset into a high-dimensional feature space suitable for advanced machine learning models.
    """
)

st.divider()

left, right = st.columns([1.7, 1])

with left:
    # ===========================
    # 3.1 Data Cleaning & Advanced Imputation
    # ===========================
    st.subheader("Data Cleaning & Advanced Imputation")

    info_card(
        "High-Performance Data Handling",
        """
        Using the polars library for high-performance data manipulation, we addressed both data quality
        and logical consistency issues across the 75,000 customer records.
        """,
        icon="⚙️",
    )

    info_card(
        "Logical Consistency",
        """
        Customers who had already responded in Wave-1 (res1 = 'Yes') were explicitly identified and excluded
        from the final Wave-2 mailing universe. This prevents redundant targeting and avoids unnecessary
        mailing costs during campaign execution.
        """,
        icon="🧾",
    )

    info_card(
        "Median Imputation",
        """
        Median imputation was applied to numerical variables such as numords (number of orders) and
        dollars (total historical spend). This approach was chosen over mean imputation to mitigate the
        influence of extreme spending outliers and ensure the model learns patterns representative of the
        typical small-business customer.
        """,
        icon="🧮",
    )

    info_card(
        "Categorical Handling",
        """
        Missing demographic values, most notably in sex, were encoded as an explicit Unknown category.
        This preserves all observations while allowing the model to learn whether missingness itself carries
        predictive information regarding upgrade behavior.
        """,
        icon="🏷️",
    )

    # ===========================
    # 3.2 Feature Engineering
    # ===========================
    st.subheader("Feature Engineering: A Journey of Discovery")

    info_card(
        "Geographic One-Hot Encoding",
        """
        Although zip_bins is represented numerically (1–20), the values correspond to geographic clusters
        rather than a continuous or ordinal scale. Treating them as numeric would impose an artificial ordering.
        We therefore applied one-hot encoding, converting zip_bins into 20 binary indicators so the Neural Network
        can learn region-specific response hotspots.
        """,
        icon="🗺️",
    )

    info_card(
        "RFM Framework",
        """
        We retained the Recency (last), Frequency (numords), and Monetary value (dollars) variables,
        which represent the historical foundation of direct marketing analytics. These predictors consistently
        emerged as strong signals during exploratory data analysis.
        """,
        icon="📊",
    )

    info_card(
        "Ecosystem Synergy Indicators",
        """
        Binary indicators such as bizflag (business versus individual) and owntaxprod (ownership of tax software)
        were incorporated to capture lock-in and cross-product synergy within the Intuit ecosystem.
        """,
        icon="🔒",
    )

    # ===========================
    # 3.3 Scaling & Normalization
    # ===========================
    st.subheader("Scaling and Normalization for Neural Networks")

    info_card(
        "Why Scaling Matters",
        """
        Neural Networks are sensitive to feature magnitude. For example, dollars may range in the hundreds or
        thousands, while bizflag is binary (0/1). Without scaling, large-magnitude variables would dominate
        gradient updates during training.
        """,
        icon="⚠️",
    )

    info_card(
        "StandardScaler",
        """
        We applied StandardScaler to numerical inputs to center each feature to a mean of zero and scale it to
        unit variance. This improves training stability, accelerates convergence, and prevents monetary variables
        from disproportionately influencing the learning process.
        """,
        icon="📐",
    )

    # ===========================
    # 3.4 Training & Validation Strategy
    # ===========================
    st.subheader("Training and Validation Strategy")

    info_card(
        "70/30 Split",
        """
        The dataset was partitioned into a training set (70 percent, 52,500 observations) and a hold-out test set
        (30 percent, 22,500 observations). The Neural Network was trained exclusively on the training set,
        while the test set was reserved for unbiased evaluation of Wave-2 profitability.
        """,
        icon="🧪",
    )

    info_card(
        "Target Definition",
        """
        The target variable was res1_bin, a binary (0/1) indicator of customer response.
        """,
        icon="🎯",
    )

    info_card(
        "Reproducibility",
        """
        A fixed random_state was used for all data splits and model initializations to ensure results are
        consistent, reproducible, and auditable by technical stakeholders.
        """,
        icon="✅",
    )

with right:
    st.subheader("Key Takeaways")

    st.markdown(
        """
        - Data integrity was enforced through logical consistency checks
        - Robust imputation preserves observations without biasing training
        - One-hot encoding enables geographic hotspot detection
        - Standardization is essential for stable neural network optimization
        - Hold-out testing provides realistic performance estimates
        """
    )

st.divider()
st.caption("Section 3 — Data Engineering & Feature Selection")
