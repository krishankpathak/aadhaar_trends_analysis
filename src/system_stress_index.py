import pandas as pd
from sklearn.preprocessing import MinMaxScaler

enrol = pd.read_csv("outputs/tables/state_enrolment_extremes.csv")
risk = pd.read_csv("outputs/tables/state_risk_profile.csv")

df = enrol.merge(
    risk,
    on="state",
    how="left"
)

features = [
    "national_share_percent",
    "avg_biometric",
    "avg_bio_to_enrol"
]

scaler = MinMaxScaler()
df["system_stress_index"] = scaler.fit_transform(
    df[features]
).mean(axis=1)

df = df.sort_values("system_stress_index", ascending=False)

df.to_csv(
    "outputs/tables/system_stress_index.csv",
    index=False
)

print("[OK] System Stress Index generated")
print(df[["state", "system_stress_index"]].head(10))
