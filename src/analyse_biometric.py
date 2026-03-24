import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
PROCESSED_PATH = "data/processed"
OUTPUT_FIGURES = "outputs/figures"
os.makedirs(OUTPUT_FIGURES, exist_ok=True)

# Load biometric data
df = pd.read_csv(os.path.join(PROCESSED_PATH, "biometric_clean.csv"))
df["date"] = pd.to_datetime(df["date"])

# Identify biometric columns dynamically (safety)
biometric_cols = [c for c in df.columns if c not in ["state", "date"]]

# -------------------------------
# 1. National biometric activity trend
# -------------------------------
national = df.groupby("date")[biometric_cols].sum()

plt.figure(figsize=(10, 6))
national.plot(ax=plt.gca())
plt.title("National Biometric Activity Trend")
plt.xlabel("Date")
plt.ylabel("Total Biometric Transactions")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIGURES, "biometric_national_trend.png"), dpi=300)
plt.close()

# -------------------------------
# 2. State-wise biometric volume
# -------------------------------
df["total_biometric"] = df[biometric_cols].sum(axis=1)

state_totals = (
    df.groupby("state")["total_biometric"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
state_totals.plot(kind="bar")
plt.title("Top 10 States by Biometric Activity")
plt.xlabel("State")
plt.ylabel("Total Biometric Transactions")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FIGURES, "top_states_biometric.png"), dpi=300)
plt.close()

print("[OK] Biometric analysis completed. Figures saved.")
