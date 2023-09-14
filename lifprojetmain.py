from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output

from lifprojet import app as page1_app, layout as page1_layout
from lifprojet2 import app as page2_app, layout2 as page2_layout
from lifprojet3 import app as page3_app, layout3 as page3_layout

app = Dash(__name__)

# Configuration de la barre de navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav([
        dcc.Link('Page 1', href='/page1'),
        dcc.Link('Page 2', href='/page2'),
        dcc.Link('Page 3', href='/page3'),

    ]),
    html.Div(id='page-content')
])

# Callback pour mettre à jour la page en fonction de l'URL
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/page1':
        return page1_layout
    if pathname == '/page2':
        return page2_layout
    if pathname == '/page3':
        return page3_layout
    else:
        return 'Page introuvable'

if __name__ == '__main__':
    app.run_server(debug=True)