# 🌾 AgriVision – AI-powered Crop Recommendation & Yield Forecasting

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)  
[![Dash](https://img.shields.io/badge/Dash-2.x-lightgrey.svg?logo=plotly)](https://dash.plotly.com/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b.svg?logo=streamlit)](https://streamlit.io/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Build with Love](https://img.shields.io/badge/Built%20with-❤️-red)](#)  

---

AgriVision helps farmers, agritech startups, and policymakers make **smarter crop decisions** using **AI-driven yield forecasting** and **climate-aware recommendations**.  
It integrates **satellite data, environmental features, and historical yield records** into an **interactive dashboard**.

---

## 🚀 Features
✅ **Crop Recommendation** – suggests best crops for higher yield  
✅ **AI-powered Forecasting** – Prophet model for time-series yield prediction  
✅ **Interactive Dashboard** – built with Dash & Plotly for data exploration  
✅ **Environmental Insights** – analyze NDVI, rainfall, temperature & soil moisture impact  
✅ **Geospatial Analytics** – choropleth & geo maps for country-level visualization  

---

## 📂 Project Structure
AgriVision/
├── data/ # Raw & processed datasets
│ ├── raw/
│ ├── processed/
├── notebooks/ # Jupyter notebooks (EDA, modeling, forecasting)
│ ├── 01_data_preprocessing.ipynb
│ ├── 02_exploratory_analysis.ipynb
│ └── 03_modeling_forecasting.ipynb
├── src/ # Model training scripts
│ └── model/
│ └── prophet_model_trainer.py
├── dashboard/ # Interactive Dash application
│ └── dashboard.py
├── docs/ # Documentation
│ └── project_overview.md
├── requirements.txt # Python dependencies
├── README.md # This file 🚀
└── LICENSE # MIT License

---

## ⚡ Quickstart

### 1️⃣ Clone Repository
```bash
git clone [https://github.com/Monika-Bhardwaj/AgriVision.git](https://github.com/Monika-Bhardwaj/AgriVision.git)
cd AgriVision

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Dashboard
python dashboard/dashboard.py

Open 👉 http://127.0.0.1:8050 in your browser 🌐

---

📓 Notebooks

🔹 01_data_preprocessing.ipynb → Clean & merge FAO + satellite data
🔹 02_exploratory_analysis.ipynb → Visualize trends & feature correlations
🔹 03_modeling_forecasting.ipynb → Build Prophet-based yield forecasting models

---

🛠 Tech Stack

Languages: Python 3.10+

Data Science: Pandas, NumPy, Prophet

Visualization: Plotly, Seaborn

Dashboard: Dash (Plotly) + Bootstrap

Data Sources: FAO, Remote Sensing (NDVI, Rainfall, Soil Moisture, Temperature)

---

### 🌾 Crop Yield & Smart Recommendations Dashboard:

Dark theme with glowing KPIs

Interactive dropdowns and filters

Global maps + recommendations

![Metrics Evaluation](images/{ED44E6ED-A8CF-42BA-ACD7-69960557A3DA}.png)

![Yield Trend Over Years](images/{B47088AF-33CE-4EFD-B478-CBFD462622CA}.png)

![Production HeatMap Animation](images/{B4287394-A66F-4BD0-B7E6-250A462D47AB}.png)

![Recommendation Model](images/{8D2192BB-DB13-4134-AF46-3BD39941381C}.png)

---

🌍 Vision & Future Innovations

AgriVision isn’t just a dashboard — it’s the foundation for future agricultural intelligence systems.
Planned innovations include:

🔮 AI-driven Crop Disease Prediction – early detection from satellite + drone imagery
🤖 Automated IoT Integration – real-time soil & weather sensor data
🌱 Personalized Farming Assistant – chatbot for farmers (multi-language support)
📡 Blockchain-based Crop Data Sharing – secure & transparent farmer-to-market insights
🚜 Smart Farming Advisory System – combines weather forecasts + AI recommendations for sustainable practices

---

📜 License

This project is licensed under the MIT License – free to use, modify, and distribute.
See the LICENSE file for details.

---

💡 About AgriVision

AgriVision is a startup initiative dedicated to solving global food security challenges through data-driven agriculture.
We believe in empowering farmers with AI, making agriculture smarter, resilient, and sustainable.

🌱 "Sowing Data, Harvesting Insights."

