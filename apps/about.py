import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

layout =  dbc.Container([
    dbc.Row([dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Markdown('''


                    #### Dashboard de Phishing en el 2020
                    Este dashboard fue realizado por Carlos Velázquez como parte de un proyecto de la materia Ingeniería de Caracteristicas, de la Maestria en Ciencia de datos
                    de la Universidad de Sonora. El dashboard se realizó en el lenguaje Python utilizando [Dash](https://dash.plotly.com/)

                    #### Datos
                    Los datos de Phishing del 2020 se obtuvieron de la página [PhishStats](https://phishstats.info/), para mas información acerca de la
                    de la obtención de datos visitar el siguiente post de Medium: [Obteniendo datos mundiales de Phishing con la API de PhishStats](https://medium.com/mcd-unison/obteniendo-datos-mundiales-de-phishing-con-la-api-de-phishstats-76ab9136103d)

                    #### Repositorio del proyecto
                    El código y los archivos utilizados para construir el dashboard se encuentran en el repositorio de [GitHub](https://github.com/carlosvelv)
                '''),
            ]
        ),
    ],
    style={"width": "12","margin-top": "25px"},
)])
])