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
villes_m2_sort= villes_m2.sort_values(by='nombre', ascending=False)
villes_m2_sort = villes_m2_sort.drop(1062)
villes_m2_sort


figue = px.scatter_mapbox(villes_m2_sort,
                    lat = "latitude",
                    lon = "longitude",
                    color = "Death Place" , 
                    hover_name = "Death Place" ,  
                    size = "nombre",
                    size_max=40 
                    )

# figue.update_layout(
#     margin ={'l':0,'t':0,'b':0,'r':0},
#     mapbox = {
#         'center': {'lon': 10, 'lat': 10},
#         'style': "open-street-map",
#         'center': {'lon': 2, 'lat': 47},
#         'zoom': 5}
# )


figue.update_traces(marker=dict(sizemode='diameter', sizeref=17))

# App layout
def page6_layout():
    
    return html.Div([

        html.Div(
            html.H1("Carte Décès",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),

         # Affichage carte
        html.Div([
            dcc.Graph(id = 'map', style={"width": "100%", "height": "80vh"})
        ], style={"width": "100vw", "height": "100%"}),
    ])


# Callback to update the figure based on zoom level
@app.callback(
    Output('map', 'figure'),
    [Input('map', 'relayoutData')]
)
def update_map_layout(relayout_data):
    
    zoom_level = relayout_data.get('mapbox.zoom', 5)
    
    # Adjust the number of markers dynamically based on zoom level
    # You can customize this logic to achieve the desired progressive zoom effect
    max_markers = 10 * (2 ** min(zoom_level - 5, 0))  # Adjust the zoom sensitivity here
    
    villes_m2_filtered = villes_m2_sort.head(int(max_markers))

    fig = px.scatter_mapbox(
        villes_m2_filtered,
        lat="latitude",
        lon="longitude",
        color="Death Place",
        hover_name="Death Place",
        size="nombre",
        size_max=40 
    )

    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 2, 'lat': 47},
            'style': "open-street-map",
            'zoom': zoom_level
        }
    )

    fig.update_traces(marker=dict(sizemode='diameter', sizeref=17))
    return fig