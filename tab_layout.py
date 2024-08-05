from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
from constants import ELECTRICITY_PRICE, GAS_PRICE
def make_layout(figure):
    layout_dennis = dbc.Container(
        [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        ['all buildings', 'detached_building', 'semi_detached_building', 'terraced_building'],
                        'all buildings',
                        id='building_standard',
                    ),
                    dcc.Dropdown(
                        ['Brugge',],
                        'Brugge',
                        id='municipality_standard',
                    ),
                ], width=2),
                dbc.Col([
                    html.Div(dcc.Graph(id='subplots', figure = figure, style={'display':'flex'})),
                ], width=9)
            ]),
            # html.Hr(),
            # dcc.Markdown("""
            # Dashboard designed for demo purposes only! No guarantee is given to the correctness of the tool, nor to that of the underlying data. All rights to the data shown belong to VITO N.V.. The author hereby waives all liability.
            # """),
        ],
        fluid=True
    )
    return layout_dennis

def make_layout_scenario_maker(figure, figure2, figure3, figure4, figure5, label_slider, economic_slider,):
    layout_kakker = dbc.Container(
        [
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.Button(id='submit-button-labels', n_clicks=0, children='Update with new values'),
                    html.Hr(),
                    dcc.Markdown('select a scaling'),
                    dcc.Dropdown(
                        
                        ['standard archetypes', 'extrapolated'],
                        'standard archetypes',
                        id='building',
                    ),
                    html.Hr(),
                    dbc.Button(
                    "Modify EPC parameters",
                    id="label_button"
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(

                                label_slider,
                            )
                        ),
                        id="label_collapse",
                        is_open=False
                ),
                html.Hr(),
                dbc.Button(
                    "Modify energy prices",
                    id="economic_button"
                ),
                dbc.Collapse(
                    dbc.Card(
                        dbc.CardBody(
                            economic_slider,
                        )
                    ),
                    id="economic_collapse",
                    is_open=False
                ),
                ], width=3),
                dbc.Col([
                    html.Div(dcc.Graph(id='bar-graph', figure = figure, style={'display':'flex'})),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='figure2', figure=figure2), width=6),
                        dbc.Col(dcc.Graph(id='figure3', figure=figure3), width=6),
                ]),
                dbc.Row([
                        dbc.Col(dcc.Graph(id='figure4', figure=figure4), width=6),
                        dbc.Col(dcc.Graph(id='figure5', figure=figure5), width=6),
                ]),
                ], width=9)
            ]),
            html.Hr(),
            # html.Hr(),
            # dcc.Markdown("""
            # Dashboard designed for demo purposes only! No guarantee is given to the correctness of the tool, nor to that of the underlying data. All rights to the data shown belong to VITO N.V.. The author hereby waives all liability.
            # """),
        ],
        fluid=True
    )
    return layout_kakker

def make_sliders():
    label_sliders = [
        html.Div([
        daq.ToggleSwitch(
            label = 'Make heat pumps mandatory',
            id='heatpump-switch',
            color="#9B51E0",
            value=False
        ),
        html.Div(id = 'heatpump-output'),
        ]),
        html.Div([
        daq.ToggleSwitch(
            label = 'Use only PV self consumptions for co2 and epc calculations',
            id='PV-switch',
            color="#9B51E0",
            value=False
        ),
        daq.ToggleSwitch(
            label = 'Equalize co2 losses from injection in the reference label when PV is on',
            id='co2-switch',
            color="#9B51E0",
            value=False
        ),
        html.Hr(),
        html.Div(id = 'PV-output'),
        ]),
        html.Div(id="epc_slider_output"),
        dcc.Slider(
            id="epc_slider_input",
            min=70,
            max=200,
            step=10,
            value=100,
        ),
        html.Div(id="co2_slider_output"),
        dcc.Slider(
            id="co2_slider_input",
            min=4000,
            max=10000,
            step=500,
            value=10000,
        ),
        html.Div(id="co2perm2_slider_output"),
        dcc.Slider(
            id="co2perm2_slider_input",
            min=0,
            max=100,
            step=None,
            marks = {0: '0', 2: '2', 4: '4', 6:'6',
                      10:'10', 15:'15', 20:'20', 
                      30:'30', 40:'40', 50:'50' ,100:'100'},
            value=100,
        ),
        html.Div(id="intensity_slider_output"),
        dcc.Slider(
            id="intensity_slider_input",
            min=0,
            max=200,
            step=10,
            value=171,
        ),

    ]

    economic_sliders = [
        html.Div(id="gas_slider_output"),
        dcc.Slider(
            id="gas_slider_input",
            min=0.04,
            max=0.30,
            step=0.02,
            value=GAS_PRICE['BE'],
        ),
        html.Div(id="electricity_slider_output"),
        dcc.Slider(
            id="electricity_slider_input",
            min=0.10,
            max=0.50,
            step=0.02,
            value=ELECTRICITY_PRICE['BE'],
        ),
        ]
    return label_sliders, economic_sliders
