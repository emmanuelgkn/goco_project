from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output


from LieuDeces_f5 import *

villes_m = merged_df.groupby('Death Place').agg({
    'longitude_death': 'first',  # Utilisez 'first' pour obtenir le premier valeur non nulle.
    'latitude_death': 'first',   # Utilisez 'first' pour obtenir le premier valeur non nulle.
}).reset_index()

def extract_city_name(place_name):
    if 'PARIS ' in place_name:
        return 'PARIS'
    if 'LYON' in place_name:
        return 'LYON'
    if 'MARSEILLE' in place_name:
        return 'MARSEILLE'
    else:
        return place_name
villes_m2 = df.copy()
villes_m2['Death Place'] = villes_m2['Death Place'].apply(extract_city_name)
#villes_m2 = villes_m2.groupby('Death Place').size().reset_index(name='nombre')
villes_m2 = villes_m2.merge(positions_geo, left_on='Deathplace Code', right_on='code_commune_INSEE', how='left')
villes_m2 = villes_m2.groupby('Death Place').agg(
    latitude=('latitude', 'first'),  # Utilisez 'first' pour obtenir la première valeur non nulle.
    longitude=('longitude', 'first'),  # Utilisez 'first' pour obtenir la première valeur non nulle.
    nombre=('Death Place', 'size')  # Utilisez 'size' pour obtenir le nombre d'occurrences.
).reset_index()
villes_m2_sort= villes_m2.sort_values(by='nombre', ascending=False).head(100)
villes_m2_sort = villes_m2_sort.drop(2148)
# print(villes_m2_sort)

figue = px.scatter_mapbox(villes_m2_sort,
                    lat = "latitude",
                    lon = "longitude",
                    color = "Death Place" , 
                    hover_name = "Death Place" ,  
                    size = "nombre",
                    size_max=40 
                    )

figue.update_layout(
     margin ={'l':0,'t':0,'b':0,'r':0},
     mapbox = {
         'center': {'lon': 10, 'lat': 10},
         'style': "carto-positron",
         'center': {'lon': 2, 'lat': 47},
         'zoom': 5}
 )


figue.update_traces(marker=dict(sizemode='diameter', sizeref=50))

# App layout
def page6_layout():
    
    return html.Div([

        html.Div(
            html.H1("Carte du nombre de décès par ville",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),

         # Affichage carte
        html.Div([
            dcc.Graph(id = 'map', figure=figue,style={"width": "100%", "height": "80vh"})
        ], style={"width": "100vw", "height": "100%"}),
    ])
