import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import joblib

# Create output directories
Path("models").mkdir(exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Load cleaned dataset
df = (
    pd.read_parquet("data/interim/02_cleaned.parquet")
    .sort_values("timestamp")
)

# Feature Engineering
# Biological rationale:
# Mushroom yield is influenced by both temperature and humidity together,
# so an interaction feature may capture combined environmental effects.
df["temp_humid_interaction"] = (
    df["temperature_c"] * df["humidity_pct"] / 100
)

# Versioned feature list
FEATURE_COLS = [
    "temperature_c",
    "humidity_pct",
    "co2_ppm",
    "temp_humid_interaction",
]

TARGET_COL = "yield_kg"

# Separate features and target
X = df[FEATURE_COLS]
y = df[TARGET_COL]

# NOTE:
# For Task 4, scaling is demonstrated on the full dataset.
# On Day 8 this will be refactored so the scaler is fit only on
# training data to prevent data leakage.
scaler = MinMaxScaler()

# Fit and transform features
X_scaled = scaler.fit_transform(X)

# Save scaler for future model inference
joblib.dump(
    scaler,
    "models/minmax_scaler.joblib"
)

# Create processed dataframe
processed = pd.DataFrame(
    X_scaled,
    columns=[f"{c}_scaled" for c in FEATURE_COLS]
)

processed[TARGET_COL] = y.values

# Save processed features
processed.to_parquet(
    "data/processed/features.parquet",
    index=False
)

# -------------------------
# Validation Checks
# -------------------------

print("\n=== Validation Checks ===")

# 1. Shape alignment
print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")

assert len(X) == len(y), "ERROR: X and y row counts do not match."

# 2. Missing values
print("\nMissing values per column:")
print(processed.isna().sum())

assert not processed.isna().any().any(), (
    "ERROR: NaN values detected after feature engineering."
)

# 3. Verify scaled feature ranges
scaled_cols = [c for c in processed.columns if c.endswith("_scaled")]

ranges = processed[scaled_cols].agg(["min", "max"])

print("\nScaled feature ranges:")
print(ranges)

assert (ranges.loc["min"] >= 0).all(), (
    "ERROR: Some scaled values are below 0."
)

assert (ranges.loc["max"] <= 1).all(), (
    "ERROR: Some scaled values are above 1."
)