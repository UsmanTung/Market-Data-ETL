import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/processed/ohlcv_1s.parquet")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.H1("Mock Market", className="text-center mt-3"),
    dcc.Graph(id="live-chart", animate=False),
    dcc.Interval(id="update-interval", interval=2000, n_intervals=0),
])


@app.callback(
    Output("live-chart", "figure"),
    Input("update-interval", "n_intervals")
)
def update_chart(_):
    if not DATA_PATH.exists():
        return go.Figure()

    try:
        df = pd.read_parquet(DATA_PATH)
    except Exception:
        return go.Figure()

    df = df[df["Ticker"] == "NVDA"].tail(50)

    if df.empty:
        return go.Figure()

    # Create subplot layout:
    # Row 1 → Candlestick
    # Row 2 → Volume bars
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3]
    )

    # Candlestick (top)
    fig.add_trace(
        go.Candlestick(
            x=df["Timestamp"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="OHLC"
        ),
        row=1, col=1
    )

    # Volume bars (bottom)
    fig.add_trace(
        go.Bar(
            x=df["Timestamp"],
            y=df["Volume"],
            name="Volume",
            marker_color="rgba(0,150,255,0.6)"
        ),
        row=2, col=1
    )

    fig.update_layout(
        title="NVDA",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=700,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )

    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)

    return fig