from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output


from LieuDeces_f5 import *

fig = go.Figure(go.Scattergeo(
    lon=[2.209666999999996],
    lat=[46.232192999999995],
    text="France",
    mode='markers',
))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'center': {'lon': 0, 'lat': 47},
        'zoom': 4}
)

# App layout
def page6_layout():
    
    return html.Div([

        html.Div(
            html.H1("Carte Décès",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),

        dcc.Dropdown(
        id='birthplace-d',
        options=birthplace_options,
        placeholder="Entrez une ville de naissance"
        ),

         # Affichage carte
        html.Div([
            dcc.Graph(id = 'map', figure = fig ,style={"width": "100%", "height": "80vh"})
        ], style={"width": "100vw", "height": "100%"}),
    ])
