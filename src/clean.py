# src/clean.py
import pandas as pd
from pathlib import Path

# Load the interim CSV data
input_file = "data/interim/01_loaded.csv"
df = pd.read_csv(input_file)

# Missing report
print("--- Initial Missing Value Report ---")
print(df.isna().sum())
print("------------------------------------\n")

# Valid ranges for oyster polyhouse
valid = (
    df["humidity_pct"].between(50, 100)
    & df["temperature_c"].between(10, 35)
    & df["co2_ppm"].between(400, 2000)
    & df["yield_kg"].notna()
)

df = df[valid].copy()

# Short gap: forward-fill sensor columns only
cols = ["temperature_c", "humidity_pct", "co2_ppm"]
df[cols] = df[cols].ffill(limit=2)

# Drop remaining rows with null target
df = df.dropna(subset=["yield_kg"])

# Duplicates by timestamp
df = df.drop_duplicates(subset=["timestamp"], keep="last")

# Save output as CSV
output_file = "data/interim/02_cleaned.csv"

# Ensure the directory exists just in case
Path(output_file).parent.mkdir(parents=True, exist_ok=True)

# index=False ensures we don't save the pandas row numbers as a new column
df.to_csv(output_file, index=False)

print(f"Clean rows: {len(df)}")