import streamlit as st
import textwrap

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Neural Network (MLP)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Global Styles (fixed)
# =========================
st.markdown(
    textwrap.dedent(
        """
        <style>
          :root{
            --bg: #F4F1EA;
            --panel: #FFFFFF;
            --text: #121417;
            --muted: rgba(18,20,23,.68);
            --primary: #1F2937;
            --accent: #F4C84A;
            --border: rgba(17,24,39,.10);
            --shadow-soft: 0 6px 18px rgba(17,24,39,.08);
            --radius: 18px;
          }

          html, body, [data-testid="stAppViewContainer"]{
            background: var(--bg) !important;
            color: var(--text);
            font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial;
          }

          .block-container{
            max-width: 1120px;
            padding-top: 1.7rem;
            padding-bottom: 2.8rem;
          }

          [data-testid="stSidebar"]{
            background: rgba(255,255,255,.70);
            backdrop-filter: blur(8px);
            border-right: 1px solid var(--border);
          }

          h1{ font-size: 1.85rem; letter-spacing: -0.03em; margin: 0; color: var(--primary); }
          p, li{ font-size: 1.0rem; line-height: 1.7; color: rgba(18,20,23,.84); }

          /* ✅ Card */
          .card{
            width: 100%;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow-soft);
            padding: 1.05rem 1.15rem;
            margin: 0 0 .9rem 0;
            box-sizing: border-box;
            overflow: hidden;
          }

          /* ✅ Card title row */
          .card-title{
            display:flex;
            align-items:flex-start;
            gap:.55rem;
            font-weight: 800;
            color: var(--primary);
            font-size: 0.98rem;
            margin: 0 0 .55rem 0;
            line-height: 1.25;
          }
          .card-title .icon{
            width: 1.35rem;
            flex: 0 0 1.35rem;
            line-height: 1.2;
          }

          /* ✅ Card body text + list reset (fixes "broken" layout) */
          .card-body{
            color: rgba(18,20,23,.84);
            font-size: 1.0rem;
            line-height: 1.7;
          }
          .card-body p{ margin: .35rem 0; }
          .card-body ul{
            margin: .35rem 0 0 1.15rem;  /* prevents huge default indent */
            padding: 0;
          }
          .card-body li{ margin: .25rem 0; }

          /* Pills / chips */
          .chip-row{
            display:flex;
            gap:0.6rem;
            flex-wrap:wrap;
            margin-bottom:0.7rem;
          }
          .chip{
            padding:0.35rem 0.7rem;
            border-radius:999px;
            background:rgba(244,200,74,.22);
            border:1px solid rgba(244,200,74,.40);
            font-size:0.82rem;
            font-weight:700;
            color:#1F2937;
            white-space:nowrap;
            line-height:1.2;
          }

          .tag{
            display:inline-flex;
            align-items:center;
            gap:.5rem;
            padding:.35rem .65rem;
            border-radius: 999px;
            background: rgba(244,200,74,.22);
            border: 1px solid rgba(244,200,74,.40);
            color: rgba(17,24,39,.85);
            font-size:.82rem;
            font-weight: 700;
          }

          .subtle{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.55;
          }

          .hr{
            height: 1px;
            background: rgba(17,24,39,.10);
            border: 0;
            margin: 1.15rem 0;
          }

          code{
            background: rgba(17,24,39,.06);
            padding: .12rem .35rem;
            border-radius: .45rem;
            border: 1px solid rgba(17,24,39,.08);
            font-size: .92em;
          }

          .stExpander > button {
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
          }
        </style>
        """
    ).strip(),
    unsafe_allow_html=True,
)


# =========================
# Helper: card renderer
# =========================
def info_card(title: str, body_html: str, icon: str = "📌"):
    body_html = textwrap.dedent(body_html).strip()
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="card">
              <div class="card-title"><span class="icon">{icon}</span><div>{title}</div></div>
              <div class="card-body">{body_html}</div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


