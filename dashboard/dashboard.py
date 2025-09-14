import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import os

# =====================
# 🎨 Theme
# =====================
THEME = {
    "background": "#121212",   # black
    "card_bg": "#1E1E1E",      # dark gray
    "text": "#FFFFFF",         # white
    "accent_blue": "#7EC8E3",  # pastel blue
    "accent_green": "#A1E887", # pastel green
    "accent_purple": "#CBA6F7" # pastel purple
}

# =====================
# 📂 Load Dataset
# =====================
df = pd.read_csv("data/processed/processed_data.csv")

if "Crop" not in df.columns:
    df.rename(columns={"Item": "Crop", "hg/ha_yield": "Yield"}, inplace=True)

# =====================
# ⚡ Dash App
# =====================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# =====================
# 📊 Helper Functions
# =====================
def kpi_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, style={"color": "white"}),
            html.H3(value, style={
                "color": "white",
                "textShadow": f"0 0 10px {color}, 0 0 20px {color}"
            })
        ]),
        style={
            "backgroundColor": THEME["card_bg"],
            "borderRadius": "12px",
            "boxShadow": f"0 0 20px {color}50",
            "margin": "10px",
            "textAlign": "center"
        }
    )

def make_comparison_graph(current_crop, best_crop, data):
    df_current = data[data["Crop"] == current_crop].groupby("Year")["Yield"].mean().reset_index()
    df_best = data[data["Crop"] == best_crop].groupby("Year")["Yield"].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_current["Year"], y=df_current["Yield"],
                             mode="lines+markers", name=current_crop,
                             line=dict(color=THEME["accent_blue"], width=3)))
    fig.add_trace(go.Scatter(x=df_best["Year"], y=df_best["Yield"],
                             mode="lines+markers", name=best_crop,
                             line=dict(color=THEME["accent_green"], width=3, dash="dot")))
    fig.update_layout(
        plot_bgcolor=THEME["card_bg"],
        paper_bgcolor=THEME["card_bg"],
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(font=dict(color="white"))
    )
    return fig

# =====================
# 🎨 Layout
# =====================
app.layout = dbc.Container([
    html.H2("🌾 Crop Yield & Smart Recommendations", style={"color": THEME["accent_blue"], "textAlign": "center"}),

    dbc.Row([
        dbc.Col([
            html.Label("🌍 Country", style={"color": "white"}),
            dcc.Dropdown(
                id="country",
                options=[{"label": c, "value": c} for c in sorted(df["Area"].unique())],
                value="India",
                style={"color": "black"}
            )
        ], md=3),

        dbc.Col([
            html.Label("🌾 Crop", style={"color": "white"}),
            dcc.Dropdown(
                id="crop",
                options=[{"label": c, "value": c} for c in sorted(df["Crop"].unique())],
                value="Wheat",
                style={"color": "black"}
            )
        ], md=3),

        dbc.Col([
            html.Label("📅 Year Range", style={"color": "white"}),
            dcc.RangeSlider(
                id="year-range",
                min=df["Year"].min(), max=df["Year"].max(),
                value=[1990, 2013],
                marks={y: str(y) for y in range(df["Year"].min(), df["Year"].max()+1, 3)}
            )
        ], md=4),

        dbc.Col([
            html.Label("🌦 Environmental Feature", style={"color": "white"}),
            dcc.Dropdown(
                id="feature",
                options=[{"label": col, "value": col} for col in ["NDVI_sat", "Rainfall_sat", "Temperature_sat", "Soil_Moisture"]],
                value="NDVI_sat",
                style={"color": "black"}
            )
        ], md=2),
    ], className="mb-4"),

    dbc.Row(id="kpi-row", className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="yield-trend"), md=6),
        dbc.Col(dcc.Graph(id="env-vs-yield"), md=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="choropleth"), md=6),
        dbc.Col(dcc.Graph(id="geo-map"), md=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="yield-forecast"), md=6),
        dbc.Col(id="crop-recommendation", md=6),
    ], className="mb-4")
], fluid=True, style={"backgroundColor": THEME["background"]})

