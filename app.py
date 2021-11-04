import dash
import dash_bootstrap_components as dbc


#Inicializamos y le agregamos las meta_tags para que sea compatible con dispositivos moviles
app = dash.Dash(__name__, suppress_callback_exceptions=True,  external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server