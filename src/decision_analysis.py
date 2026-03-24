import pandas as pd
import os

PROCESSED = "data/processed"
OUTPUTS = "outputs/tables"
os.makedirs(OUTPUTS, exist_ok=True)

# --------------------------------------------------
# Load processed datasets
# --------------------------------------------------
enrol = pd.read_csv(os.path.join(PROCESSED, "enrolment_clean.csv"))
bio = pd.read_csv(os.path.join(PROCESSED, "biometric_clean.csv"))
demo = pd.read_csv(os.path.join(PROCESSED, "demographic_clean.csv"))

# --------------------------------------------------
# Prepare totals
# --------------------------------------------------
enrol["total_enrolment"] = (
    enrol["age_0_5"] + enrol["age_5_17"] + enrol["age_18_greater"]
)

bio_cols = [c for c in bio.columns if c not in ["state", "date"]]
bio["total_biometric"] = bio[bio_cols].sum(axis=1)

demo_cols = [c for c in demo.columns if c not in ["state", "date"]]
demo["total_demographic"] = demo[demo_cols].sum(axis=1)

# --------------------------------------------------
# Merge (state + date)
# --------------------------------------------------
df = enrol[["state", "date", "total_enrolment"]] \
    .merge(bio[["state", "date", "total_biometric"]],
           on=["state", "date"], how="inner") \
    .merge(demo[["state", "date", "total_demographic"]],
           on=["state", "date"], how="inner")

# --------------------------------------------------
# 1. PATTERN METRIC: Biometric Load Ratio
# --------------------------------------------------
df["bio_to_enrol_ratio"] = df["total_biometric"] / df["total_enrolment"]

state_profile = (
    df.groupby("state")
    .agg(
        avg_enrolment=("total_enrolment", "mean"),
        avg_biometric=("total_biometric", "mean"),
        avg_demographic=("total_demographic", "mean"),
        avg_bio_to_enrol=("bio_to_enrol_ratio", "mean")
    )
    .reset_index()
)

state_profile.to_csv(
    os.path.join(OUTPUTS, "state_risk_profile.csv"),
    index=False
)

# --------------------------------------------------
# 2. ANOMALY DETECTION
# --------------------------------------------------
mean_ratio = state_profile["avg_bio_to_enrol"].mean()
std_ratio = state_profile["avg_bio_to_enrol"].std()

anomalies = state_profile[
    state_profile["avg_bio_to_enrol"] > mean_ratio + 2 * std_ratio
]

anomalies.to_csv(
    os.path.join(OUTPUTS, "anomalous_states.csv"),
    index=False
)

# --------------------------------------------------
# 3. PREDICTIVE INDICATOR (Lag-based)
# --------------------------------------------------
df = df.sort_values(["state", "date"])
df["enrolment_growth"] = (
    df.groupby("state")["total_enrolment"]
    .pct_change()
)

predictive = (
    df.groupby("state")["enrolment_growth"]
    .mean()
    .reset_index()
    .rename(columns={"enrolment_growth": "avg_enrolment_growth"})
)

predictive.to_csv(
    os.path.join(OUTPUTS, "predictive_pressure_states.csv"),
    index=False
)

# --------------------------------------------------
# 4. DECISION FRAMEWORK: Priority Intervention
# --------------------------------------------------
decision = state_profile.merge(
    predictive, on="state", how="left"
)

decision["priority_flag"] = (
    (decision["avg_bio_to_enrol"] > mean_ratio) &
    (decision["avg_enrolment"] > decision["avg_enrolment"].mean())
)

decision[decision["priority_flag"]].to_csv(
    os.path.join(OUTPUTS, "priority_intervention_states.csv"),
    index=False
)

print("[OK] Decision-oriented analysis completed")
print("Generated tables in outputs/tables/")
