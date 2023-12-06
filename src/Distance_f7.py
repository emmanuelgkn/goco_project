from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from geopy.distance import distance
import time


from Carte_deces_f6 import *

# Créer une copie de votre dataframe
df_distance = merged_df.copy()


# Supprimer les lignes avec des données manquantes
df_distance = df_distance.dropna(subset=['latitude_birth', 'longitude_birth', 'latitude_death', 'longitude_death'])

# Fonction pour calculer la distance entre deux points
def calculate_distance(row, round_to=10):
    birth_latitude, birth_longitude = row['latitude_birth'], row['longitude_birth']
    death_latitude, death_longitude = row['latitude_death'], row['longitude_death']

    birth_coords = (birth_latitude, birth_longitude)
    death_coords = (death_latitude, death_longitude)

    distancee = distance(birth_coords, death_coords).kilometers
    rounded_distance = round(distancee / round_to) * round_to

    return rounded_distance

# Appliquer la fonction pour calculer la distance
df_distance['distance'] = df_distance.apply(calculate_distance, axis=1)


fig = px.histogram(df_distance, 
                   x="distance", 
                   labels={'count':'Nombre de personnes','distance':'Distance (Km)'},
                   range_x=[0, 18000],
                   range_y=[0, 4],
                   title='Nombre de personnes par de distance parcourue')

fig.update_layout(yaxis_title='Nombre de personnes', plot_bgcolor= '#292A30', paper_bgcolor= '#292A30', font_color='#e0e0e0')
fig.update_layout(yaxis_type="log", plot_bgcolor= '#292A30', paper_bgcolor= '#292A30', font_color='#e0e0e0')

def page7_layout():
    return html.Div(className='corpslambda' ,children=[
    html.H1("Distance parcourue", className = "titlePage"),
    html.Br(),
    dcc.Markdown(className = "manu",children = """
    Ce graphique représente la distance parcourue (ici la distance entre  le lieu de naissance et le lieu de mort)  
    en fonction du nombre de personnes. Ici on pourra choisir la ville de naissance pour visualiser les distances    
    parcourues par les personnes nées dans la ville. Vous pourrez aussi choisir l'année de déces.
    """),
    html.Br(),
    dcc.Dropdown(
        id='birthplace-dropdown-distance',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance",
        style={'background-color':'#292A30', 'color':'black','border-color':'grey'}
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

],style = {'font-family':'arial'})


@app.callback(
    Output('my-graph', 'figure'),
    Input('birthplace-dropdown-distance', 'value'),
    Input('yaxis-type','value'),
)

def update_graph(selected_birthplace, typeaxis):
    filtered_df = df_distance.copy()
    if selected_birthplace:
        filtered_df = filtered_df[filtered_df['Birthplace'] == selected_birthplace]
    else:
        filtered_df = filtered_df

    if typeaxis == 'linear':
        counts = filtered_df['distance'].value_counts().sort_index()
        figure = px.line(x=counts.index, y=counts.values, labels={'y':'Nombre de personnes','x':'Distance (Km)'},
                         title='Nombre de personnes par de distance parcourue', line_shape="spline", render_mode="svg")
        figure.update_layout(xaxis=dict(title='Distance (Km)'), yaxis=dict(title='Nombre de personnes'),
                             plot_bgcolor= '#292A30', paper_bgcolor= '#292A30', font_color='#e0e0e0')
        figure.update_layout(xaxis_range=[0, 3000])
    else:
        counts = filtered_df['distance'].value_counts().sort_index()
        figure = px.line(x=counts.index, y=counts.values, labels={'y':'Nombre de personnes','x':'Distance (Km)'},
                         title='Nombre de personnes par de distance parcourue', line_shape="spline", render_mode="svg")
        figure.update_layout(xaxis=dict(title='Distance (Km)'), yaxis=dict(title='Nombre de personnes'), 
                             plot_bgcolor= '#292A30', paper_bgcolor= '#292A30', font_color='#e0e0e0')
        figure.update_layout(yaxis_type=typeaxis, plot_bgcolor= '#292A30', paper_bgcolor= '#292A30', font_color='#e0e0e0')
        figure.update_layout(xaxis_type=typeaxis, plot_bgcolor= '#292A30', paper_bgcolor= '#292A30', font_color='#e0e0e0')
 
    return figure