# =====================
# 🔄 Callbacks
# =====================
@app.callback(
    [Output("kpi-row", "children"),
     Output("yield-trend", "figure"),
     Output("env-vs-yield", "figure"),
     Output("choropleth", "figure"),
     Output("geo-map", "figure"),
     Output("yield-forecast", "figure"),
     Output("crop-recommendation", "children")],
    [Input("country", "value"),
     Input("crop", "value"),
     Input("year-range", "value"),
     Input("feature", "value")]
)
def update_dashboard(country, crop, year_range, feature):
    dff = df[(df["Area"] == country) & (df["Crop"] == crop) &
             (df["Year"].between(year_range[0], year_range[1]))]

    if dff.empty:
        return [
            [kpi_card("No Data", "—", THEME["accent_blue"])],
            go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(),
            dbc.Card(dbc.CardBody([html.H5("🌱 No recommendation available (empty dataset)", style={"color": "white"})]))
        ]

    # KPIs
    avg_yield = round(dff["Yield"].mean(), 2)
    max_yield = round(dff["Yield"].max(), 2)
    growth = round(((dff["Yield"].iloc[-1] - dff["Yield"].iloc[0]) / dff["Yield"].iloc[0]) * 100, 2)

    kpis = [
        kpi_card("📊 Avg Yield", avg_yield, THEME["accent_blue"]),
        kpi_card("🏆 Max Yield", max_yield, THEME["accent_green"]),
        kpi_card("📈 Growth %", f"{growth}%", THEME["accent_purple"])
    ]

    # Yield trend
    trend = px.line(dff, x="Year", y="Yield", title="Yield Trend Over Years", markers=True,
                    color_discrete_sequence=[THEME["accent_blue"]])
    trend.update_layout(plot_bgcolor=THEME["card_bg"], paper_bgcolor=THEME["card_bg"], font=dict(color="white"))

    # Env vs Yield
    env = px.scatter(dff, x=feature, y="Yield", title=f"{feature} vs Yield",
                     color_discrete_sequence=[THEME["accent_green"]])
    env.update_layout(plot_bgcolor=THEME["card_bg"], paper_bgcolor=THEME["card_bg"], font=dict(color="white"))

    # Choropleth
    choropleth = px.choropleth(df, locations="Area", locationmode="country names", color="Yield",
                               title="Global Yield Heatmap", animation_frame="Year",
                               color_continuous_scale=px.colors.sequential.Viridis)
    choropleth.update_layout(paper_bgcolor=THEME["card_bg"], font=dict(color="white"))

    # Static geo map
    geo = px.scatter_geo(dff, locations="Area", locationmode="country names",
                         size="Yield", color="Yield", projection="natural earth",
                         title="Geospatial Crop Yield")
    geo.update_layout(paper_bgcolor=THEME["card_bg"], font=dict(color="white"))

    # Forecast (placeholder: line continuation)
    forecast = go.Figure()
    forecast.add_trace(go.Scatter(x=dff["Year"], y=dff["Yield"], mode="lines+markers", name="Actual",
                                  line=dict(color=THEME["accent_blue"], width=3)))
    forecast.update_layout(title="AI-based Yield Forecast", paper_bgcolor=THEME["card_bg"],
                           plot_bgcolor=THEME["card_bg"], font=dict(color="white"))

    # Recommendation
    crop_means = df.groupby("Crop")["Yield"].mean()
    best_crop = crop_means.idxmax()

    recommendation = dbc.Card(
        dbc.CardBody([
            html.H4("🌱 Recommended Crop", style={"color": THEME["accent_green"]}),
            html.H5(f"{best_crop} (based on yield trends 🚀)", style={"color": "white"}),
            dcc.Graph(figure=make_comparison_graph(crop, best_crop, df), config={"displayModeBar": False}, style={"height": "250px"})
        ]),
        style={"backgroundColor": THEME["card_bg"], "boxShadow": "0 0 15px #A1E887"}
    )

    return kpis, trend, env, choropleth, geo, forecast, recommendation

# =====================
# ▶️ Run
# =====================
if __name__ == "__main__":
    app.run(debug=True)
