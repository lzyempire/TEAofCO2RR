# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from TEAofCO2RR import CaseCustom, NPV_df, OpEx_df, CapEx_df

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



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

Custom_fig = go.Figure()
Custom_fig.add_trace(go.Bar(x = NPV_df['Custom'], y = NPV_df.index,
                orientation='h', 
                base=0,
                marker_color='crimson',
                name='Custom'
                ))
Custom_fig.add_trace(go.Bar(x = NPV_df['Current'], y = NPV_df.index,
                orientation='h', 
                base=0,
                marker_color='lightslategrey',
                name='Current'))
Custom_fig.update_xaxes(title_text="Profit/$")
Custom_fig.update_yaxes(title_text="CO2RR Products")
fig_Custom = dcc.Graph(figure=Custom_fig)

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

Slider_ElectricityPrice = dcc.Slider(0, 1.5, 0.1,
               value=0.5,
               id='input_ElectricityPrice'
               )
Slider_CurrentDensity = dcc.Slider(0, 2000, 100,
               value=200,
               id='input_CurrentDensity'
               )
Slider_CellVoltage = dcc.Slider(1, 3, 0.1,
               value=2.3,
               id='input_CellVoltage'
               )
Slider_CO2Price = dcc.Slider(0, 200, 10,
               value=70,
               id='input_CO2Price'
               )
Slider_ElectrolyzerCost = dcc.Slider(1000, 5000, 100,
               value=250.25/1000*0.175*10000*1.75*1.2*2,
               id='input_ElectrolyzerCost'
               )
Slider_SellPriceRate = dcc.Slider(0, 5, 0.5,
               value=1,
               id='input_SellPriceRate'
               )
Slider_Selectivity = dcc.Slider(50, 100, 1,
               value=90,
               id='input_Selectivity'
               )
Slider_Conversion = dcc.Slider(0, 100, 10,
               value=50,
               id='input_Conversion'
               )

items = [
    dbc.DropdownMenuItem('All Products', id='All'),
    dbc.DropdownMenuItem('Ethanol', id='EtOH'),
    dbc.DropdownMenuItem('Formic Acid', id='HCOOH'),
    dbc.DropdownMenuItem('Methanol', id='MeOH'),
    dbc.DropdownMenuItem('n-Propanol', id='PrOH'),
    dbc.DropdownMenuItem('Carbon Monoxide', id='CO'),
    dbc.DropdownMenuItem('Ethylene', id='C2H4'),
    dbc.DropdownMenuItem('Methane',id='CH4'),
]

dropdown = dbc.DropdownMenu(
    label='Products',
    children=items
)

tabs = dbc.Tabs(
    [
        dbc.Tab(fig_overview, label="Overview"),
        dbc.Tab(fig_NPV, label="Optimistic vs Current"),
        dbc.Tab(
            [
                dropdown,
                Slider_ElectricityPrice,
                Slider_CurrentDensity,
                Slider_CellVoltage,
                Slider_CO2Price,
                Slider_ElectrolyzerCost,
                Slider_SellPriceRate,
                Slider_Selectivity,
                Slider_Conversion,
                html.Div(id='slider-output-container'),
                fig_Custom
            ],
            label="Customize Sensitivity"
        ),
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
    

@app.callback(
    Output('slider-output-container', 'children'),
    Input('input_ElectricityPrice', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)

# @app.callback(
#     Output('Product-output-container', 'children'),
#     Input('Product-dropdown', 'value')
# )

# def update_output(value):
#     return f'You have selected {value} as the product of CO2RR'

if __name__ == '__main__':
    app.run_server(debug=True)


