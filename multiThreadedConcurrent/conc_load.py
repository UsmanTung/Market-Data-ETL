import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


from conc_transform import transformDeque


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.H1("Mock Market", className="text-center mt-3"),
    dcc.Graph(id="live-chart"),
    dcc.Interval(id="update-interval", interval=150)
], fluid=True)

def init_callbacks(transformer):
    @app.callback(
        Output("live-chart", "figure"),
        Input("update-interval", "n_intervals")
    )
    def update_chart(_):
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.8, 0.2]
        )

        # Full candle
        if transformDeque:
            dfBars = pd.DataFrame(list(transformDeque))
            fig.add_trace(
                go.Candlestick(
                    x=dfBars["Timestamp"].dt.strftime("%H:%M:%S"),
                    open=dfBars["open"],
                    high=dfBars["high"],
                    low=dfBars["low"],
                    close=dfBars["close"],
                    name="OHLC"
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Bar(
                    x=dfBars["Timestamp"].dt.strftime("%H:%M:%S"),
                    y=dfBars["volume"],
                    marker_color="rgba(0,150,255,0.6)",
                    name="Volume"
                ),
                row=2, col=1
            )

        curr = transformer.currentCandle

        # Not full candle
        if curr:
            ts = curr["Timestamp"].strftime("%H:%M:%S")
            fig.add_trace(
                go.Candlestick(
                    x=[ts],
                    open=[curr["open"]],
                    high=[curr["high"]],
                    low=[curr["low"]],
                    close=[curr["close"]],
                    showlegend=False
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Bar(
                    x=[ts],
                    y=[curr["volume"]],
                    marker_color="rgba(0,150,255,0.6)",
                    showlegend=False
                ),
                row=2, col=1
            )

        fig.update_layout(
            title="NVDA",
            template="plotly_dark",
            height=700,
            xaxis_rangeslider_visible=False,
            uirevision="fixed"
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(title_text="Price", showgrid=False, side="right", row=1, col=1)
        fig.update_yaxes(title_text="Volume", side="right", row=2, col=1, fixedrange=True)

        return fig
