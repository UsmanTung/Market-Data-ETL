import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd


from conc_transform import transformDeque


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.H1("Mock Market", className="text-center mt-3"),
    dcc.Graph(id="live-chart"),
    dcc.Interval(id="update-interval", interval=100, n_intervals=0)
], fluid=True)

def init_callbacks(transformer):
    @app.callback(
        Output("live-chart", "figure"),
        Input("update-interval", "n_intervals")
    )
    def update_chart(_):
        fig = go.Figure()

        # Candle
        if transformDeque:
            df_bars = pd.DataFrame(list(transformDeque))
            fig.add_trace(go.Candlestick(
                x=df_bars["Timestamp"].dt.strftime("%H:%M:%S"),
                open=df_bars["open"],
                high=df_bars["high"],
                low=df_bars["low"],
                close=df_bars["close"],
                name="OHLC",
                showlegend=False
            ))

        curr = transformer.currentCandle
        if curr:
            fig.add_trace(go.Candlestick(
                x=[curr["Timestamp"].strftime("%H:%M:%S")],
                open=[curr["open"]],
                high=[curr["high"]],
                low=[curr["low"]],
                close=[curr["close"]],
                increasing_line_color="green",
                decreasing_line_color="red",
                showlegend=False
            ))



        fig.update_layout(
            title="NVDA",
            template="plotly_dark",
            height=700,
            xaxis_rangeslider_visible=False,
            uirevision="fixed"
        )

        return fig
