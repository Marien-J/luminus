from dash import html, dcc, Input, Output, State, Dash
import dash_bootstrap_components as dbc
import os
import importlib

from server import app, server

import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash
import os

from layout import banner, build_tabs, footer

from tabs.archetypes import layout_scenario_maker
#from scenario_maker import layout_scenario_maker

app.title = "Dashboard: Luminus"
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "0"},
    children=[
        dcc.Location(id="url", refresh=False),
        banner(),
        html.Div(id="page-content"),
        footer(),
    ],
)

@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return build_tabs()
    # elif pathname == "/changelog":
    #     return html.Div(children=[changelog()])


# Handle tab selection
@app.callback(
    Output("tabs-content", "children"),
    [
        Input("tabs", "value"),
    ],
)
def render_content(tab):
    """Update the contents of the page depending on what tab the user selects."""
    print(tab)
    if tab == "tab-select":
        return layout_scenario_maker
    # if tab == "tab-scenario":
    #     return layout_scenario_maker
    # elif tab == "tab-sun":
    #     return layout_warmtezonering
    # elif tab == 'tab-wind':
    #     return layout_dennis
    # elif tab == "tab-samenvatting":
    #      return layout_test()
    # elif tab == "tab-data-explorer":
    #     return layout_data_explorer()
    # elif tab == "tab-outdoor-comfort":
    #     return layout_outdoor_comfort()
    # elif tab == "tab-natural-ventilation":
    #     return layout_natural_ventilation(si_ip)
    # elif tab == "tab-psy-chart":
    #     return layout_psy_chart()
    else:
         return "404"

if __name__ == "__main__":
    app.run_server(
        debug=False,
        host="0.0.0.0",
        #port=8050,
        processes=1,
        threaded=True,
    )