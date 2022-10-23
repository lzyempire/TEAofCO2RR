# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from TEAofCO2RR import NPVChart
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(NPVChart, x="Year", y="CumCash_PV")

app.layout = html.Div(children=[
    html.H1(
        children='Techno-Economic Analysis of Electrochemical Carbon Dioxide Reduction', 
        style={
            'textAlign': 'center',
        }),

    html.Div(children='''
        Model from the literature General Techno-Economic Analysis of CO2 Electrolysis Systems
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
