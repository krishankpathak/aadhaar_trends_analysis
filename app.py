import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Aadhaar National Decision Intelligence",
    layout="wide"
)

st.title("Aadhaar National Decision Intelligence Dashboard")
st.caption(
    "System-level analysis of Aadhaar enrolment and update activity to support "
    "policy prioritisation, operational planning, and inclusion risk management."
)

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    enrol = pd.read_csv("data/processed/enrolment_clean.csv")
    bio = pd.read_csv("data/processed/biometric_clean.csv")
    demo = pd.read_csv("data/processed/demographic_clean.csv")

    extremes = pd.read_csv("outputs/tables/state_enrolment_extremes.csv")
    dominance = pd.read_csv("outputs/tables/state_dominance_summary.csv")
    stress = pd.read_csv("outputs/tables/system_stress_index.csv")
    failure = pd.read_csv("outputs/tables/state_failure_modes.csv")

    enrol["date"] = pd.to_datetime(enrol["date"])
    enrol["total_enrolment"] = (
        enrol["age_0_5"] + enrol["age_5_17"] + enrol["age_18_greater"]
    )

    return enrol, bio, demo, extremes, dominance, stress, failure

enrol, bio, demo, extremes, dominance, stress, failure = load_data()

# ============================================================
# SIDEBAR — GLOBAL FILTERS
# ============================================================
st.sidebar.header("Global Filters")

states = sorted(extremes["state"].unique())
selected_states = st.sidebar.multiselect(
    "States included in analysis",
    options=states,
    default=states
)

extremes_f = extremes[extremes["state"].isin(selected_states)]
stress_f = stress[stress["state"].isin(selected_states)]
failure_f = failure[failure["state"].isin(selected_states)]

# Resolve national share column safely
share_col = next(
    c for c in extremes_f.columns if "national" in c and "share" in c
)

# ============================================================
# SECTION 1 — NATIONAL SYSTEM OVERVIEW
# ============================================================
st.header("1. National Aadhaar System Overview")

