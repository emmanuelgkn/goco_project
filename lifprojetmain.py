from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output


from Carte_deces_f6 import *

# Configuration de la barre de navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav(className="nave",children = [
        dcc.Link('Accueil', href='/Accueil'),
        dcc.Link('Base', href='/page1'),
        dcc.Link('Histogramme', href='/page2'),
        dcc.Link('Carte', href='/page3'),
        dcc.Link('Top Noms', href='/page4'),
        dcc.Link('Lieux Décès', href='/page5'),
        dcc.Link('Carte Deces', href='/page6')],
    ),
    html.Div(id='page-content')
])

# Callback pour mettre à jour la page en fonction de l'URL
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/page1':
        return page1_layout()
    if pathname == '/page2':
        return page2_layout()
    if pathname == '/page3':
        return page3_layout()
    if pathname == '/page4':
        return page4_layout()
    if pathname == '/page5':
        return page5_layout()
    if pathname == '/page6':
        return page6_layout()
    if pathname == '/Accueil':
        return Accueil_layout()
    else:
        return Accueil_layout()

if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)