from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import geopandas as gpd
import shapely 
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
import dash_daq as daq
from constants import columns, energy_prices
from helpers import packs, subplot_maker
from tab_layout import make_layout
from server import app
#external_stylesheets = [dbc.themes.SUPERHERO]
load_figure_template('SUPERHERO')

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,     external_scripts=[
#                     {'src':"https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"}])
sel = [("epc_ind", "<=", 200)]
df = pd.DataFrame()
for municipality in ['Brugge',]:
    temp = pd.read_parquet(f'C:/projects/wijkrenovatie/voorlopers/{municipality}.parquet',  columns = columns)
    df = pd.concat([df, temp])
current = df[df.name == 'current situation']
df = df[df.epc_ind <= 200]

df['tco'] = df.total_investment_cost + df.electricity_consumption*30*energy_prices['electricity'] + df.gas_consumption*energy_prices['gas'] * 30 + df.total_oil_cost*30 -df.pv_kWh_injection * energy_prices['injection'] * 30
df['oil_consumption'] = df['oil_consumption'].fillna(0)
df['gas_consumption'] = df['gas_consumption'].fillna(0)
df['electricity_consumption'] = df['electricity_consumption'].fillna(0)
df['total_co2_no_inj'] = df.electricity_consumption * 0.06 *3.6 + df.oil_consumption * 0.074 * 3.6 + df.gas_consumption * 0.056 * 3.6
df['heating_system'] = np.select([df.name.str.contains('hpaw'), 
                                    ~df.name.str.contains('hpaw')],
                                    ['heatpump', 'gasboiler'])

inputs, labels, subplot_titles = packs(df)
fig = subplot_maker(inputs = inputs, labels = labels, titles = subplot_titles)

layout_standard = make_layout(figure = fig)

@app.callback(
    Output("subplots", "figure"),
    [Input("building_standard", "value"),
     Input("municipality_standard", "value")]
)
def update_figures(value, municipality):
    if value == 'all buildings':
        tmp = [x[x.municipality == municipality] for x in inputs]
        return subplot_maker(inputs = tmp, labels = labels, titles = subplot_titles)
    else:
        tmp = [x[x.municipality == municipality] for x in inputs]
        return subplot_maker(inputs = tmp, labels = labels, titles = subplot_titles, building_type = value)

# @app.callback(
#     Output("bar-graph", "figure"),
#     [Input("municipality", "value")]
# )
# def update_figures(value):
#     if value == 'all buildings':
#         return subplot_maker(inputs = inputs, labels = labels, titles = subplot_titles)
#     else:
#         return subplot_maker(inputs = inputs, labels = labels, titles = subplot_titles, building_type = value)


if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=True)
