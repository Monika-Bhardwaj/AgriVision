import pandas as pd
import os
from prophet import Prophet
import pickle

# --- File paths ---
yield_file = "data/yield_df.csv"  # Your crop yield dataset
sat_file = "data/satellite_data/processed_satellite.csv"  # Your processed satellite data
model_dir = "model/saved_models/prophet_models"
os.makedirs(model_dir, exist_ok=True)

# --- Load datasets ---
df_yield = pd.read_csv(yield_file)
df_sat = pd.read_csv(sat_file)

print("Yield columns:", df_yield.columns)
print("Satellite columns:", df_sat.columns)

# --- Rename satellite columns to avoid conflicts ---
df_sat.rename(columns={
    "Temperature": "Temperature_sat",
    "Rainfall": "Rainfall_sat",
    "NDVI": "NDVI_sat"
}, inplace=True)

# Rename yield columns for clarity
df_yield.rename(columns={
    "avg_temp": "Temperature_yield",
    "average_rain_fall_mm_per_year": "Rainfall_yield",
    "hg/ha_yield": "Yield",
    "Item": "Crop"
}, inplace=True)

# --- Merge datasets on Crop ---
df = pd.merge(df_yield, df_sat, left_on="Crop", right_on="Crop_Type", how="left")
print("✅ Merged dataset shape:", df.shape)

# --- Drop unnecessary or NA rows ---
required_columns = ['Yield', 'NDVI_sat', 'Temperature_sat', 'Rainfall_sat', 'Humidity', 'Soil_Moisture']
df = df.dropna(subset=required_columns)
print("✅ Dataset after dropping missing values:", df.shape)

# --- Train Prophet models for each crop ---
crops = df['Crop'].unique()
for crop in crops:
    print(f"Training model for {crop}...")
    
    df_crop = df[df['Crop'] == crop][['Year', 'Yield']].copy()
    df_crop.rename(columns={"Year": "ds", "Yield": "y"}, inplace=True)
    
    # Prophet requires datetime, convert Year to datetime
    df_crop['ds'] = pd.to_datetime(df_crop['ds'], format='%Y')
    
    model = Prophet()
    model.fit(df_crop)
    
    # Save model with pickle
    crop_file = os.path.join(model_dir, f"{crop}_prophet.pkl")
    with open(crop_file, "wb") as f:
        pickle.dump(model, f)
    
    print(f"✅ Saved Prophet model for {crop} at {crop_file}")

print("🎉 All available crop models trained and saved!")

# --- Optional: save merged dataset for dashboard ---
df.to_csv("data/merged_crop_data.csv", index=False)
