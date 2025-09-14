import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# File paths
data_file = "data/processed_data.csv"
model_file = "model/saved_models/recommender_model.pkl"

# Load dataset
df = pd.read_csv(data_file)

print("📊 Columns in dataset:", df.columns.tolist())

# Rename columns for consistency
col_mapping = {
    'hg/ha_yield': 'Yield',
    'NDVI_sat': 'NDVI',
    'Temperature_sat': 'Temperature',
    'Rainfall_sat': 'Rainfall',
    'avg_temp': 'Temperature_yield',
    'average_rain_fall_mm_per_year': 'Rainfall_yield'
}
df.rename(columns=col_mapping, inplace=True)

# ✅ Select features (all available environment + yield features)
feature_cols = [
    'NDVI', 'Temperature', 'Rainfall', 'Humidity', 'Soil_Moisture',
    'pesticides_tonnes', 'Temperature_yield', 'Rainfall_yield'
]

# Keep only existing features
feature_cols = [col for col in feature_cols if col in df.columns]

print("✅ Features used:", feature_cols)

# Drop rows with missing values
df = df.dropna(subset=feature_cols + ['Item'])

# Define X and y
X = df[feature_cols]
y = df['Item']   # Crop name

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Train RandomForest classifier
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("✅ Recommender model trained successfully!")
print("🔍 Training accuracy:", model.score(X_train, y_train))
print("🔍 Testing accuracy:", model.score(X_test, y_test))

# Save model + scaler
with open(model_file, "wb") as f:
    pickle.dump({"model": model, "scaler": scaler, "features": feature_cols}, f)

print(f"🎉 Saved recommender model at {model_file}")
