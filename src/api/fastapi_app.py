from fastapi import FastAPI
import pandas as pd
import joblib
import os

app = FastAPI(title="Crop Recommendation API")

MODEL_PATH = os.getenv("MODEL_PATH", "saved_models/crop_recommender.pkl")
DATA_PATH = os.getenv("DATA_PATH", "data/processed/processed_data.csv")

model = joblib.load(MODEL_PATH)
data = pd.read_csv(DATA_PATH)

features = ["Rainfall_sat", "Temperature_sat", "NDVI_sat"]

@app.get("/")
def home():
    return {"message": "🌱 Crop Recommendation API is running!"}

@app.post("/recommend")
def recommend(rainfall: float, temperature: float, ndvi: float):
    X = [[rainfall, temperature, ndvi]]
    prediction = model.predict(X)[0]
    return {"recommended_crop": prediction}
