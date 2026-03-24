import pandas as pd
import glob
import os
import sys

# ============================================================
# PATH CONFIG
# ============================================================

RAW_BASE = "data/raw"
PROCESSED_BASE = "data/processed"

ENROLMENT_PATH = os.path.join(RAW_BASE, "enrolment")
BIOMETRIC_PATH = os.path.join(RAW_BASE, "biometric")
DEMOGRAPHIC_PATH = os.path.join(RAW_BASE, "demographic")

os.makedirs(PROCESSED_BASE, exist_ok=True)

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def normalize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )
    return df


def load_and_concat(folder_path):
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    frames = []
    for f in files:
        df = pd.read_csv(f)
        df = normalize_columns(df)
        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def standardize_common_fields(df):
    df["state"] = df["state"].astype(str).str.strip().str.upper()
    df["district"] = df["district"].astype(str).str.strip().str.upper()
    df["pincode"] = pd.to_numeric(df["pincode"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def clean_numeric_columns(df, cols):
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def ensure_columns(df, required):
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

# ============================================================
# ENROLMENT CLEANING
# ============================================================

def clean_enrolment():
    print("[INFO] Cleaning ENROLMENT dataset")

    df = load_and_concat(ENROLMENT_PATH)
    df = standardize_common_fields(df)

    age_cols = ["age_0_5", "age_5_17", "age_18_greater"]
    ensure_columns(df, ["date", "state", "district", "pincode"] + age_cols)

    df = clean_numeric_columns(df, age_cols)

    df = df.dropna(subset=["date", "state"])
    df = df[(df[age_cols] >= 0).all(axis=1)]

    df_clean = (
        df.groupby(["state", "date"], as_index=False)[age_cols]
        .sum()
    )

    output = os.path.join(PROCESSED_BASE, "enrolment_clean.csv")
    df_clean.to_csv(output, index=False)

    print(f"[OK] Enrolment cleaned -> {df_clean.shape[0]} rows")
    return df_clean

# ============================================================
# BIOMETRIC CLEANING
# ============================================================

def clean_biometric():
    print("[INFO] Cleaning BIOMETRIC dataset")

    df = load_and_concat(BIOMETRIC_PATH)
    df = standardize_common_fields(df)

    # Support BOTH naming styles
    if "bio_age_5" in df.columns and "bio_age_17" in df.columns:
        bio_cols = ["bio_age_5", "bio_age_17"]
    elif "bio_age_5_17" in df.columns and "bio_age_17_" in df.columns:
        bio_cols = ["bio_age_5_17", "bio_age_17_"]
    else:
        raise ValueError("Biometric age columns not found")

    ensure_columns(df, ["date", "state"] + bio_cols)
    df = clean_numeric_columns(df, bio_cols)

    df = df.dropna(subset=["date", "state"])
    df = df[(df[bio_cols] >= 0).all(axis=1)]

    df_clean = (
        df.groupby(["state", "date"], as_index=False)[bio_cols]
        .sum()
    )

    output = os.path.join(PROCESSED_BASE, "biometric_clean.csv")
    df_clean.to_csv(output, index=False)

    print(f"[OK] Biometric cleaned -> {df_clean.shape[0]} rows")
    return df_clean

# ============================================================
# DEMOGRAPHIC CLEANING
# ============================================================

def clean_demographic():
    print("[INFO] Cleaning DEMOGRAPHIC dataset")

    df = load_and_concat(DEMOGRAPHIC_PATH)
    df = standardize_common_fields(df)

    if "demo_age_5" in df.columns and "demo_age_17" in df.columns:
        demo_cols = ["demo_age_5", "demo_age_17"]
    elif "demo_age_5_17" in df.columns and "demo_age_17_" in df.columns:
        demo_cols = ["demo_age_5_17", "demo_age_17_"]
    else:
        raise ValueError("Demographic age columns not found")

    ensure_columns(df, ["date", "state"] + demo_cols)
    df = clean_numeric_columns(df, demo_cols)

    df = df.dropna(subset=["date", "state"])
    df = df[(df[demo_cols] >= 0).all(axis=1)]

    df_clean = (
        df.groupby(["state", "date"], as_index=False)[demo_cols]
        .sum()
    )

    output = os.path.join(PROCESSED_BASE, "demographic_clean.csv")
    df_clean.to_csv(output, index=False)

    print(f"[OK] Demographic cleaned -> {df_clean.shape[0]} rows")
    return df_clean

# ============================================================
# MAIN PIPELINE
# ============================================================

def main():
    try:
        e = clean_enrolment()
        b = clean_biometric()
        d = clean_demographic()

        print("\n[OK] ALL CSV FILES CLEANED & CONSOLIDATED")
        print("---------------------------------------")
        print("Enrolment rows :", e.shape[0])
        print("Biometric rows :", b.shape[0])
        print("Demographic rows:", d.shape[0])

    except Exception as ex:
        print("\n[ERROR] CLEANING FAILED")
        print(str(ex))
        sys.exit(1)

if __name__ == "__main__":
    main()
