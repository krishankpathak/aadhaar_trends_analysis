import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
PROCESSED_PATH = "data/processed"
OUTPUT_FIGURES = "outputs/figures"
os.makedirs(OUTPUT_FIGURES, exist_ok=True)

# Load demographic data
df = pd.read_csv(os.path.join(PROCESSED_PATH, "demographic_clean.csv"))
df["date"] = pd.to_datetime(df["date"])

# Identify demographic columns dynamically
demographic_cols = [c for c in df.columns if c not in ["state", "date"]]

# -------------------------------
# 1. National demographic distribution
# -------------------------------
national = df[demographic_cols].sum()

plt.figure(figsize=(8, 6))
national.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("National Demographic Distribution (Aadhaar)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_FIGURES, "demographic_national_distribution.png"),
    dpi=300
)
plt.close()

# -------------------------------
# 2. State-wise demographic pressure
# -------------------------------
df["total_population"] = df[demographic_cols].sum(axis=1)

state_totals = (
    df.groupby("state")["total_population"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
state_totals.plot(kind="bar")
plt.title("Top 10 States by Demographic Aadhaar Activity")
plt.xlabel("State")
plt.ylabel("Total Count")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_FIGURES, "top_states_demographic.png"),
    dpi=300
)
plt.close()

print("[OK] Demographic analysis completed. Figures saved.")
