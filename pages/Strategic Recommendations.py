import streamlit as st
import textwrap

# Must be the first Streamlit command
st.set_page_config(
    page_title="Strategic Recommendations",
    page_icon="🧭",
    layout="wide",
)


def info_card(title: str, body_md: str, icon: str = "📌"):
    body_md = textwrap.dedent(body_md).strip()

    st.markdown(
        f"""
        <div style="
            padding: 1.1rem 1.3rem;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.04);
            margin-bottom: 1.0rem;
        ">
            <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">
                {icon} {title}
            </div>
            <div style="line-height: 1.65; font-size: 1.02rem;">
                {body_md}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================
# Page Title
# ===========================
st.title("Strategic Recommendations")

st.markdown(
    """
    Based on the modeling results, profitability analysis, and targeting simulations,
    the following recommendations are proposed to guide the execution of the Wave-2 campaign.
    These actions are designed to maximize return on marketing investment while minimizing
    unnecessary operational spend.
    """
)

st.divider()

left, right = st.columns([1.8, 1])

with left:
    # ===========================
    # Recommendation 1
    # ===========================
    info_card(
        "Recommendation 1: Deploy the MLP Model",
        """
        Use the Neural Network (MLP) as the production scoring engine for Wave-2.
        Its primary advantage is not overall accuracy, but concentration: the model
        consistently ranks the most profitable responders at the top of the list.
        This enables Intuit to capture a larger share of upgrades with fewer mailings
        and significantly reduces wasted outreach to low-propensity customers.
        """,
        icon="✅",
    )

    # ===========================
    # Recommendation 2
    # ===========================
    info_card(
        "Recommendation 2: Focus on Multi-Product Loyalists",
        """
        Customers already engaged in the Intuit ecosystem, particularly those with
        tax-product ownership, represent a substantially higher-propensity segment.
        Future campaigns should prioritize bundled offers and coordinated messaging
        to reinforce cross-product adoption and deepen customer lifetime value.
        """,
        icon="🧩",
    )

    # ===========================
    # Recommendation 3
    # ===========================
    info_card(
        "Recommendation 3: Regional Prioritization",
        """
        Geographic insights derived from zip-bin patterns should be used to prioritize
        outreach in high-performing regions. Allocating additional marketing resources
        and field-sales support to these clusters enables more efficient budget deployment
        and maximizes conversion potential where demand is strongest.
        """,
        icon="📍",
    )

with right:
    st.subheader("Why These Actions Matter")

    st.markdown(
        """
        - Aligns model choice with business profitability
        - Concentrates spend on the highest-return customers
        - Leverages ecosystem and geographic advantages
        - Translates analytics directly into execution strategy
        """
    )

    with st.expander("Connection to Prior Sections", expanded=False):
        st.markdown(
            """
            - Section 3 established a robust data foundation for non-linear modeling
            - Section 4 demonstrated the Neural Network’s superior profit performance
            - Section 5 quantified the financial impact of profit-based targeting

            This section converts those analytical findings into actionable decisions.
            """
        )

st.divider()
st.caption("Section 6 — Strategic Recommendations")
