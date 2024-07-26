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
from helpers import packs, scenario_maker_fig
from tab_layout import make_layout_scenario_maker, make_sliders
from server import app
#external_stylesheets = [dbc.themes.SUPERHERO]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,     external_scripts=[
#                     {'src':"https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"}])
load_figure_template('SUPERHERO')

df = pd.DataFrame() 
for municipality in ['Brugge']:
    temp = pd.read_parquet(f'C:/projects/wijkrenovatie/voorlopers/{municipality}.parquet',  columns = columns)
    df = pd.concat([df, temp])
current = df[df.name == 'current situation']
df['oil_consumption'] = df['oil_consumption'].fillna(0)
df['gas_consumption'] = df['gas_consumption'].fillna(0)
df['electricity_consumption'] = df['electricity_consumption'].fillna(0)
df['tco'] = df.total_investment_cost + df.electricity_consumption*30*energy_prices['electricity'] + df.gas_consumption*energy_prices['gas'] * 30 + df.total_oil_cost*30 -df.pv_kWh_injection * energy_prices['injection'] * 30
df['total_co2_no_inj'] = df.electricity_consumption * 0.06 *3.6 + df.oil_consumption * 0.074 * 3.6 + df.gas_consumption * 0.056 * 3.6
df['total_co2'] = df.electricity_consumption * 0.195  + df.oil_consumption * 0.074 * 3.6 + df.gas_consumption * 0.056 * 3.6 - df.pv_kWh_injection * 0.195
df['total_co2perm2'] = df.total_co2 / df.total_floor_area
df['heating_system'] = np.select([df.name.str.contains('hpaw'), 
                                    ~df.name.str.contains('hpaw')],
                                    ['heatpump', 'gasboiler'])

Alab = df[(df.epc_ind <=100) & (df.municipality == 'Brugge')].copy().sort_values(by = 'tco').drop_duplicates(subset = 'uidn', keep = 'first')
def_pack = df[(df.epc_ind <=100) & (df.total_co2 <= 10000) & (df.municipality == 'Brugge')].copy().sort_values(by = 'tco').drop_duplicates(subset = 'uidn', keep = 'first')

uidnset = list(set(Alab.uidn.unique().tolist() + def_pack.uidn.unique().tolist()))
Alab = Alab[Alab.uidn.isin(uidnset)]
def_pack = def_pack[def_pack.uidn.isin(uidnset)]

figure = scenario_maker_fig(Alab, def_pack,
                            # titles = ['Current A label', 
                            #                            r'A label EPC<=70 <br> CO₂<6 tonnes',
                            #                            'CO2 emission',
                            #                            'total_investment_cost',
                            #                            'total_tco',
                            #                            'amount of heat pumps'],
                                            labels = ['A label','your pack'],
                                            building_type = None )

label_sliders, economic_sliders = make_sliders()
layout_scenario_maker = make_layout_scenario_maker(figure, label_sliders, economic_sliders)
#app.layout = make_layout_scenario_maker(figure, label_sliders, economic_sliders)


@app.callback(
    Output("economic_collapse", "is_open"),
    [Input("economic_button", "n_clicks")],
    [State("economic_collapse", "is_open")]
)
def toggle_shape_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

### Callback to make operating parameters menu expand
@app.callback(
    Output("label_collapse", "is_open"),
    [Input("label_button", "n_clicks")],
    [State("label_collapse", "is_open")]
)
def toggle_operating_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("epc_slider_output", "children"),
    [Input("epc_slider_input", "drag_value")]
)
def display_rent_slider(drag_value):
    return f"EPC constraint: {drag_value}kWh/m2"

@app.callback(
    Output("co2_slider_output", "children"),
    [Input("co2_slider_input", "drag_value")]
)
def display_rent_slider(drag_value):
    return f"CO2 constraint: {drag_value}kg"

@app.callback(
    Output("co2perm2_slider_output", "children"),
    [Input("co2perm2_slider_input", "drag_value")]
)
def display_rent_slider(drag_value):
    return f"CO2 constraint: {drag_value}kg/m2"

