from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from geopy.distance import geodesic
import time


from Carte_deces_f6 import *

# Créer une copie de votre dataframe
df_distance = merged_df.copy()

# Supprimer les lignes avec des données manquantes
df_distance = df_distance.dropna(subset=['latitude_birth', 'longitude_birth', 'latitude_death', 'longitude_death'])

# Fonction pour calculer la distance entre deux points
def calculate_distance(row):
    birth_coords = (row['latitude_birth'], row['longitude_birth'])
    death_coords = (row['latitude_death'], row['longitude_death'])
    return geodesic(birth_coords, death_coords).kilometers

# Appliquer la fonction pour calculer la distance
df_distance['distance'] = df_distance.apply(calculate_distance, axis=1)

# Afficher la nouvelle dataframe avec la colonne de distance
df_distance_sort = df_distance[['Nom', 'Prenom(s)', 'distance']].sort_values(by='distance', ascending=False)

fig = px.histogram(df_distance, 
                   x="distance", 
                   labels={'count':'Nombre de personnes','distance':'Distance (Km)'},
                   range_x=[0, 2000],
                   title='Nombre de personnes par de distance parcourue')

fig.update_layout(yaxis_title='Nombre de personnes')

def page7_layout():
    return html.Div([
    html.Div(
        html.H1("Distance",
            style = {"font-family" : "verdana"}),
        style = { "background-color" : "antiquewhite"}),
    dcc.Markdown(className = "manu",children = """
    Cet Histogramme représente la distance parcourue (ici la distance entre
    le lieu de naissance et le lieu de mort) en fonction du nombre de personnes.
    Ici on pourra choisir la ville de naissance pour visualiser les distances 
    parcourues par les personnes nées dans cette ville vous pourrez sélectionner 
    "All" pour voir les dépacements de toutes les personnes de la base.
    """),
    dcc.Dropdown(
        id='birthplace-dropdown',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance",
        ),
    dcc.Graph(id='my-graph',figure = fig)
# Autres composants pour la page 1
])

@app.callback(
    Output('my-graph', 'figure'),
    [Input('birthplace-dropdown', 'value')],
)
def update_graph(selected_birthplace):
    print("truc",selected_birthplace)
    # Vérifiez si une ville de naissance est sélectionnée
    if selected_birthplace:
        filtered_df = df_distance[df_distance['Birthplace'] == selected_birthplace].copy()
    else:
        # Si aucune ville n'est sélectionnée, utilisez la dataframe complète
        filtered_df = df_distance.copy()

    figure = px.histogram(filtered_df, 
                   x="distance", 
                   labels={'count':'Nombre de personnes','distance':'Distance (Km)'},
                   range_x=[0, 2000],
                   title='Nombre de personnes par de distance parcourue')
    figure.update_layout(yaxis_title='Nombre de personnes')
    return figure

