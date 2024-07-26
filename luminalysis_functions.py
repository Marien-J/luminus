import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px
import json
import plotly.graph_objects as go

from scipy.optimize import curve_fit

from constants import ELEC_CO2_INTENSITY, ELEC_CO2_INTENSITY_ELECTRIFICATION

def example_cases(df, sortcol = 'tco', solar = False, co2_intensity = 171/1000, dynamic = False):
    if solar == True:
        df['total_co2'] = df.total_co2 + df.electricity_injected * co2_intensity
        df['epc_ind'] = df.epc_ind + df.electricity_injected * 2.5 / df.total_floor_area
    if dynamic == True:
        if df.total_emissions not in df.columns:
            return print('please provide the total emissions in the dynamic case and name the column total_emissions')
            
        else:
            co2_metric_column = 'total_emissions'
    case1 = df[df.epc_ind <= 100].sort_values(by = sortcol, ascending = True).drop_duplicates(subset = 'name')
    case2 = df[(df.epc_ind <= 100) & (df.total_co2/df.total_floor_area <= 6)].sort_values(by = sortcol, ascending = True).drop_duplicates(subset = 'name') # french with flemish epc
    case3 = df[(df.epc_ind <= 70) & (df.total_co2/df.total_floor_area <= 6)].sort_values(by = sortcol, ascending = True).drop_duplicates(subset = 'name') # french A
    case4 = df[(df.epc_ind <= 110) & (df.total_co2/df.total_floor_area <= 11)].sort_values(by = sortcol, ascending = True).drop_duplicates(subset = 'name') # french B
    case5 = df[(df.epc_ind <= 200) & (df.total_co2/df.total_floor_area <= 10)].sort_values(by = sortcol, ascending = True).drop_duplicates(subset = 'name') # modified to B label with a co2 limit

    return case1, case2, case3, case4, case5

def mod_solar(df, co2_flag = True, co2_intensity = 171/1000):
     
     if co2_flag == True:
        df['total_co2_modified'] = df.total_co2 + df.electricity_injected * co2_intensity
    
     df['epc_ind_modified'] = df.epc_ind + df.electricity_injected * 2.5 / df.total_floor_area

     return df

def fit_co2(central_scenario = ELEC_CO2_INTENSITY, electrification_scenario = ELEC_CO2_INTENSITY_ELECTRIFICATION, returnplot = False):
    # Convert dictionary to arrays
    years = np.array(list(central_scenario.keys()))
    central_scenario = np.array(list(central_scenario.values()))
    electrification_scenario = np.array(list(electrification_scenario.values()))

    # Exponential decay function
    def exp_decay(x, a, b):
        return a * np.exp(b * x)

    # Fit the central scenario data
    popt_central, pcov_central = curve_fit(exp_decay, years - 2020, central_scenario, p0=(0.171, -0.1))
    a_central, b_central = popt_central

    # Fit the electrification scenario data
    popt_electrification, pcov_electrification = curve_fit(exp_decay, years - 2020, electrification_scenario, p0=(0.171, -0.1))
    a_electrification, b_electrification = popt_electrification

    # Generate data for plotting
    x_fit = np.linspace(2020, 2040, 21)
    y_fit_central = exp_decay(x_fit - 2020, *popt_central)
    y_fit_electrification = exp_decay(x_fit - 2020, *popt_electrification)

    # Plot the data and the fit
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = years, y = central_scenario, mode = 'markers', name = 'central scenario'))
    fig.add_trace(go.Scatter(x = years, y = electrification_scenario, mode = 'markers', name = 'electrification scenario'))
    fig.add_trace(go.Scatter(x = x_fit, y = y_fit_central, mode = 'lines', name = 'central fit'))
    fig.add_trace(go.Scatter(x = x_fit, y = y_fit_electrification, mode = 'lines', name = 'electrification fit'))
    legendict = dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=1,
        bgcolor = 'RGBA(255,255,255,0.4)'
        )
    fig.update_traces( marker = dict(size = 8),)
    fig.update_layout(width = 400, height = 400, legend = legendict,
                    
                    margin={'l': 50, 'b': 10, 't': 10, 'r': 40},
                    xaxis_title="Year", yaxis_title='CO₂ intensity (kg/kWh)')
    if returnplot == True:
        return x_fit, y_fit_central, y_fit_electrification, fig
    else:
        return x_fit, y_fit_central, y_fit_electrification

def dynamic_co2(df, years, scenario, start_year = 2025, solar = False):
    if start_year not in years:
        print('year is not in the provided years array')
    if len(scenario) != len(years):
        print('One of the scenarios has more values than there are years. \n example use:\n years: [2020, 2021, 2022] \n scenarios: [[0.1, 0.8, 0.6], [0.6, 0.55, 0.5]]')
    k = np.where(years == start_year) # integers


    scenario = scenario[k[0][0]:]

    # Constants for gas and oil emissions in kg/kWh
    co2_intensity_gas = 0.056 * 3.6
    co2_intensity_oil = 0.074 * 3.6

    # Calculate emissions for each year and store in new columns
    for year in range(len(scenario)):
        co2_electricity = scenario[year]
        df[f'emissions_{year + start_year}'] = (
            df['electricity_consumption'] * co2_electricity +
            df['gas_consumption'] * co2_intensity_gas +
            df['oil_consumption'] * co2_intensity_oil -
            df['electricity_injected'] * co2_electricity
        )
        if solar == True:
            df[f'modified_emissions_{year + start_year}'] = (
                df['electricity_consumption'] * co2_electricity +
                df['gas_consumption'] * co2_intensity_gas +
                df['oil_consumption'] * co2_intensity_oil
            )

    df['total_emissions'] = df[[f'emissions_{year + start_year}' for year in range(len(scenario))]].sum(axis=1)
    df['modified_total_emissions'] = df[[f'modified_emissions_{year + start_year}' for year in range(len(scenario))]].sum(axis=1)
    
    return df

