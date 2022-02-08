import dash
import dash_bootstrap_components as dbc
from flask import Flask


# meta_tags are required for the app layout to be mobile responsive
server = Flask(__name__)
server.config.update(SECRET_KEY='0140aee4b41878a384c4ccd13fdbd53d7ecc47238c4018d8')
app = dash.Dash(__name__, server=server, title='Bridge Dashboard', suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.CERULEAN]
                )