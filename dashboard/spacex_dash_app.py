"""SpaceX launch records dashboard (Plotly Dash).

Run:  python spacex_dash_app.py   then open http://127.0.0.1:8050
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_URL = ("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
            "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
LOCAL_COPY = Path(__file__).resolve().parent.parent / "data" / "spacex_launch_dash.csv"
spacex_df = pd.read_csv(LOCAL_COPY if LOCAL_COPY.exists() else DATA_URL)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

site_options = [{"label": "All Sites", "value": "ALL"}] + [
    {"label": site, "value": site} for site in sorted(spacex_df["Launch Site"].unique())
]

app = Dash(__name__)
app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40}),
    # Task 1: launch site drop-down
    dcc.Dropdown(id="site-dropdown", options=site_options, value="ALL",
                 placeholder="Select a launch site", searchable=True),
    html.Br(),
    # Task 2: pie chart of successful launches
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),
    html.P("Payload range (kg):"),
    # Task 3: payload range slider
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 2500)},
                    value=[min_payload, max_payload]),
    # Task 4: scatter plot of payload against launch outcome
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])


@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        successes = spacex_df[spacex_df["class"] == 1]
        return px.pie(successes, names="Launch Site",
                      title="Share of all successful launches by site")
    site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
    counts = site_df["class"].map({1: "Success", 0: "Failure"}).value_counts().reset_index()
    counts.columns = ["outcome", "count"]
    return px.pie(counts, values="count", names="outcome",
                  title=f"Launch outcomes at {entered_site}")


@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    df = spacex_df[spacex_df["Payload Mass (kg)"].between(low, high)]
    if entered_site != "ALL":
        df = df[df["Launch Site"] == entered_site]
    title = "all sites" if entered_site == "ALL" else entered_site
    return px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                      title=f"Payload mass and launch outcome, {title}")


if __name__ == "__main__":
    app.run(debug=False)
