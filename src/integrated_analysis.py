import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
PROCESSED_PATH = "data/processed"
OUTPUT_FIGURES = "outputs/figures"
os.makedirs(OUTPUT_FIGURES, exist_ok=True)

# -------------------------------
# Load processed datasets
# -------------------------------
enrol = pd.read_csv(os.path.join(PROCESSED_PATH, "enrolment_clean.csv"))
bio = pd.read_csv(os.path.join(PROCESSED_PATH, "biometric_clean.csv"))
demo = pd.read_csv(os.path.join(PROCESSED_PATH, "demographic_clean.csv"))

enrol["date"] = pd.to_datetime(enrol["date"])
bio["date"] = pd.to_datetime(bio["date"])
demo["date"] = pd.to_datetime(demo["date"])

# -------------------------------
# Harmonise metrics
# -------------------------------
enrol["total_enrolment"] = enrol[
    ["age_0_5", "age_5_17", "age_18_greater"]
].sum(axis=1)

bio_cols = [c for c in bio.columns if c not in ["state", "date"]]
bio["total_biometric"] = bio[bio_cols].sum(axis=1)

demo_cols = [c for c in demo.columns if c not in ["state", "date"]]
demo["total_demographic"] = demo[demo_cols].sum(axis=1)

# -------------------------------
# Merge datasets (state + date)
# -------------------------------
merged = enrol[["state", "date", "total_enrolment"]] \
    .merge(bio[["state", "date", "total_biometric"]],
           on=["state", "date"], how="inner") \
    .merge(demo[["state", "date", "total_demographic"]],
           on=["state", "date"], how="inner")

# -------------------------------
# 1. Correlation Analysis
# -------------------------------
corr = merged[
    ["total_enrolment", "total_biometric", "total_demographic"]
].corr()

print("\nCorrelation Matrix:")
print(corr)

# -------------------------------
# 2. Enrolment vs Biometric Load
# -------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(
    merged["total_enrolment"],
    merged["total_biometric"],
    alpha=0.5
)
plt.xlabel("Total Enrolment")
plt.ylabel("Total Biometric Activity")
plt.title("Enrolment vs Biometric Load")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_FIGURES, "enrolment_vs_biometric.png"),
    dpi=300
)
plt.close()

# -------------------------------
# 3. Demographic Pressure vs Usage
# -------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(
    merged["total_demographic"],
    merged["total_biometric"],
    alpha=0.5
)
plt.xlabel("Demographic Volume")
plt.ylabel("Biometric Activity")
plt.title("Demographic Pressure vs Biometric Usage")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_FIGURES, "demographic_vs_biometric.png"),
    dpi=300
)
plt.close()

print("[OK] Integrated analysis completed. Figures saved.")