# =========================
# Header + Metrics
# =========================
st.markdown(
    textwrap.dedent(
        """
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
          <div>
            <div class="tag">🧱 Section 4</div>
            <div style="height:.45rem"></div>
            <h1>Neural Network (MLP): Catching the Hidden Signals</h1>
            <div class="subtle">High-precision model focused on profit-first validation and top-decile concentration.</div>
          </div>
        </div>
        <hr class="hr"/>
        """
    ).strip(),
    unsafe_allow_html=True,
)

# Metrics (your values)
MLP_ARCH = "(64, 32, 16)"
MLP_LIFT_TOP10 = 3.74
MLP_TEST_PROFIT = 14718
WAVE2_ELIGIBLE = 118_000
WAVE2_SELECTED_APPROX = 18_000
AUC = 0.780  # <-- your AUC

m1, m2, m3, m4 = st.columns(4)
m1.metric("Architecture", MLP_ARCH)
m2.metric("Top-Decile Lift (Top 10%)", f"{MLP_LIFT_TOP10:.2f}")
m3.metric("Expected Profit (Test)", f"${MLP_TEST_PROFIT:,.0f}")
m4.metric("Wave-2 Eligible Pool", f"{WAVE2_ELIGIBLE:,.0f}")

st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)

# =========================
# Executive Summary (TOP) — FINAL FIX (no code-block rendering)
# =========================
exec_html = (
    f'<div class="card" id="exec-summary-top">'
    f'  <div class="chip-row">'
    f'    <div class="chip">📈 AUC: {AUC:.3f}</div>'
    f'    <div class="chip">🔝 Top-Decile Lift: {MLP_LIFT_TOP10:.2f}×</div>'
    f'    <div class="chip">💰 Expected Profit: ${MLP_TEST_PROFIT:,.0f}</div>'
    f"  </div>"
    f'  <div class="card-title"><span class="icon">✅</span><div>Executive Summary</div></div>'
    f'  <div class="card-body">'
    f"    <ul>"
    f"      <li><b>Heavy hitter:</b> MLP captures non-linear patterns and interaction effects missed by linear models.</li>"
    f"      <li><b>Top-decile focus:</b> High concentration in the top 10% reduces mailing waste and increases ROI.</li>"
    f"      <li><b>Profit-first validation:</b> Evaluated by Expected Profit, not just accuracy.</li>"
    f"    </ul>"
    f'    <div class="subtle" style="margin-top:0.5rem;">'
    f"      Wave-2 eligible pool: <b>{WAVE2_ELIGIBLE:,}</b> "
    f"      (Selected for targeting: ~<b>{WAVE2_SELECTED_APPROX:,}</b> leads)"
    f"    </div>"
    f"  </div>"
    f"</div>"
)

st.markdown(exec_html, unsafe_allow_html=True)

with st.expander("Implementation notes", expanded=False):
    st.markdown(
        """
        If desired, we can include:
        - Coefficient-like feature importances,
        - Top-decile precision/recall slices,
        - Uplift or incremental profit slices for the selected ~18k leads.

        These outputs help translate model outputs into concrete campaign rules and A/B test designs.
        """
    )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)

# =========================
# Main content
# =========================
left, right = st.columns([1.7, 1])

