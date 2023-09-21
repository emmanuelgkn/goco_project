from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

from MoyenneAge_f2 import *
from dash.dependencies import Input, Output

birthplace_options = [{'label': city, 'value': city} for city in df['Birthplace'].unique()]
birthplace_options.sort(key=lambda x: x['label'])

# On initialise la app


# App layout
def page3_layout():
    
    return html.Div([

        html.Div(
            html.H1("Carte",
                    style = {"font-family" : "verdana"}),
            style = { "background-color" : "antiquewhite"}),
    
        # Création ménu déroulant
        dcc.Dropdown(
        id='birthplace-dropdown',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance"
        ),

         # On affiche les noms et prénoms qui sont nés dans la ville selectionnée
         html.Div(id='selected-names'),

         # Affichage carte
         html.Div([
            dcc.Graph(id='map-plot')
        ], style={"width": "50%", "margin-top": "20px", "text-align": "center"}),
         ])

@app.callback(
    Output('map-plot', 'figure'),
    Input('birthplace-dropdown', 'value')
)
def update_map(selected_birthplace):
    # Verifier si Birthplace dans le ménu déroulant a été bien sélectionné
    if selected_birthplace:
        # Filtrer merged_df pour trouver l'information correspondante au Birthplace sélectionné
        filtered_df = merged_df[merged_df['Death Place'] == selected_birthplace]
        
        #print(filtered_df)
        # On obtient la longitude et la latitude
        longitude = filtered_df.iloc[0]['longitude']
        latitude = filtered_df.iloc[0]['latitude']
        
        # On affiche le point sur la carte
        fig = go.Figure(go.Scattermapbox(
            mode="markers+lines",
            lon=[longitude],
            lat=[latitude],
            marker={'size': 10}
        ))

        # On affiche la carte
        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 10, 'lat': 10},
                'style': "stamen-terrain",
                'center': {'lon': 0, 'lat': 47},
                'zoom': 4})
    else:
        # On affiche la carte même si on a pas sélectionné une ville
        fig = go.Figure(go.Scattermapbox())

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 10, 'lat': 10},
                'style': "stamen-terrain",
                'center': {'lon': 0, 'lat': 47},
                'zoom': 4})

    return fig
      

# Définissez un callback pour mettre à jour les noms et prénoms en fonction de la ville sélectionnée
@app.callback(
    Output('selected-names', 'children'),
    Input('birthplace-dropdown', 'value')
)
def update_selected_names(selected_birthplace):

    # On filtre le DataFrame pour obtenir les noms et prénoms correspondants à la ville sélectionnée
    filtered_data = df[df['Birthplace'] == selected_birthplace]
      
    # On crée une liste de noms et prénoms à afficher
    names_to_display = [f"{row['Prenom(s)']} {row['Nom']} Naissance: {row['Birthplace Code']} Mort à: {row['Deathplace Code']} Ville: {row['Death Place']}" for index, row in filtered_data.iterrows()]
    
    # On affiche tous les noms
    if len(names_to_display) > 0:
        return html.Ul([html.Li(name) for name in names_to_display])


    
layout3 = app.layout