@app.callback(
    Output("gas_slider_output", "children"),
    [Input("gas_slider_input", "drag_value")]
)
def display_rent_slider(drag_value):
    return f"Gas price: €{drag_value}"

@app.callback(
    Output("electricity_slider_output", "children"),
    [Input("electricity_slider_input", "drag_value")]
)
def display_rent_slider(drag_value):
    return f"Electricity price: €{drag_value}"

@app.callback(
    Output("intensity_slider_output", "children"),
    [Input("intensity_slider_input", "drag_value")]
)
def display_rent_slider(drag_value):
    return f"CO2 intensity of electricity: {drag_value} g/kWh"

@app.callback(
    Output("bar-graph", "figure"),
    [Input("submit-button-labels", "n_clicks"),
     State("building", "value"),
     State("municipality", "value"),
     State("electricity_slider_input", "drag_value"),
     State("gas_slider_input", "drag_value"),
     State("epc_slider_input", "drag_value"),
     State("co2_slider_input", "drag_value"),
     State("co2perm2_slider_input", "drag_value"),
     State("intensity_slider_input", "drag_value"),
     State("heatpump-switch", "value"),
     State("PV-switch", "value"),]
)
def update_figures(buttonval, buitype, municipality,
                   electricity_price, gas_price,
                   epc_lim, co2_lim, co2perm2, co2_intensity,
                   hp, pv):


    df['tco'] = df.total_investment_cost + df.electricity_consumption*30*electricity_price + df.gas_consumption*gas_price * 30 + df.total_oil_cost*30 -df.pv_kWh_injection * energy_prices['injection'] * 30
    
    
    if co2_intensity is not None:
        co2_intensity = co2_intensity/1000
    if pv == True:
        tmp = df[(df.epc_ind <= epc_lim)  & (df.municipality == municipality)].copy()
        tmp['total_co2'] = tmp.electricity_consumption * co2_intensity + tmp.oil_consumption * 0.074 * 3.6 + tmp.gas_consumption * 0.056 * 3.6
        tmp['total_co2perm2'] = tmp.total_co2/tmp.total_floor_area
        tmp = tmp[(tmp.total_co2 <= co2_lim) & (tmp.total_co2perm2 <= co2perm2)]
    else:
        tmp = df[(df.epc_ind <= epc_lim)  & (df.municipality == municipality)].copy()
        tmp['total_co2'] = tmp.electricity_consumption * co2_intensity + tmp.oil_consumption * 0.074 * 3.6 + tmp.gas_consumption * 0.056 * 3.6 - tmp.pv_kWh_injection * co2_intensity
        tmp['total_co2perm2'] = tmp.total_co2/tmp.total_floor_area
        tmp = tmp[(tmp.total_co2 <= co2_lim) & (tmp.total_co2perm2 <= co2perm2)]
    
    if hp == True:
        tmp = tmp[tmp.heating_system == 'heatpump']

        
    tmp = tmp.sort_values(by = 'tco').drop_duplicates(subset = 'uidn', keep = 'first')

    new_Alab = df[df.epc_ind<=100].copy().sort_values(by = 'tco').drop_duplicates(subset = 'uidn', keep = 'first')
    new_Alab['total_co2'] = new_Alab.electricity_consumption * co2_intensity + new_Alab.oil_consumption * 0.074 * 3.6 + new_Alab.gas_consumption * 0.056 * 3.6 - new_Alab.pv_kWh_injection * co2_intensity
    new_Alab['total_co2perm2'] = new_Alab.total_co2/new_Alab.total_floor_area
    uidnset = list(set(new_Alab.uidn.unique().tolist() + tmp.uidn.unique().tolist()))

    new_Alab = new_Alab[new_Alab.uidn.isin(uidnset)]
    tmp = tmp[tmp.uidn.isin(uidnset)]
    if buitype != 'all buildings':
        return scenario_maker_fig(new_Alab, tmp,
                                    labels = ['A label','your pack'],
                                    building_type = buitype)
    
    return scenario_maker_fig(new_Alab, tmp,
                                            labels = ['A label','your pack'],
                                            building_type = None)

    
    
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=False)