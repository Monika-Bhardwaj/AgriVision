import pandas as pd
from prophet import Prophet
import plotly.express as px

class ProphetModelTrainer:
    """
    Wrapper class for training and forecasting crop yields using Facebook Prophet.
    """

    def __init__(self):
        """Initialize the Prophet forecaster with default parameters."""
        self.model = None
        self.forecast = None

    def prepare_data(self, df, crop_name):
        """
        Prepares crop-specific data for Prophet.
        
        Args:
            df (pd.DataFrame): Dataset with Year & Yield columns.
            crop_name (str): Crop name to filter.
        
        Returns:
            pd.DataFrame: Data formatted for Prophet.
        """
        crop_df = df[df["Crop"] == crop_name][["Year", "Yield"]].dropna()
        if crop_df.empty:
            return pd.DataFrame(columns=["ds", "y"])

        # Prophet expects 'ds' as datetime and 'y' as target
        crop_df = crop_df.rename(columns={"Year": "ds", "Yield": "y"})
        crop_df["ds"] = pd.to_datetime(crop_df["ds"], format="%Y")
        return crop_df

    def train(self, df, crop_name):
        """
        Trains a Prophet model on historical crop yield data.
        
        Args:
            df (pd.DataFrame): Input dataset with Year & Yield.
            crop_name (str): Crop to forecast.
        """
        data = self.prepare_data(df, crop_name)
        if data.empty:
            return None

        self.model = Prophet(yearly_seasonality=True, daily_seasonality=False, weekly_seasonality=False)
        self.model.fit(data)

        # Create future dataframe (next 5 years)
        future = self.model.make_future_dataframe(periods=5, freq="Y")
        self.forecast = self.model.predict(future)
        return self.forecast

    def forecast_crop(self, df, crop_name):
        """
        Generates a forecast figure for the given crop.
        
        Args:
            df (pd.DataFrame): Dataset with Year & Yield.
            crop_name (str): Crop to forecast.
        
        Returns:
            plotly.graph_objects.Figure: Forecast visualization.
        """
        forecast = self.train(df, crop_name)
        if forecast is None:
            return px.line(title=f"No forecast available for {crop_name}")

        # Merge actual + forecast
        data = self.prepare_data(df, crop_name)

        fig = px.line(forecast, x="ds", y="yhat", title=f"📈 Forecasted Yield for {crop_name}")
        fig.add_scatter(x=data["ds"], y=data["y"], mode="markers+lines",
                        name="Actual Yield", line=dict(width=3))
        fig.update_layout(template="plotly_dark", height=250, margin=dict(l=30, r=30, t=30, b=30))

        return fig
