from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd

app = Dash(__name__)

# ---------- Simulated Data ----------
def generate_data():

    n = 60  # only last 60 points

    t = pd.date_range(
        end=pd.Timestamp.now(),
        periods=n,
        freq="min"
    )

    soft = np.random.lognormal(
        mean=-14,
        sigma=0.5,
        size=n
    )

    # create flare spike
    soft[40:45] *= 50

    derivative = np.gradient(soft)

    derivative[derivative < 0] = 0

    hxr = derivative + np.random.random(n) * derivative.std()

    background = (
        pd.Series(soft)
        .rolling(15, min_periods=1)
        .quantile(0.2)
    )

    flare = soft > (background * 3)

    return (
        t,
        soft,
        hxr,
        derivative,
        background,
        flare
    )

# ---------- Layout ----------

app.layout = html.Div([

    html.H1(
        "Solar Flare Forecast System"
    ),

    html.Div(
        id="status"
    ),

    dcc.Graph(
        id="soft-graph"
    ),

    dcc.Graph(
        id="hxr-graph"
    ),

    dcc.Graph(
        id="derivative-graph"
    ),

    dcc.Graph(
        id="background-graph"
    ),

    dcc.Graph(
        id="flare-graph"
    ),

    html.H2("Forecast"),

    html.Div(
        id="forecast"
    ),

    dcc.Interval(
        id="interval",
        interval=5000,  # 5 sec
        n_intervals=0
    )

])

# ---------- Update ----------

@app.callback(
    [
        Output("status", "children"),
        Output("soft-graph", "figure"),
        Output("hxr-graph", "figure"),
        Output("derivative-graph", "figure"),
        Output("background-graph", "figure"),
        Output("flare-graph", "figure"),
        Output("forecast", "children")
    ],
    Input("interval", "n_intervals")
)
def update_dashboard(n):

    (
        t,
        soft,
        hxr,
        derivative,
        background,
        flare
    ) = generate_data()

    # Soft X-Ray

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=t,
            y=soft,
            mode="lines",
            name="Soft X-Ray"
        )
    )

    fig1.update_layout(
        title="Soft X-Ray Flux"
    )

    # HXR

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=t,
            y=hxr,
            mode="lines",
            name="Synthetic HXR"
        )
    )

    fig2.update_layout(
        title="Synthetic HXR"
    )

    # Derivative

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=t,
            y=derivative,
            mode="lines"
        )
    )

    fig3.update_layout(
        title="Flux Derivative"
    )

    # Background

    fig4 = go.Figure()

    fig4.add_trace(
        go.Scatter(
            x=t,
            y=soft,
            name="Soft"
        )
    )

    fig4.add_trace(
        go.Scatter(
            x=t,
            y=background,
            name="Background"
        )
    )

    fig4.update_layout(
        title="Background Estimation"
    )

    # Flare Detection

    fig5 = go.Figure()

    fig5.add_trace(
        go.Scatter(
            x=t,
            y=soft,
            mode="lines"
        )
    )

    flare_x = t[flare]
    flare_y = soft[flare]

    fig5.add_trace(
        go.Scatter(
            x=flare_x,
            y=flare_y,
            mode="markers",
            name="Detected Flare"
        )
    )

    fig5.update_layout(
        title="Flare Detection"
    )

    p30 = np.random.randint(20, 95)
    p60 = np.random.randint(10, 80)
    p120 = np.random.randint(5, 60)

    forecast = html.Div([

        html.H3(
            f"30 min : {p30}%"
        ),

        html.H3(
            f"60 min : {p60}%"
        ),

        html.H3(
            f"120 min : {p120}%"
        )

    ])

    status = html.Div([

        html.H3(
            "NOAA Feed : ONLINE"
        ),

        html.H3(
            "Model : READY"
        )

    ])

    return (
        status,
        fig1,
        fig2,
        fig3,
        fig4,
        fig5,
        forecast
    )

if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=8050
    )
