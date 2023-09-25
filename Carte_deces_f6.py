from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output


from LieuDeces_f5 import *

villes_m = merged_df_death.groupby('Death Place').agg({
    'longitude_death': 'first',  # Utilisez 'first' pour obtenir le premier valeur non nulle.
    'latitude_death': 'first',   # Utilisez 'first' pour obtenir le premier valeur non nulle.
}).reset_index()

villes_m2 = merged_df_death.groupby('Death Place').size().reset_index(name='nombre')
villes_m2 = villes_m2.merge(villes_m[['Death Place', 'longitude_death', 'latitude_death']], on='Death Place', how='left')
villes_m2_sort= villes_m2.sort_values(by='nombre', ascending=False).head(15)
villes_m2_sort = villes_m2_sort.drop(1068)
print(villes_m2_sort)

figue = px.scatter_mapbox(villes_m2_sort,
                    lat = "latitude_death",
                    lon = "longitude_death",
                    color = "Death Place" , 
                    hover_name = "Death Place" ,  
                    size = "nombre" 
                    )

figue.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "open-street-map",
        'center': {'lon': 2, 'lat': 47},
        'zoom': 5}
)

# App layout
def page6_layout():
    
    return html.Div([

        html.Div(
            html.H1("Carte Décès",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),

         # Affichage carte
        html.Div([
            dcc.Graph(id = 'map', figure = figue ,style={"width": "100%", "height": "80vh"})
        ], style={"width": "100vw", "height": "100%"}),
    ])

