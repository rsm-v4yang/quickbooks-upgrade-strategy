import streamlit as st
import textwrap

# Must be the first Streamlit command in the file
st.set_page_config(
    page_title="Targeting Strategy & Financial Impact", page_icon="💰", layout="wide"
)


def info_card(title: str, body_html: str, icon: str = "📌"):
    body_html = textwrap.dedent(body_html).strip()

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
            <div style="line-height: 1.65; opacity: 0.95;">
                {body_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------
# Page Title
# ---------------------------
st.title("Targeting Strategy & Financial Impact")

# ---------------------------
# Inputs (from your HTML results + report constants)
# ---------------------------
MAIL_COST = 1.41
MARGIN = 60
DECAY = 0.50

# From HTML export checks
TEST_BASE_IDS = 22500
TEST_MAIL_IDS = 3489

# From HTML model comparison (NN Best) profit scenario
# (This is the reported profit when mailing the top 50% of mailable customers under 50% response drop.)
TEST_PROFIT_NN_50MAIL = 14718.14

# From your report / slide
FULL_POP_ELIGIBLE = 763_334
FULL_POP_RECOMMENDED_MAILS = 118_000

# Derived metrics
test_mailing_depth = TEST_MAIL_IDS / TEST_BASE_IDS
full_pop_mailing_depth = FULL_POP_RECOMMENDED_MAILS / FULL_POP_ELIGIBLE

# Scaled projection (simple, transparent scaling)
profit_per_customer_test = TEST_PROFIT_NN_50MAIL / TEST_BASE_IDS
projected_profit_full_pop = profit_per_customer_test * FULL_POP_ELIGIBLE

# Cost avoided by NOT mailing the rest of eligible population
not_mailed = FULL_POP_ELIGIBLE - FULL_POP_RECOMMENDED_MAILS
avoided_cost = not_mailed * MAIL_COST

# Breakeven response rate under the Wave-2 rule:
# expected_profit > 0  =>  (p_model * DECAY * MARGIN) - MAIL_COST > 0
breakeven_rate = MAIL_COST / (DECAY * MARGIN)

# ---------------------------
# Top metrics row
# ---------------------------
m0, m1, m2, m3 = st.columns([1.6, 1, 1, 1])

with m0:
    st.markdown(
        """
        **Decision Rule**

        Expected Profit > 0
        (Apply Wave-2 decay and mailing cost)
        """
    )

m1.metric("Breakeven Response Rate", f"{breakeven_rate * 100:.2f}%")
m2.metric("Test Mailing Depth", f"{test_mailing_depth * 100:.1f}%")
m3.metric("Test Targeted Volume", f"{TEST_MAIL_IDS:,}")

st.divider()

left, right = st.columns([1.8, 1])

with left:
    st.subheader("5. Targeting Strategy & Financial Impact")

    info_card(
        "Profit Maximization Rule",
        f"""
        We apply a strict profit maximization rule and only mail customers whose expected profit is positive.
        <br><br>
        <div style="padding: 0.7rem 0.9rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.10); background: rgba(255,255,255,0.03);">
            <span style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;">
            Expected Profit = (P_model × {DECAY:.2f} × ${MARGIN}) − ${MAIL_COST}
            </span>
        </div>
        <br>
        This rule is economically equivalent to requiring a minimum (breakeven) response probability of
        <b>{breakeven_rate * 100:.2f}%</b>.
        """,
        icon="💡",
    )

    st.subheader("5.1 Campaign Results (Test Set)")

    info_card(
        "What the Test Set Shows",
        f"""
        Using the Neural Network scoring and the profit-based cutoff:
        <ul style="margin: 0.3rem 0 0 1.1rem;">
            <li><b>Targeted Volume:</b> {TEST_MAIL_IDS:,} customers</li>
            <li><b>Mailing Depth:</b> {test_mailing_depth * 100:.1f}% of the test set ({TEST_BASE_IDS:,} customers)</li>
        </ul>
        <br>
        In addition, the notebook’s scenario comparison reports that the Neural Network produces
        <b>${TEST_PROFIT_NN_50MAIL:,.2f}</b> expected profit on the test set under the 50% response-drop assumption
        (NN Best, 50% mailing scenario).
        """,
        icon="🧾",
    )

    info_card(
        "Why the Cutoff Works",
        """
        The ranked-profit curve (cumulative expected profit) rises sharply for the top customers and then
        flattens. Once lower-ranked customers are included, expected profit approaches zero and eventually
        turns negative. This pattern justifies using <b>Expected Profit &gt; 0</b> as the operational cutoff:
        it prevents budget from being spent on the unprofitable tail.
        """,
        icon="📈",
    )

    st.subheader("5.2 Scaled Projections (Full Population)")

    info_card(
        "Wave-2 Scale Impact",
        f"""
        Applying the same Neural Network targeting logic to the full eligible population of
        <b>{FULL_POP_ELIGIBLE:,}</b> non-respondents yields:
        <ul style="margin: 0.3rem 0 0 1.1rem;">
            <li><b>Total Recommended Mailings:</b> {FULL_POP_RECOMMENDED_MAILS:,}</li>
            <li><b>Projected Mailing Depth:</b> {full_pop_mailing_depth * 100:.1f}%</li>
            <li><b>Projected Campaign Profit:</b> approximately <b>${projected_profit_full_pop:,.0f}</b> (scaled from test performance)</li>
            <li><b>Efficiency Gain:</b> by not mailing the remaining {not_mailed:,} customers, we avoid about <b>${avoided_cost:,.0f}</b> in mailing cost</li>
        </ul>
        <br>
        Note: the projected profit is a transparent scale-up using test-set profit per customer.
        If you have a finalized projection number from your report (e.g., 492,000+), you can replace it here.
        """,
        icon="🌍",
    )

    st.subheader("6. Strategic Recommendations")

    info_card(
        "Recommendation 1: Deploy the MLP Model",
        """
        Use the Neural Network as the production scoring engine for Wave-2. Its advantage is not just accuracy,
        but concentration: it pushes profitable responders to the top of the ranked list and reduces waste.
        """,
        icon="✅",
    )

    info_card(
        "Recommendation 2: Focus on Multi-Product Loyalists",
        """
        Customers already engaged in the Intuit ecosystem (e.g., tax-product ownership) represent a higher-propensity
        segment. Future campaigns should bundle offers and messaging to reinforce cross-product adoption.
        """,
        icon="🧩",
    )

    info_card(
        "Recommendation 3: Regional Prioritization",
        """
        Use geographic bin insights (zip-bin patterns) to prioritize outreach in high-performing clusters.
        This enables smarter allocation of budget and field-sales support in regions with the strongest conversion potential.
        """,
        icon="📍",
    )

with right:
    st.subheader("Quick Summary")

    st.markdown(
        f"""
        - Decision rule: Expected Profit > 0
        - Breakeven response rate: {breakeven_rate * 100:.2f}%
        - Test targeting: {TEST_MAIL_IDS:,} customers ({test_mailing_depth * 100:.1f}% depth)
        - Full scale: {FULL_POP_RECOMMENDED_MAILS:,} recommended mailings ({full_pop_mailing_depth * 100:.1f}% depth)
        """
    )

    with st.expander("Assumptions (Appendix)", expanded=False):
        st.markdown(
            f"""
            - Mailing cost: ${MAIL_COST}
            - Gross margin per upgrade: ${MARGIN}
            - Wave-2 response decay: {DECAY:.2f}
            - Test set size: {TEST_BASE_IDS:,}
            - Eligible population: {FULL_POP_ELIGIBLE:,}
            """
        )

st.divider()
st.caption("Targeting Strategy & Financial Impact")
