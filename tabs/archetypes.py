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
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent))
from figure_functions import barchart_heating_systems, boxplot_co2, boxplot_investment, boxplot_co2_abatement, boxplot_electricity_consumption
from constants import INJECTION_PRICE, GAS_PRICE, ELECTRICITY_PRICE
from tab_layout import make_layout_scenario_maker, make_sliders
from server import app
from functions import map_epc

#external_stylesheets = [dbc.themes.SUPERHERO]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,     external_scripts=[
#                     {'src':"https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"}])
load_figure_template('SUPERHERO')

df = pd.read_feather('data/archetypes_luminus_trimmed.ftr')
df['tco'] = df.total_investment_cost + df.electricity_consumption*15*ELECTRICITY_PRICE['BE'] + df.gas_consumption*GAS_PRICE['BE'] * 15+ df.total_oil_cost -df.electricity_injected * INJECTION_PRICE['BE'] * 15
df['mapped_epc'] = df.apply(lambda x: map_epc( epc = x.epc_ind, 
                                                co2 = x.total_co2 / x.total_floor_area), axis = 1)
optimal_unmodded_temp = df[df.epc_ind<=100].sort_values(by = 'tco', ascending = True).drop_duplicates(subset = 'name', keep = 'first')
optimal_unmodded_temp['dataset'] = 'unmodded'
optimal_modded_temp = df[df.epc_ind<=100].sort_values(by = 'tco', ascending = True).drop_duplicates(subset = 'name', keep = 'first')
optimal_modded_temp['dataset'] = 'modded'
df_plot = pd.concat([
    optimal_unmodded_temp, optimal_modded_temp
])
figure = barchart_heating_systems(df_plot, dataset = 'dataset')
figure2 = boxplot_co2(df_plot)
figure3 = boxplot_investment(df_plot)
figure4 = boxplot_co2_abatement(df_plot)
figure5 = boxplot_electricity_consumption(df_plot)
label_sliders, economic_sliders = make_sliders()
layout_scenario_maker = make_layout_scenario_maker(figure, figure2, figure3, figure4, figure5, label_sliders, economic_sliders)
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
     Output('figure2','figure' ),
     Output('figure3','figure' ),
     Output('figure4','figure' ),
     Output('figure5','figure' ),
    [Input("submit-button-labels", "n_clicks"),
     State("building", "value"),
     State("electricity_slider_input", "drag_value"),
     State("gas_slider_input", "drag_value"),
     State("epc_slider_input", "drag_value"),
     State("co2_slider_input", "drag_value"),
     State("co2perm2_slider_input", "drag_value"),
     State("intensity_slider_input", "drag_value"),
     State("heatpump-switch", "value"),
     State("PV-switch", "value"),
     State("co2-switch", "value")]
)
def update_figures(buttonval, extrapolation,
                   electricity_price, gas_price,
                   epc_lim, co2_lim, co2perm2, co2_intensity,
                   hp, pv, co2, df = df, time_horizon = 15):

    
    if co2_intensity is not None:
        co2_intensity = co2_intensity/1000
    df['tco'] = df.total_investment_cost + df.electricity_consumption*time_horizon*electricity_price + df.gas_consumption*gas_price * time_horizon + df.total_oil_cost -df.electricity_injected * INJECTION_PRICE['BE'] * time_horizon
    df['total_co2'] = df.electricity_consumption * co2_intensity + df.oil_consumption * 0.074 * 3.6 + df.gas_consumption * 0.056 * 3.6 - df['electricity_injected'] * co2_intensity
    current = df[df.scenario_name == 'current situation']
    current.loc[:,'heating_system'] = 'Heat Pump'
    current.loc[(current.gas_consumption > current.domestic_hot_water_consumption) & (current.oil_consumption == 0), 'heating_system' ] = 'Gasboiler'
    current.loc[(current.oil_consumption >= current.heating_consumption), 'heating_system' ] = 'Oil'
    current.loc[:, 'dataset'] = 'Current Situation'
    optimal_unmodded = df[df.epc_ind <= 100].sort_values(by = 'tco', ascending = True).drop_duplicates(subset = 'name', keep = 'first')
    optimal_unmodded.loc[:,'dataset'] = 'Flemish A Label'
    

    

    if pv == True:
        df['total_co2_mapped'] = df.total_co2 + df.electricity_injected * co2_intensity
        df['epc_ind_mapped'] = df.epc_ind + df.electricity_injected * 2.5 / df.total_floor_area
        if co2 == True:
            optimal_unmodded['total_co2'] = optimal_unmodded.total_co2 + optimal_unmodded.electricity_injected * co2_intensity
    
    if hp == True:
        df = df[df.heating_system == 'Heat Pump']



    # df['mapped_epc'] = df.apply(lambda x: map_epc( epc = x.epc_ind, 
    #                                             co2 = x.total_co2 / x.total_floor_area), axis = 1)
    # optimal_unmodded = df[df.epc_ind <= 100].sort_values(by = 'tco', ascending = True).drop_duplicates(subset = 'name', keep = 'first')
    # optimal_unmodded['dataset'] = 'unmodded'
    if pv == True:
        optimal_modded = df[ (df.epc_ind_mapped <= epc_lim) & (df.total_co2_mapped/df.total_floor_area <= co2perm2) & (df.total_co2_mapped <= co2_lim)].sort_values(by = 'tco', ascending = True).drop_duplicates(subset = 'name')
        optimal_modded['dataset'] = 'Modified Target'
        optimal_modded['total_co2'] = optimal_modded['total_co2_mapped']
    else:
        optimal_modded = df[ (df.epc_ind <= epc_lim) & (df.total_co2/df.total_floor_area <= co2perm2) & (df.total_co2 <= co2_lim)].sort_values(by = 'tco', ascending = True).drop_duplicates(subset = 'name')
        optimal_modded['dataset'] = 'Modified Target'


    # if buitype != 'all buildings':
    #     return scenario_maker_fig(new_Alab, tmp,
    #                                 labels = ['A label','your pack'],
    #                                 building_type = buitype)
    df_plot = pd.concat([
        optimal_unmodded, optimal_modded, current
    ])
    figure = barchart_heating_systems(df_plot, dataset = 'dataset', extrapolation = extrapolation)
    figure2 = boxplot_co2(df_plot, extrapolation= extrapolation)
    figure3 = boxplot_investment(df_plot, extrapolation=extrapolation)
    figure4 = boxplot_co2_abatement(df_plot, extrapolation = extrapolation)
    figure5 = boxplot_electricity_consumption(df_plot, extrapolation = extrapolation)
    return figure, figure2, figure3, figure4, figure5

    
    
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=False)