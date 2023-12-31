from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

from Noms_f4 import *

paris = df[df['Death Place'].str.contains('PARIS ', case=False, regex=True)]
toulouse = df[df['Death Place'].str.contains('TOULOUSE', case=False, regex=True)]
lyon = df[df['Death Place'].str.contains('LYON', case=False, regex=True)]
marseille = df[df['Death Place'].str.contains('MARSEILLE', case=False, regex=True)]

#Pour calculer le nombre de morts 
nb_mort_paris = len(paris)
nb_mort_toulouse = len(toulouse)
nb_mort_lyon = len(lyon)
nb_mort_marseille = len(marseille)

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}


dff = pd.DataFrame({
    "Ville": ["Paris","Lyon","Toulouse","Marseille"],
    "Nombre": [nb_mort_paris, nb_mort_lyon, nb_mort_toulouse, nb_mort_marseille]
})

fig = px.bar(dff, x="Ville", y="Nombre")
fig.update_layout(
    plot_bgcolor= '#111111',
    paper_bgcolor= '#111111',
    font_color='#e0e0e0'
)



def page5_layout():
        return html.Div(className='corpslambda' ,children=[
            html.H1("Top villes décès", className = "titlePage"),
            html.Br(),
            dcc.Markdown(className="manu", children="""
                Ce graphe representent le nombre de morts dans les 4 villes plus grandes en France.
            """),
            html.Br(),
            dcc.Graph(id='example-graph-2', figure=fig),
            dash_table.DataTable(
                data=dff.to_dict('records'),
                columns=[{'name': 'Ville', 'id': 'Ville'}, {'name': 'Nb Morts', 'id': 'Nombre'}],
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
