from dash import Dash, html, dash_table, dcc, no_update
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

from MoyenneAge_f2 import *
from dash.dependencies import Input, Output

display_options = ["Lignes", "Densité"]
french_cities = merged_df[merged_df['Birthplace Details'] == 'FRANCE']
birthplace_options = [{'label': city, 'value': city} for city in french_cities['Birthplace'].unique() ]
birthplace_options.sort(key=lambda x: x['label'])

international_countries = merged_df[merged_df['Birthplace Details'] != 'FRANCE']
international_countries_options = [{'label': country, 'value': country} for country in international_countries['Birthplace Details'].unique() ]
international_countries_options.sort(key=lambda x: x['label'])


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
        id='display-dropdown',
        options=display_options,
        placeholder="Sélectionnez le type d'affichage"
        ),

        dcc.Dropdown(
        id='birthplace-dropdown',
        options=birthplace_options,
        placeholder="Sélectionnez une ville de naissance"
        ),

        dcc.Dropdown(
        id='international_countries-dropdown',
        options=international_countries_options,
        placeholder="Sélectionnez un pays étranger"
        ),

         # Affichage carte
         html.Div([
            dcc.Graph(id='map-plot', style={"width": "100%", "height": "80vh"})
        ], style={"width": "100vw", "height": "100%"}),

         ])

@app.callback(
    Output('birthplace-dropdown', 'value'),
    [Input('international_countries-dropdown', 'value')]
)
def clear_birthplace(selected_country):
    # Borrar la selección del lugar de nacimiento cuando se seleccione un país extranjero
    if selected_country:
        return None
    return no_update

@app.callback(
    Output('international_countries-dropdown', 'value'),
    [Input('birthplace-dropdown', 'value')]
)
def clear_country(selected_birthplace):
    # Borrar la selección del país extranjero cuando se seleccione un lugar de nacimiento
    if selected_birthplace:
        return None
    return no_update

@app.callback(
    Output('map-plot', 'figure'),
    [Input('display-dropdown', 'value'),
     Input('birthplace-dropdown', 'value'),
     Input('international_countries-dropdown', 'value')]
)
def update_map(selected_display, selected_birthplace, selected_country):
    # Initialisation de filtered_df
    filtered_df = merged_df

    if selected_country:
        # Filtrer merged_df pour trouver les informations correspondant au pays de Birthplace Details sélectionné
        filtered_df = merged_df[merged_df['Birthplace Details'] == selected_country]

    elif selected_birthplace:
        # Filtrer merged_df pour trouver les informations correspondant au Birthplace sélectionné
        filtered_df = merged_df[merged_df['Birthplace'] == selected_birthplace]

    else:
        # Afficher une figure vide si ni Birthplace ni pays n'ont été sélectionnés
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
            mapbox={
                'center': {'lon': 10, 'lat': 10},
                'style': "stamen-terrain",
                'center': {'lon': 0, 'lat': 47},
                'zoom': 4
            }
        )
        return fig
    
    # Obtention de la longitude et de la latitude
    longitude_birth = filtered_df.iloc[0]['longitude_birth']
    latitude_birth = filtered_df.iloc[0]['latitude_birth']

    # Création de la figure du carte
    fig = go.Figure(go.Scattermapbox(
        mode="markers+lines",
        lon=[longitude_birth],
        lat=[latitude_birth],
        marker={'size': 10, 'color': 'blue'}
    ))

    # Création de listes vides pour les coordonnées de latitude et de longitude des lieux de décès
    lats_death = []
    lons_death = []
    lon_list = []
    lat_list = []

    for _, row in filtered_df.iterrows():
        lon_list.append(row['longitude_death'])
        lat_list.append(row['latitude_death'])

    lons_death = np.empty(3* len(filtered_df))
    lons_death[::3] = longitude_birth
    lons_death[1::3] = lon_list
    lons_death[2::3] = None

    lats_death = np.empty(3* len(filtered_df))
    lats_death[::3] = latitude_birth
    lats_death[1::3] = lat_list
    lats_death[2::3] = None

    if selected_display == "Lignes":
        fig.add_trace(go.Scattermapbox(
                mode="markers+lines",
                lon=lons_death,
                lat=lats_death,
                marker={'size': 10, 'color': 'red'},
                showlegend=False,
                #hovertext=[hover_text],  # Utiliser le texte de surbrillance créé
                hoverinfo=None,
            
        ))
        
    elif selected_display == "Densité":
        fig = px.density_mapbox(filtered_df, lat='latitude_death', lon='longitude_death', z='density', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        mapbox_style="stamen-terrain")

    # Mettre à jour la mise en page de la carte
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': 0, 'lat': 47},
            'zoom': 4
        }
    )

    return fig

layout3 = app.layout