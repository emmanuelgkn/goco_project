from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

from MoyenneAge_f2 import *
from dash.dependencies import Input, Output

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
    Output('map-plot', 'figure'),
    [Input('birthplace-dropdown', 'value'),
     Input('international_countries-dropdown', 'value')]
)
def update_map(selected_birthplace, selected_country):
    # 
    if selected_birthplace:
        # Filtrar merged_df para encontrar la información correspondiente al Birthplace seleccionado
        filtered_df = merged_df[merged_df['Birthplace'] == selected_birthplace]
    elif selected_country:
        # Filtrar merged_df para encontrar la información correspondiente al país de Birthplace Details seleccionado
        filtered_df = merged_df[merged_df['Birthplace Details'] == selected_country]
    else:
        # Mostrar una figura vacía si no se ha seleccionado ni Birthplace ni país
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

    # Obtener la longitud y latitud
    longitude_birth = filtered_df.iloc[0]['longitude_birth']
    latitude_birth = filtered_df.iloc[0]['latitude_birth']

    # Crear la figura del mapa
    fig = go.Figure(go.Scattermapbox(
        mode="markers+lines",
        lon=[longitude_birth],
        lat=[latitude_birth],
        marker={'size': 10, 'color': 'blue'}
    ))

    # Crear listas vacías para las coordenadas de latitud y longitud de los lugares de fallecimiento
    lats_death = []
    lons_death = []

    # Iterar sobre las filas de filtered_df
    for _, row in filtered_df.iterrows():
        latitude_death = row['latitude_death']
        longitude_death = row['longitude_death']

        if latitude_death is not latitude_birth and longitude_death is not longitude_birth:
            # Agregar las coordenadas a la lista
            lats_death.append(latitude_death)
            lons_death.append(longitude_death)

    # Agregar marcadores para cada lugar de fallecimiento
    for i in range(len(lats_death)):
        if filtered_df.iloc[i]['Death Place'] != "NULL":
            hover_text = filtered_df.iloc[i]['Death Place']
        else:
            hover_text = ""  # Texto vacío si el valor es "NULL"

        fig.add_trace(go.Scattermapbox(
            mode="markers+lines",
            lon=[lons_death[i], longitude_birth],
            lat=[lats_death[i], latitude_birth],
            marker={'size': 10, 'color': 'red'},
            showlegend=False,
            hovertext=[hover_text],  # Usar el texto de sobrecrecimiento creado
            hoverinfo=None,
        ))

    # Actualizar el diseño del mapa
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