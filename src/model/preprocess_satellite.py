import pandas as pd
import os

# Paths
sat_file = "data/satellite_data/crop_health_env_stress.csv"
processed_file = "data/satellite_data/processed_satellite.csv"

# Load satellite data
sat_df = pd.read_csv(sat_file)
print("Columns:", list(sat_df.columns))
print("Sample data:\n", sat_df.head())

# Keep only relevant columns for modeling
required_cols = [
    'Crop_Type', 'NDVI', 'Temperature', 'Rainfall',
    'Humidity', 'Soil_Moisture'
]

# Check missing columns
for col in required_cols:
    if col not in sat_df.columns:
        raise ValueError(f"❌ Column '{col}' not found in satellite dataset!")

sat_df = sat_df[required_cols]

# Aggregate by crop type (mean values)
sat_agg = sat_df.groupby('Crop_Type').agg({
    'NDVI': 'mean',
    'Temperature': 'mean',
    'Rainfall': 'mean',
    'Humidity': 'mean',
    'Soil_Moisture': 'mean'
}).reset_index()

# Save processed satellite data
os.makedirs(os.path.dirname(processed_file), exist_ok=True)
sat_agg.to_csv(processed_file, index=False)
print(f"✅ Processed satellite data saved at {processed_file}")
