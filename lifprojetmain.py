from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output


from lifprojet4 import *

# Configuration de la barre de navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav(children = [
        dcc.Link('Accueil', href='/Accueil'),
        dcc.Link('Base', href='/page1'),
        dcc.Link('Histogramme', href='/page2'),
        dcc.Link('Carte', href='/page3')],
        style={
                'display' : 'flex',
                'justify-content' : 'space-around',
                'background-color' : 'rgb(74, 172, 185)',
                ' padding-left': '1em',
                'padding-right': '1em',
                'line-height': '2em',
                'border': '1px black',
                'font-family': 'verdana',
                'font-size': '20px'
        }
    ),
    html.Div([
         html.Iframe(open("emmanuel.html", "r").read(),
                                width = '100%', 
                                height= '100%',
                                style={'border':'none'})

    ]),
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
    if pathname == '/Accueil':
        return Accueil_layout()
    else:
        return 'Page introuvable'

if __name__ == '__main__':
    app.run_server(debug=True, port = 8080)