# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from TEAofCO2RR import NPV_df, OpEx_df, CapEx_df

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# dropdown_Product = dbc.DropdownMenu(
#     label="Product",
#     children=[
#         dbc.DropdownMenuItem(NPV_df_item) for NPV_df_item in NPV_df.index
#     ],
# )

fig_overview = dcc.Graph(figure=px.bar(NPV_df, x=NPV_df.index, y="Current", labels={"index":"CO2RR Products", "Current":"Profit/$"}))


NPV_fig = go.Figure()
NPV_fig.add_trace(go.Bar(x = NPV_df['Optimistic'], y = NPV_df.index,
                orientation='h', 
                base=0,
                marker_color='crimson',
                name='Optimistic'
                ))
NPV_fig.add_trace(go.Bar(x = NPV_df['Current'], y = NPV_df.index,
                orientation='h', 
                base=0,
                marker_color='lightslategrey',
                name='Current'))
NPV_fig.update_xaxes(title_text="Profit/$")
NPV_fig.update_yaxes(title_text="CO2RR Products")
fig_NPV = dcc.Graph(figure=NPV_fig)

OpEx_fig = px.bar(
    OpEx_df.T, x = OpEx_df.T.index, y = OpEx_df.T.columns, 
    title="Operation Expenses for CO2RR Products", 
    labels={"index":"CO2RR Products", "value":"Operation Expenses/$", "variable":"Expenses"}
    )
fig_OpEx = dcc.Graph(figure=OpEx_fig)

CapEx_fig = px.bar(
    CapEx_df.T, x = CapEx_df.T.index, y = CapEx_df.T.columns, 
    title = "Capital Expenses for CO2RR Products",
    labels={"index":"CO2RR Products", "value":"Capital Expenses/$", "variable":"Expenses"}
    )
fig_CapEx = dcc.Graph(figure=CapEx_fig)

tabs = dbc.Tabs(
    [
        dbc.Tab(fig_overview, label="Overview"),
        dbc.Tab(fig_NPV, label="Optimistic vs Current"),
        dbc.Tab(fig_OpEx, label="Operation Expenses"),
        dbc.Tab(fig_CapEx, label="Capital Expenses"),
    ]
)

app.layout = dbc.Container(
    children=[
        dcc.Markdown('''
        # Techno-Economic Analysis of Electrochemical Carbon Dioxide Reduction 
        This TEA model is from the literature: [*General Techno-Economic Analysis of CO2 Electrolysis Systems*]
        (http://doi.org/10.1021/acs.iecr.7b03514). 
        '''),
        tabs
    ]
)


# @app.callback(
#     Output('Product-output-container', 'children'),
#     Input('Product-dropdown', 'value')
# )

# def update_output(value):
#     return f'You have selected {value} as the product of CO2RR'

if __name__ == '__main__':
    app.run_server(debug=True)


