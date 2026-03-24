import pandas as pd

df = pd.read_csv("outputs/tables/state_enrolment_extremes.csv")

# How many states account for X% load?
thresholds = [50, 80, 90]
results = []

for t in thresholds:
    count = df[df["cumulative_share_percent"] <= t].shape[0]
    results.append({
        "threshold_percent": t,
        "states_required": count
    })

dominance = pd.DataFrame(results)

dominance.to_csv(
    "outputs/tables/state_dominance_summary.csv",
    index=False
)

print("[OK] State dominance analysis complete")
print(dominance)
