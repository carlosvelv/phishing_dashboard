import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, State, html

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import dashboard, about


app.layout = dbc.Container([
    dbc.Row([
            dbc.Col(dbc.Navbar(
                        dbc.Container(
                                [
                                html.A(
                                        # Use row and col to control vertical alignment of logo / brand
                                        dbc.Row(
                                        [
                                                dbc.Col(html.Img(src='https://mcd.unison.mx/wp-content/themes/awaken/img/logo_mcd.png', height="70px"), width={'offset':0}),
                                                dbc.Col(dbc.NavbarBrand("Phishing en el 2020", className="ms-2")),
                                        ],
                                        align="center",
                                        className="g-0",
                                        ),
                                        href="https://mcd.unison.mx/",
                                        style={"textDecoration": "none"},
                                ),
                                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                                dbc.Nav([dbc.NavLink("Dashboard", href="/apps/dashboard"),
                                         dbc.NavLink("Acerca De", href="/apps/about"),
                ]),

                                ]
                        ),
                        color="dark",
                        dark=True,
                        ))
    ]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
], fluid= True)

#Sitio que se pasara al children de page-content
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/about':
        return about.layout
    if pathname == '/apps/dashboard':
        return dashboard.layout
    else:
        return dashboard.layout


if __name__ == '__main__':
    app.run_server(debug=False)
