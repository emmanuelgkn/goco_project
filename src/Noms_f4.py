from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from Carte_f3 import *


# Pour filtrer les données pour chaque ville
paris_data = df[df['Birthplace'].str.contains('PARIS ', case=False, regex=True)]
lyon_data = df[df['Birthplace'].str.contains('LYON', case=False, regex=True)]
bordeaux_data = df[df['Birthplace'].str.contains('BORDEAUX', case=False, regex=True)]
toulouse_data = df[df['Birthplace'].str.contains('TOULOUSE', case=False, regex=True)]
marseille_data = df[df['Birthplace'].str.contains('MARSEILLE', case=False, regex=True)]

# Pour compter les noms les plus populaires pour chaque ville

name_countsp = paris_data.groupby('Nom').size().reset_index(name='Count')
# Pour trier les noms par ordre décroissant de comptagex
top_names_paris = name_countsp.sort_values(by='Count', ascending=False).head(5)

name_countsl = lyon_data.groupby('Nom').size().reset_index(name='Count')
top_names_lyon = name_countsl.sort_values(by='Count', ascending=False).head(5)

name_countsb = bordeaux_data.groupby('Nom').size().reset_index(name='Count')
top_names_bordeaux = name_countsb.sort_values(by='Count', ascending=False).head(5)

name_countst = toulouse_data.groupby('Nom').size().reset_index(name='Count')
top_names_toulouse = name_countst.sort_values(by='Count', ascending=False).head(5)

name_countsm = marseille_data.groupby('Nom').size().reset_index(name='Count')
top_names_marseille = name_countsm.sort_values(by='Count', ascending=False).head(5)

# On crée une fonction pour afficher un tableau des noms les plus populaires
def create_top_names_table(city_name, top_names_df):
    return html.Div([
        html.H2(f"Top 5 des Noms Populaires à {city_name}"),
        dash_table.DataTable(
            data=top_names_df.to_dict('records'),
            columns=[{'name': 'Nom', 'id': 'Nom'}, {'name': 'Count', 'id': 'Count'}],
            style_data={
                'color': '#e0e0e0',
                'backgroundColor': 'rgb(50, 50, 50)',
                'fontWeight': 'bold',
            },
            style_cell={'padding': '5px'},
            style_header={
                'color': '#e0e0e0',
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold',
            },
        ),
    ])


# App layout
def page4_layout():
    return html.Div(className='corpslambda', children=[
        html.H1("Top noms", className = "titlePage"),
        html.P("Ce sont les noms les plus populaires donneés des dates de naissances allant de l'année 1912 à 2023", style={"font-family": "verdana", "font-size": "15px", 'text-align': 'center'}),
        html.Div([
        create_top_names_table("Paris", top_names_paris),
        create_top_names_table("Lyon", top_names_lyon),
        create_top_names_table("Bordeaux", top_names_bordeaux),
        create_top_names_table("Toulouse", top_names_toulouse),
        create_top_names_table("Marseille", top_names_marseille)]),
    ])
