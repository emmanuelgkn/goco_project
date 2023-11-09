from PyramideAge_f8 import *
from dash import exceptions

myorigins_df = merged_df.copy()

# Extraction du premier prénom
myorigins_df['Prenom(s)'] = myorigins_df['Prenom(s)'].str.split().str[0]

# Filtrage des prénoms pour ne conserver que les chaînes de caractères
firstnames = myorigins_df['Prenom(s)'].dropna().unique()

# Filtrage des prénoms pour ne conserver que les chaînes de caractères
secondnames = myorigins_df['Nom'].dropna().unique()

# Création de firstname_options à partir des prénoms filtrés
firstname_options = [{'label': fstname, 'value': fstname} for fstname in firstnames]

# Tri de firstname_options
firstname_options.sort(key=lambda x: x['label'])

# Création de firstname_options à partir des prénoms filtrés
secondname_options = [{'label': sndname, 'value': sndname} for sndname in secondnames]

# Tri de firstname_options
secondname_options.sort(key=lambda x: x['label'])

def page9_layout():

    #Affichage titre et sous-titre
    return html.Div(className='corpslambda', children=[
    html.H1("Mes origines", style={"font-family": "verdana"}),
    dcc.Markdown(className="manu", children="""
    Cette carte représente les origines d'un prénom ou nom famille en France.
    """),

    # Affichage menu déroulant pour les prénoms
    dcc.Dropdown(
        id='firstname-dropdown',
        options=firstname_options,
        placeholder="Sélectionnez un prénom"
    ),

    # Affichage menu déroulant pour les prénoms
    dcc.Dropdown(
        id='secondname-dropdown',
        options=secondname_options,
        placeholder="Sélectionnez un nom"
    ),

    # Affichage carte
    html.Div([
        dcc.Graph(id='map-myorigins', style={"width": "100%", "height": "80vh"})
    ], style={"width": "100vw", "height": "100%"}),

])

# Ajoutez ces lignes avant votre fonction de rappel
prev_firstname_value = None
prev_secondname_value = None

@app.callback(
    [Output('firstname-dropdown', 'value'),
     Output('secondname-dropdown', 'value')],
    [Input('firstname-dropdown', 'value'),
     Input('secondname-dropdown', 'value')]
)
def update_dropdowns(selected_firstname, selected_secondname):
    global prev_firstname_value, prev_secondname_value
    if selected_firstname != prev_firstname_value:
        prev_firstname_value = selected_firstname
        return selected_firstname, None
    elif selected_secondname != prev_secondname_value:
        prev_secondname_value = selected_secondname
        return None, selected_secondname
    else:
        return selected_firstname, selected_secondname


@app.callback(
    Output('map-myorigins', 'figure'),
    [Input('firstname-dropdown', 'value'),
     Input('secondname-dropdown', 'value'),]
)


def update_map(selected_fstname, selected_sndname):

    if selected_fstname:
        myorigins_filtered_df = myorigins_df[myorigins_df['Prenom(s)'] == selected_fstname]
        fig = px.density_mapbox(myorigins_filtered_df, lat='latitude_birth', lon='longitude_birth', z='density', radius=10,
                                center=dict(lat=47, lon=0), zoom=4,
                                mapbox_style="carto-positron")
    elif selected_sndname:
        myorigins_filtered_df = myorigins_df[myorigins_df['Nom'] == selected_sndname]
        fig = px.density_mapbox(myorigins_filtered_df, lat='latitude_birth', lon='longitude_birth', z='density', radius=10,
                                center=dict(lat=47, lon=0), zoom=4,
                                mapbox_style="carto-positron")    
    else:
        fig = go.Figure(go.Scattermapbox())
        # Afficher une figure vide si ni Birthplace ni pays n'ont été sélectionnés
        fig.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
            mapbox={
                'style': "carto-positron",
                'center': {'lon': 0, 'lat': 47},
                'zoom': 4
            }
        )
        return fig
        
    # Mettre à jour la mise en page de la carte
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'style': "carto-positron",
            'center': {'lon': 0, 'lat': 47},
            'zoom': 4
        }
    )

    return fig
