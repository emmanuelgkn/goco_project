from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output

from lifprojet import app as page1_app, layout as page1_layout
from lifprojet2 import app as page2_app, layout as page2_layout

app = Dash(__name__)

# Configuration de la barre de navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback pour mettre à jour la page en fonction de l'URL
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
        return page1_layout
    elif pathname == '/page2':
        return page2_layout
    else:
        return 'Page introuvable'

if __name__ == '__main__':
    app.run_server(debug=True)