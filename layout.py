import dash_bootstrap_components as dbc
from dash import dcc, html


def footer():
    return dbc.Row(
        align="center",
        justify="between",
        id="footer-container",
        children=[
            dbc.Col(
                children=[
                    dbc.Row(
                        html.A(
                            children=[
                                html.Img(
                                    src="assets/logo_combined_3.png",
                                    style={
                                        'width': '300px',  # Adjust the width as needed
                                        'height': 'auto'   # Maintain aspect ratio
                                }
                                )
                            ],
                            href="https://vito.be/",
                        )
                    ),
                ],
                width=12,
                md=4,
                style={"padding": "15px"},
            ),
            dbc.Col(
                children=[
                    dbc.Row(
                        [
                            dcc.Markdown(
                                """
                                This tool is developed for demo purposes only. 
                                There is no guarantee to its correctness nor to the correctness of the underlying data.
                                No rights can be derived from its content or from its usage. 
                                The author hereby waives all liability.
                                All data shown is for internal usage only and its ownership rests solely with Vito N.V.. 
                                """
                            ),
                            # dcc.Markdown(
                            #     """
                            #         [Contributors](Jonas Marien, Pieter Bosmans),
                            #         [Contact](https://vito.be/en),
                            #     """,
                            #     style={"marginTop": "1rem"},
                            # ),
                        ],
                        style={"marginTop": "1rem"},
                    ),
                ],
                width=12,
                md=8,
            ),
        ],
    )


def banner():
    """Build the banner at the top of the page."""
    return html.Div(
        id="banner",
        children=[
            dbc.Row(
                align="center",
                children=[
                    dbc.Col(
                        html.A(
                            href="/",
                            children=[
                                html.Img(
                                    src="assets/logo_vito.png",
                                        style={
                                        'width': '100px',  # Adjust the width as needed
                                        'height': 'auto'   # Maintain aspect ratio
                                }),
                            ],
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        children=[
                            html.H1(id="banner-title", children=["Dashboard: Luminus"]),
                            html.H5(
                                id="banner-subtitle",
                                children=["Creator: J. Marien"],
                            ),
                        ],
                    ),
                    # dbc.Col(
                    #     style={"fontWeight": "400", "padding": "1rem"},
                    #     align="end",
                    #     children=[
                    #         dbc.Row(
                    #             # style={"text-align": "right"},
                    #             # children=[
                    #             #     dbc.RadioItems(
                    #             #         options=[
                    #             #             {
                    #             #                 "label": "Global Value Ranges",
                    #             #                 "value": "global",
                    #             #             },
                    #             #             {
                    #             #                 "label": "Local Value Ranges",
                    #             #                 "value": "local",
                    #             #             },
                    #             #         ],
                    #             #         value="local",
                    #             #         id="global-local-radio-input",
                    #             #         inline=True,
                    #             #     ),
                    #             # ],
                    #         ),
                    #         dbc.Row(
                    #             align="end",
                    #             style={"text-align": "right"},
                    #             children=[
                    #                 dbc.RadioItems(
                    #                     options=[
                    #                         {"label": "SI", "value": "si"},
                    #                         {"label": "IP", "value": "ip"},
                    #                     ],
                    #                     value="si",
                    #                     id="si-ip-radio-input",
                    #                     inline=True,
                    #                 ),
                    #             ],
                    #         ),
                    #     ],
                    #     width="auto",
                    # ),
                ],
            ),
        ],
    )


def build_tabs():
    """Build the seven different tabs."""
    return html.Div(
        id="tabs-container",
        children=[
            dcc.Tabs(
                id="tabs",
                parent_className="custom-tabs",
                value="tab-select",
                children=[
                    dcc.Tab(
                        id = 'tab-select',
                        label="Overview",
                        value="tab-select",
                        className="custom-tab",
                        
                        selected_className="custom-tab--selected",
                        disabled=False,
                    ),
                    dcc.Tab(
                        id = "tab-scenario",
                        label="Try it yourself",
                        value="tab-scenario",
                        className="custom-tab",

                        selected_className="custom-tab--selected",
                        disabled =True,
                    ),

                ],colors = {'primary':'black', 'border': 'gold', 'background':'gray'},
            ),
            html.Div(
                id="store-container",
                children=[store(), html.Div(id="tabs-content")],
            ),
        ],
    )


def store():
    return html.Div(
        id="store",
        children=[
            dcc.Loading(
                [
                    dcc.Store(id="df-store", storage_type="session"),
                    dcc.Store(id="meta-store", storage_type="session"),
                    dcc.Store(id="url-store", storage_type="session"),
                    dcc.Store(id="si-ip-unit-store", storage_type="session"),
                    dcc.Store(id="lines-store", storage_type="session"),
                ],
                fullscreen=True,
                type="dot",
            )
        ],
    )