st.markdown(
    """
    **Objective:**  
    Understand how Aadhaar enrolment load is distributed across India and
    whether system demand is evenly spread or concentrated in a few regions.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Enrolment by State (Log Scale)")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(
        extremes_f["state"],
        extremes_f["total_enrolment"],
        color="#4C72B0"
    )
    ax.set_yscale("log")
    ax.set_ylabel("Total Enrolment (log scale)")
    ax.set_xlabel("State")
    ax.tick_params(axis="x", rotation=90)
    st.pyplot(fig)

with col2:
    st.subheader("Cumulative Contribution to National Load")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(
        range(1, len(extremes_f) + 1),
        extremes_f.sort_values("total_enrolment", ascending=False)[
            "cumulative_share_percent"
        ],
        marker="o"
    )
    for y in [50, 80, 90]:
        ax.axhline(y, linestyle="--", alpha=0.6)
    ax.set_ylabel("Cumulative Share of National Enrolment (%)")
    ax.set_xlabel("States (ranked by enrolment)")
    st.pyplot(fig)

st.info(
    "Key Insight: Aadhaar enrolment activity is highly concentrated. "
    "A limited number of states account for a majority of national enrolment load, "
    "making them critical leverage points for system reliability."
)

# ============================================================
# SECTION 2 — TEMPORAL & SOCIETAL TRENDS
# ============================================================
st.header("2. Temporal and Societal Enrolment Trends")

st.markdown(
    """
    **Objective:**  
    Analyse how Aadhaar enrolment evolves over time and across age cohorts,
    revealing lifecycle dynamics and inclusion patterns.
    """
)

national_time = (
    enrol.groupby("date", as_index=False)[
        ["age_0_5", "age_5_17", "age_18_greater", "total_enrolment"]
    ].sum()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("National Enrolment Trend Over Time")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        national_time["date"],
        national_time["total_enrolment"],
        color="#55A868"
    )
    ax.set_xlabel("Time")
    ax.set_ylabel("Total Enrolment")
    st.pyplot(fig)

with col2:
    st.subheader("Age-Group Composition Over Time")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.stackplot(
        national_time["date"],
        national_time["age_0_5"],
        national_time["age_5_17"],
        national_time["age_18_greater"],
        labels=["Age 0–5", "Age 5–17", "Age 18+"],
        alpha=0.9
    )
    ax.legend(loc="upper left")
    ax.set_ylabel("Enrolment Volume")
    st.pyplot(fig)

st.info(
    "Key Insight: Aadhaar demand shows a gradual transition from early-age enrolment "
    "towards adult-centric updates, indicating a shift from expansion to lifecycle maintenance."
)

# ============================================================
# SECTION 3 — OPERATIONAL STRESS & FAILURE MODES
# ============================================================
st.header("3. Operational Stress and Failure Modes")

st.markdown(
    """
    **Objective:**  
    Translate anomalies into system-level risks by identifying where Aadhaar
    operations experience sustained stress or potential failure conditions.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("System Stress Index by State")
    stress_sorted = stress_f.sort_values(
        "system_stress_index", ascending=False
    )
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(
        stress_sorted["state"],
        stress_sorted["system_stress_index"],
        color="#C44E52"
    )
    ax.invert_yaxis()
    ax.set_xlabel("System Stress Index")
    st.pyplot(fig)

with col2:
    st.subheader("Failure Mode Distribution Across States")
    failure_counts = failure_f["failure_mode"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(
        failure_counts.index,
        failure_counts.values,
        color="#8172B3"
    )
    ax.set_ylabel("Number of States")
    ax.tick_params(axis="x", rotation=25)
    st.pyplot(fig)

st.warning(
    "Key Insight: System stress is not uniformly distributed. "
    "High-load states disproportionately experience usage saturation, "
    "inclusion friction, and infrastructure concentration risks."
)

# ============================================================
# SECTION 4 — DECISION INTELLIGENCE & ACTION FRAMEWORK
# ============================================================
st.header("4. Decision Intelligence for Policy and Operations")

st.markdown(
    """
    **Objective:**  
    Convert analytical findings into actionable guidance that can support
    UIDAI’s operational planning, capacity allocation, and inclusion strategies.
    """
)

# ------------------------------------------------------------
# Resolve national share column safely
# ------------------------------------------------------------
share_candidates = [
    c for c in extremes_f.columns
    if ("national" in c.lower()) and ("share" in c.lower())
]

if len(share_candidates) == 0:
    st.error("National share column not found in enrolment extremes data.")
    st.stop()

share_col = share_candidates[0]

# ------------------------------------------------------------
# Build decision intelligence table defensively
# ------------------------------------------------------------
decision_table = (
    stress_f
    .merge(
        failure_f[["state", "failure_mode"]],
        on="state",
        how="left"
    )
    .merge(
        extremes_f[["state", share_col]],
        on="state",
        how="left"
    )
)

# Explicitly create the expected column
decision_table["national_share_percent"] = (
    decision_table[share_col]
    if share_col in decision_table.columns
    else 0
)

decision_table["national_share_percent"] = (
    decision_table["national_share_percent"].fillna(0)
)

decision_table = decision_table.sort_values(
    "system_stress_index", ascending=False
)

st.subheader("State-Level Decision Intelligence Table")

st.dataframe(
    decision_table[
        [
            "state",
            "national_share_percent",
            "system_stress_index",
            "failure_mode"
        ]
    ],
    use_container_width=True
)

st.success(
    "Recommended Actions:\n"
    "- High national share + high stress → proactive capacity scaling\n"
    "- High stress + inclusion failure → assisted or alternative authentication\n"
    "- Moderate stress → targeted monitoring and incremental upgrades"
)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(
    "This dashboard is fully reproducible and generated directly from the "
    "submitted analytical pipeline. It is intended as decision support, "
    "not as a standalone exploratory tool."
)
