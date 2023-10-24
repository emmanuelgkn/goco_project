from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from Noms_f4 import *

paris = df[df['Death Place'].str.contains('PARIS ', case=False, regex=True)]
toulouse = df[df['Death Place'].str.contains('TOULOUSE', case=False, regex=True)]
lyon = df[df['Death Place'].str.contains('LYON', case=False, regex=True)]
marseille = df[df['Death Place'].str.contains('MARSEILLE', case=False, regex=True)]

nb_mort_paris = len(paris)
nb_mort_toulouse = len(toulouse)
nb_mort_lyon = len(lyon)
nb_mort_marseille = len(marseille)

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
dff = pd.DataFrame({
    "Ville": ["Paris","Lyon","Toulouse","Marseille"],
    "Nombre": [nb_mort_paris, nb_mort_lyon, nb_mort_toulouse, nb_mort_marseille]
})

fig = px.bar(dff, x="Ville", y="Nombre")


def page5_layout():
        return html.Div(className='corpslambda' ,children=[
            dcc.Graph(id='example-graph-2', figure=fig),
            dash_table.DataTable(
            data=dff.to_dict('records'),
            columns=[{'name': 'Ville', 'id': 'Ville'}, {'name': 'Nb Morts', 'id': 'Nombre'}],
        ),
])