with left:
    st.subheader("1. High-Level Performance Snapshot")

    info_card(
        "Snapshot",
        f"""
        <p><b>Architecture:</b> {MLP_ARCH} — a tapering three-layer MLP that funnels broad signals into focused upgrade predictors.</p>
        <p><b>Top-Decile Lift:</b> {MLP_LIFT_TOP10:.2f} — the top 10% of scored customers are ~{MLP_LIFT_TOP10:.2f}× more likely to respond than random.</p>
        <p><b>Expected Profit (Test):</b> ${MLP_TEST_PROFIT:,.0f} — estimated net profit from the test partition.</p>
        <p><b>Wave-2 Eligible Pool:</b> {WAVE2_ELIGIBLE:,} (Selected: ~{WAVE2_SELECTED_APPROX:,}) — precision targeting reduces mailing costs while preserving profit potential.</p>
        """,
        icon="📈",
    )

    st.subheader("2. Why Use a Neural Network? (Executive Rationale)")

    info_card(
        "Capturing Complexity",
        """
        <p>
        Real customer behavior is not perfectly linear. The MLP detects subtle non-linear relationships
        (e.g., how geography modifies the effect of spend), which simple models cannot capture without
        extensive manual feature engineering.
        </p>
        """,
        icon="🧠",
    )

    info_card(
        "Precision Targeting",
        """
        <p>
        The MLP concentrates high-propensity customers at the top of the list — crucial for direct mail
        where unit costs matter. High top-decile lift translates directly into fewer wasted mailers and
        higher campaign ROI.
        </p>
        """,
        icon="🎯",
    )

    st.subheader("3. Inside the Engine (Architecture & Settings)")

    info_card(
        "Funnel Structure",
        """
        <p>
        The tapering design (64 → 32 → 16) lets early layers learn broad, generalizable patterns while
        deeper layers extract decisive upgrade signals.
        </p>
        """,
        icon="🏗️",
    )

    info_card(
        "Activation & Output",
        """
        <p>
        ReLU activations are used in hidden layers to speed learning and avoid vanishing gradients.
        The final layer uses a sigmoid activation to output a calibrated probability between 0 and 1.
        </p>
        """,
        icon="⚡",
    )

    info_card(
        "Training Rigor (note)",
        """
        <p>
        The model was trained using the Adam optimizer. In the implementation we used
        <code>max_iter=200</code> to balance convergence and overfitting risk — providing sufficient
        iterations for stable learning without excessive training time.
        </p>
        """,
        icon="🧪",
    )

    st.subheader("4. Performance vs. Complexity Trade-off")

    info_card(
        "Profitability",
        f"""
        <p>
        We prioritized Expected Profit as the primary validation metric. On the test set the MLP produced
        approximately ${MLP_TEST_PROFIT:,.0f}, outperforming the logistic baseline on profit while
        accepting increased model complexity.
        </p>
        """,
        icon="⚖️",
    )

    info_card(
        "Stability",
        """
        <p>
        StandardScaler was applied to numeric features (e.g., dollars, last) to stabilize training by
        removing scale differences. This improved convergence and helped generalization to the hold-out set.
        </p>
        """,
        icon="🧯",
    )

    st.subheader("5. Strategic Implementation")

    info_card(
        "Wave-2 Mailing Strategy",
        """
        <div>
          <p>Pipeline steps:</p>
          <ol style="margin:.35rem 0 0 1.15rem;">
            <li>Score all non-respondents with the trained MLP.</li>
            <li>Apply a conservative 50% Wave-2 decay and economic filter (mail cost $1.41) to compute expected incremental profit.</li>
            <li>Select the top leads that pass the profitability threshold — final selection ≈ 18,000 leads from the 118,000 eligible.</li>
          </ol>
        </div>
        """,
        icon="📬",
    )

    st.success(
        f"Final Wave-2 targeting focuses on ~{WAVE2_SELECTED_APPROX:,} leads (from {WAVE2_ELIGIBLE:,} eligible) with the highest ROI potential."
    )

with right:
    st.subheader("Quick Executive Recap")

    st.markdown(
        """
        - Captures non-linear relationships and interaction effects<br>
        - Produces strong top-decile concentration for cost-sensitive direct mail targeting<br>
        - Validated using Expected Profit and business thresholds (mail cost & decay)
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Model Settings", expanded=False):
        st.markdown(
            f"""
            - Architecture: {MLP_ARCH}
            - Hidden activation: ReLU
            - Output activation: Sigmoid
            - Optimizer: Adam
            - Max iterations (implementation): 200
            - Scaling: StandardScaler
            """
        )

st.markdown('<hr class="hr"/>', unsafe_allow_html=True)
st.caption("Neural Network (MLP)")
