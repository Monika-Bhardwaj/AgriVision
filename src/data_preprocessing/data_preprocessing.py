import pandas as pd
import os

def load_processed_data(data_path="data/processed/processed_data.csv"):
    """Load processed dataset for dashboard & ML models."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{data_path} not found. Run preprocessing first.")
    return pd.read_csv(data_path)


def preprocess_raw_data(raw_path="data/raw/merged_crop_data.csv",
                        sat_path="data/raw/processed_satellite.csv",
                        output_path="data/processed/processed_data.csv"):
    """Example preprocessing pipeline to merge raw & satellite data."""
    # Load
    raw_df = pd.read_csv(raw_path)
    sat_df = pd.read_csv(sat_path)

    # Merge (placeholder logic, adapt for real pipeline)
    df = pd.merge(raw_df, sat_df, left_on="Crop", right_on="Crop_Type", how="left")

    # Drop duplicates / NaNs
    df = df.drop_duplicates().dropna(how="any")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Processed data saved to {output_path}")
    return df
