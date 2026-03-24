import subprocess
import sys
import os

# -----------------------------------------
# Utility to run scripts safely
# -----------------------------------------
def run_step(step_name, script_path):
    print("\n" + "=" * 60)
    print(f"▶ RUNNING: {step_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ FAILED: {step_name}")
        print(result.stderr)
        sys.exit(1)
    else:
        print(f"✔ COMPLETED: {step_name}")
        print(result.stdout)


# -----------------------------------------
# PIPELINE START
# -----------------------------------------
print("\n[START] STARTING AADHAAR NATIONAL ANALYTICS PIPELINE")

# 1. Cleaning
run_step(
    "Data Cleaning",
    "src/clean.py"
)

# 2. Base Analysis (optional but reproducible)
run_step(
    "Enrolment Analysis",
    "src/analyse_enrolment.py"
)

run_step(
    "Biometric Analysis",
    "src/analyse_biometric.py"
)

run_step(
    "Demographic Analysis",
    "src/analyse_demographic.py"
)

# 3. Integrated + Decision Analysis
run_step(
    "Integrated Analysis",
    "src/integrated_analysis.py"
)

run_step(
    "Decision Analysis",
    "src/decision_analysis.py"
)

# 4. ML Risk Intelligence
run_step(
    "ML Risk Intelligence",
    "src/ml_risk_intelligence.py"
)

# 5. Extreme Scale Analysis (CORRECT AGGREGATION)
run_step(
    "Extreme Scale Analysis",
    "src/extreme_scale_analysis.py"
)

# 6. State Dominance (Pareto logic)
run_step(
    "State Dominance Analysis",
    "src/state_dominance_analysis.py"
)

# 7. System Stress Index
run_step(
    "System Stress Index",
    "src/system_stress_index.py"
)

# 8. Failure Mode Tagging
run_step(
    "Failure Mode Tagging",
    "src/failure_mode_tagging.py"
)

# -----------------------------------------
# PIPELINE END
# -----------------------------------------
print("\n[DONE] PIPELINE COMPLETED SUCCESSFULLY")
print("All outputs generated in outputs/tables/")
print("You now have a NATIONAL-LEVEL, SCALE-AWARE ANALYTICS SYSTEM")
