# loader.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from conc_extract import extractDeque
from conc_transform import transformDeque

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.H1("Mock Market", className="text-center mt-3"),
    dcc.Graph(id="live-chart"),
    dcc.Interval(id="update-interval", interval=2000, n_intervals=0)
], fluid=True)

@app.callback(
    Output("live-chart", "figure"),
    Input("update-interval", "n_intervals")
)
def update_chart(_):
    fig = go.Figure()

    # Tick/Dot
    if extractDeque:
        df_ticks = pd.DataFrame(list(extractDeque))
        fig.add_trace(go.Scatter(
            x=df_ticks["Timestamp"],
            y=df_ticks["Price"],
            mode="markers",
            marker=dict(size=4, opacity=0.5, color="cyan"),
            name="Trades",
            showlegend=False
        ))

    # Candle
    if transformDeque:
        df_bars = pd.DataFrame(list(transformDeque))
        fig.add_trace(go.Candlestick(
            x=df_bars["Timestamp"],
            open=df_bars["open"],
            high=df_bars["high"],
            low=df_bars["low"],
            close=df_bars["close"],
            name="OHLC",
            showlegend=False
        ))

    fig.update_layout(
        title="NVDA",
        template="plotly_dark",
        height=700,
        xaxis_rangeslider_visible=False,
        uirevision="constant"
    )

    return fig
