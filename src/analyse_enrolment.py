import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
PROCESSED_PATH = "data/processed"
OUTPUT_FIGURES = "outputs/figures"
os.makedirs(OUTPUT_FIGURES, exist_ok=True)

# Load processed enrolment data
df = pd.read_csv(os.path.join(PROCESSED_PATH, "enrolment_clean.csv"))
df["date"] = pd.to_datetime(df["date"])

# -------------------------------
# 1. National-level trend
# -------------------------------
national = df.groupby("date")[["age_0_5", "age_5_17", "age_18_greater"]].sum()

plt.figure(figsize=(10, 6))
national.plot(ax=plt.gca())
plt.title("National Aadhaar Enrolment Trend by Age Group")
plt.xlabel("Date")
plt.ylabel("Total Enrolments")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIGURES, "enrolment_national_trend.png"), dpi=300)
plt.close()

# -------------------------------
# 2. State-wise total enrolment
# -------------------------------
df["total_enrolment"] = (
    df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
)

state_totals = (
    df.groupby("state")["total_enrolment"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
state_totals.plot(kind="bar")
plt.title("Top 10 States by Aadhaar Enrolment")
plt.xlabel("State")
plt.ylabel("Total Enrolments")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIGURES, "top_states_enrolment.png"), dpi=300)
plt.close()

print("[OK] Enrolment analysis completed. Figures saved.")

