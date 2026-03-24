import pandas as pd

df = pd.read_csv("outputs/tables/system_stress_index.csv")

def assign_failure_mode(row):
    if row["national_share_percent"] > 10 and row["avg_bio_to_enrol"] > 1.5:
        return "Usage Saturation Failure"
    elif row["avg_bio_to_enrol"] > 2:
        return "Inclusion Friction Failure"
    elif row["national_share_percent"] > 15:
        return "Infrastructure Concentration Risk"
    else:
        return "Stable / Monitor"

df["failure_mode"] = df.apply(assign_failure_mode, axis=1)

df.to_csv(
    "outputs/tables/state_failure_modes.csv",
    index=False
)

print("[OK] Failure modes assigned")
print(df[["state", "failure_mode"]].value_counts())
