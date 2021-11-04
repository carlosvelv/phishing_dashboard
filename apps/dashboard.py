import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, State, html
from app import app
import pathlib 
#TODO:https://www.youtube.com/watch?v=RMBSQ6leonU&t=17s Y TERMINAR

#obteniendo folder relativo
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()



#Data stuff
df = pd.read_csv(DATA_PATH.joinpath("datos_para_dashboard_2020.csv"), index_col=0)
df['date'] = df['date'].str[:10]
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['day'] = df.date.dt.day
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
df = df[df['year'] == 2020]

#Para titulos df_regex_clean.csv
df_regex = pd.read_csv(DATA_PATH.joinpath("df_regex_clean.csv"), index_col=0)

#Cleaning
list_to_filter = ['Not Acceptable!','403 Forbidden', '404 Not Found', 'Sign in to your account', 'Website sleeping | 000webhost', 
                  'Website sleeping | 000webhost', 'None', 'Account Suspended', '509 Bandwidth Limit Exceeded', '508 Resource Limit Reached',
                  'Error 404 (Page not found)!!1', 'Suspected phishing site | Cloudflare', 'Sign in', 'Sign In',
                 'Поступил платеж - Служба экспресс доставки', '406 Not Acceptable']


months = {1:'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'}


#App Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H5("Seleccione el rango de meses a analizar",
                        className='text-center text-white ', style={'textAlign': 'end', "margin-top": "25px"}),
                width=12)
    ]),    
    dbc.Row([
            dbc.Col(dcc.RangeSlider(
                        id='value_slider',
                        min=1,
                        max=12,
                        step=None,
                        marks=months,
                        value=[1, 12]), style={"margin-top": "25px"}),
    ]),
    dbc.Row([
            dbc.Col(dcc.Graph(id='fig_line', figure = {}), width={'size':6}),
            dbc.Col(dcc.Graph(id='fig_world', figure = {}), width={'size':6}),
    ], style={"margin-top": "15px"}),

    dbc.Row([
            dbc.Col(dcc.Graph(id='fig_title', figure = {}), width={'size':6}),
            dbc.Col(dcc.Graph(id='fig_isp', figure = {}), width={'size':6}),
    ], style={"margin-top": "15px"}),

    
], fluid= True) #Pasarlo a False si queremos tener margenes a los lados


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single

# World Map
@app.callback(
    Output('fig_world', 'figure'),
    Input('value_slider', 'value')
)
def update_graph(months_to_use):
        month_1 = months_to_use[0]
        month_2 = months_to_use[1]
        ddf = df[df['month'].between(month_1,month_2,'both')]
        df_map = ddf.groupby('countryname').size()
        df_map

        graph_title = "Sitios de Phishing detectados de " + str(months[month_1]) + " a " + str(months[month_2]) + " por pais"

        fig_map = go.Figure(data = go.Choropleth(
                locations = df_map.index,
                z = df_map.values,
                locationmode = 'country names',
                text = df_map.index,
                colorscale = 'emrld',
                autocolorscale=False,
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar_title = 'Sitios detectados',
                colorbar_title_font_color = 'white',
                hovertemplate =
                "<b>%{text} </b><br>" +
                "Sitios detectados: %{z} <extra></extra>" ))

        fig_map.update_layout(
                title={
                        'text': graph_title,
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                title_font_color="white",
                title_font_size=25,
                template= 'plotly_dark',
                geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        showcountries = True,
                        countrycolor =  "#444444")
                )

        return fig_map

# World Map
@app.callback(
    Output('fig_line', 'figure'),
    Input('value_slider', 'value')
)
def update_graph(months_to_use):
        month_1 = months_to_use[0]
        month_2 = months_to_use[1]
        ddf = df[df['month'].between(month_1,month_2,'both')]
        url_by_day = ddf.groupby('date').size()
        url_by_day = url_by_day.reset_index()
        url_by_day.rename(columns={0:'url_count'}, inplace=True)

        graph_title = "Sitios de Phishing detectados de " + str(months[month_1]) + " a " + str(months[month_2]) + " (2020)"

        fig_line = go.Figure(data=go.Scatter(x=url_by_day.date, y=url_by_day.url_count, line=dict(color="#86d491"), ), )

        fig_line.update_layout(
        title={
                'text': graph_title,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        font_family="Courier New",
        font_color="white",
        title_font_family="Times New Roman",
        title_font_color="white",
        legend_title_font_color="white",
        title_font_size=25,
        template= 'plotly_dark',
        xaxis_title="Fecha",
        yaxis_title="Sitios detectados",)

        fig_line.update_traces(hovertemplate="%{x}<br>Sitios detectados: %{y} <extra></extra>")
        return fig_line


# ISP Chart
@app.callback(
    Output('fig_isp', 'figure'),
    Input('value_slider', 'value')
)
def update_graph(months_to_use):
        month_1 = months_to_use[0]
        month_2 = months_to_use[1]
        ddf = df[df['month'].between(month_1,month_2,'both')]
        top_ten_isp = ddf.groupby('isp').size().sort_values(ascending=False)[:10]
        top_ten_isp.index = top_ten_isp.index.str.slice(start=0, stop=-4) #Cleaning
        top_ten_isp = top_ten_isp.sort_values(ascending=True)

        fig_isp = go.Figure([go.Bar(x=top_ten_isp.values, y=top_ten_isp.index, orientation='h')])

        graph_title = "Sitios de Phishing detectados de " + str(months[month_1]) + " a " + str(months[month_2]) + " por ISP"


        fig_isp.update_layout(
        title={
                'text': graph_title,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        font_family="Courier New",
        font_color="white",
        title_font_family="Times New Roman",
        title_font_color="white",
        legend_title_font_color="white",
        title_font_size=25,
        template= 'plotly_dark',
        xaxis_title="Número de sitios hosteados",
        yaxis_title="ISP",)

        fig_isp.update_traces(marker_color='#86d491', hovertemplate="%{y}<br>Sitios detectados: %{x} <extra></extra>")

        return fig_isp

# Top Sites
@app.callback(
    Output('fig_title', 'figure'),
    Input('value_slider', 'value')
)
def update_graph(months_to_use):
        month_1 = months_to_use[0]
        month_2 = months_to_use[1]
        ddf = df_regex[df_regex['month'].between(month_1,month_2,'both')]
        top_ten_title = ddf.groupby('title').size().sort_values(ascending=False)[:50]
        top_ten_title = top_ten_title[~top_ten_title.index.isin(list_to_filter)][:10]
        top_ten_title = top_ten_title.sort_values(ascending=True)

        fig_title = go.Figure([go.Bar(x=top_ten_title.values, y=top_ten_title.index, orientation='h', )])

        graph_title = "Top Titulos Utilizados en Sitios de Phishing Detectados de " + str(months[month_1]) + " a " + str(months[month_2])


        fig_title.update_layout(
        title={
                'text': graph_title,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        font_family="Courier New",
        font_color="white",
        title_font_family="Times New Roman",
        title_font_color="white",
        legend_title_font_color="white",
        title_font_size=25,
        template= 'plotly_dark',
        xaxis_title="Sitios Detectados",
        yaxis_title="Titulo",)

        fig_title.update_traces(marker_color='#86d491', hovertemplate="%{y}<br>Sitios detectados: %{x} <extra></extra>")

        return fig_title


if __name__ == "__main__":
    app.run_server(debug=True)