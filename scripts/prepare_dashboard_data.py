import pandas as pd
import os

# =============================
# File paths
# =============================
yield_file = "data/yield_df.csv"
sat_folder = "data/satellite_data"
output_file = "data/processed_data.csv"

print("📂 Loading datasets...")

# =============================
# Load Yield Data
# =============================
yield_df = pd.read_csv(yield_file)
print(f"✅ Yield columns: {list(yield_df.columns)}")

# Normalize columns
yield_df.rename(columns={
    "Item": "Crop",
    "hg/ha_yield": "Yield"
}, inplace=True)

# =============================
# Load Satellite Data
# =============================
sat_dfs = []
for file in os.listdir(sat_folder):
    if file.endswith(".csv"):
        path = os.path.join(sat_folder, file)
        df = pd.read_csv(path)
        print(f"✅ Loaded {path}, columns: {list(df.columns)}")
        sat_dfs.append(df)

if not sat_dfs:
    raise FileNotFoundError("⚠️ No satellite CSV files found inside data/satellite_data")

# Combine all satellite data
sat_df = pd.concat(sat_dfs, axis=0, ignore_index=True)

# Normalize crop column
if "Crop_Type" in sat_df.columns:
    sat_df.rename(columns={"Crop_Type": "Crop"}, inplace=True)

# Rename important features
sat_df.rename(columns={
    "NDVI": "NDVI_sat",
    "Temperature": "Temperature_sat",
    "Rainfall": "Rainfall_sat"
}, inplace=True)

# Remove duplicate columns
sat_df = sat_df.loc[:, ~sat_df.columns.duplicated()]

# =============================
# Aggregate satellite data per crop
# =============================
numeric_cols = sat_df.select_dtypes(include="number").columns
sat_summary = sat_df.groupby("Crop")[numeric_cols].mean().reset_index()

print(f"✅ Satellite summary shape: {sat_summary.shape}")

# =============================
# Merge Yield + Aggregated Satellite
# =============================
print("\n🔄 Merging datasets...")
df_merged = pd.merge(yield_df, sat_summary, on="Crop", how="left")

print(f"✅ Merged dataset shape: {df_merged.shape}")

# =============================
# Save Processed Data
# =============================
df_merged.to_csv(output_file, index=False)
print(f"💾 Processed dataset saved to {output_file}")

# =============================
# Dataset Summary
# =============================
print("\n📊 Dataset Summary:")
print(f"   Crops: {df_merged['Crop'].nunique()} → {df_merged['Crop'].unique()[:10]}")
print(f"   Areas: {df_merged['Area'].nunique()} → {df_merged['Area'].unique()[:10]}")
print(f"   Years: {df_merged['Year'].nunique()} → {df_merged['Year'].min()} - {df_merged['Year'].max()}")
print("   Columns:", list(df_merged.columns))
