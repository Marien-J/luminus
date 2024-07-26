
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.ZEPHYR]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,     external_scripts=[
                    {'src':"https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"}])
app.config.suppress_callback_exceptions = True
server = app.server
