from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from lifprojet2 import *
from dash.dependencies import Input, Output

birthplace_options = [{'label': city, 'value': city} for city in df['Birthplace'].unique()]
birthplace_options.sort(key=lambda x: x['label'])

# On initialise la app


# App layout
def page3_layout():
    return html.Div([
    
        # Création ménu déroulant
        dcc.Dropdown(
        id='birthplace-dropdown',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance"
        ),

         # On affiche les noms et prénoms qui sont nés dans la ville selectionnée
         html.Div(id='selected-names')
         ])

# Définissez un callback pour mettre à jour les noms et prénoms en fonction de la ville sélectionnée
@app.callback(
    Output('selected-names', 'children'),
    Input('birthplace-dropdown', 'value')
)
def update_selected_names(selected_birthplace):

    # On filtre le DataFrame pour obtenir les noms et prénoms correspondants à la ville sélectionnée
    filtered_data = df[df['Birthplace'] == selected_birthplace]
    
    
    # On crée une liste de noms et prénoms à afficher
    names_to_display = [f"{row['Prenom(s)']} {row['Nom']} Naissance: {row['Birthplace Code']} Mort à: {row['Deathplace Code']}" for index, row in filtered_data.iterrows()]
    
    # On affiche tous les noms
    if len(names_to_display) > 0:
        return html.Ul([html.Li(name) for name in names_to_display])

layout3 = app.layout