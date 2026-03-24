import pandas as pd
import numpy as np
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor

# --------------------------------------------------
# Paths
# --------------------------------------------------
INPUT_PATH = "outputs/tables"
OUTPUT_PATH = "outputs/tables"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# --------------------------------------------------
# Load state-level risk profile
# --------------------------------------------------
df = pd.read_csv(os.path.join(INPUT_PATH, "state_risk_profile.csv"))

# Base features (guaranteed to exist)
features = [
    "avg_enrolment",
    "avg_biometric",
    "avg_demographic",
    "avg_bio_to_enrol"
]

# Optional predictive feature
if "avg_enrolment_growth" in df.columns:
    features.append("avg_enrolment_growth")

X = df[features].fillna(0)
# Base features (guaranteed to exist)
features = [
    "avg_enrolment",
    "avg_biometric",
    "avg_demographic",
    "avg_bio_to_enrol"
]

# Optional predictive feature
if "avg_enrolment_growth" in df.columns:
    features.append("avg_enrolment_growth")

X = df[features].fillna(0)


# --------------------------------------------------
# SCALE FEATURES (important for clustering)
# --------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------------------------------------------
# MODEL 1: STATE ARCHETYPES (CLUSTERING)
# --------------------------------------------------
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["state_archetype"] = kmeans.fit_predict(X_scaled)

df[["state", "state_archetype"]].to_csv(
    os.path.join(OUTPUT_PATH, "state_archetypes.csv"),
    index=False
)

# --------------------------------------------------
# MODEL 2: RISK DRIVER ANALYSIS (SUPERVISED)
# --------------------------------------------------
target = df["avg_biometric"]

rf = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
rf.fit(X, target)

importance = pd.DataFrame({
    "feature": features,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False)

importance.to_csv(
    os.path.join(OUTPUT_PATH, "risk_driver_importance.csv"),
    index=False
)

# --------------------------------------------------
# MODEL 3: CONTINUOUS RISK SCORE
# --------------------------------------------------
predicted_load = rf.predict(X)
df["risk_score"] = predicted_load / predicted_load.max()

df[["state", "risk_score"]].to_csv(
    os.path.join(OUTPUT_PATH, "state_risk_score.csv"),
    index=False
)

# --------------------------------------------------
# Console summary (for sanity check)
# --------------------------------------------------
print("[OK] ML Risk Intelligence Completed")
print("--------------------------------")
print("Generated:")
print("- state_archetypes.csv")
print("- risk_driver_importance.csv")
print("- state_risk_score.csv")
