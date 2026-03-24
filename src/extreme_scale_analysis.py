import pandas as pd

# Load cleaned enrolment data
enrol = pd.read_csv("data/processed/enrolment_clean.csv")

# Total enrolment per row
enrol["total_enrolment"] = (
    enrol["age_0_5"]
    + enrol["age_5_17"]
    + enrol["age_18_greater"]
)

# Aggregate to STATE level (CRITICAL FIX)
state_totals = (
    enrol
    .groupby("state", as_index=False)["total_enrolment"]
    .sum()
)

# National total
national_total = state_totals["total_enrolment"].sum()

# Share of national load
state_totals["national_share_percent"] = (
    state_totals["total_enrolment"] / national_total * 100
)

# Sort by dominance
state_totals = state_totals.sort_values(
    by="total_enrolment",
    ascending=False
)

# Cumulative contribution
state_totals["cumulative_share_percent"] = (
    state_totals["national_share_percent"].cumsum()
)

# Save for dashboard & report
state_totals.to_csv(
    "outputs/tables/state_enrolment_extremes.csv",
    index=False
)

print("[OK] Extreme-scale enrolment analysis complete")
print("Top 5 states by enrolment:")
print(state_totals.head())
