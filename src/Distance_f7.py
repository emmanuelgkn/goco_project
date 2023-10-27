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
def calculate_distance(row, round_to=10):
    birth_coords = (row['latitude_birth'], row['longitude_birth'])
    death_coords = (row['latitude_death'], row['longitude_death'])
    distance = geodesic(birth_coords, death_coords).kilometers
    rounded_distance = round(distance / round_to) * round_to
    return rounded_distance

# Appliquer la fonction pour calculer la distance
df_distance['distance'] = df_distance.apply(calculate_distance, axis=1)

# Afficher la nouvelle dataframe avec la colonne de distance
df_distance_sort = df_distance[['Nom', 'Prenom(s)', 'distance']].sort_values(by='distance', ascending=False)


df_distance['Date of Death'] = pd.to_datetime(df_distance['Date of Death'], format='%d/%m/%Y', errors='coerce')
df_distance['Year of Death'] = df_distance['Date of Death'].dt.year.fillna(-1).astype('int')

fig = px.histogram(df_distance, 
                   x="distance", 
                   labels={'count':'Nombre de personnes','distance':'Distance (Km)'},
                   range_x=[0, 18000],
                   range_y=[0, 4],
                   title='Nombre de personnes par de distance parcourue')

fig.update_layout(yaxis_title='Nombre de personnes', plot_bgcolor= '#111111', paper_bgcolor= '#111111', font_color='#e0e0e0')
fig.update_layout(yaxis_type="log", plot_bgcolor= '#111111', paper_bgcolor= '#111111', font_color='#e0e0e0')

def page7_layout():
    return html.Div(className='corpslambda' ,children=[
    html.H1("Distance"),
    dcc.Markdown(className = "manu",children = """
    Cet Histogramme représente la distance parcourue (ici la distance entre
    le lieu de naissance et le lieu de mort) en fonction du nombre de personnes.
    Ici on pourra choisir la ville de naissance pour visualiser les distances 
    parcourues par les personnes nées dans la ville. Vous pourrez aussi choisir
    l'année de déces.
    """),
    dcc.Dropdown(
        id='birthplace-dropdown',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance",
        ),
    dcc.RadioItems(
        options=[
            {'label': 'Lineaire', 'value': 'linear'},
            {'label': 'Log', 'value': 'log'}],
        value='linear',
        id='yaxis-type',
        inline=True,
        style={'font-family': 'arial'}),

    dcc.Graph(id='my-graph',figure = fig),
    dcc.Slider(
    min=1990,
    max=2023,
    step=5,
    id='year--slider',
    value=df_distance['Year of Death'].max(),
    marks={str(year): str(year) for year in df_distance['Year of Death'].unique()},),
    html.Div("  ")

],style = {'font-family':'arial'})


@app.callback(
    Output('my-graph', 'figure'),
    Input('birthplace-dropdown', 'value'),
    Input('yaxis-type','value'),
    Input('year--slider', 'value'),
)

def update_graph(selected_birthplace, typeaxis, yearselected):
    filtered_df = df_distance[df_distance['Year of Death'] == yearselected].copy()

    if selected_birthplace:
        filtered_df = filtered_df[filtered_df['Birthplace'] == selected_birthplace]
    else:
        filtered_df = filtered_df

    if typeaxis == 'linear':
        counts = filtered_df['distance'].value_counts().sort_index()
        figure = px.line(x=counts.index, y=counts.values, labels={'y':'Nombre de personnes','x':'Distance (Km)'},
                         title='Nombre de personnes par de distance parcourue', line_shape="spline", render_mode="svg")
        figure.update_layout(xaxis=dict(title='Distance (Km)'), yaxis=dict(title='Nombre de personnes'),
                             plot_bgcolor= '#111111', paper_bgcolor= '#111111', font_color='#e0e0e0')
    else:
        counts = filtered_df['distance'].value_counts().sort_index()
        figure = px.line(x=counts.index, y=counts.values, labels={'y':'Nombre de personnes','x':'Distance (Km)'},
                         title='Nombre de personnes par de distance parcourue', line_shape="spline", render_mode="svg")
        figure.update_layout(xaxis=dict(title='Distance (Km)'), yaxis=dict(title='Nombre de personnes'), 
                             plot_bgcolor= '#111111', paper_bgcolor= '#111111', font_color='#e0e0e0')
        figure.update_layout(yaxis_type=typeaxis, plot_bgcolor= '#111111', paper_bgcolor= '#111111', font_color='#e0e0e0')
        figure.update_layout(xaxis_type=typeaxis, plot_bgcolor= '#111111', paper_bgcolor= '#111111', font_color='#e0e0e0')


    return figure
